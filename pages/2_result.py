import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime
import pandas as pd

def generate_map_new():
    """Karsste mit Marker erzeugen nach der neuen Methode. Die Hoffnung war, dadurch eine dynamische Karte ohne Rerendern zu erzeugen."""
    width, height = (300, 400) if st.session_state.device_mode == "mobile" else (700, 500)

    # Get the two locations
    location1 = st.session_state.marker_pos
    location2 = st.session_state.photo_position
    zoom = st.session_state.zoom

    # Create the map object
    map_obj = folium.Map(location=location1, zoom_start=zoom)

    # Create a feature group for markers and lines
    fg = folium.FeatureGroup(name="Markers and Lines")

    # Add markers for both locations
    fg.add_child(folium.Marker(
        location=location1,
        tooltip="Geratene Position",
        icon=folium.Icon(color='red', icon='user', prefix='fa')
        ))
    fg.add_child(folium.Marker(
        location=location2,
        tooltip="Photo Position",
        icon=folium.Icon(color='green', icon='camera', prefix='fa')  # Font Awesome camera icon
    ))

    # Add a line connecting the two locations
    fg.add_child(
        folium.PolyLine(
            locations= [location1, location2],
            color= 'black',
            weight= 2.5,
            tooltip= (f"Distanz: {st.session_state.distance:.0f} m"),
            opacity =0.8
            )
        )

    # Add the feature group to the map
    map_obj.add_child(fg)

    # Calculate the bounds to fit all markers and lines
    bounds = [location1, location2]
    map_obj.fit_bounds(bounds)    

    # Render the map in Streamlit
    map_output = st_folium(
        map_obj,
        center=location1,
        zoom=zoom,
        width=width,
        height=height,
        key="updated_map"
    )
    
    return map_output

def query_highscore_list():
    query = 'SELECT * FROM "KAFotoFinder-Scoreboard" WHERE photo_id = :photo_id;'
    df = st.session_state.conn.query(
        query,
        ttl=5,
        params = {"photo_id" : st.session_state.photo_id}
        )
    
    return df

def update_highscore_list():
    """Manuelles Update mit dem neuen Wert, um nicht auf Latenz der Datenbank angewiesen zu sein"""
    
    ### Highscore Liste abrufen und auf bestes Ergebnis pro Spieler filtern
    df = query_highscore_list()
    df['new_flag'] = "old"
    df_unique = df.loc[df.groupby('username')['distance'].idxmin()]

    ### Neuen Versuch eintragen
    new_entry = pd.DataFrame({'username': st.session_state.user_name,
                              'timestamp': datetime.now().date(),
                              'distance': st.session_state.distance,
                              'photo_id': st.session_state.photo_id,
                              'device_id': [None],
                              'new_flag': "new"
                              })

    df_updated = pd.concat([df_unique, new_entry], ignore_index=True)

    ### Formatieren
    df_renamed = df_updated.rename(columns={'username': 'Name', 'timestamp': 'Zeit', 'distance': 'Score'})
    df_sorted = df_renamed.sort_values(by='Score', ascending=True)
    df_sorted['Platz'] = range(1, len(df_sorted) + 1)
    df_sorted = df_sorted[['Platz', 'Name', 'Zeit', 'Score', 'new_flag']]

    st.session_state.highscore_list = df_sorted


def calculate_rank():
    df = st.session_state.highscore_list
    filtered_df = df[df['new_flag'] == 'new']
    min_score_index = filtered_df['Score'].idxmin()
    platz_min_score = filtered_df.loc[min_score_index, 'Platz']
    st.session_state.rank = platz_min_score

def print_highscore():
    df = st.session_state.highscore_list
    df['Score'] = df['Score'].astype(int)
    styled_df = df.style.apply(
        lambda row: ['font-weight: bold; background-color: red' if row['new_flag'] == 'new' else '' for _ in row],
        axis=1  # Zeilenweise anwenden
    )
    st.dataframe(styled_df, hide_index=True, column_order=("Platz", "Name", "Zeit", "Score"))

def main():
    update_highscore_list()
    calculate_rank()

    st.markdown(f"<h2 style='text-align: center;'>{st.session_state.distance:.0f}m</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>{st.session_state.rank}. Platz für dich!</p>", unsafe_allow_html=True)

    st.write("### Dein Score:")
    map_obj = generate_map_new()

    st.write("### Highscore Liste:")
    print_highscore()

##main
if 'init_flag' in st.session_state:
    main()
else:
    st.write("Initialization failed. Read QR-Code to resume.")

# Output für Entwicklung
#st.write(st.session_state)