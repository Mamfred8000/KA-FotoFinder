import streamlit as st
import folium
from streamlit_folium import st_folium

def generate_map(show_result=False):
    """Karte mit Marker erzeugen nach der neuen Methode. Die Hoffnung war, dadurch eine dynamische Karte ohne Rerendern zu erzeugen."""
    
    width, height = (300, 400) if st.session_state.device_mode == "mobile" else (700, 500)

    # Get the two locations
    location1 = st.session_state.marker_pos
    location2 = st.session_state.photo_position
    zoom = st.session_state.zoom

    # Create the map object
    map_obj = folium.Map(location=location1, zoom_start=zoom)

    # Create a feature group for markers and lines
    fg = folium.FeatureGroup(name="Markers and Lines")

    # Add marker for guess location
    fg.add_child(folium.Marker(
        location=location1,
        tooltip="Geratene Position",
        icon=folium.Icon(color='red', icon='user', prefix='fa')
        ))
    bounds = [location1]
    
    # Show goal location only when flag is set
    if show_result:
        # Add marker for goal location
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
        bounds.append(location2)

    # Add the feature group to the map
    map_obj.add_child(fg)

    # Calculate the bounds to fit all markers and lines
    #bounds = [location1, location2]
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