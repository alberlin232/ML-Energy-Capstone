# berlin
import pandas as pd
import numpy as np


if __name__ == "__main__":
    df = pd.read_csv("eoa.csv")
    data = {"county":[], "plant_number":[]}
    for county in df["County"].unique():
        d = df.loc[df["County"] == county]
        fac = d["Facility ID (ORISPL)"].unique()
        data["county"].append(county)
        data["plant_number"].append(len(fac))
    data = pd.DataFrame().from_dict(data)
    data.to_csv("plantCount.csv", index=False)