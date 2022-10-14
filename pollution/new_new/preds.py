import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import stan
import h5py

class AR1:
    """
    LinReg model with Stan
    """

    def __init__(self, data: np.ndarray, N_tilde: int):
        self.model_name = "StanLinReg"
        self.data = data.to_numpy()
        self.N = len(self.data)
        self.N_tilde = N_tilde

    def fit(self):
        stan_code = """
            data {
                int<lower=0> N;
                vector[N] y;
                int<lower=0> N_tilde;
            }
            parameters {
                real alpha;
                real beta;
                real gamma;
                real<lower=0> sigma;
            }
            model {
                alpha ~ normal(0, 10);
                beta ~ normal(0, 10);
                gamma ~ normal(0, 10);
                sigma ~ cauchy(0, 2.5);
                for (n in 3:N)
                    y[n] ~ normal(alpha + beta*y[n-1] + gamma*y[n-2], sigma);
            }
            generated quantities {
                vector[N_tilde] y_tilde;
                vector[2] i = y[N-1:N];
                for (n in 1:N_tilde) {
                    y_tilde[n] = normal_rng(alpha + beta * i[2] + gamma * i[1], sigma);
                    i[1] = i[2];
                    i[2] = y_tilde[n];
                    }
            }
        """

        data = {
            "N": self.N,
            "y": self.data,
            "N_tilde": self.N_tilde,
        }
        model = stan.build(program_code=stan_code, data=data)
        self.fit = model.sample(num_chains=1, num_samples=1 * 10**3)

    def predict(self):
        predictions = self.fit["y_tilde"]  # this is coming from the model object
        predictions = self.format_quantiles(predictions, 100000)
        return predictions
        
    def format_quantiles(self, data: pd.DataFrame, length: int):
        """
        Formats the samples form the stan model (precessed througth the format_sample function) into a percentiles.

        Parameters
        -----------
        data: pd.DataFrame
            This is the dataframe that is returned from the format_sample function.
        
        Returns
        --------
        data: pd.DataFrame
        """
        def createQuantiles(x):
            quantiles = np.array(
                [
                    0.010,
                    0.025,
                    0.050,
                    0.100,
                    0.150,
                    0.200,
                    0.250,
                    0.300,
                    0.350,
                    0.400,
                    0.450,
                    0.500,
                    0.550,
                    0.600,
                    0.650,
                    0.700,
                    0.750,
                    0.800,
                    0.850,
                    0.900,
                    0.950,
                    0.975,
                    0.990,
                ]
            )
            quantileValues = np.percentile(x["value"], q=100 * quantiles)
            return pd.DataFrame(
                {"quantile": list(quantiles), "value": list(quantileValues)}
            )

        data_predictions = {
            "prediction_idx": [],
            "sample": [],
            "value": [],
        }

        for N_tilde, samples in enumerate(data):
            for n, sample in enumerate(samples):
                data_predictions["prediction_idx"].append(length + N_tilde)
                data_predictions["sample"].append(n)
                data_predictions["value"].append(sample)
        
        data_predictions = pd.DataFrame(data_predictions)

        dataQuantiles = (
            data_predictions.groupby(["prediction_idx"])
            .apply(lambda x: createQuantiles(x))
            .reset_index()
            .drop(columns="level_1")
        )

        return dataQuantiles

def plot_single_predictions(data: pd.DataFrame, preds: pd.DataFrame):
    """
    Plot the predictions and the 95% confidence interval for a single prediction.
    
    Parameters
    -----------
    data: pd.DataFrame
        The original dataframe of data from `get_data` function.
    preds: pd.DataFrame
        This is a dataframe that is in the same format as a dataframe from `format_quantiles`
    
    Returns
    --------
    A plt plot
    """

    low = preds.loc[preds["quantile"] == 0.025, "value"]
    mid = preds.loc[preds["quantile"] == 0.500, "value"]
    high = preds.loc[preds["quantile"] == 0.975, "value"]
    x = preds.loc[preds["quantile"] == 0.025, "prediction_idx"]

    # plt.figure(figsize=(10, 6), dpi=150)
    plt.plot(data, label="Truth Data")
    plt.plot(x, mid, label="Predictions", color="black")
    plt.fill_between(
        x, low, high, color="red", alpha=0.5, label="95% Confidence Interval"
    )
    plt.legend()
    plt.xlabel("idx")
    plt.ylabel("")
    plt.show()

if __name__ == "__main__":
    with h5py.File('./Site_Callahan_Divide_Wind_Energy_Center_wind_actuals_2018.h5', 'r') as f:
        actuals = pd.DataFrame(f['actuals'][...])[0]
        model = AR1(actuals[90000:100000], 24)
        model.fit()
        preds = model.predict()
        plot_single_predictions(actuals[99000:100000], preds)