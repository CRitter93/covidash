import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import datetime

from covidash.dashboard.data_store import DataStore
import covidash.dashboard.figures as figures

data_store = DataStore('../../data')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

map_fig = figures.get_main_map_landkreise(data_store)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
        html.H1(children='Covid-19 Ausbreitung in Deutschland'),

        html.Div(children=[
                html.Div(children='''
                Dieses Dashboard dient der Visualisierung und Analyse der zeitlichen und geographischen Ausbreitung von Covid-19 in Deutschland.\n
                Die Daten stammen vom Robert-Koch Institut und können auf der folgenden Seite abgerufen werden (Stand 20.03.2020): 
                '''),

                dcc.Link('NPGEO Corona Hub 2020',
                         href="https://npgeo-corona-npgeo-de.hub.arcgis.com/"],
                className='row'),

        html.Div(children=[
                dcc.Dropdown(
                        id='gender-dropdown',
                        options=[
                                {'label': 'Alle Geschlechter', 'value': 'All'},
                                {'label': 'Männlich', 'value': 'M'},
                                {'label': 'Weiblich', 'value': 'W'}
                                ],
                        value='All',
                        className="six columns"
                        ),

                dcc.Dropdown(
                        id='age-dropdown',
                        options=[
                                {'label': 'Alle Altersgruppen', 'value': 'All'},
                                {'label': '0-4', 'value': 'A00-A04'},
                                {'label': '5-14', 'value': 'A05-A14'},
                                {'label': '15-34', 'value': 'A15-A34'},
                                {'label': '35-59', 'value': 'A35-A59'},
                                {'label': '60-79', 'value': 'A60-A79'},
                                {'label': '80+', 'value': 'A80+'}
                                ],
                        value='All',
                        className="six columns"
                        )],
                className='row'),

        html.Div(children=[
                dcc.Graph(
                        id='map-graph',
                        figure=map_fig,
                        className="six columns",
                        ),

                dcc.Graph(
                        id='time-graph',
                        figure=figures.line_plot(data_store),
                        className="six columns"
                        )],
                className='row',
                style={'height': 'auto'})

        ], className='twelve columns', style={'height': 'auto'})


@app.callback(
        Output('map-graph', 'figure'),
        [Input('gender-dropdown', 'value'), Input('age-dropdown', 'value')])
def test_slider_graph(gender_filter, age_filter):
    return figures.update_map(data_store, map_fig, gender_filter=gender_filter, age_filter=age_filter)

# @app.callback(
#     Output('time-graph', 'figure'),
#     [Input('map-graph', 'clickData')])
# def display_click_data(click_data):
#     print(click_data)
#     # if click_data:
#     #     return figures.line_plot(data_store, click_data['points'][0]['customdata'][1])
#     # else:
#     #     return figures.line_plot(data_store)


if __name__ == '__main__':
    app.run_server(debug=True)
