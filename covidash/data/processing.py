import pandas as pd
import os.path

DATA_DIR = '../../data'


def process_rki_covid_19():
    raw_data_df = pd.read_csv(os.path.join(DATA_DIR, 'raw', 'rki_covid_19.csv'))
    landkreis_df = pd.read_csv(os.path.join(DATA_DIR, 'raw', 'rki_corona_landkreise.csv'))
    covid_19_df = raw_data_df.merge(landkreis_df[['county', 'OBJECTID', 'GEN']], left_on='Landkreis', right_on='county')
    covid_19_df.Meldedatum = covid_19_df.Meldedatum.astype('datetime64').dt.strftime('%Y-%m-%d')
    covid_19_df = covid_19_df[['Altersgruppe', 'Geschlecht', 'AnzahlFall', 'AnzahlTodesfall', 'Meldedatum', 'OBJECTID', 'GEN', 'IdBundesland', 'Bundesland']]
    covid_19_df.columns = ['age', 'gender', 'cases', 'deaths', 'date', 'OBJECTID', 'GEN', 'OBJECTID_1', 'Bundesland']
    covid_19_df.age = covid_19_df.age.astype(str)
    covid_19_df.age = covid_19_df.age.replace({
            'A35-A59': '35 bis 59',
            'A60-A79': '60 bis 79',
            'A80+'   : '80+',
            'A15-A34': '15 bis 34',
            'A05-A14': '05 bis 14',
            'A00-A04': '00 bis 04'
            })
    covid_19_df.to_csv(os.path.join(DATA_DIR, 'processed', 'rki_covid_19.csv'), index=False)


def process_rki_covid_19_dense():
    covid_19_df = pd.read_csv(os.path.join(DATA_DIR, 'processed', 'rki_covid_19.csv'))
    date_range = pd.date_range(covid_19_df.date.min(), covid_19_df.date.max())

    # set index to date
    covid_19_df = covid_19_df.set_index('date')
    covid_19_df.index = pd.DatetimeIndex(covid_19_df.index)

    dimensions = ['OBJECTID_1', 'OBJECTID', 'age', 'gender', 'GEN', 'Bundesland']

    # sort for safety of assignments
    covid_19_df = covid_19_df.sort_values(dimensions)

    # fill missing dates per dimension
    covid_19_df = covid_19_df.groupby(dimensions) \
        .apply(lambda x: x[['cases', 'deaths']].reindex(date_range).fillna(0)) \
        .reset_index().rename(columns={'level_{}'.format(len(dimensions)): 'date'})

    # calculate total cases until each point in time per dimension
    covid_19_df[['total_cases', 'total_deaths']] = covid_19_df.groupby(dimensions)[['cases', 'deaths']].cumsum()

    # add trend comparing two subsequent days
    covid_19_df[['cases_trend', 'deaths_trend']] = covid_19_df.groupby(dimensions)[['cases', 'deaths']] \
        .apply(lambda x: x[['cases', 'deaths']] - x[['cases', 'deaths']].shift(1)) \
        .reset_index()[['cases', 'deaths']].fillna(0)

    covid_19_df.to_csv(os.path.join(DATA_DIR, 'processed', 'rki_covid_19_dense.csv'), index=False)

    dimensions = ['OBJECTID_1', 'age', 'gender', 'date', 'Bundesland']

    covid_19_state_df = covid_19_df.groupby(dimensions)[['cases', 'deaths', 'total_cases', 'total_deaths', 'cases_trend', 'deaths_trend']].sum().reset_index()

    covid_19_state_df.to_csv(os.path.join(DATA_DIR, 'processed', 'rki_covid_19_dense_bundeslaender.csv'), index=False)


if __name__ == '__main__':
    process_rki_covid_19()
    process_rki_covid_19_dense()
