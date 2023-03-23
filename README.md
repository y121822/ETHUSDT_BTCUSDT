<p float="left" align="center">
    <img src="https://dtjn1pr44tf3g.cloudfront.net/BTCUSDT_plot.png" alt="BTCUSDT scatter plot" width="32%">
    <img src="https://dtjn1pr44tf3g.cloudfront.net/ETHUSDT_plot.png" alt="ETHUSDT scatter plot" width="32%">
    <img src="https://dtjn1pr44tf3g.cloudfront.net/ETHUSDT_BTCUSDT.png" alt="ETHUSDT/BTCUSDT linear regression" width="32%">
</p>


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