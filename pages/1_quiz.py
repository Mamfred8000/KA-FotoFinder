import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

from datetime import date
from sqlalchemy import text
import time

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

def generate_map_new():
    """Karte mit Marker erzeugen nach der neuen Methode. Die Hoffnung war, dadurch eine dynamische Karte ohne Rerendern zu erzeugen."""
    width, height = (300, 400) if st.session_state.device_mode == "mobile" else (700, 500)

    location = st.session_state.marker_pos
    zoom = st.session_state.zoom

    map_obj = folium.Map(location=location, zoom_start=zoom)
    fg = folium.FeatureGroup(name="Markers")

    fg.add_child(folium.Marker(
        location=location,
        tooltip="Geratene Position",
        icon=folium.Icon(color='red', icon='user', prefix='fa')
    ))

    map_output = st_folium(
        map_obj,
        center=location,
        zoom=zoom,
        feature_group_to_add=fg,
        width=width,
        height=height,
        key="updated_map"
    )
    
    return map_output

def calculate_distance():
    guess = st.session_state.guess_position
    goal = st.session_state.photo_position
    st.session_state.distance = geodesic(guess, goal).meters
    return True

def insert_data(username, timestamp, distance, photo_id):
    #conn = st.connection("postgresql", type="sql")
    
    insert_query = text(
        'INSERT INTO "KAFotoFinder-Scoreboard" (username, timestamp, distance, photo_id) '
        'VALUES (:username, :timestamp, :distance, :photo_id)'
    )
    
    # Execute the insert query with a progress spinner
    with st.spinner('Warum auch immer ist die Datenbank Latenz relativ hoch...'):
        with st.session_state.conn.session as s:
            s.execute(insert_query, {
                'username': username,
                'timestamp': timestamp,
                'distance': distance,
                'photo_id': photo_id
            })
            s.commit()
            #time.sleep(4)  #Latency of database is 1-4 seconds
    
    st.success("Data inserted successfully!")

def main():
    #st.title("quiz")
    st.write("### Ort auswählen und bestätigen")

    # Karte Initial erstellen
    map_output = generate_map_new()

    # Verarbeite die Klicks auf der Karte
    if map_output and map_output.get('last_clicked'):
        st.session_state.marker_pos = [map_output['last_clicked']['lat'], map_output['last_clicked']['lng']]
        st.session_state.zoom = map_output['zoom']
        st.rerun()

    if st.button("Abschicken", type="primary"):
        st.session_state.guess_position = st.session_state.marker_pos
        calculate_distance()
        insert_data(
            st.session_state.user_name,
            date.today(),
            st.session_state.distance,
            st.session_state.photo_id
        )
        st.switch_page("pages/2_result.py")

##main
if 'init_flag' in st.session_state:
    main()
else:
    st.write("Initialization failed. Read QR-Code to resume.")

# Output für Entwicklung
#st.write(st.session_state)