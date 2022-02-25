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

    county = epa.getCounties("48")["code"]
    params = epa.getParams()["code"]


    data, _ = epa.DailySummaryCounty(params, [["20170101", "20171231"], ["20180101", "20181231"]], "48", county)

    data = pd.DataFrame(data)
    data.to_csv("EPAData.csv", index = False)