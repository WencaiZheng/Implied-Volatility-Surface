import re
import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import timedelta
import datetime
class Maturity():

    @staticmethod
    def yahoo_option_maturity(ticker):
        """
        Find the maturities for all the options trading on one stock
        
        Input: Ticker like 'AAPL'
        Output: List of date formating as Timestamp
        """
        try:
            init_web = f"https://finance.yahoo.com/quote/{ticker}/options"
        except:
            print("The website address has been changed!")
            return [0]

        init_html = urlopen(init_web)
        raw_source = BeautifulSoup(init_html, features='lxml').text
        
        head_position = raw_source.find("expirationDates")
        tail_position = raw_source.find("hasMiniOptions")
        if head_position != -1 or tail_position != -1:
            maturities = re.findall(r'\d+',raw_source[head_position:tail_position])
        else:
            print("webside source code changed! check the source code struction")
        return maturities
    
    @staticmethod
    def get_special_dates(mon_dates):
        # only get first 4 month and last two leaps
        if len(mon_dates) > 6:
            # after 4th date the rest years
            leap_year = np.arange(int(mon_dates[4][:4]),int(mon_dates[-1][:4]))+1
            # first and last maturity are the same year, there is no leap
            if len(leap_year) ==0:
                return mon_dates[:6]
            # first and last maturity are different year, there are leaps
            else:
                leaps=[]
                first_dates = mon_dates[:4]
                second_dates = mon_dates[4:]
                #if 2020 2021 2020, find 2021 first
                for iyear in leap_year:
                    for dt in second_dates:
                        if dt[:4] == str(iyear):
                            leaps.append(dt)
                            break
            mon_dates = first_dates + leaps

        return mon_dates

    @staticmethod
    def get_monthly_timestamp(maturities_stamp):
        """ Select the date that is the 3rd Friday
        """
        fdate = lambda i:str(datetime.datetime.fromtimestamp(int(i)).date()+timedelta(days=1))
        maturity_date = [fdate(i) for i in maturities_stamp]
        #get monthlies option
        today_date  = str(datetime.date.today())
        future_date = str(datetime.date.today() + timedelta(days=365*5))
        monthlies = pd.date_range(today_date,future_date,freq='WOM-3FRI')
        mon_dates_idx = [i for i,d in enumerate(maturity_date) if d in monthlies]
        #get monthlies timestamp on Yahoo Finance
        monthly_timestamp = np.array(maturities_stamp)[mon_dates_idx]
        return monthly_timestamp


    @classmethod
    def get_special_timestamp(cls,maturities_stamp):
        mon_stamp = cls.get_monthly_timestamp(maturities_stamp)
        fdate = lambda i:str(datetime.datetime.fromtimestamp(int(i)).date()+timedelta(days=1))
        mon_dates = [fdate(i) for i in mon_stamp]
        #only get 4 font months and possible leaps
        special_dates = cls.get_special_dates(mon_dates)
        special_dates_idx = [mon_dates.index(i) for i in special_dates]
        special_timestamp = np.array(mon_stamp)[special_dates_idx]
        return special_timestamp
