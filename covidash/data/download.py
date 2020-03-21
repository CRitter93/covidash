import os.path
import urllib.request

DATA_DIR = '../../data/raw'


def download_rki_covid_19():
    url = 'https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.csv'
    file_name = os.path.join(DATA_DIR, 'rki_covid_19.csv')
    urllib.request.urlretrieve(url, file_name)


def download_rki_corona_landkreise():
    url = 'https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv'
    file_name = os.path.join(DATA_DIR, 'rki_corona_landkreise.csv')
    urllib.request.urlretrieve(url, file_name)


def download_rki_corona_landkreise():
    "Data Source https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/esri-de-content::bundesl%C3%A4ndergrenzen-2019/geoservice"
    url = 'https://opendata.arcgis.com/datasets/9ae4f23075d340adb6580a6d9603f9fa_0.geojson'
    file_name = os.path.join(DATA_DIR, 'bundeslaender_grenzen_2019.geojson')


if __name__ == '__main__':
    download_rki_covid_19()
    download_rki_corona_landkreise()
