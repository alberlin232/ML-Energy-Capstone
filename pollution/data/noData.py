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

    county = epa.getCounties("48")
    county_dict = county.set_index("code")["value_represented"].to_dict()

    params = epa.getParams()
    params_dict = params.set_index("code")["value_represented"].to_dict()

    df = {"param":[],"date":[], "county":[]}
    dates = [["20170101", "20171231"], ["20180101", "20181231"], ["20190101", "20191231"]]
    for d in dates:
        bdate = d[0]
        edate = d[1]
        for param in params["code"]:
            _, noData = epa.DailySummaryCounty([param], bdate, edate, "48", county["code"])
            for code in noData:
                df["param"].append(params_dict.get(param))
                df["date"].append(bdate)
                df["county"].append(county_dict.get(code))
    data = pd.DataFrame(df)
    data.to_csv("noData.csv", index = False)