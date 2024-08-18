import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# Hauptfunktion
def main():
    st.title("KA-FotoFinder")
    st.write("### Wähle einen Punkt auf der Karte aus und bestätige ihn")

    # Start Koordinaten
    start_loc = [51.1657, 10.4515]
    start_zoom = 13

    # Session State
    if 'marker_pos' not in st.session_state:
        st.session_state.marker_pos = start_loc
    if 'zoom' not in st.session_state:
        st.session_state.zoom = start_zoom
    st.write(f"Marker Position: Latitude: {st.session_state.marker_pos[0]}, Longitude: {st.session_state.marker_pos[1]}")

    # Karte definieren
    map_obj = folium.Map(location=st.session_state.marker_pos, zoom_start=st.session_state.zoom)

    ## Marker definieren
    folium.Marker(st.session_state.marker_pos, tooltip="Marker Position").add_to(map_obj)

    # Karte anzeigen
    map_output = st_folium(map_obj, width=700, height=500)

    # Verarbeite die Klicks auf der Karte
    if map_output and map_output.get('last_clicked'):
        lat = map_output['last_clicked']['lat']
        lon = map_output['last_clicked']['lng']
        zoom = map_output['zoom']
        st.session_state.marker_pos = [lat, lon]  # Update marker position
        st.session_state.zoom = zoom

        # Karte neu erstellen, um die aktualisierte Marker-Position und Zoom-Stufe zu reflektieren
        map_obj = folium.Map(location=st.session_state.marker_pos, zoom_start=st.session_state.zoom)
        folium.Marker(st.session_state.marker_pos, tooltip="Marker Position").add_to(map_obj)
        st_folium(map_obj, width=700, height=500)

if __name__ == "__main__":
    main()