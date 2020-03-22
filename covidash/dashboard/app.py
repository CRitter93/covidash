import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from covidash.dashboard.data_store import DataStore
import covidash.dashboard.figures as figures
from covidash.dashboard.figures import DATA_TYPE_MAPPING

data_store = DataStore('../../data')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
        html.H1(children='Covid-19 Ausbreitung in Deutschland'),

        html.Div(children=[
                html.Div(children=[
                        html.Div(children='''
                                Dieses Dashboard dient der Visualisierung und Analyse der zeitlichen und geographischen Ausbreitung von Covid-19 in Deutschland.\n
                                Die Daten stammen vom Robert-Koch Institut und können auf der folgenden Seite abgerufen werden (Stand {}): 
                                '''.format(data_store.get('latest_date')), className='ten columns'),

                        dcc.Link('NPGEO Corona Hub 2020',
                                 href="https://npgeo-corona-npgeo-de.hub.arcgis.com/", className='two columns')
                        ], className='row'),
                html.Div(children=[
                        dcc.DatePickerSingle(
                                id='date-picker',
                                min_date_allowed=data_store.get('first_date'),
                                max_date_allowed=data_store.get('latest_date'),
                                initial_visible_month=data_store.get('latest_date'),
                                date=str(data_store.get('latest_date')),
                                display_format='DD.MM.YYYY',
                                className='two columns'
                                ),
                        dcc.Dropdown(
                                id='data-dropdown',
                                options=[
                                        {'label': DATA_TYPE_MAPPING[type], 'value': type} for type in DATA_TYPE_MAPPING
                                        ],
                                value='total',
                                clearable=False,
                                className='two columns'
                                ),
                        dcc.Dropdown(
                                id='granularity-dropdown',
                                options=[
                                        {'label': 'Landkreise', 'value': 'landkreis'},
                                        {'label': 'Bundesländer', 'value': 'bundesland'}
                                        ],
                                value='landkreis',
                                clearable=False,
                                className='two columns'
                                ),
                        ], className='row')

                ],

                className='row'),

        html.Div(children=[
                dcc.Graph(
                        id='map-graph',
                        figure=figures.get_main_map_landkreise(data_store),
                        className="six columns",
                        ),
                html.Div(children=[
                        dcc.Graph(
                                id='the-curve-graph',
                                figure=figures.the_curve_line(data_store, {}),
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
        html.Div(children='{}', id='filter-values', style={'display': 'none'})

        ], style={'height': 'auto'})


@app.callback(
        Output('filter-values', 'children'),
        [Input('map-graph', 'selectedData'), Input('gender-graph', 'selectedData'), Input('age-graph', 'selectedData'), Input('date-picker', 'date'),
         Input('data-dropdown', 'value'), Input('granularity-dropdown', 'value')],
        [State('filter-values', 'children')]
        )
def update_filtering(geo_selection, gender_selection, age_selection, date, data, granularity, current_filters):
    current_filters = json.loads(current_filters)
    current_granularity = current_filters.get('granularity')
    current_data = current_filters.get('data')
    filters = {}
    if geo_selection:
        filters['geo'] = [data['location'] for data in geo_selection['points']]
    if gender_selection:
        filters['gender'] = [data['x'] for data in gender_selection['points']]
    if age_selection:
        filters['age'] = [data['x'] for data in age_selection['points']]
    if date:
        filters['date'] = date
    if data:
        filters['data'] = data
        if current_data != data:
            filters['data_changed'] = True
    if granularity:
        filters['granularity'] = granularity
        if current_granularity != granularity:
            filters['granularity_changed'] = True
            # clear geo filters
            if filters.get('geo') is not None:
                del filters['geo']
    return json.dumps(filters)


@app.callback(
        [Output('the-curve-graph', 'figure'), Output('gender-graph', 'figure'), Output('age-graph', 'figure'), Output('map-graph', 'figure')],
        [Input('filter-values', 'children')],
        [State('the-curve-graph', 'figure'), State('gender-graph', 'figure'), State('age-graph', 'figure'), State('map-graph', 'figure')])
def filter_graphs(filter_data, the_curve, gender_bar, age_bar, map_graph):
    filters = json.loads(filter_data)
    if filters.get('granularity_changed'):
        if filters.get('granularity') == 'landkreis':
            map_figure = figures.get_main_map_landkreise(data_store)
        elif filters.get('granularity') == 'bundesland':
            map_figure = figures.get_main_map_bundeslaender(data_store)
        else:
            raise ValueError
        # update map anyways to apply the correct filter
        map_figure = figures.update_map(data_store, map_figure, filters)
    else:
        map_figure = figures.update_map(data_store, map_graph, filters)

    if filters.get('data_changed'):
        if filters['data'] == 'total':
            the_curve_figure = figures.the_curve_line(data_store, filters)
        else:
            the_curve_figure = figures.the_curve_bar(data_store, filters)
    else:
        the_curve_figure = figures.update_the_curve(data_store, the_curve, filters)

    return [the_curve_figure,
            figures.update_bar(data_store, gender_bar, 'gender', filters),
            figures.update_bar(data_store, age_bar, 'age', filters),
            map_figure]


if __name__ == '__main__':
    app.run_server(debug=True)
