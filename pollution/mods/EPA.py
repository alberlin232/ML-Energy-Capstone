import numpy as np
import pandas as pd
import requests
from datetime import date

class EPA():
    def __init__(self, email=None, key=None):
        if email is None:
            print("If you don't have an acount please make one with the SignUp func")
        else:
            self.auth = {'email': email, 'key': key}

    def SignUp(self, email):
        payload = {"email": email}
        req = requests.get("https://aqs.epa.gov/data/api/signup", params=payload)
        if req.status_code == 200:
            print("OK!")
        else:
            print("BOO!")


    def getCounties(self, state):
        payload = {"state": state}
        req = requests.get("https://aqs.epa.gov/data/api/list/countiesByState", params= (self.auth | payload))
        return pd.DataFrame.from_dict(req.json()["Data"])

    def getParams(self):
        payload = {"pc":"CRITERIA"}
        req = requests.get("https://aqs.epa.gov/data/api/list/parametersByClass", params= (self.auth | payload))
        return pd.DataFrame.from_dict(req.json()["Data"])

    def DailySummaryState(self, param, bdate, edate, state):
        payload = {"param":param, "bdate": bdate, "edate": edate, "state": state}
        req = requests.get("https://aqs.epa.gov/data/api/dailyData/byState", params= (self.auth | payload))
        return pd.DataFrame.from_dict(req.json()["Data"])

    def DailySummaryCounty(self, param, dates, state, counties):
        data = pd.DataFrame()
        noData = []
        for date in dates:
            bdate = date[0]
            edate = date[1]
            for county in counties:
                print("Getting: ", county, " : ", bdate)
                payload = {"param":param, "bdate": bdate, "edate": edate, "state": state, "county": county}
                req = requests.get("https://aqs.epa.gov/data/api/dailyData/byCounty", params= (self.auth | payload))
                if req.json()["Header"][0].get("status") == "No data matched your selection":
                    noData.append(county)
                data = data.append(pd.DataFrame.from_dict(req.json()["Data"]))
        return (data, noData)  
          
    def DailySummarySite(self, param, bdate, edate, state, county, site):
        payload = {"param":param, "bdate": bdate, "edate": edate, "state": state, "county": county, "site": site}
        req = requests.get("https://aqs.epa.gov/data/api/dailyData/bySite", params= (self.auth | payload))
        return pd.DataFrame.from_dict(req.json()["Data"])



if __name__ == "__main__":
    pass