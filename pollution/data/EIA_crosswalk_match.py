#berlin

import pandas as pd
import requests


if __name__ == "__main__":

    # Get plant data from EIA
    req = requests.get("https://api.eia.gov/category/?api_key=9ndbfvcHxIEgQ8KnDGhmVFdw3xiyOgqhhwdJg5Wo&category_id=902974")

    # Parse to Dataframe
    data = pd.DataFrame.from_dict(req.json()['category']['childcategories'])
    data["plant_id"] = data["name"].map(lambda x: x.split()[0].replace('(','').replace(')','')).astype(int)
    data['name'] = data["name"].map(lambda x: x.split()[1]).astype(str)
    data = data.drop(["category_id"], axis=1)

    # Import crosswalk and fuel types
    walk = pd.read_csv("./TX_crosswalk.csv")
    walk["EIA_PLANT_ID"] = walk["EIA_PLANT_ID"].astype(int)
    walk["EIA_GENERATOR_ID"] = walk["EIA_GENERATOR_ID"].astype(str)

    fuel = pd.read_csv("./EIA_860_generator_list.csv")
    fuel = fuel[["Plant Code", "Generator ID", "Energy Source 1"]]

    data = data.merge(fuel, how="inner", left_on="plant_id", right_on="Plant Code")

    # Fuel Conversions
    dic = {"Coal":["ANT", "BIT", "LIG", "SUB", "WC", "RC"], 
        "Petroleum": ["DFO", "JF", "KER", "PC", "RFO", "WO"],
        "Natural Gas": ["BFG", "NG", "OG", "PG", "SG", "SGC"],
        "Renewable": ["AB", "NSW", "OBS", "WDS", "OBL", "SLW", "BLQ", "WDL", "LFG", "OBG"],
        "Solar": ["SUN"],
        "Wind": ["WND"],
        "Nuclear": ["NUC"],
        "Hydro": ["WAT"],
        "Geothermal": ["GEO"],
        "Other": ["MWH", "WH", "PUR"]
        }


    #iterates through data and changed value of Energy Source 1 to the key value in the dic
    for index, row in data.iterrows():
        for key, value in dic.items():
            if row["Energy Source 1"] in value:
                data.at[index, "Energy Source 1"] = key

    # Check to see if plant_id from EIA is in crosswalk and add to df
    data["match"] = data["plant_id"].isin(walk["EIA_PLANT_ID"])

    match_unitId = []
    for index, row in data.iterrows():
        if row["match"]:
            walk_part = walk.loc[walk["EIA_PLANT_ID"] == row["plant_id"]]
            walk_part = walk_part["EIA_GENERATOR_ID"].tolist()
            match_unitId.append(row["Generator ID"] in walk_part)
        else:
            match_unitId.append(False)
    data["match"] = match_unitId
    # Write to file
    data.to_csv("EIA_plant_list.csv", index = False)