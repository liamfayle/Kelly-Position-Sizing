import numpy as np
import sys
from copy import deepcopy
sys.path.append('../BSM')
from bsm import BsmOption, OptionPosition
import pandas_market_calendars as mcal
from datetime import date, timedelta
import pandas as pd



class Sizing:
    def __init__(self):
        self.terminal_paths = None

    def generatePaths(self, S0, r, volatility, M, I, returned=False):
        '''
        Geometric brownian motion path monte carlo  \n
        Stored in self.terminal_price \n
        Returned if True\n
        NOTE redundant to call if calling kelly method \n

        S0 - Current stock price \n
        r - interest rate / drift term\n
        volatility - annualized \n
        M - DTE \n
        I - number of paths \n
        '''
        dt = 1.0 / M
        paths = np.zeros((M + 1, I), np.float64)
        paths[0] = S0
        for t in range(1, M + 1):
            rand = np.random.standard_normal(I)
            paths[t] = paths[t-1] * np.exp((r - 0.5 * volatility ** 2) * dt + volatility * np.sqrt(dt) * rand)
        self.terminal_paths = paths[-1]

        if (returned):
            return paths[-1]

    def getTradingDays(self, dte):
        '''
        Converts from DTE to number of trading days
        '''
        today = date.today()
        expiry = today + timedelta(days=dte)
        nyse = mcal.get_calendar('NYSE')
        days = nyse.schedule(start_date=today, end_date=expiry)
        return len(days)


    def getKellyFraction(self, pos, volatilityForecast, numPaths):
        '''
        Get approximate f* value by maximizing growth function \n
        pos object is not edited \n
        
        pos = OptionPosition object
        volatilityForecast = volatility forecast annualized\n
        numPaths = number of GBM paths to create \n
        http://www.eecs.harvard.edu/cs286r/courses/fall12/papers/Thorpe_KellyCriterion2007.pdf \n
        g(f) = E log(Xn /X0) = p log(1 + bf) + q log(1 - f)
        '''
        adjustedDte = self.getTradingDays(pos.getDTE())
        self.generatePaths(pos.getSpot(), pos.getR(), (volatilityForecast / np.sqrt(252)) * np.sqrt(adjustedDte), adjustedDte, numPaths)

        forecast_position = deepcopy(pos)
        forecast_position.updateSigma(volatilityForecast)
        forecast_position.updateDTE(1)

        terminalPrice = []
        paths = np.asarray(self.terminal_paths)

        terminalPrice = forecast_position.updateSpotReturnPrice(paths) 
        W_i = (terminalPrice - pos.price()) / np.abs(pos.price())

        G = []

        end = False
        for f in range(0, 100):
            G.append(np.sum( (1/len(self.terminal_paths)) * np.log10(1 + W_i*(f/100)) ))
            if np.isnan(G[f]):
                G.pop()
                break
        return G.index(max(G))

        


