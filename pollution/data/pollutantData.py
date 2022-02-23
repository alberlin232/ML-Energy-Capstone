# berlin

import sys
sys.path.append("../")
from mods.EPA import EPA

import pandas as pd
import numpy as np
from datetime import date


if __name__ == "__main__":
    epa = EPA
    epa = EPA("alb323@lehigh.edu", "indigoswift15")

    
    df = {"param":[], "county":[]}
    for param in epa.getParams()["code"]:
        _, noData = epa.DailySummaryCounty([param], "20170101", "20171231", "48", epa.getCounties("48")["code"])
        for code in noData:
            df["param"].append(param)
            df["county"].append(code)
    data = pd.DataFrame(df)
    data.to_csv("noData.csv")