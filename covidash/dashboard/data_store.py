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
        self.data['rki_covid_19'] = pd.read_csv(os.path.join(data_folder, 'processed', 'rki_covid_19.csv'))
        self.data['rki_bundeslaender'] = pd.read_csv(os.path.join(data_folder, 'raw', 'rki_corona_bundeslaender.csv'))
        with open(os.path.join(data_folder, 'raw', 'rki_corona_bundeslaender.geojson')) as json_file:
            self.data['geo_bundeslaender'] = json.load(json_file)

    def get(self, data_name):
        return self.data.get(data_name)
