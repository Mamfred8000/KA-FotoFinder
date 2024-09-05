import time
import streamlit as st
from streamlit import runtime
from streamlit_javascript import st_javascript

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

# Query Parameter lesen
def get_photo_param():
    query_params = st.query_params
    if 'photo_id' in query_params:
        photo_id = query_params['photo_id']
    else:
        photo_id = 'nA'
    return photo_id

def init():
    st.session_state.init_flag = True
    st.session_state.user_name = ""
    st.session_state.marker_pos = [49.01357217893837, 8.404385447502138]
    st.session_state.zoom = 13
    st.session_state.counter = 1
    st.session_state.guess_position = [0, 0]
    st.session_state.photo_id = get_photo_param()

# Hauptfunktion
def main():
    st.title("KA-FotoFinder")

    if st.session_state.user_name:
        st.write(f"## Hallo {st.session_state.user_name}!")
        if st.button("Starten", type="primary"): st.switch_page("pages/1_quiz.py")
    else:
        st.write("## Neu hier...?")
        name = st.text_input("Wie heißt du?", placeholder="Name")
        if name:
            st.session_state.user_name = name
            st.rerun()

if __name__ == "__main__":
    if 'init_flag' in st.session_state:
        main()
    else:
        init_deviceMode()
        init()
        st.rerun()