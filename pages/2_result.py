import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

def calculate_distance():
    guess = st.session_state.guess_position
    goal = st.session_state.photo_position
    st.session_state.distance = geodesic(guess, goal).meters
    return True

def generate_map_new():
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

def calculate_rank():
    st.session_state.rank = 1

def main():
    st.title("result")
    
    calculate_distance()
    calculate_rank()

    st.markdown(f"<h2 style='text-align: center;'>{st.session_state.distance:.0f}m</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Super, {st.session_state.rank}. Platz für dich!</p>", unsafe_allow_html=True)

    map_obj = generate_map_new()

    st.write(f"Geratene Position: {st.session_state.guess_position}")
    st.write(f"Ziel Position: {st.session_state.photo_position}")
    st.write(f"Distanz: {st.session_state.distance:.0f} m")

##main
if 'init_flag' in st.session_state:
    main()
else:
    st.write("Initialization failed. Read QR-Code to resume.")

# Output für Entwicklung
st.write(st.session_state)