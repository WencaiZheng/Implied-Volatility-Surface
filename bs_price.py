import math
import yfinance as yf
from scipy.stats import norm


def BS_price(my_ticker,Exercise,Time,sigma):
    """ Calculate Black-Sholes price
    """
    
    S = yf.Ticker(my_ticker).info["regularMarketPrice"]
    r =0.05
    
    K = float(Exercise)
    T = float(Time)
    d_1 = float(float((math.log( S/K)+( r+(sigma**2)/2)*T))/float((sigma*(math.sqrt(T)))))
    d_2 = float(float((math.log( S/K)+( r-(sigma**2)/2)*T))/float((sigma*(math.sqrt(T)))))
    BSPrice = float( S*norm.cdf(d_1) - K*math.exp(- r*T)*norm.cdf(d_2))
    return BSPrice