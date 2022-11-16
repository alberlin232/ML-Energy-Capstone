import argparse
import pandas as pd
import numpy as np
import requests
import io

class DATA():
    def __init__(self, key=None):
        if key is None:
            print("You need a key in order to use this API.")
        else:
            self.key = key

    def EIA(self, plant_id):
        series_id = 'ELEC.PLANT.GEN.{}-ALL-ALL.Q'.format(plant_id)
        req = requests.get("https://api.eia.gov/series/?series_id={}&api_key={}".format(series_id, self.key))
        return pd.DataFrame.from_dict(req.json().get('series')[0].get('data'))


    def EPA(self, orisCode, unitID, year, quarter):
        url = "https://api.epa.gov/FACT/1.0/emissions/hourlyData/csv/{}/{}/{}/{}?api_key={}".format(
            orisCode, 
            unitID, 
            year, 
            quarter, 
            self.key)
        try:
           data = pd.read_csv(url)
           return data
        except:
            return pd.DataFrame()


def generateData(api, year, q, date, walk, epa):
    dic = {"date":[], "plant_id":[], "eia":[], "epa":[], "valid":[]}
    for i in walk["EIA_PLANT_ID"].unique():
        print("Computing:", i)
        oris = walk.loc[walk["EIA_PLANT_ID"] == i].reset_index(drop=True).at[0,'CAMD_PLANT_ID']
        epa_data = epa.loc[epa["ORISPL_CODE"] == oris]
        epa_sum = epa_data["GLOAD (MWh)"].sum()
        try:
            temp = api.EIA(i)
            eia_sum = temp.loc[temp[0] == date].reset_index(drop=True).at[0,1]
        except: 
            dic["date"].append(date)
            dic["plant_id"].append(i)
            dic["eia"].append(-1)
            dic["epa"].append(-1)
            dic["valid"].append(False)
            continue
        dic["date"].append(date)
        dic["plant_id"].append(i)
        dic["eia"].append(eia_sum)
        dic["epa"].append(epa_sum)
        dic["valid"].append(True)
    return pd.DataFrame().from_dict(dic)



# main
if __name__ == "__main__":

    print("START")
    # parser = argparse.ArgumentParser(description='What date to get')
    # parser.add_argument('--YEAR',type=str)

    # args = parser.parse_args()
    
    # year = args.YEAR

    api = DATA("9ndbfvcHxIEgQ8KnDGhmVFdw3xiyOgqhhwdJg5Wo")
    print("API has been make")
    walk = pd.read_csv("./TX_crosswalk.csv")
    walk = walk[["CAMD_PLANT_ID", "CAMD_UNIT_ID", "EIA_PLANT_ID", "EIA_GENERATOR_ID"]]
    print(walk)

    walk["EIA_PLANT_ID"] = walk["EIA_PLANT_ID"].astype(int)
    print("Importing data") 
    data = pd.DataFrame(columns=["date", "plant_id", "eia", "epa", "valid"])
    for year in range(2010,2022):
        for q in range(1,5):
            epa = pd.read_csv("./epa/DLY_{}txQ{}.zip".format(year, q), compression='zip')
            date = "{}Q{}".format(year, q)
            data = data.append(generateData(api, year, q, date, walk, epa))
    data.to_csv("allMatch.csv", index=False)
