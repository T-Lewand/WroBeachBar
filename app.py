from flask import Flask, render_template
import folium
from Area import Area
import utilities as util

wroclaw = Area(center_lat=51.11, center_lon=17.035, grid_shape=(3, 3))


app = Flask(__name__)
@app.route('/')
def base():
    api_key = 'https://api.mapbox.com/styles/v1/tlewand/cl0b7fd35008214mgftf1cfv7/tiles/256/{z}/{x}/{y}@2x?access_token=' \
              'pk.eyJ1IjoidGxld2FuZCIsImEiOiJjbDBiN2VybWkwMWQ5M2JvbWc0cmcwdjg3In0.VEUJOJlMoRGOBHjtrbmJ8Q'
    base_map = folium.Map(location=[51.11, 17.035], zoom_start=14, tiles='Stamen Terrain')
    bars = util.bars_init('beach_bars.txt')

    for bar in bars:
        bar.current_weather()
        folium.Marker([bar.lat, bar.lon], popup=f'{bar.name}\nTemperatura: {bar.temp}').add_to(base_map)

    return base_map._repr_html_()

@app.route('/sidebar')
def sidebar():
    return render_template('home.html')