import time
import streamlit as st
#import pandas as pd
#import numpy as np
import folium
from streamlit_folium import st_folium
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit_javascript import st_javascript

# Initialisieren
def init():
    st.session_state.init_flag = True
    
    st.session_state.marker_pos = [49.01357217893837, 8.404385447502138]
    st.session_state.zoom = 13
    st.session_state.counter = 1
    st.session_state.guess_position = [0, 0]

def init_deviceMode():
    user_agent = st_javascript("window.navigator.userAgent")
    #Javascript library has loading time
    timeout = 60  # seconds
    start_time = time.time()
    while True:
        if isinstance(user_agent, str):
            st.session_state.device_mode = "mobile" if "Mobi" in user_agent else "desktop"
            break
        elif time.time() - start_time > timeout:
            st.write("Timeout feching javascript data reached; exiting loop.")
            break
        else:
            time.sleep(0.01)

# Karte erzeugen
def generate_map():
    """Karte mit Marker erzeugen. Lese Position aus session state"""
    width, height = (300, 400) if st.session_state.device_mode == "mobile" else (700, 500)
    location = st.session_state.marker_pos
    zoom = st.session_state.zoom
    map_obj = folium.Map(location=location, zoom_start=zoom)
    folium.Marker(location=location, tooltip="Marker Position").add_to(map_obj)
    map_output = st_folium(map_obj, width=width, height=height)
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
    st.session_state.counter += 1
    st.session_state.guess_position = st.session_state.marker_pos

# Hauptfunktion
def main():
    st.title("KA-FotoFinder")
    col1, col2 = st.columns(spec=[0.7, 0.3])
    with col1:
        st.write("### Ort auswählen und bestägigen")
    with col2:
        st.button("Abschicken", type="primary", on_click=button_func, use_container_width=True)
    
    # Verarbeite Parameter aus QR-Code
    photo_id = get_params()

    # Karte Initial erstellen
    map_output = generate_map()

    # Verarbeite die Klicks auf der Karte
    if  map_output and map_output.get('last_clicked'):
        st.session_state.marker_pos = [map_output['last_clicked']['lat'], map_output['last_clicked']['lng']]
        st.session_state.zoom = map_output['zoom']
        st.rerun()
    
    # Output für Entwicklung
    st.write(f"Marker Position: Latitude: {st.session_state.marker_pos[0]}, Longitude: {st.session_state.marker_pos[1]}, Foto: {photo_id}")
    st.write(f"Button Click Counter: {st.session_state.counter}, Guess Position: {st.session_state.guess_position}")
    st.write(f"Device mode: {st.session_state.device_mode}")


if __name__ == "__main__":
    if 'init_flag' not in st.session_state:
        init_deviceMode()
        init()
    main()