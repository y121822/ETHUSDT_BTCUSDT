### Задача № 1:
Определить собственные движения цены фьючерса ETHUSDT, исключив из них движения вызванные 
влиянием цены BTCUSDT. Описать какие метод и параметры подобраны и почему.

### Задача № 2:
Написать программу на Python, которая в реальном времени (с минимальной задержкой) следит за 
ценой фьючерса ETHUSDT и используя выбранный метод, определяет собственные движение цены ETH. 
При изменении цены на 1% за последние 60 минут, программа выводит сообщение в консоль. 
При этом программа должна продолжать работать дальше, постоянно считывая актуальную цену.

----

### Решение задачи №1:
Графики ниже показывают что зависимость между движениями фьючерсов ETHUSDT и BTCUSDT существует
и имеет выраженный линейный характер. 

<p float="left" align="center">
    <img src="https://d19ehgb5eebwoa.cloudfront.net/BTCUSDT_plot2.png" alt="BTCUSDT scatter plot" width="32%">
    <img src="https://d19ehgb5eebwoa.cloudfront.net/ETHUSDT_plot2.png" alt="ETHUSDT scatter plot" width="32%">
    <img src="https://d19ehgb5eebwoa.cloudfront.net/ETHUSDT_BTCUSDT2.png" alt="ETHUSDT/BTCUSDT linear regression" width="32%">
</p>

Для построения графиков делались выборки из 15-ти минутных значений соответствующих фьючерсов
в течении 30 дней (объем каждой выборки - 2899 наблюдений). Коэффициент корреляции между
фьючерсами близок к единице, как видно из приведенных ниже вычислений выполненных в R.

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
Вышеизложенное позволяет использовать линейную регрессию для предсказания значений зависимой
переменной ETHUSDT, основываясь на значениях независмой переменной BTCUSDT.
Разница (остатки) между истинными и предсказанными значениями ETHUSDT будет интерпретироваться
как собственные движения ETHUSDT.

### Решение задачи №2:
см. файл app.py и комментарии в нем.

----

### Использование
Скачайте файлы из данного репозитория, установите зависимости и запустите app.py или используйте
Docker.
```bash
docker container run -it y121822/ethusdt_btcusdt
```
