import streamlit as st
import folium
from streamlit_folium import st_folium

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

def button_func():
    st.session_state.counter += 1
    st.session_state.guess_position = st.session_state.marker_pos

def main():
    st.title("quiz")

    col1, col2 = st.columns(spec=[0.7, 0.3])
    with col1:
        st.write("### Ort auswählen und bestätigen")
    with col2:
        st.button("Abschicken", type="primary", on_click=button_func, use_container_width=True)
    
    # Karte Initial erstellen
    map_output = generate_map()

    # Verarbeite die Klicks auf der Karte
    if  map_output and map_output.get('last_clicked'):
        st.session_state.marker_pos = [map_output['last_clicked']['lat'], map_output['last_clicked']['lng']]
        st.session_state.zoom = map_output['zoom']
        st.rerun()
    
    # Output für Entwicklung
    st.write(st.session_state)

    if st.button("Go Back Home"):
        st.switch_page("app.py")

##main
if 'init_flag' in st.session_state:
    main()
else:
    st.write("Initialization failed. Read QR-Code to resume.")