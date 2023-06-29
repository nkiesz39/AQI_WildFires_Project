import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv('data\cleaned_AQI.csv')

fig = px.scatter(df, x='first_max_value', y='aqi', title='AQI vs Stuff')

app.layout = html.Div(children=[
    html.H1(children='Hello Group2!'),

    # html.Div(children='''
    #     Dash: A web application framework for your data.
    # '''),

    dcc.Graph(
        id='first-graph',
        figure=fig
    ),

])


if __name__ == '__main__':
    app.run_server()
