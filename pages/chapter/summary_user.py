from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash
import numpy as np
import pickle as pkl
from pages import medoid_functions
from pages import help_functions
import base64
import pandas as pd
from dash import dash_table

dash.register_page(__name__, path='/summary_user')

layout = html.Div([
    html.H2('PERFORMANCE.'),
    dbc.Label('Most confusing configurations of the last 25 attempts:'),
    html.Br(),
    dash_table.DataTable(id='table-performance',row_selectable="single"),
    dcc.Interval(id='b',interval=1000,n_intervals=0),
    html.Div([
        html.Div([
            html.H5(id='real-config'),
            html.Img(id='real-img',src=None,style={'height':'15%', 'width':'15%'})
        ],style={'width':'49%','display':'inline-block'}),
        html.Div([
            html.H5(id='pred-config'),
            html.Img(id='pred-img',src=None,style={'height':'15%', 'width':'15%'})
        ], style={'width':'49%','display':'inline-block'})
    ],id='images-performance',style={'display':'none'}),
    html.Div([
        dbc.Button('Continue learning',n_clicks=0,outline=True, color='primary',id='button-performance',href='/medoids')
    ],style={'margin-top':'20px'})
],id='container-performance')



@callback([Output(component_id='table-performance', component_property='data'),
     Output(component_id='table-performance', component_property='columns')],#[Output('table-results','children'), Output('table-results','style')],
          Input('store-user-performance', 'modified_timestamp'),
          Input('store-user-performance','data')) #Input('b','interval'), 
def print_now(ts, data):
    df = pd.DataFrame.from_dict(data)
    df = df.groupby(df.columns.tolist(),as_index=False).size()
    df = df.sort_values('size', ascending=False)

    df.columns = ['Chosen configuration', 'Performed configuration', '# Wrong performances']

    columns = [{'name': col, 'id': col} for col in df.columns]
    data = df.to_dict(orient='records')

    return data, columns



@callback([Output('images-performance','style'), Output('real-config','children'), Output('real-img','src'), 
          Output('pred-config','children'), Output('pred-img','src')],
         [Input('table-performance', 'selected_rows'), Input('table-performance','data')])
def show_configs(selected_rows, data):
    if(selected_rows):
        selected = selected_rows[0]
        real_sel = data[selected]['Chosen configuration']
        pred_sel = data[selected]['Performed configuration']

        text1 = 'You have selected to practice configuration '+ real_sel
        text2 = 'But you have performed configuration '+ pred_sel

        from global_ import pngs
        img1 = pngs[int(real_sel)-1]
        img2 = pngs[int(pred_sel)-1]

        return {'display':'inline-block'}, text1 , img1, text2, img2
    
    return {'display':'none'}, None, None, None, None