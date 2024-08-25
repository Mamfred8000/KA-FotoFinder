import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# Initialisieren
def init():
    START_LOC = [49.01357217893837, 8.404385447502138]
    START_ZOOM = 13

    if 'marker_pos' not in st.session_state:
        st.session_state.marker_pos = START_LOC
    if 'zoom' not in st.session_state:
        st.session_state.zoom = START_ZOOM

# Karte erzeugen
def generate_map():
    """Karte mit Marker erzeugen. Lese Position aus session state"""
    location = st.session_state.marker_pos
    zoom = st.session_state.zoom
    map_obj = folium.Map(location=location, zoom_start=zoom)
    folium.Marker(location=location, tooltip="Marker Position").add_to(map_obj)
    map_output = st_folium(map_obj, width=700, height=500)
    return map_output

# Query Parameter lesen
def get_params():
    query_params = st.query_params
    if 'photo_id' in query_params:
        photo_id = query_params['photo_id']
    else:
        photo_id = 'nA'
    return photo_id

def button_func():
    st.session_state.payload = {
        'guess_loc' : st.session_state.marker_pos
    }

# Hauptfunktion
def main():
    st.title("KA-FotoFinder")
    col1, col2 = st.columns(spec=[0.7, 0.3])
    with col1:
        st.write("### Ort auswählen und bestägigen")
    with col2:
        st.button("Abschicken", type="primary", on_click=button_func(), use_container_width=True)
    
    # Verarbeite Parameter aus QR-Code
    photo_id = get_params()

    # Karte Initial erstellen
    map_output = generate_map()

    # Verarbeite die Klicks auf der Karte
    if map_output and map_output.get('last_clicked'):
        st.session_state.marker_pos = [map_output['last_clicked']['lat'], map_output['last_clicked']['lng']]
        st.session_state.zoom = map_output['zoom']
        map_output = generate_map()
    
    # Output für Entwicklung
    st.write(f"Marker Position: Latitude: {st.session_state.marker_pos[0]}, Longitude: {st.session_state.marker_pos[1]}, Foto: {photo_id}, Payload = {st.session_state.payload}")

if __name__ == "__main__":
    init()
    main()