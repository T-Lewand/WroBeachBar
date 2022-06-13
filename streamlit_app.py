import streamlit_app as st
import pandas as pd
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style(style='whitegrid')
import streamlit_folium
import folium
import folium.plugins
from objecthandler import BeachBar
import utilities as util
import streamlit_utilities as st_util
import pydeck as pdk
from Area import Area
side_menu = st.sidebar

def bar_info():
    side_menu.write('Temperatura')
    side_menu.write('Humidity')

bars = util.bars_init_df('beach_bars.txt')

st.set_page_config(layout='wide')


api_key = 'https://api.mapbox.com/styles/v1/tlewand/cl0b7fd35008214mgftf1cfv7/tiles/256/{z}/{x}/{y}@2x?access_token=' \
          'pk.eyJ1IjoidGxld2FuZCIsImEiOiJjbDBiN2VybWkwMWQ5M2JvbWc0cmcwdjg3In0.VEUJOJlMoRGOBHjtrbmJ8Q'
bars['icon'] = None
for i in bars.index:
    icon_data = {'url': f"{bars['logo_url'][i]}",
            "width": 242,
            "height": 242,
            "anchorY": 242}

    bars["icon"][i] = icon_data

bar_layer = pdk.Layer(type='IconLayer', data=bars, get_icon='icon', get_size=4, size_scale=15,
                      get_position=['lon', 'lat'], pickable=True)

side_menu.write("SIDEBAR")
options = ['Wybierz']
options.extend([i for i in bars.index])
option = side_menu.selectbox(label='Beach Bar', options=options)

if option == 'Wybierz':
    st_util.define_map(layer=bar_layer)
else:
    bar_location = bars.loc[option, ['lat', 'lon']]
    st_util.define_map(lat=bar_location['lat'], lon=bar_location['lon'], zoom=13, layer=bar_layer)
    # st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',
    #                          initial_view_state=pdk.ViewState(latitude=bar_location['lat'], longitude=bar_location['lon'],
    #                                                           zoom=13, height=740),
    #                          layers=bar_layer), use_container_width=True)

    bar = BeachBar(option, bars.loc[option, 'lat'], bars.loc[option, 'lon'])
    bar.current_weather()
    bar.forecast()
    hourly = bar.hourly
    dataframe = pd.DataFrame(data=hourly)
    dataframe['dt'] = pd.to_datetime(dataframe['dt'], unit='s')
    dataframe = dataframe.loc[dataframe['dt'] <= (datetime.now() + timedelta(hours=7))]
    labels = []
    for i in dataframe.index:
        labels.append(dataframe.loc[i, 'dt'].hour)
    dataframe.set_index('dt', inplace=True)

    with side_menu.container():
        st.write(f'Temperatura: {bar.temp:.1f}')
        st.write(f'Odczuwalna: {bar.temp_feeled:.1f}')
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=dataframe, x='dt', y='temp')
        sns.lineplot(data=dataframe, x='dt', y='feels_like')
        plt.xticks(rotation=45, fontsize=20)
        ax.set_xticklabels(labels)
        plt.xlabel('Godzina', fontsize=15)
        plt.yticks(fontsize=20)
        plt.ylabel('\N{DEGREE SIGN}C', fontsize=18, rotation=90)
        st.pyplot(fig)

# Style
with open('style.css') as file:
    st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

# streamlit_folium.folium_static(m)