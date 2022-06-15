from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc
import dash
import pandas as pd
from dash import dash_table
import numpy as np

dash.register_page(__name__, path='/summary_user')

layout = html.Div([
    html.H2('PERFORMANCE.'),
    html.B(id='textarea-correct-percentage', style={'whiteSpace': 'pre','margin-bottom':'20px'}),
    html.Br(),
    dbc.Label('These are the ten most confusing configurations in your attempts.'),
    html.Br(),
    dash_table.DataTable(id='table-performance',row_selectable="single"),
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
    ],style={'margin-top':'20px'}),
],id='container-performance')



@callback([Output(component_id='table-performance', component_property='data'),
     Output(component_id='table-performance', component_property='columns'),
     Output('textarea-correct-percentage','children')],#[Output('table-results','children'), Output('table-results','style')],
          Input('store-user-performance-prueba', 'modified_timestamp'),
          Input('store-user-performance-prueba','data')) #Input('store-user-performance','data')
def print_now(ts, data): #saved_preds,

    if data['total'] != 0:
        real_config, predicted =np.where(np.array(data['errors'])!=0)
        values = [data['errors'][real][pred] for real,pred in zip(real_config,predicted)]

        df = pd.DataFrame({'real':np.array(real_config)+1,
                            'pred': np.array(predicted)+1,
                            'size': [round(x,2) for x in np.array(values)/data['total']*100.0]})

        # df = pd.DataFrame.from_dict(saved_preds)
        # df = df.groupby(df.columns.tolist(),as_index=False).size()
        df = df.sort_values('size', ascending=False)

        df.columns = ['Chosen configuration', 'Performed configuration', '% Wrong performances']

        columns = [{'name': col, 'id': col} for col in df.columns]
        saved_preds = df.head(10).to_dict(orient='records')

        return saved_preds, columns, 'The ' + str(round(data['correct']/data['total']*100.0,2)) + '% of the trials were well performed.' 
    
    else:
        return None, None, None


@callback([Output('images-performance','style'), Output('real-config','children'), Output('real-img','src'), 
          Output('pred-config','children'), Output('pred-img','src')],
         [Input('table-performance', 'selected_rows'), Input('table-performance','data')])
def show_configs(selected_rows, data):
    if(selected_rows):
        selected = selected_rows[0]
        real_sel = data[selected]['Chosen configuration']
        pred_sel = data[selected]['Performed configuration']

        text1 = 'You have selected to practice configuration '+ str(real_sel)
        text2 = 'But you have performed configuration '+ str(pred_sel)

        from global_ import pngs
        img1 = pngs[real_sel-1]
        img2 = pngs[pred_sel-1]

        return {'display':'inline-block'}, text1 , img1, text2, img2
    
    return {'display':'none'}, None, None, None, None