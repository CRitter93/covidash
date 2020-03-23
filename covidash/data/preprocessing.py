import pandas as pd
import json
import numpy as np
import pprint
# from shapely.geometry import Polygon, Point
import geopandas as gpd
from tqdm import tqdm


def read_json_data(json_file):
    with open(json_file) as json_file:
        json_data = json.load(json_file)
    return json_data


def merge_hopital_with_state_info():
    file_name = "../../data/processed/osm_hospital_locations_germany_with_States.geojson"
    if not Path(file_name).is_file():
        gdf_states = gpd.read_file("../../data/raw/bundeslaender_grenzen_2019.geojson")

        gdf_hospitals = gpd.read_file("../../data/raw/osm_hospital_locations_germany.json").drop([166, 284, 285, 291])

        hospital_state_map = {}
        for idx, coord in gdf_hospitals.iterrows():
            for _idx, _row in gdf_states.iterrows():
                if coord['geometry'].within(_row.geometry):
                    hospital_state_map[idx] = _row.LAN_GEN

        gdf_hospitals['hospital_index'] = gdf_hospitals.index.tolist()

        def hosp_index_to_state(state_map, item_idx):
            try:
                state_name = state_map[item_idx]
                return state_name
            except KeyError:
                return np.nan

        gdf_hospitals['state_name'] = gdf_hospitals.hospital_index.apply(
            lambda row: hosp_index_to_state(hospital_state_map, row))

        gdf_hospitals.to_file("../../data/processed/osm_hospital_locations_germany_with_States.geojson",driver='GeoJSON')


