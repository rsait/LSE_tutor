from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import dash
import numpy as np
import pickle as pkl
from pages import medoid_functions
from pages import help_functions
import base64
import pandas as pd


dash.register_page(__name__, path='/medoids')

from global_ import configurations, medoids, figures_medoids, pngs #, fingers

# medoids = [help_functions.transform_data(medoid_functions.get_shape_medoid(
#            pkl.load(open('dataset/configs/' + config + '/itsaso_newCam.pkl','rb')))) for config in configurations]
# pkl.dump(medoids,open('dataset/configs/itsaso_newCam_allMEDOIDS.pkl','wb'))
# figures = [medoid_functions.obtain_graph(medoid) for medoid in medoids]
# pkl.dump(figures, open('dataset/configs/itsaso_newCam_allMEDOIDS_GRAPHS.pkl','wb'))

layout = html.Div([
    html.Div([
        html.Img(id='video', src='/user/configurations/video_mediapipe_feed'),
    ], style = {'width':'49%','display':'inline-block','verticalAlign':'top'}),
    html.Div([
        html.Div([
            html.H3('Choose a configuration to practice'),
            dcc.Dropdown(
                id='config-medoid',
                options=[dict((('label',config), ('value',config))) for config in configurations],
                value = '1',
                clearable=False
                #style = {'width':'130%'}
            )
        ]),
        
        # html.Div(id='textarea-classif', style={'whiteSpace': 'pre'}),
        html.Div(html.Img(id='img-config-medoid',src=pngs[0],style={'height':'50%', 'width':'50%'}),style={'width':'49%','display':'inline-block','verticalAlign':'top'}),                            
        html.Div(dcc.Graph(
            id='graph-medoid',
            figure=figures_medoids[int(configurations[0])-1],#medoid_functions.obtain_graph(medoids[int(configurations[0])-1]), #medoid_functions.get_shape_medoid(pkl.load(open('dataset/configs/1/itsaso_newCam.pkl','rb')))),
            responsive=True,
            # style={
            #     'width': '100%',
            #     'height': '100%',
            #     'display':'inline-block',
            #     'verticalAlign':'middle'
            # }
        ),style={'display':'inline-block','width':'49%','margin-right':'10px'}),
        dcc.Interval('interval-prediction',
                    interval=0.5*1000,
                    n_intervals=0
        ),
    ], id='div-medoid', style={'display':'inline-block', 'width':'49%'}),
    html.Div(id='textarea-prediction-output', style={'whiteSpace': 'pre','width':'49%'}),
    html.Div(id='textarea-prediction-wrong', style={'whiteSpace': 'pre','width':'49%'}),
    html.Div(html.Img(id='img-config-wrong',src=None,style={'height':'10%', 'width':'10%'}),style={'width':'49%','display':'inline-block','verticalAlign':'top'}),
    #dcc.Store(id='store-user-performance',data={'real':[],'pred':[], 'times':[]}),
    html.Div([
        dbc.Button('PERFOMANCE SUMMARY',n_clicks=0,outline=True, color='primary',id='button-performance',href='/summary_user'),
    ])
    
])

@callback([Output('graph-medoid','figure'),Output('graph-medoid','style'),
           Output('img-config-medoid','src')],
           Input('config-medoid','value'), prevent_initial_call=True)
def show_medoid_graph(configuration):

    # # data = pkl.load(open('dataset/configs/' + configuration + '/itsaso_newCam.pkl','rb'))
    # # medoid = medoid_functions.get_shape_medoid(data)
    # medoid = medoids[int(configuration)-1]
    # figure_actual = medoid_functions.obtain_graph(medoid)
    figure_actual = figures_medoids[int(configuration)-1]
    style = {
                'width': '100%',
                'height': '100%',
                'display':'inline-block'
            }

    src_img = pngs[int(configuration)-1]
    return figure_actual, style, src_img

@callback([Output('textarea-prediction-output','children'), Output('textarea-prediction-output','style'), 
          Output('img-config-wrong','src'), Output('textarea-prediction-wrong','children'),
          Output('store-user-performance','data')],
          Input('interval-prediction','n_intervals'),
          [State('config-medoid','value'), State('textarea-prediction-output','style'), State('store-user-performance','data')])
def make_prediction_medoid(interval, config_value, actual_style, saved_preds):
    from global_ import landmarks
    png_actual = None
    text = None
    if landmarks is not None:
        landmarks_to_predict = help_functions.transform_data(landmarks)

        dists = [medoid_functions.procrustes_disparity(actual_medoid, landmarks_to_predict) for actual_medoid in medoids]
        min_index = int(np.where(dists == np.amin(dists))[0])
        result = configurations[min_index]

        if result == config_value:
            style = {'backgroundColor':'#99FF99'}
        else:
            png_actual = pngs[int(result)-1]
            text = 'The hand configuration you are performing looks like the image below. Try again!'
            style = {'backgroundColor':'#FF9999'}

            # GUARDAR SOLO LOS FALLOS
            if(len(saved_preds['pred'])>24):
                saved_preds['pred'].pop(0)
                saved_preds['real'].pop(0)

            saved_preds['pred'].append(result)
            saved_preds['real'].append(config_value)


        # #tr1, tr2 = medoid_functions.procrustes_disparity_transformed_matrices(medoids[min_index],landmarks_to_predict)
        # for finger in range(5):
        #     medoid_finger = medoids[min_index][finger*4+1:finger*4+5,:]
        #     landmark_finger = landmarks_to_predict[finger*4+1:finger*4+4+1,:] 
        #     print(fingers[finger])
        #     print(medoid_finger)
        #     print(landmark_finger)
        #     close = np.allclose(medoid_finger,landmark_finger, rtol=0, atol=1e-01) #rtol=1e-03, atol=1e-01)
        #     print(close)
        #     print('--------------------------------')
        #     if not close:
        #         result = result + ' - Please pay attention to your ' + fingers[finger] + ' finger'

        return result, style, png_actual, text, saved_preds

    return '', actual_style, png_actual, text, saved_preds