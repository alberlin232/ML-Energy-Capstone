import numpy as np
import pandas as pd
import requests

class EIA():
    def __init__(self, key=None):
        if key is None:
            print("You need a key in order to use this API.")
        else:
            self.key = key

    def electric_plant_all(self, plant_id):
        series_id = 'ELEC.PLANT.GEN.{}-ALL-ALL.M'.format(plant_id)
        req = requests.get("https://api.eia.gov/series/?series_id={}&api_key={}".format(series_id, self.key))
        return pd.DataFrame.from_dict(req.json().get('series')[0].get('data'))



if __name__ == "__main__":
    pass