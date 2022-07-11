from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash
import numpy as np
from pages import medoid_functions
from pages import help_functions

dash.register_page(__name__, path='/medoids')

from global_ import configurations, medoids, pngs, figures_medoids 

layout = html.Div([
    html.Div([
        html.Img(id='video', src='/user/configurations/video_mediapipe_feed'),
        html.Div([
            html.Div(id='textarea-prediction-output', style={'whiteSpace': 'pre','width':'49%'}),
            html.Div(id='textarea-prediction-wrong', style={'whiteSpace': 'pre','width':'49%'}),
            html.Div(html.Img(id='img-config-wrong',src=None,style={'height':'20%', 'width':'20%'}),style={'width':'49%','display':'inline-block','verticalAlign':'top'}),
            html.Div([
                dbc.Button('PERFORMANCE SUMMARY',n_clicks=0,outline=True, color='primary',id='button-performance',href='/summary_user'),
            ]),  
        ], style={'display':'block'})
    ], style = {'width':'49%','display':'inline-block','verticalAlign':'top'}),
    html.Div([
        html.Div([
            html.H3('Choose which hand you are using'),
            dcc.RadioItems(id = 'which-hand', 
                           options=['Right hand', 'Left hand'], 
                           value='Right hand', 
                           persistence=True, 
                           persistence_type='session',
                           inputStyle={"margin-right": "5px", 'cursor': 'pointer', 'margin-left':'20px'}
            ),
            html.Br(),
            html.H3('Choose a configuration to practice'),
            dcc.Dropdown(
                id='config-medoid',
                options=[dict((('label',config), ('value',config))) for config in configurations],
                value = '1',
                clearable=False,
                persistence=True,
                persistence_type='session'
            )
        ]),
        html.Div(html.Img(id='img-config-medoid',src=None,style={'height':'50%', 'width':'50%'}),style={'width':'49%','display':'inline-block','verticalAlign':'top'}),                            
        html.Div(dcc.Graph(
            id='graph-medoid',
            figure=figures_medoids[int(configurations[0])-1],
            responsive=True,
            style={
                'width': '100%',
                'height': '100%',
                'display':'none',
                'verticalAlign':'middle'
            }
        ),style={'display':'inline-block','width':'49%','margin-right':'10px'}),
        dcc.Interval('interval-prediction',
                    interval=0.5*1000,
                    n_intervals=0
        ),
    ], id='div-medoid', style={'display':'inline-block', 'width':'49%'}),
    
])

@callback([Output('graph-medoid','figure'), Output('graph-medoid','style'),
           Output('img-config-medoid','src')],
           Input('config-medoid','value'), prevent_initial_call=False)
def show_medoid_graph(configuration):

    figure_actual = figures_medoids[int(configuration)-1]
    style = {
                'width': '100%',
                'height': '100%',
                'display': 'inline-block'
            }

    src_img = pngs[int(configuration)-1]
    

    return figure_actual, style, src_img

@callback([Output('textarea-prediction-output','children'), Output('textarea-prediction-output','style'), 
          Output('img-config-wrong','src'), Output('textarea-prediction-wrong','children'),
          Output('store-user-performance-prueba','data')],
          Input('interval-prediction','n_intervals'),
          [State('config-medoid','value'), State('textarea-prediction-output','style'), 
          State('store-user-performance-prueba','data'), State('which-hand','value')])
def make_prediction_medoid(interval, config_value, actual_style, data, which_hand):
    import global_
    png_actual = None
    text = None
    if (which_hand=='Right hand'):
        landmarks = global_.landmarks_right
    else:
        landmarks = global_.landmarks_left
    
    if landmarks is not None:
        landmarks_to_predict = help_functions.transform_data(landmarks)

        dists = [medoid_functions.procrustes_disparity(actual_medoid, landmarks_to_predict) for actual_medoid in medoids]
        min_index = int(np.where(dists == np.amin(dists))[0])
        result = configurations[min_index]

        if result == config_value:
            style = {'backgroundColor':'#99FF99','width':'35.1%'}
            data['correct'] += 1 
        else:
            png_actual = pngs[int(result)-1]
            text = 'The hand configuration you are performing looks like the image below. Try again!'
            style = {'backgroundColor':'#FF9999','width':'35.1%'}

            data['errors'][int(config_value)-1][int(result)-1] +=1

        data['total'] += 1 

        return result, style, png_actual, text, data 

    return '', actual_style, png_actual, text, data 