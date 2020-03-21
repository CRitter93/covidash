import plotly.express as px
import plotly.graph_objects as go


def _apply_filters(values, filters, ignore=None):
    if 'geo' in filters and ignore != 'geo':
        values = values[values.OBJECTID.isin(filters['geo'])]
    if 'age' in filters and ignore != 'age':
        values = values[values.age.isin(filters['age'])]
    if 'gender' in filters and ignore != 'gender':
        values = values[values.gender.isin(filters['gender'])]
    if 'date' in filters and ignore != 'date':
        values = values[values.date.isin(filters['date'])]
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
                                   zoom=5.5,
                                   labels={'cases': 'Fälle'}
                                   )
    map_fig.update_layout(height=800, margin={"r": 20, "t": 20, "l": 20, "b": 20}, clickmode='event+select')
    return map_fig


def update_map(data_store, figure, filters):
    values = data_store.get('rki_covid_19')

    obj_ids = data_store.get('rki_landkreise')[['OBJECTID']]

    values = _apply_filters(values, filters, 'geo')

    new_data = values.groupby('OBJECTID').agg({'cases': 'sum'}).reset_index()
    new_data = obj_ids.merge(new_data, on='OBJECTID', how='left').fillna(0)
    figure['data'][0]['z'] = new_data.cases
    return figure


def line_plot(data_store, filters):
    values = data_store.get('rki_covid_19')
    values = _apply_filters(values, filters)
    data = values.groupby('date').agg({'cases': 'sum'}).reset_index().sort_values('date')
    data.cases = data.cases.cumsum()
    line_plot = go.Figure()
    line_plot.add_trace(go.Scatter(x=data.date, y=data.cases, mode='lines+markers', line_shape='spline'))
    line_plot.update_layout(title='Anzahl der Covid-19 Fälle in {}'.format('Deutschland' if not 'geo' in filters else filters['geo']))
    return line_plot


def bar_chart(data_store, category, filters):
    values = data_store.get('rki_covid_19')
    all_vals = values[[category]].drop_duplicates()
    values = _apply_filters(values, filters, category)
    values = values.groupby(category).agg({'cases': 'sum'}).reset_index().merge(all_vals, on=category, how='right').fillna(0).sort_values(category)
    donut = go.Figure(data=[go.Bar(x=values[category], y=values.cases)])
    category_german = ''
    if category == 'age':
        category_german = 'Alters'
    if category == 'gender':
        category_german = 'Geschlechts'
    donut.update_layout(title='Verteilung des {}'.format(category_german), clickmode='event+select')
    return donut


def update_bar(data_store, figure, category, filters):
    values = data_store.get('rki_covid_19')
    all_vals = values[[category]].drop_duplicates()
    values = _apply_filters(values, filters, category)
    values = values.groupby(category).agg({'cases': 'sum'}).reset_index().merge(all_vals, on=category, how='right').fillna(0).sort_values(category)
    figure['data'][0]['y'] = values.cases
    return figure


def update_line(data_store, figure, filters):
    values = data_store.get('rki_covid_19')
    values = _apply_filters(values, filters)
    data = values.groupby('date').agg({'cases': 'sum'}).reset_index().sort_values('date')
    data.cases = data.cases.cumsum()
    figure['data'][0]['y'] = data.cases
    return figure
