import datetime
import time
import bs_price
import pandas as pd
import numpy as np




def implied_volatility(Price,Exercise,Time):
    """ Calculate the impied volatility with Biseciton
    
    Output: implied vol
    """
    P = float(Price);K = float(Exercise)
    
    today_stamp = time.mktime(datetime.date.today().timetuple())
    # T is the days to maturities
    T = int((int(Time)-today_stamp)/3600/24)
    
    left=0.0001; right=10
    PLeft=BS_price(K,T,left )-P
    PRight=BS_price(K,T,right )-P
    # Simple Bisection
    while  right-left> 0.001:
        PLeft=BS_price(K,T,left )-P
        PRight=BS_price(K,T,right )-P
        if PLeft*PRight<=0:
            sigma=(left+right)/2
            PMid=BS_price(K,T,sigma )-P
            if PMid*PLeft<0:
                right=sigma
            else:
                left=sigma
        else:
            return 0
    return (left+right)/2


def construct_iv(K,T,callOpt,putOpt,ifcall):
    """ Construct my implied volatitlity surface data
    """
    IV=[]
    for k in K: # for each strike
        cur=[]
        for t in T:# for each date stamp
            p = real_opt_price(callOpt,putOpt,t,k,ifcall)# choose call option here
            cur.append(implied_volatility(p,k,t))
        IV.append(cur)

    for i in IV:
        for j in range(len(i)):
            if i[j]==0:
                if j==0:
                    k=j+1
                    while i[k]==0 and k!=len(i)-1:##find next nonzero
                        k+=1
                    if k==len(i)-1:
                        break
                    i[j]=i[k]
                else:
                    i[j]=i[j-1]
    IV=np.array(IV).T.tolist()
    return IV