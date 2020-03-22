import pandas as pd
import json
import numpy as np
import pprint
#from shapely.geometry import Polygon, Point
import geopandas as gpd
from tqdm import tqdm

def read_json_data(json_file):
    with open(json_file) as json_file:
        json_data = json.load(json_file)
    return json_data

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

def get_hospital_list():
    """"reads a json extracts hospital info and merges it with lat long coordinates"""
    json_hospital = read_json_data("../../data/raw/osm_hospital_locations_germany.json")
    features = json_hospital['features']
    df_hospital_properties = pd.DataFrame([item['properties'] for item in features])
    df_hospital_points = pd.DataFrame([item['geometry']['coordinates'] for item in features])

    df_hospitals = df_hospital_properties.join(df_hospital_points)
    return df_hospitals.rename(columns={0:"x",1:"y"})

df_covid = pd.read_csv('../../data/raw/rki_covid_19.csv')

df__rki_landkreise = pd.read_csv('../../data/raw/rki_corona_landkreise.csv')

df_hospital = get_hospital_list()

gdf_states = gpd.read_file("../../data/raw/bundeslaender_grenzen_2019.geojson")

gdf_hospitals = gpd.read_file("../../data/raw/osm_hospital_locations_germany.json").drop([166, 284, 285, 291])


hospital_state_map = {}
for idx, coord in gdf_hospitals.iterrows():
    for _idx, _row in  gdf_states.iterrows():
        if coord['geometry'].within(_row.geometry):
            hospital_state_map[idx] = _row.LAN_GEN

gdf_hospitals['hospital_index'] = gdf_hospitals.index.tolist()

def hosp_index_to_state(state_map,item_idx):
    try:
        state_name = state_map[item_idx]
        return state_name
    except KeyError:
        return np.nan

gdf_hospitals['state_name'] = gdf_hospitals.hospital_index.apply(lambda row: hosp_index_to_state(hospital_state_map,row))

gdf_hospitals.to_json("../../data/processed/osm_hospital_locations_germany_with_States.json")






print("1")
