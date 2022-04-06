import numpy as np
import pandas as pd
import requests
import io

class EPA():
    def __init__(self, key=None):
        if key is None:
            print("You need a key in order to use this API.")
        else:
            self.key = key

    def hourlyData(self, orisCode, unitID, year, quarter):
        req = requests.get("https://api.epa.gov/FACT/1.0/emissions/hourlyData/csv/{}/{}/{}/{}?api_key={}".format(
            orisCode, 
            unitID, 
            year, 
            quarter, 
            self.key))
        con = req.content
        return pd.read_csv(io.StringIO(con.decode('utf-8')))



if __name__ == "__main__":
    eia = EIA('9ndbfvcHxIEgQ8KnDGhmVFdw3xiyOgqhhwdJg5Wo')
    df = eia.electric_plant_all(plant_id=9)
    print(df)