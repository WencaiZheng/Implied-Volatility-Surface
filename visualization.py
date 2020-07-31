import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

class Visual:

    def __init__(self,ticker):
        self.ticker = ticker
        self.today = str(datetime.date.today())

    def plot_iv_surface(self,c_iv,p_iv):
        """ Plot the implied volatility surface
        """
        #clean data
        c_iv = c_iv.replace(0,np.nan)
        p_iv = p_iv.replace(0,np.nan)

        c_iv = c_iv.dropna()
        p_iv = p_iv.dropna()

        # c_iv = c_iv.fillna(method='ffill').fillna(method='bfill')
        # p_iv = p_iv.fillna(method='ffill').fillna(method='bfill')
        # Initialize figure with 3D subplots
        
        fig = make_subplots(rows=1, cols=2,
            specs=[[{'type': 'surface'}, {'type': 'surface'}],])

        # adding surfaces to subplots.
        fig.add_trace(
            go.Surface(x=c_iv.index, y=c_iv.columns, z=c_iv.T.values, colorscale='Viridis', showscale=False),
            row=1, col=1)

        fig.add_trace(
            go.Surface(x=p_iv.index, y=p_iv.columns, z=p_iv.T.values, colorscale='RdBu', showscale=False),
            row=1, col=2)

        fig.update_layout(
            title_text=f'Implied volatility Surface for {self.ticker} at {self.today}',
            height=800,width=1200)

        fig.show()
        pass

    def plot_iv_curves(self,c_iv):
        #plot skew
        c_iv = c_iv.replace(0,np.nan)
        c_iv = c_iv.dropna()
        
        fig = go.Figure()
        for date in c_iv.columns:
            fig.add_trace(go.Scatter(x=c_iv.index, y=c_iv.loc[:,date],
                            mode='lines+markers',
                            name=date))

        fig.update_layout(title_text=f'Implied volatility Skew for {self.ticker} at {self.today}',height=600,width=1200)
        fig.show()
        pass


if __name__ == "__main__":

    pass