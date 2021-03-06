from dash import dcc, html, Input, Output, State, callback
import dash
import numpy as np
import base64
from pages import medoid_functions
from pages import help_functions

dash.register_page(__name__, path='/practice_signs')

from global_ import signs_table, pngs, configurations, medoids, styles

layout = html.Div([
    html.H2('SIGNS'),
    html.B('Choose a sign to practice its configurations',style={'margin-bottom':'20px'}),
    html.Div('After choosing a sign, the configurations that form that sign are going to appear in the screen. You will have to reproduce them correctly.'),
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
        html.Label(['Topic:'], style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(
            id='sign-dropdown-topic',
            options=[dict((('label',topic), ('value',topic))) for topic in np.unique(signs_table['TOPIC'])],
            value = signs_table['TOPIC'][0],
            clearable=False,
            style = {'width':'100%','display':'inline-block'},
        ),
        html.Label(['Word:'], style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(
            id='sign-dropdown',
            options=[dict((('label',signo), ('value',signo))) for signo in signs_table[signs_table['TOPIC']==signs_table['TOPIC'][0]]['SIGNO']],
            value = signs_table['SIGNO'][0],
            clearable=False,
            style = {'width':'100%','display':'inline-block'},
        ),
        dcc.Interval(id='pred-sign-interval',interval=0.5*1000,n_intervals=0),
        html.Div([
            html.Div('These are the configurations you must perform:',id='text_configs_number'),
            dcc.Store(id='store-configs',data=[]),
            dcc.Store(id='index-conf',data=0),
            html.Br(),
            html.Div(id='images-sign')
        ],id='imgs-conf-sign',style={'display':'none','margin-top':'20px'})
    ],style = {'width':'49%','display':'inline-block'}),
],id='container-performance')


@callback(Output('sign-dropdown','options'), Output('sign-dropdown','value'),
          Input('sign-dropdown-topic','value'),prevent_initial_call=True)
def change_topic(topic):

    import global_
    global_.index = 0

    new_options=[dict((('label',signo), ('value',signo))) for signo in signs_table[signs_table['TOPIC']==topic]['SIGNO']]
    return new_options, new_options[0]['value']

@callback([Output('images-sign','children'), Output('imgs-conf-sign','style'),
           Output('store-configs','data'), Output('text_configs_number','children')], 
           Input('sign-dropdown','value'))
def show_all_images(sign_name):
    
    import global_
    global_.index = 0

    configs = signs_table[signs_table['SIGNO']==sign_name]['CONFIGS'].to_string(index=False).split(',')
    num_configs = len(configs)
    width = str(round(100/num_configs))+'%' if num_configs!=1 else '49%'
    
    children = [html.Div([
        html.Img(id={'type':'img-sign','index':index},src=pngs[int(config)-1],
                style={'height':'50%', 'width':'50%',
                'margin-left':'20px','padding':'10px'})
    ],style={'width':width,'display':'inline-block'}) for index, config in enumerate(configs)]
    data_confs = configs

    style={'display':'inline-block','margin-top':'20px'}
    
    if num_configs==1:
        text_configs_number = 'This is the configuration you must perform:'
    else:
        text_configs_number = 'These are the ' + str(num_configs) + ' configurations you must perform:'

    return children, style, data_confs, text_configs_number 

@callback(Output({'type':'img-sign','index':dash.dependencies.ALL},'style'),
          Input('pred-sign-interval','n_intervals'),
          [State('which-hand-sign','value'), State('store-configs','data')],
          prevent_initial_call=True)
def pred3(n, which_hand, data):

    import global_

    imgs_number = len(dash.callback_context.outputs_list)
    return_styles = np.empty(shape=imgs_number,dtype=object)

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
            prev = global_.index
            return_styles[0:global_.index+1]=styles[0]
            if imgs_number>1:
                global_.index = (global_.index+1) % imgs_number
                return_styles[global_.index]=styles[1]
                return_styles[global_.index+1:]=styles[2]
            return_styles[prev]=styles[0]
        else:
            return_styles[0:global_.index] = styles[0]
            return_styles[global_.index] = styles[1]
            return_styles[global_.index+1:] = styles[2]

    else:
        return_styles[0:global_.index] = styles[0]
        return_styles[global_.index] = styles[1]
        return_styles[global_.index+1:] = styles[2]

    return [ret_sty for ret_sty in return_styles]