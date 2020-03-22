import plotly.express as px
import plotly.graph_objects as go

DATA_TYPE_MAPPING = {
        'total': 'Fälle insgesamt',
        'new'  : 'Neuinfektionen',
        'trend': 'Trend'
        }

GERMAN_CATEGORY_MAPPING = {
        'age'   : 'Alter',
        'gender': 'Geschlecht'
        }

DATA_DROPDOWN_TO_COLUMN_MAPPING = {
        'total': 'total_cases',
        'new'  : 'cases',
        'trend': 'cases_trend'
        }

BAR_CHART_TITLE = 'Verteilung des {}s über {}'

THE_CURVE_TITLE = 'Verlauf der Covid-19 {} in {}'


def _apply_filters(values, filters, ignore=None):
    if ignore is None:
        ignore = []
    if 'date' in filters and 'date' not in ignore:
        values = values[values.date == filters['date']]
    if 'geo' in filters and 'geo' not in ignore:
        if filters['granularity'] and filters['granularity'] == 'bundesland':
            values = values[values.OBJECTID_1.isin(filters['geo'])]
        else:
            values = values[values.OBJECTID.isin(filters['geo'])]
    if 'age' in filters and 'age' not in ignore:
        values = values[values.age.isin(filters['age'])]
    if 'gender' in filters and 'gender' not in ignore:
        values = values[values.gender.isin(filters['gender'])]
    return values


def get_main_map_landkreise(data_store):
    geodata = data_store.get('geo_landkreise')

    values = data_store.get('rki_landkreise')

    map_fig = px.choropleth_mapbox(values, geojson=geodata, locations='OBJECTID', color='cases',
                                   featureidkey="properties.OBJECTID",
                                   mapbox_style='open-street-map',
                                   hover_name='GEN',
                                   hover_data=['cases'],
                                   center=dict(lat=51.1657, lon=10.4515),
                                   zoom=5.5
                                   )
    map_fig.update_layout(height=800, margin={"r": 20, "t": 20, "l": 20, "b": 20}, clickmode='event+select')

    map_fig['data'][0]['hovertemplate'] = '<b>%{hovertext}</b><br><br>' + DATA_TYPE_MAPPING['total'] + ': %{z}'

    return map_fig


def get_main_map_bundeslaender(data_store):
    geodata = data_store.get('geo_bundeslaender')

    values = data_store.get('rki_bundeslaender').sort_values('OBJECTID_1')

    map_fig = px.choropleth_mapbox(values, geojson=geodata, locations='OBJECTID_1', color='Fallzahl',
                                   featureidkey="properties.OBJECTID_1",
                                   mapbox_style='open-street-map',
                                   hover_name='LAN_ew_GEN',
                                   hover_data=['Fallzahl'],
                                   center=dict(lat=51.1657, lon=10.4515),
                                   zoom=5.5
                                   )
    map_fig.update_layout(height=800, margin={"r": 20, "t": 20, "l": 20, "b": 20}, clickmode='event+select')

    map_fig['data'][0]['hovertemplate'] = '<b>%{hovertext}</b><br><br>' + DATA_TYPE_MAPPING['total'] + ': %{z}'

    return map_fig


def update_map(data_store, figure, filters):
    values = data_store.get('rki_covid_19_dense')

    obj_id = 'OBJECTID'
    granularity = filters.get('granularity')
    rki_data = data_store.get('rki_landkreise')
    if granularity and granularity == 'bundesland':
        obj_id = 'OBJECTID_1'
        rki_data = data_store.get('rki_bundeslaender')

    obj_ids = rki_data[[obj_id]].drop_duplicates().sort_values(obj_id)

    values = _apply_filters(values, filters, ['geo'])

    column = DATA_DROPDOWN_TO_COLUMN_MAPPING.get(filters['data'])

    new_data = values.groupby(obj_id).agg({column: 'sum'}).reset_index()
    new_data = obj_ids.merge(new_data, on=obj_id, how='left').fillna(0)
    figure['data'][0]['z'] = new_data[column]
    figure['data'][0]['hovertemplate'] = '<b>%{hovertext}</b><br><br>' + DATA_TYPE_MAPPING[filters['data']] + ': %{z}'
    return figure


def the_curve_line(data_store, filters):
    values = data_store.get('rki_covid_19_dense')
    if filters is not None:
        values = _apply_filters(values, filters, ['date'])
    column = DATA_DROPDOWN_TO_COLUMN_MAPPING.get(filters['data']) if filters.get('data') else 'total_cases'
    data = values.groupby('date').agg({column: 'sum'}).reset_index().sort_values('date')
    line_plot = go.Figure()
    name_mapping = data_store.get('object_id_to_name_bundesland') if filters.get('granularity') == 'bundesland' else data_store.get('object_id_to_name_landkreis')
    line_plot.add_trace(go.Scatter(x=data.date.astype(str), y=data[column], mode='lines+markers', line_shape='spline'))
    line_plot.update_layout(title=THE_CURVE_TITLE.format(DATA_TYPE_MAPPING.get(filters['data'] if filters.get('data') else 'total'),
                                                         'Deutschland' if filters is None or not 'geo' in filters else ', '.join([name_mapping.get(id) for id in filters['geo']])))
    return line_plot


def the_curve_bar(data_store, filters):
    values = data_store.get('rki_covid_19_dense')
    if filters is not None:
        values = _apply_filters(values, filters, ['date'])
    column = DATA_DROPDOWN_TO_COLUMN_MAPPING.get(filters['data']) if filters.get('data') else 'total_cases'
    data = values.groupby('date').agg({column: 'sum'}).reset_index().sort_values('date')
    bar_plot = go.Figure()
    name_mapping = data_store.get('object_id_to_name_bundesland') if filters.get('granularity') == 'bundesland' else data_store.get('object_id_to_name_landkreis')
    bar_plot.add_trace(go.Bar(x=data.date.astype(str), y=data[column]))
    bar_plot.update_layout(title=THE_CURVE_TITLE.format(DATA_TYPE_MAPPING.get(filters['data'] if filters.get('data') else 'total'),
                                                        'Deutschland' if filters is None or not 'geo' in filters else ', '.join([name_mapping.get(id) for id in filters['geo']])))
    return bar_plot


def bar_chart(data_store, category, filters):
    values = data_store.get('rki_covid_19_dense')
    all_vals = values[[category]].drop_duplicates()
    values = _apply_filters(values, filters, [category])
    values = values.groupby(category).agg({'total_cases': 'sum'}).reset_index().merge(all_vals, on=category, how='right').fillna(0).sort_values(category)
    donut = go.Figure(data=[go.Bar(x=values[category], y=values.total_cases)])
    donut.update_layout(title=BAR_CHART_TITLE.format(GERMAN_CATEGORY_MAPPING.get(category), DATA_TYPE_MAPPING['total']), clickmode='event+select')
    return donut


def update_bar(data_store, figure, category, filters):
    values = data_store.get('rki_covid_19_dense')
    all_vals = values[[category]].drop_duplicates()
    values = _apply_filters(values, filters, [category])

    data_type = filters['data']
    column = DATA_DROPDOWN_TO_COLUMN_MAPPING.get(data_type)

    values = values.groupby(category).agg({column: 'sum'}).reset_index().merge(all_vals, on=category, how='right').fillna(0).sort_values(category)
    figure['data'][0]['y'] = values[column]
    figure['layout']['title']['text'] = BAR_CHART_TITLE.format(GERMAN_CATEGORY_MAPPING.get(category), DATA_TYPE_MAPPING[data_type])
    return figure


def update_the_curve(data_store, figure, filters):
    values = data_store.get('rki_covid_19_dense')
    values = _apply_filters(values, filters, ['date'])
    column = DATA_DROPDOWN_TO_COLUMN_MAPPING.get(filters['data'])
    data = values.groupby('date').agg({column: 'sum'}).reset_index().sort_values('date')
    figure['data'][0]['y'] = data[column]
    name_mapping = data_store.get('object_id_to_name_bundesland') if filters.get('granularity') == 'bundesland' else data_store.get('object_id_to_name_landkreis')
    figure['layout']['title']['text'] = THE_CURVE_TITLE.format(DATA_TYPE_MAPPING.get(filters['data'] if filters.get('data') else 'total'),
                                                               'Deutschland' if filters is None or not 'geo' in filters else ', '.join([name_mapping.get(id) for id in filters['geo']]))
    return figure
