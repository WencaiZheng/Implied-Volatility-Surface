
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

class Visual():

    @staticmethod
    def plot_iv_surface(c_iv,p_iv):
        """ Plot the implied volatility surface
        """
        #clean data
        c_iv = c_iv.fillna(method='ffill').fillna(method='bfill')
        p_iv = p_iv.fillna(method='ffill').fillna(method='bfill')
        # Initialize figure with 3D subplots
        
        fig = make_subplots(rows=1, cols=2,
            specs=[[{'type': 'surface'}, {'type': 'surface'}],])

        # adding surfaces to subplots.
        fig.add_trace(
            go.Surface(x=c_iv.index, y=c_iv.columns, z=c_iv.values, colorscale='Viridis', showscale=False),
            row=1, col=1)

        fig.add_trace(
            go.Surface(x=p_iv.index, y=p_iv.columns, z=p_iv.values, colorscale='RdBu', showscale=False),
            row=1, col=2)

        fig.update_layout(
            title_text='3D subplots with different colorscales',
            height=800,width=1600)

        fig.show()

    @staticmethod
    def plot_iv_curves(c_iv,ticker):
        #plot skew
        c_iv = c_iv.dropna()
        today = str(datetime.date.today())
        fig = go.Figure()
        for date in c_iv.columns:
            fig.add_trace(go.Scatter(x=c_iv.index, y=c_iv.loc[:,date],
                            mode='lines+markers',
                            name=date))

        fig.update_layout(title_text=f'Implied volatility Skew for {ticker} at {today}',height=600,width=1200)
        fig.show()
        pass


if __name__ == "__main__":

    pass