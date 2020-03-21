import pandas as pd
import json
import numpy as np


def read_json_data(json_file):
    with open(json_file) as json_file:
        json_data = json.load(json_file)
    return json_data

def get_hospital_list():
    """"reads a json extracts hospital info and merges it with lat long coordinates"""
    json_hospital = read_json_data("data/raw/osm_hospital_locations_germany.json")
    df_hospital_properties = pd.DataFrame([item['properties'] for item in features])
    df_hospital_points = pd.DataFrame([item['geometry']['coordinates'] for item in features])

    df_hospitals = df_hospital_properites.join(df_hospital_points)
    return df_hospitals.rename(columns={0:"x",1:"y"})

df_covid = pd.read_csv('data/raw/rki_covid_19.csv')

df_landkreise = pd.read_csv('data/raw/rki_corona_landkreise.csv')

df_hospital = get_hospital_list()



