
"""
Created on Fri Jan  4 11:39:52 2019
@author: wencai
"""
from datetime import  datetime,timedelta

import maturity
import option_data
import visualization


def main(ticker,plot_type):
    # get maturities date
    maturities_stamp = maturity.Maturity.yahoo_option_maturity(ticker)
    if plot_type =="3D":
        monthly_stamp  = maturity.Maturity.get_monthly_timestamp(maturities_stamp)
        call_dic, put_dic = option_data.parse_option(ticker,monthly_stamp)
        #from dictionary to a dataframe
        c_iv,p_iv = option_data.get_iv_df(call_dic,put_dic)
        #plot 3D
        visualization.Visual(ticker).plot_iv_surface(c_iv,p_iv)

    elif plot_type =="2D":
        special_stamp  = maturity.Maturity.get_special_timestamp(maturities_stamp)
        call_dic, put_dic = option_data.parse_option(ticker,special_stamp)
        c_iv,p_iv = option_data.get_iv_df(call_dic,put_dic)
        # plot skew
        visualization.Visual(ticker).plot_iv_curves(c_iv)
        visualization.Visual(ticker).plot_iv_curves(p_iv)
    

if __name__=="__main__":

    main(ticker='AAPL',plot_type='2D')

