from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash
import numpy as np
import pickle as pkl
from pages import medoid_functions
from pages import help_functions
import base64
import pandas as pd

dash.register_page(__name__, path='/summary_user')

layout = html.Div([
    html.H2('PERFORMANCE.'),
    dbc.Label('Most confused configurations of the last 25 attemps:'),
    html.Br(),
    dbc.Table(id='table-results', style={'margin-top':'25px', 'display':'none'}),
    dcc.Interval(id='b',interval=1000,n_intervals=0),
    html.Div(
        dbc.Button('Continue learning',n_clicks=0,outline=True, color='primary',id='button-performance',href='/medoids')
    )
],id='container-performance')


@callback([Output('table-results','children'), Output('table-results','style')],
          Input('store-user-performance', 'modified_timestamp'),
          Input('store-user-performance','data')) #Input('b','interval'), 
def print_now(ts, data):
    df = pd.DataFrame.from_dict(data)
    df = df.groupby(df.columns.tolist(),as_index=False).size()
    df = df.sort_values('size', ascending=False)

    df.columns = ['Chosen configuration', 'Performed configuration', '# Wrong performances']

    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

    # table = dbc.Table([
    #     html.Thead(
    #         html.Tr([html.Th(col) for col in df.columns])
    #     ),
    #     html.Tbody([
    #         html.Tr([
    #             html.Td(df.iloc[i][col]) for col in df.columns
    #         ]) for i in range(len(df))
    #     ])
    # ])

    return table, {'margin-top':'25px', 'display':'inline-block'}