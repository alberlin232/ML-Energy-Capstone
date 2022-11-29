import glob
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


def load_data():
    # setting the path for joining multiple files
    files = os.path.join("../data/epa/TXHOURLY", "*tx*.csv")

    # list of merged files returned
    files = glob.glob(files)

    print("Resultant CSV after joining all CSV files at a particular location...");

    # joining files with concat and read_csv
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    cols = ['ORISPL_CODE', 'UNITID', 'OP_DATE','OP_HOUR', 'GLOAD (MW)', 'SO2_RATE (lbs/mmBtu)',
        'NOX_RATE (lbs/mmBtu)', 'CO2_RATE (tons/mmBtu)', 'HEAT_INPUT (mmBtu)']
    df = df[cols]
    df['OP_DATE'] = pd.to_datetime(df['OP_DATE']).apply(lambda x: x.weekday())
    return df

def prep_data(df):
    df.dropna(inplace=True)
    df = pd.get_dummies(df, columns=['ORISPL_CODE', 'UNITID'])
    return df

if __name__ == '__main__':
    df = load_data()
    df = prep_data(df)
    preds = pd.DataFrame(columns=['truth', 'pred', 'hour'])
    for i in df['OP_HOUR'].unique():
        d = df[df['OP_HOUR'] == i]
        X = d.drop('CO2_RATE (tons/mmBtu)', axis=1).to_numpy()
        y = d['CO2_RATE (tons/mmBtu)'].to_numpy()

        #split into train and test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)
        pred = model.predict(X_test)

        preds = preds.append(pd.DataFrame({'truth': y_test, 'pred': pred, 'hour': i}))
    
    preds.to_csv('preds.csv', index=False)

