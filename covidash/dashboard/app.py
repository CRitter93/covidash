import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import datetime

from covidash.dashboard.data_store import DataStore
import covidash.dashboard.figures as figures

data_store = DataStore('../../data')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
        html.H1(children='Covid-19 Ausbreitung in Deutschland'),

        html.Div(children=[
                html.Div(children='''
                Dieses Dashboard dient der Visualisierung und Analyse der zeitlichen und geographischen Ausbreitung von Covid-19 in Deutschland.\n
                Die Daten stammen vom Robert-Koch Institut und können auf der folgenden Seite abgerufen werden (Stand 20.03.2020): 
                '''),

                dcc.Link('NPGEO Corona Hub 2020',
                         href="https://npgeo-corona-npgeo-de.hub.arcgis.com/")],
                className='row'),

        # html.Div(children=[
        #         dcc.Dropdown(
        #                 id='gender-dropdown',
        #                 options=[
        #                         {'label': 'Alle Geschlechter', 'value': 'All'},
        #                         {'label': 'Männlich', 'value': 'M'},
        #                         {'label': 'Weiblich', 'value': 'W'}
        #                         ],
        #                 value='All',
        #                 className="six columns"
        #                 ),
        #
        #         dcc.Dropdown(
        #                 id='age-dropdown',
        #                 options=[
        #                         {'label': 'Alle Altersgruppen', 'value': 'All'},
        #                         {'label': '0-4', 'value': 'A00-A04'},
        #                         {'label': '5-14', 'value': 'A05-A14'},
        #                         {'label': '15-34', 'value': 'A15-A34'},
        #                         {'label': '35-59', 'value': 'A35-A59'},
        #                         {'label': '60-79', 'value': 'A60-A79'},
        #                         {'label': '80+', 'value': 'A80+'}
        #                         ],
        #                 value='All',
        #                 className="six columns"
        #                 )],
        #         className='row'),

        html.Div(children=[
                dcc.Graph(
                        id='map-graph',
                        figure=figures.get_main_map_landkreise(data_store),
                        className="six columns",
                        ),
                html.Div(children=[
                        dcc.Graph(
                                id='time-graph',
                                figure=figures.line_plot(data_store, {}),
                                className='row'
                                ),
                        html.Div(children=[
                                dcc.Graph(
                                        id='gender-graph',
                                        figure=figures.bar_chart(data_store, 'gender', {}),
                                        className='six columns'
                                        ),
                                dcc.Graph(
                                        id='age-graph',
                                        figure=figures.bar_chart(data_store, 'age', {}),
                                        className='six columns'
                                        )
                                ],
                                className='row')],
                        className="six columns")],
                className='row',
                style={'height': 'auto'}),

        # hidden div for storing filtering
        html.Div(id='filter-values', style={'display': 'none'})

        ], className='twelve columns', style={'height': 'auto'})


@app.callback(
        Output('filter-values', 'children'),
        [Input('map-graph', 'selectedData'), Input('gender-graph', 'selectedData'), Input('age-graph', 'selectedData')]
        )
def update_filtering(geo_selection, gender_selection, age_selection):
    filters = {}
    if geo_selection:
        filters['geo'] = [data['location'] for data in geo_selection['points']]
    if gender_selection:
        filters['gender'] = [data['x'] for data in gender_selection['points']]
    if age_selection:
        filters['age'] = [data['x'] for data in age_selection['points']]
    return json.dumps(filters)


@app.callback(
        [Output('time-graph', 'figure'), Output('gender-graph', 'figure'), Output('age-graph', 'figure'), Output('map-graph', 'figure')],
        [Input('filter-values', 'children')],
        [State('time-graph', 'figure'), State('gender-graph', 'figure'), State('age-graph', 'figure'), State('map-graph', 'figure')])
def filter_graphs(filter_data, time_plot, gender_bar, age_bar, map_graph):
    filters = json.loads(filter_data)
    return [figures.update_line(data_store, time_plot, filters),
            figures.update_bar(data_store, gender_bar, 'gender', filters),
            figures.update_bar(data_store, age_bar, 'age', filters),
            figures.update_map(data_store, map_graph, filters)]


if __name__ == '__main__':
    app.run_server(debug=True)
