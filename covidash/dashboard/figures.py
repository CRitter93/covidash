import plotly.express as px
import plotly.graph_objects as go


def get_main_map_landkreise(data_store):
    geodata = data_store.get('geo_landkreise')

    values = data_store.get('rki_landkreise')

    map_fig = px.choropleth_mapbox(values, geojson=geodata, locations='OBJECTID', color='cases',
                                   featureidkey="properties.OBJECTID",
                                   mapbox_style='open-street-map',
                                   hover_name='GEN',
                                   hover_data=['cases'],#, 'OBJECTID'],
                                   center=dict(lat=51.1657, lon=10.4515),
                                   zoom=5.5,
                                   labels={'cases': 'Fälle'}
                                   )
    map_fig.update_layout(height=800, margin={"r": 20, "t": 20, "l": 20, "b": 20})#, clickmode='event+select')
    return map_fig


def update_map(data_store, figure, gender_filter='All', age_filter='All', date_filter='All', delta=False):
    values = data_store.get('rki_covid_19')

    obj_ids = data_store.get('rki_landkreise')[['OBJECTID']]

    if gender_filter != 'All':
        values = values[values.gender == gender_filter]

    if age_filter != 'All':
        values = values[values.age == age_filter]

    if date_filter != 'All':
        values = values[values.date <= date_filter]
        if delta:
            values = values[values.date == date_filter]

    new_data = values.groupby('OBJECTID').agg({'cases': 'sum'}).reset_index()
    new_data = obj_ids.merge(new_data, on='OBJECTID', how='left').fillna(0)
    figure.plotly_restyle({'z': new_data.cases.values})
    return figure


def line_plot(data_store, obj_id='All'):
    values = data_store.get('rki_covid_19')
    if obj_id != 'All':
        values = values[values.OBJECTID == obj_id]
    data = values.groupby('date').agg({'cases': 'sum'}).reset_index()
    data.cases = data.cases.cumsum()
    line_plot = go.Figure()
    line_plot.add_trace(go.Scatter(x=data.date, y=data.cases, mode='lines+markers', line_shape='spline'))
    line_plot.update_layout(title='Anzahl der Covid-19 Fälle in {}'.format('Deutschland' if obj_id == 'All' else values.GEN.values[0]))
    return line_plot
