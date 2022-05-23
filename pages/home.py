from dash import html
import dash
import dash_bootstrap_components as dbc
import base64

dash.register_page(__name__, path="/")

# app = Dash(__name__, suppress_callback_exceptions=True)
# server = app.server


layout = html.Div([
    html.Div([
        html.Div("In the Spanish Sign Language, apart from the body position and facial expression, four different manual elements define the articulation of the sign:"),
        #html.Div(html.Img(id='img-config-medoid',src='data:image/png;base64,{}'.format(base64.b64encode(open("dataset/elements.png", 'rb').read()).decode()))),#style={'width':'40%','height':'40%'})),
        html.Div(
            children=[
                html.Ul(id='my-list', children=[
                    html.Li('Location.'),
                    html.Li('Configuration (hand shape).'),
                    html.Li('Orientation.'),
                    html.Li('Movement.')
                ])
            ]
        ),
        html.Div('For a first contact with sign language, here you can learn and practise the 42 configurations of the LSE, shown on the image below.'),
        html.Div(html.Img(id='img-config-medoid',src='data:image/png;base64,{}'.format(base64.b64encode(open("dataset/configs.png", 'rb').read()).decode()),style={'width':'70%','height':'70%'}),style={'textAlign':'center'}),
        dbc.Button('LEARN CONFIGURATIONS', outline=True, color="danger", href='/medoids/'),
        dbc.Button('PRACTICE CONFIGURATIONS WITH SIGNS', outline=True, color="success", href='/practice_signs/'),
    ], style={'width':'100%', 'display':'inline-block'}, className="d-grid gap-2 col-6 mx-auto"),                           

], style={'display':'flex'})


# if __name__ == '__main__':
#     app.run_server(debug=True)


