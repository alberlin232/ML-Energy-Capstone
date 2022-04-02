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

    # Import crosswalk
    walk = pd.read_csv("./TX_crosswalk.csv")

    # Check to see if plant_id from EIA is in crosswalk and add to df
    data["match"] = data["plant_id"].isin(walk["EIA_PLANT_ID"])
    
    # Write to file
    data.to_csv("EIA_plant_list.csv", index = False)


