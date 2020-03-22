import json
import os.path

import pandas as pd


class DataStore:
    def __init__(self, data_folder):
        self.data = {}
        with open(os.path.join(data_folder, 'raw', 'rki_corona_landkreise.geojson')) as json_file:
            self.data['geo_landkreise'] = json.load(json_file)
        self.data['rki_landkreise'] = pd.read_csv(os.path.join(data_folder, 'raw', 'rki_corona_landkreise.csv'))[['OBJECTID', 'GEN',
            'cases', 'deaths', 'cases_per_100k', 'cases_per_population', 'BL', 'BL_ID', 'county']]
        self.data['rki_covid_19'] = pd.read_csv(os.path.join(data_folder, 'processed', 'rki_covid_19.csv'), dtype={'age': str})
        self.data['rki_bundeslaender'] = pd.read_csv(os.path.join(data_folder, 'raw', 'rki_corona_bundeslaender.csv'))
        with open(os.path.join(data_folder, 'raw', 'rki_corona_bundeslaender.geojson')) as json_file:
            self.data['geo_bundeslaender'] = json.load(json_file)
        self.data['rki_covid_19_dense'] = pd.read_csv(os.path.join(data_folder, 'processed', 'rki_covid_19_dense.csv'), dtype={'age': str})
        dates = self.data['rki_covid_19_dense'].date.unique()
        self.data['first_date'] = dates.min()
        self.data['latest_date'] = dates.max()
        unique_id_name_pairs = self.data['rki_landkreise'][['OBJECTID', 'GEN']].drop_duplicates()
        self.data['object_id_to_name_landkreis'] = {id: name for id, name in zip(unique_id_name_pairs.OBJECTID.values, unique_id_name_pairs.GEN.values)}
        unique_id_name_pairs = self.data['rki_bundeslaender'][['OBJECTID_1', 'LAN_ew_GEN']].drop_duplicates()
        self.data['object_id_to_name_bundesland'] = {id: name for id, name in zip(unique_id_name_pairs.OBJECTID_1.values, unique_id_name_pairs.LAN_ew_GEN.values)}
        self.data['rki_covid_19_dense_bundeslaender'] = pd.read_csv(os.path.join(data_folder, 'processed', 'rki_covid_19_dense_bundeslaender.csv'), dtype={'age': str})

    def get(self, data_name):
        return self.data.get(data_name)
