# Kelly Position Sizing for Options
Implementation of the "Kelly Criterion" (Maximizing Expected Value of Log Wealth) for options positions. 

### Requirements
- My other [repo](https://github.com/liamfayle/Black-Scholes-Merton "repo") containing a BSM model & Option position model implementation.

### References
- [THE KELLY CRITERION IN BLACKJACK SPORTS BETTING, AND THE STOCK MARKET.](http://www.eecs.harvard.edu/cs286r/courses/fall12/papers/Thorpe_KellyCriterion2007.pdf "THE KELLY CRITERION IN BLACKJACK SPORTS BETTING, AND THE STOCK MARKET") by Edward O. Thorp.

### Approach
1. Obtain *N*  [geometric Brownian motion (GBM)](https://en.wikipedia.org/wiki/Geometric_Brownian_motion "geometric Brownian motion (GBM)") paths given an annualized volatility forecast, current spot price, risk free rate, days to expiration, and N. 
2. Obtain terminal spot prices from each path.
3. Obtain return on premium at expiration for each terminal spot price given an option position object.
4. Obtain expected growth rate *G* for a range of bet sizes *f*.
5. Obtain *f\** where growth rate *G* is at its maximum, where *f\** represents the optimal bet size.

### Results
[Curve]
- Growth rate curve *G(f)* where *f\* ~= 14.5%*
	- Position is a short straddle struck at $20, with spot initially at $20, 60 DTE, 4.8% risk free rate, 59% implied volatility, and a position value of $3.80 (credit). 
	- Monte Carlo simulation of 100,000 GBM paths with a forecasted volatility of 50%.

[Sampling Dist]
- Sampling distribution of *f\** with same parameters as above sampled n = 1000 times.

### Sanity Check
- Using same option position described above and number of paths N = 100,000.
	#### Mean Return at Various GBM Volatility Forecasts
		| Implied Vol | Forecast Vol | Mean Return |
		| ------------ | ------------ | ------------ |
		| 59% | 200% |-235.17% |
		| 59% | 70% | -22.80% |
		| 59% | 59% | -4.03% |
		| 59% | 50% | 10.95% |
		| 59% | 20% | 59.43% |
	#### Optimal Bet Size *f\** at Various GBM Volatility Forecasts
		| Implied Vol | Forecast Vol | f\* |
		| ------------ | ------------ | ------------ |
		| 59% | 200% | 0.0% |
		| 59% | 70% | 0.0% |
		| 59% | 59% | 0.0% |
		| 59% | 50% | 15.20% |
		| 59% | 20% | 71.10% |
