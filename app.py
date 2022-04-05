import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from helpers.key_finder import api_key
from helpers.api_call import *
from helpers.vader import sentiment_scores
import pandas as pd

########### Define a few variables ######

tabtitle = 'Movies'
sourceurl = 'https://www.kaggle.com/tmdb/tmdb-movie-metadata'
sourceurl2 = 'https://developers.themoviedb.org/3/getting-started/introduction'
githublink = 'https://github.com/pratikadyalkar/603-movie-reviews-sentiment'
titles = pd.read_csv('data/titles.csv')
titlesdict = pd.Series(titles.id.values, index = titles.title).to_dict()

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout

app.layout = html.Div(children=[
    dcc.Store(id='tmdb-store', storage_type='session'),
    dcc.Store(id='summary-store', storage_type='session'),
    html.Div([
        html.H4(['Movie Reviews']),
        html.Div([
            html.Div([

                html.Div([
                #html.Div('Randomly select a movie summary'),
                dcc.Input(id='text', type='text', placeholder='Search a movie', list='browse',value='',style={'textAlign': 'center', 'font-size':'14px','border': 'thin black solid','margin':'10px',}),
                html.Datalist(id='browse', children=[html.Option(value=word) for word in titlesdict.keys()]),
                html.Button(id='eek-button', n_clicks=0, children='API call', style={'color': 'rgb(255, 255, 255)','backgroundColor': '#999999','border': 'thin black solid','textAlign': 'center'}),
                html.Div(id='movie-title', children=[]),
                html.Div(id='movie-release', children=[]),
                html.Div(id='movie-overview', children=[]),
                ],className='six columns'),
                html.Div([
                html.Img(src='', id='imge',
                style={'height':'400px'})
                ],className='six columns'),

            ], style={ 'padding': '12px',
                    'font-size': '22px',
                    # 'height': '400px',
                    'border': 'thin red solid',
                    #'color': 'rgb(255, 255, 255)',
                    'backgroundColor': '#D3D3D3',
                    'textAlign': 'left',
                    },
            className='twelve columns'),


            html.H4('Output:'),
            html.Div(id='output-div-1',
            style={
            'padding': '12px',
            'border':'thin black solid',
            'backgroundColor': '#D3D3D3',

            }),



        ], className='twelve columns'),
        html.Br(),

    ], className='twelve columns'),


        # Output
    html.Div([
        # Footer
        html.Br(),
        html.A('Code on Github', href=githublink, target="_blank"),
        html.Br(),
        html.A("Data Source: Kaggle", href=sourceurl, target="_blank"),
        html.Br(),
        html.A("Data Source: TMDB", href=sourceurl2, target="_blank"),
    ], className='twelve columns'),



    ]
)

########## Callbacks

# TMDB API call
@app.callback(Output('tmdb-store', 'data'),
              [Input('eek-button', 'n_clicks'),
              Input('text','value')],
              [State('tmdb-store', 'data')])
def on_click(n_clicks,id, data):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks==0:
        data = {'title':' ', 'release_date':' ', 'overview':' '}
    elif n_clicks>0:
        #print(id)
        data = api_pull(titlesdict[id])
    return data

@app.callback([Output('movie-title', 'children'),
                Output('movie-release', 'children'),
                Output('movie-overview', 'children'),
                Output('imge', 'src'),
                Output(component_id='output-div-1', component_property='children'),
                ],
              [Input('tmdb-store', 'modified_timestamp')],
              [State('tmdb-store', 'data')])
def on_data(ts, data):
    if ts is None:
        raise PreventUpdate
    else:
        print(data)
        sentence = data['overview']
        message = sentiment_scores(sentence)
        src = 'https://image.tmdb.org/t/p/original/'+ data['poster_path']
        return data['title'], data['release_date'], data['overview'],src, message


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
