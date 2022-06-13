import pandas as pd
from datetime import datetime, timedelta
from Area import Area
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style(style='whitegrid')
import utilities as util

wroclaw = Area(center_lat=51.11, center_lon=17.035, grid_shape=(3, 3))
# wroclaw.forecast()
# hourly = wroclaw.hourly
# dataframe = pd.DataFrame(data=hourly)
# print(datetime.now())
#
#
# dataframe['dt'] = pd.to_datetime(dataframe['dt'], unit='s')
# dataframe = dataframe.loc[dataframe['dt']<=(datetime.now()+timedelta(hours=7))]
#
# dataframe.set_index('dt', inplace=True)
#
# print(dataframe.columns)
wroclaw.forecast(interval='hourly')
minutely = wroclaw.minutely
dataframe = pd.DataFrame(data=minutely)
dataframe['dt'] = pd.to_datetime(dataframe['dt'], unit='s')
print(dataframe.columns)
print(dataframe)
