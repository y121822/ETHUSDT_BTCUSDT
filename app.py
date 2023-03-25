import sys
import asyncio
import logging
import pandas as pd
from scipy import stats
from binance.client import Client
from binance import AsyncClient, BinanceSocketManager
from binance.exceptions import BinanceAPIException
from datetime import datetime, timedelta


class Setup:
    """Get historical data for modelling. Apply the linear regression.
       Return slope and intercept coefficients"""

    def __init__(self, interval, days):
        self.client = Client()
        self.interval, self.days = interval, days

    def get_data(self):
        start_point = (datetime.now() - timedelta(days=self.days)).strftime("%d %B, %Y")
        try:
            df1 = pd.DataFrame(self.client.futures_historical_klines('BTCUSDT', self.interval, start_point))
            df2 = pd.DataFrame(self.client.futures_historical_klines('ETHUSDT', self.interval, start_point))

            return df1.iloc[:, 4].astype(float).values, df2.iloc[:, 4].astype(float).values
        except BinanceAPIException as e:
            logging.exception(f'Setup.get_data: {e.status_code}, {e.message}')
            sys.exit(1)

    def create_coefficients(self):
        x, y = self.get_data()
        stats_lr = stats.linregress(x, y)

        return stats_lr[0], stats_lr[1]


class Process:
    """Asynchronously retrieve and process current data"""

    def __init__(self, interval=Client.KLINE_INTERVAL_15MINUTE, threshold=1., days=30, minutes=60):
        self.slope, self.intercept = Setup(interval, days).create_coefficients()
        self.now, self.btcusdt, self.ethusdt, self.ethusdt_decoupled_prev = None, None, None, None
        self.threshold, self.minutes = threshold, minutes
        self.start, self.delta = datetime.utcnow(), timedelta(minutes=minutes)

    async def process(self):
        """The coroutine to find independent of BTCUSDT ETHUSDT futures price movements and to send
           the console message if they change beyond a threshold within a time period"""

        if self.ethusdt and self.btcusdt:
            ethusdt_decoupled = abs(self.ethusdt - (self.intercept + self.slope * self.btcusdt))

            if (self.now - self.start) < self.delta:
                if not self.ethusdt_decoupled_prev:
                    self.ethusdt_decoupled_prev = ethusdt_decoupled
                percentage = abs((ethusdt_decoupled-self.ethusdt_decoupled_prev)/self.ethusdt_decoupled_prev * 100)
                self.ethusdt_decoupled_prev = ethusdt_decoupled
                if percentage >= self.threshold:
                    print(f'{percentage}% change of the BTCUSDT free ETHUSDT price within {self.minutes} minutes '
                          f'starting from {self.start.strftime("%Y-%m-%d %H:%M:%S")} UTC')
            else:
                self.start = self.now
                self.ethusdt_decoupled_prev = None

    async def futures_listener(self, client):
        """The coroutine to infinitely retrieve and set the current BTCUSDT and ETHUSDT price
           and time data from the websocket stream and then call the processing coroutine."""

        try:
            async with BinanceSocketManager(client).all_ticker_futures_socket() as stream:
                while True:
                    res = await stream.recv()
                    if res['data']['s'] == 'BTCUSDT':
                        self.btcusdt = float(res['data']['a'])
                    if res['data']['s'] == 'ETHUSDT':
                        self.ethusdt = float(res['data']['a'])
                        self.now = datetime.utcfromtimestamp(res['data']['E']/1000)
                    loop.call_soon(asyncio.create_task, self.process())  # avoid blocking the loop
        except BinanceAPIException as e:
            logging.exception(f'Process.futures_listener: {e.status_code}, {e.message}')
            sys.exit(1)

    async def activate(self):
        client = await AsyncClient.create()
        await self.futures_listener(client)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Process().activate())
