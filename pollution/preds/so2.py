import glob
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import stan



# setting the path for joining multiple files
files = os.path.join("../data/epa/TXHOURLY", "*tx*.csv")

# list of merged files returned
files = glob.glob(files)

print("Resultant CSV after joining all CSV files at a particular location...");

# joining files with concat and read_csv
df = pd.concat(map(pd.read_csv, files), ignore_index=True)
cols = ['STATE', 'FACILITY_NAME', 'ORISPL_CODE', 'UNITID', 'OP_DATE', 'OP_HOUR',
       'OP_TIME', 'GLOAD (MW)', 'SO2_MASS (lbs)', 'SO2_RATE (lbs/mmBtu)',
       'NOX_RATE (lbs/mmBtu)', 'NOX_MASS (lbs)', 'CO2_MASS (tons)',
       'CO2_RATE (tons/mmBtu)', 'HEAT_INPUT (mmBtu)']
df = df[cols]
df.dropna(inplace=True)


co2_model = """
data {
  int<lower=0> N;   // number of data items
  int<lower=0> K;   // number of predictors
  matrix[N, K] x;   // predictor matrix
  vector[N] y;      // outcome vector
}
parameters {
  real alpha;           // intercept
  vector[K] beta;       // coefficients for predictors
  real<lower=0> sigma;  // error scale
}
model {
  alpha ~ normal(0, 10);      // prior for intercept
  beta ~ normal(0, 10);       // prior for coefficients
  sigma ~ cauchy(0, 5);       // prior for error scale
  y ~ normal(x * beta + alpha, sigma);  // likelihood
}
"""


d = df.loc[df.OP_HOUR ==1]


X = d[['GLOAD (MW)', 'HEAT_INPUT (mmBtu)']].to_numpy()
y = d['CO2_RATE (tons/mmBtu)'].to_numpy()

N = X.shape[0]
K = X.shape[1]

epa_data = {"N": N,
    "K": K,
    "x": X,
    "y": y}

posterior = stan.build(co2_model, data=epa_data)
fit = posterior.sample(num_chains=1, num_samples=1000)