import pandas as pd
import os.path

DATA_DIR = '../../data'


def process_rki_covid_19():
    raw_data_df = pd.read_csv(os.path.join(DATA_DIR, 'raw', 'rki_covid_19.csv'))
    landkreis_df = pd.read_csv(os.path.join(DATA_DIR, 'raw', 'rki_corona_landkreise.csv'))
    covid_19_df = raw_data_df.merge(landkreis_df[['county', 'OBJECTID', 'GEN']], left_on='Landkreis', right_on='county')
    covid_19_df.Meldedatum = covid_19_df.Meldedatum.astype('datetime64').dt.strftime('%Y-%m-%d')
    covid_19_df = covid_19_df[['Altersgruppe', 'Geschlecht', 'AnzahlFall', 'AnzahlTodesfall', 'Meldedatum', 'OBJECTID', 'GEN']]
    covid_19_df.columns = ['age', 'gender', 'cases', 'deaths', 'date', 'OBJECTID', 'GEN']
    covid_19_df.to_csv(os.path.join(DATA_DIR, 'processed', 'rki_covid_19.csv'))


if __name__ == '__main__':
    process_rki_covid_19()
