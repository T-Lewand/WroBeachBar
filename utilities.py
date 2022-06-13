import pandas as pd

from objecthandler import BeachBar

def bars_init(file):
    with open(file) as file:
        text = file.read()
    beachbars = text.split('\n')
    bars = []
    for i in beachbars:
        single_bar = i.split(';')
        name, lat, lon = single_bar[0], float(single_bar[1]), float(single_bar[2])
        bars.append(BeachBar(name, lat, lon))

    return bars

def bars_init_df(file):
    with open(file) as file:
        text = file.read()
    beachbars = text.split('\n')
    bars=[]
    for i in beachbars:
        single_bar = i.split(';')
        name, lat, lon, logo_url = single_bar[0], float(single_bar[1]), float(single_bar[2]), single_bar[3]
        bars.append([name, lat, lon, logo_url])

    bars = pd.DataFrame(data=bars, columns=['name', 'lat', 'lon', 'logo_url'])
    bars.set_index('name', inplace=True)
    return bars