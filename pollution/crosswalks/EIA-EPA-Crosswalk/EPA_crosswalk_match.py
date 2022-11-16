#berlin

import pandas as pd
import requests

if __name__ == "__main__":

    # Get plant data from EIA
    req = requests.get("https://api.epa.gov/FACT/1.0/facilities?api_key=9ndbfvcHxIEgQ8KnDGhmVFdw3xiyOgqhhwdJg5Wo")
    df = pd.DataFrame().from_dict(req.json()["data"])
    # Parse to Dataframe
    data = {"orisCode":[], "state":[], "county":[], "unitId":[], "fuel":[]}
    for i in range(len(df)):
        for j in range(len(df["units"][i])):
            data["orisCode"].append(df["orisCode"][i])
            data["state"].append(df["state"][i].get("abbrev"))
            data["county"].append(df["county"][i].get("name"))
            data["unitId"].append(df["units"][i][j].get("unitId"))
            for z in range(len(df["units"][i][j].get("fuels"))):
                if df["units"][i][j].get("fuels")[z].get("indicatorDescription") == "Primary":
                    data["fuel"].append(df["units"][i][j].get("fuels")[z].get("fuelDesc"))
                    break
            else:
                data["fuel"].append("NONE")
    data = pd.DataFrame().from_dict(data)
    data = data.loc[data["state"] == "TX"].reset_index(drop=True)
    

    # Import crosswalk
    walk = pd.read_csv("./TX_crosswalk.csv")
    walk["CAMD_PLANT_ID"] = walk["CAMD_PLANT_ID"].astype(int)
    walk["CAMD_UNIT_ID"] = walk["CAMD_UNIT_ID"].astype(str)
    data["orisCode"] = data["orisCode"].astype(int)
    data["unitId"] = data["unitId"].astype(str)        

    # Check to see if each orisCode and unitId matches a CAMD_PLANT_ID and CAMD_UNIT_ID in walk and output a boolean to a new column
    data["match"] = data["orisCode"].isin(walk["CAMD_PLANT_ID"])

    match_unitId = []
    for index, row in data.iterrows():
        if row["match"]:
            walk_part = walk.loc[walk["CAMD_PLANT_ID"] == row["orisCode"]]
            walk_part = walk_part["CAMD_UNIT_ID"].tolist()
            match_unitId.append(row["unitId"] in walk_part)
        else:
            match_unitId.append(False)
    data["match"] = match_unitId
    # Write to file
    data.to_csv("EPA_plant_list.csv", index = False)


