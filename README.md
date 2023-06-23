### Task # 1:
Determine own movements of the ETHUSDT price at Binance, cleared from influence 
caused by BTCUSDT. Describe the used method, its parameters and why it was chosen.

### Task # 2:
Write a Python program to constantly (in real time with minimal delay) control 
the ETHUSDT futures price and using the chosen method to determine 
own changes of the ETH price. If there is a 1% price change within the last 
60 minutes, the program sends a message to the console and continue to run 
without any pauses, reading actual price values.

----

### Task #1 solution:
The graphs below demonstrate that the dependence between ETHUSDT and BTCUSDT exists 
and has the emphasized linear character.

<p float="left" align="center">
    <img src="https://d19ehgb5eebwoa.cloudfront.net/BTCUSDT_plot2.png" alt="BTCUSDT scatter plot" width="32%">
    <img src="https://d19ehgb5eebwoa.cloudfront.net/ETHUSDT_plot2.png" alt="ETHUSDT scatter plot" width="32%">
    <img src="https://d19ehgb5eebwoa.cloudfront.net/ETHUSDT_BTCUSDT2.png" alt="ETHUSDT/BTCUSDT linear regression" width="32%">
</p>

Data for the graphs consists of 15 minutes values of the proper futures obtained 
within 30 days (2899 observations for each). As it seen in the R code snippet 
bellow, the correlation coefficient is close to one.

```R
> cor.test(btcusdt$X4, ethusdt$X4)

	Pearson's product-moment correlation

data:  btcusdt$X4 and ethusdt$X4
t = 223.41, df = 2897, p-value < 2.2e-16
alternative hypothesis: true correlation is not equal to 0
95 percent confidence interval:
 0.9701128 0.9741121
sample estimates:
      cor 
0.9721832
```

The said above allows using linear regression for predicting the value of ETHUSDT
based on BTCUSDT values. 

Residuals between the real and predicted values are interpreted as own movements of the 
ETHUSDT prices

### Task #2 solution:
Please see app.py and comments inside. The asynchronous approach was used to meet the minimal delay
requirement.

----

### Usage:
Download files from this repository, install dependencies and launch app.py or
use Docker.

```bash
docker container run -it y121822/ethusdt_btcusdt
```
