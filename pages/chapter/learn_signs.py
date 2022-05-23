from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash
import pandas as pd
from dash import dash_table
import numpy as np
import base64
from pages import medoid_functions
from pages import help_functions

dash.register_page(__name__, path='/practice_signs')

from global_ import signs_table, pngs, configurations, medoids, styles

layout = html.Div([
    html.H2('SIGNS.'),
    html.B('Choose a sign to practice its configurations',style={'margin-bottom':'20px'}),
    html.Div('After choosing a sign, the configurations that form that signs are going to appear in the screen.You will have to reproduce them correctly.'),
    html.Br(),
    html.Div([
        html.Img(id='video', src='/user/configurations/video_mediapipe_feed'),
    ], style = {'width':'49%','display':'inline-block','verticalAlign':'top'}),
    html.Div([
        html.H3('Choose which hand you are using'),
        dcc.RadioItems(id = 'which-hand-sign', 
                    options=['Right hand', 'Left hand'], 
                    value='Right hand', 
                    persistence=True, 
                    persistence_type='session',
                    inputStyle={"margin-right": "5px", 'cursor': 'pointer', 'margin-left':'20px','margin-bottom':'20px'}
        ),
        dcc.Dropdown(
            id='sign-dropdown-topic',
            options=[dict((('label',topic), ('value',topic))) for topic in np.unique(signs_table['TOPIC'])],
            value = signs_table['TOPIC'][0],
            clearable=False,
            #persistence=True,
            #persistence_type='session',
            #placeholder='Select sign...',
            style = {'width':'100%','display':'inline-block'},
        ),
        dcc.Dropdown(
            id='sign-dropdown',
            options=[dict((('label',signo), ('value',signo))) for signo in signs_table[signs_table['TOPIC']==signs_table['TOPIC'][0]]['SIGNO']],
            value = signs_table['SIGNO'][0],
            clearable=False,
            #persistence=True,
            #persistence_type='session',
            #placeholder='Select sign...',
            style = {'width':'100%','display':'inline-block'},
        ),
        # html.Select(
        #     id='a',
        #     children=[
        #         html.Optgroup(label='Animales'),
        #         html.Option('Gato'),
        #         html.Option('Perro'),
        #         html.Optgroup(label='Comida'),
        #         html.Option('Cereal')
        #     ]
        # ),
        
        dcc.Interval(id='pred-sign-interval',interval=0.5*1000,n_intervals=0),
        html.Div([
            html.Div('Selected sign:'),
            html.Img(id='sign-img',src=None,style={'height':'30%', 'width':'30%','margin-left':'20px'}),
            html.Video(id='video-sign',src=None, controls=True, style={'height':'37%', 'width':'37%','margin-left':'20px'})
        ], id='div-sel-sign',style={'display':'none'}),
        html.Div([
            html.Div('These are the configurations you must perform:'),
            dcc.Store(id='store-configs',data=[]),
            dcc.Store(id='index-conf',data=0),
            html.Br(),
            html.Div([
                html.H5(id='first-config'),
                html.Img(id='first-img',src=None,
                         style={'height':'50%', 'width':'50%',
                         'margin-left':'20px','border':'2px red solid', 
                         'backgroundColor':'#EF989F','padding':'10px'})
            ],style={'width':'49%','display':'inline-block'}),
            html.Div([
                html.H5(id='second-config'),
                html.Img(id='second-img',src=None,
                        style={'height':'50%', 'width':'50%'})
            ], style={'width':'49%','display':'inline-block'})
        ],id='imgs-conf-sign',style={'display':'none','margin-top':'20px'})
    ],style = {'width':'49%','display':'inline-block'}),
],id='container-performance')


@callback(Output('sign-dropdown','options'), Output('sign-dropdown','value'),
          Input('sign-dropdown-topic','value'),prevent_initial_call=True)
def change_topic(topic):

    import global_
    global_.index = 0

    new_options=[dict((('label',signo), ('value',signo))) for signo in signs_table[signs_table['TOPIC']==topic]['SIGNO']]
    print(new_options[0]['value'])
    return new_options, new_options[0]['value']

@callback([Output('sign-img','src'),Output('video-sign','src'), Output('first-img','src'), Output('second-img','src'),
           Output('imgs-conf-sign','style'),Output('div-sel-sign','style'), Output('store-configs','data')],
           Input('sign-dropdown','value'))#, prevent_initial_call=True)
def show_selected_sign(sign_name):

    import global_
    global_.index = 0
    print(sign_name)

    first_conf = signs_table[signs_table['SIGNO']==sign_name]['CONFIG INICIO'].to_string(index=False)
    last_conf = signs_table[signs_table['SIGNO']==sign_name]['CONFIG FINAL'].to_string(index=False)
    sign_path_name = signs_table[signs_table['SIGNO']==sign_name]['PATH_IMG'].to_string(index=False)
    path_sign_img = 'dataset/images_signs/'+ sign_path_name + '.png'
    path_sign_vid = '/static/' + sign_path_name + '.mov'

    img1_src=pngs[int(first_conf)-1]
    img2_src=pngs[int(last_conf)-1]
    imgSigno_src='data:image/png;base64,{}'.format(base64.b64encode(open(path_sign_img, 'rb').read()).decode())

    style={'display':'inline-block','margin-top':'20px'}
    style2={'display':'flex','margin-top':'20px'}

    return imgSigno_src, path_sign_vid, img1_src, img2_src, style, style2, [first_conf,last_conf]

@callback(Output('first-img','style'),Output('second-img','style'),
          Input('pred-sign-interval','n_intervals'),
          [State('first-img','style'), State('second-img','style'),
          State('which-hand-sign','value'), State('store-configs','data')],
          prevent_initial_call=True)
def pred(n, st1,st2, which_hand, data):

    import global_

    conf_actual = data[global_.index]
    
    if (which_hand=='Right hand'):
        landmarks = global_.landmarks_right
    else:
        landmarks = global_.landmarks_left
    
    if landmarks is not None:
        landmarks_to_predict = help_functions.transform_data(landmarks)

        dists = [medoid_functions.procrustes_disparity(actual_medoid, landmarks_to_predict) for actual_medoid in medoids]
        min_index = int(np.where(dists == np.amin(dists))[0])
        result = configurations[min_index]

        if result==conf_actual:
            st1 = styles[global_.index]
            global_.index = int(not global_.index)
            st2 = styles[global_.index]
        
        else:
            st1 = styles[global_.index-1] if global_.index==1 else styles[global_.index+1] #styles[global_.index+1]

            st2 = styles[1] if global_.index==1 else styles[2]

    else:
        st1 = styles[global_.index-1] if global_.index==1 else styles[global_.index+1]
        st2 = styles[1] if global_.index ==1 else styles[2]

    return st1, st2

