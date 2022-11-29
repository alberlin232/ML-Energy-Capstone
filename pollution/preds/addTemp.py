import glob
import os
import pandas as pd
import numpy as np
from meteostat import Stations, Daily



def get_station(lat, lon):
    stations = Stations()
    stations = stations.nearby(lat, lon)
    stations = stations.fetch()
    if stations.empty:
        return None
    return stations.index[0]

def get_weather(station, start, end):
    if station is None:
        return None
    data = Daily(station, start, end)
    data = data.fetch()
    if data.empty:
        return None
    data = data['tmax'][0]
    return data


if __name__=='__main__':
    # setting the path for joining multiple files
    files = os.path.join("../data/epa/TXHOURLY", "*tx*.csv")

    # list of merged files returned
    files = glob.glob(files)

    print("Resultant CSV after joining all CSV files at a particular location...");

    # joining files with concat and read_csv
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    cols = ['ORISPL_CODE', 'UNITID', 'OP_DATE','OP_HOUR', 'GLOAD (MW)', 'SO2_RATE (lbs/mmBtu)',
        'NOX_RATE (lbs/mmBtu)', 'CO2_RATE (tons/mmBtu)', 'HEAT_INPUT (mmBtu)']
    df = df[cols]
    df['day'] = pd.to_datetime(df['OP_DATE']).apply(lambda x: x.weekday())




    cross = pd.read_csv('../crosswalks/EIA-EPA-Crosswalk/TX_crosswalk.csv')
    cross = cross[['CAMD_PLANT_ID', 'EIA_LATITUDE', 'EIA_LONGITUDE']]
    df = df.merge(cross, how='left', left_on='ORISPL_CODE', right_on='CAMD_PLANT_ID')
    df.dropna(inplace=True)

    df['tmax'] = df[0:10].apply(lambda x: get_weather(get_station(x['EIA_LATITUDE'], x['EIA_LONGITUDE']), x["OP_DATE"], x["OP_DATE"]), axis=1)
    df.dropna(inplace=True)

    df.to_csv('./temps.csv', index=False)
