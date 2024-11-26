import streamlit as st
from geopy.distance import geodesic
from datetime import datetime
import src.database
import src.map

def main():
    st.title("KA-FotoFinder")
    st.write("Ort auswählen und bestätigen")

    # Karte Initial erstellen
    map_output = src.map.generate_map()

    # Verarbeite die Klicks auf der Karte
    if map_output and map_output.get('last_clicked'):
        st.session_state.marker_pos = [map_output['last_clicked']['lat'], map_output['last_clicked']['lng']]
        st.session_state.zoom = map_output['zoom']
        st.rerun()

    if st.button("Abschicken", type="primary"):
        st.session_state.guess_position = st.session_state.marker_pos
        st.session_state.distance = geodesic(
            st.session_state.guess_position,
            st.session_state.photo_position).meters
        st.session_state.hs_list = src.database.query_highscore_list()

        src.database.insert_score_data(
            st.session_state.user_name,
            datetime.now(),
            st.session_state.distance,
            st.session_state.photo_id,
            "dummy"
        )

        st.switch_page("pages/2_result.py")

##main
if 'init_flag' in st.session_state:
    main()
else:
    st.write("Initialization failed. Read QR-Code to resume.")

# Output für Entwicklung
#st.write(st.session_state)