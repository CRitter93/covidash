import os.path
import urllib.request
from pathlib import Path

DATA_DIR = '../../data/raw'


def get_rki_data(url="", file_name=""):
    file_name = os.path.join(DATA_DIR, file_name)
    if not Path(file_name).is_file():
        urllib.request.urlretrieve(url, file_name)

def download_rki_covid_19():
    get_rki_data(url='https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.csv',
                 file_name='rki_covid_19.csv')

def download_osm_hospital_locations():
    get_rki_data(url="https://opendata.arcgis.com/datasets/348b643c8b234cdc8b1b345210975b87_0.geojson",
                 file_name="osm_hospital_locations_germany.json")

def download_rki_corona_landkreise():
    get_rki_data(url='https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv',
                 file_name='rki_corona_landkreise.csv')

def download_rki_corona_laendergrenzen():
    "Data Source https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/esri-de-content::bundesl%C3%A4ndergrenzen-2019/geoservice"
    get_rki_data(url='https://opendata.arcgis.com/datasets/9ae4f23075d340adb6580a6d9603f9fa_0.geojson',
                 file_name='bundeslaender_grenzen_2019.geojson')



if __name__ == '__main__':
    download_rki_covid_19()
    download_osm_hospital_locations()
    download_rki_corona_landkreise()
    download_rki_corona_laendergrenzen()
