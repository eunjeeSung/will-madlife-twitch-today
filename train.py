# %%
import os
import datetime

import IPython
import IPython.display
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf

mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['axes.grid'] = False

# %%
CSV_PATH = 'data/notice_dates.csv'

# %%
# slice [start:stop:step], starting from index 5 take every 3th record.
df = pd.read_csv(CSV_PATH)
df.columns = ['year', 'month', 'day']
df = df[5::3]
df

# %%
dates = pd.to_datetime(df)
print(len(dates))

# %%
PM_25 = [1] * len(dates)
plt.scatter(dates, PM_25, s = 100, c = 'red', alpha=0.1)