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

# Karte erzeugen
def generate_map():
    """Karte mit Marker erzeugen. Lese Position aus session state"""
    if st.session_state.device_mode == "desktop":
        width, height = 700, 500
    else:
        width, height = 300, 300
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

def get_remote_ip() -> str:
    """Get remote ip."""
    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None
        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None
    return session_info.request.remote_ip

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
    st.write(f"The remote ip is {get_remote_ip()}")
    st.write(f"Device mode: {st.session_state.device_mode}")


if __name__ == "__main__":
    st.session_state.device_mode = "mobile" if "Mobi" in st_javascript("window.navigator.userAgent") else "desktop"
    if 'init_flag' not in st.session_state: init()
    main()