import streamlit as st
import pydeck as pdk

def define_map(lat=51.11, lon=17.035, zoom=11, map_height=740, layer=None):
    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',
                             initial_view_state=pdk.ViewState(latitude=lat,
                                                              longitude=lon,
                                                              zoom=zoom, height=map_height),
                             layers=layer), use_container_width=True)