import pandas as pd
import numpy as np
import datetime
from statsmodels.tsa.api import VAR

def invert_transformation(df_train, df_forecast, second_diff=False):
    """Revert back the differencing to get the forecast to original scale."""
    df_fc = df_forecast.copy()
    columns = df_train.columns
    for col in columns:        
        # Roll back 2nd Diff
        if second_diff:
            df_fc[str(col)+'_1d'] = (df_train[col].iloc[-1]-df_train[col].iloc[-2]) + df_fc[str(col)+'_2d'].cumsum()
        # Roll back 1st Diff
        df_fc[str(col)] = df_train[col].iloc[-1] + df_fc[str(col)+'_2d'].cumsum()
    return df_fc

def forecast(filepath="./file/data_calls_tmp.csv", n_days=15, date_column="CallsDateTime"):
  df = pd.read_csv(filepath, parse_dates=[date_column])
  df["date"] = df[[date_column]]
  # df.drop(["CallsDateTime"],inplace=True)
  df.set_index("date",inplace=True) 
  start = df.index[-1].date()+datetime.timedelta(days=1)
  end = df.index[-1].date()+datetime.timedelta(days=n_days)

  df = df.resample("D").mean()
  df = df.iloc[:-30]
  nobs = n_days 
  df_differenced = np.log(df).diff().dropna()
  model = VAR(df_differenced)
  model_fitted = model.fit(6)
  # Get the lag order
  lag_order = model_fitted.k_ar
  # Input data for forecasting
  forecast_input = df_differenced.values[-lag_order:]
  fc = model_fitted.forecast(y=forecast_input, steps=nobs)
  df_forecast = pd.DataFrame(fc, columns=df.columns + '_2d')
  df_forecast = np.exp(df_forecast)
  df_forecast["date"] = pd.date_range(start=start, end=end)
  df_forecast.set_index("date",inplace=True)

  df_results = invert_transformation(df, df_forecast, second_diff=False)
  drop_columns = [
                  items+"_2d" for items in df.columns
  ]
  df_new = df_results.drop(drop_columns,axis=1)
  df_new1 = pd.concat([df,df_new])
  return df_new1.to_json(
    index=True,
    indent=4,
    orient="table"

  )
