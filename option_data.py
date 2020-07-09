import re
import requests
import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
headers = {'User-Agent': 'Chrome/39.0.2171.95'}

def parse_option(ticker,stamp_list):
    """Parse option data from 'finance.yahoo.com'
    Input: maturities of options
    Output: all call and put data like strike, price
    """
    call={}
    put={}
    dates = [str(datetime.fromtimestamp(int(i)).date()+timedelta(days=1)) for i in stamp_list]
    # get options in each maturity
    for i,timestamp in enumerate(stamp_list):
        print(f'Parsing options expiring at {dates[i]}')
        the_url = f'https://finance.yahoo.com/quote/{ticker}/options?p=AAPL&date={timestamp}'
        response = requests.get(the_url, headers=headers)
        soup = BeautifulSoup(response.text, features='lxml')
        Strike= soup.find_all('td', {'class': re.compile('data-col2')})
        Price=soup.find_all('td', {'class': re.compile('data-col3')})
        iVol= soup.find_all('td', {'class': re.compile('data-col10')})

        callPrice=[Price[0].get_text()]
        putPrice=[] 
        strike=[Strike[0].get_text()]
        iV=[iVol[0].get_text()]

        flag=0
        for i in range(1,len(Price)):
            iV.append(iVol[i].get_text())
            strike.append(Strike[i].get_text())
            if float(strike[i])<=float(strike[i-1]):####begin to record put opiton price
                flag=1
            if flag==0:
                callPrice.append(Price[i].get_text())
            else:
                putPrice.append(Price[i].get_text())

        ####split the strikes into call and put
        callStrike= list(map(float,strike[:len(callPrice)]))
        putStrike= list(map(float,strike[len(callPrice):]))

        iv = [float(i[:-1]) for i in iV]
        callIV=iv[:len(callPrice)]
        putIV=iv[len(callPrice):]

        maturity = str(datetime.fromtimestamp(int(timestamp)).date())
        call[maturity] = pd.DataFrame([callPrice,callIV],columns=callStrike,index=['price','iv']).T.astype(float)
        put[maturity] = pd.DataFrame([putPrice,putIV],columns=putStrike,index=['price','iv']).T.astype(float)

    print("Successfully parsed!")
    return call,put


def get_iv_df(call_dic,put_dic):
    """Get implied volatility of options from parsed result
    """
    c_iv,p_iv = pd.DataFrame(),pd.DataFrame()
    for dt,call in call_dic.items():
        c_iv = pd.concat([c_iv,call.iv],sort=True,join = 'outer',axis=1)

    for dt,put in put_dic.items():
        p_iv = pd.concat([p_iv,put.iv],sort=True,join = 'outer',axis=1)

    c_iv.columns = call_dic.keys()
    p_iv.columns = put_dic.keys()

    return c_iv,p_iv
    
def get_price_df(call_dic,put_dic):
    """ Get price of option data
    """
    pass