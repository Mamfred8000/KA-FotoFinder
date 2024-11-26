import time
from streamlit_javascript import st_javascript

def set_deviceMode():
    user_agent = st_javascript("window.navigator.userAgent")
    #Javascript library has loading time
    timeout = 60  # seconds
    start_time = time.time()
    while True:
        if isinstance(user_agent, str):
            device_mode = "mobile" if "Mobi" in user_agent else "desktop"
            return device_mode
        elif time.time() - start_time > timeout:
            return "desktop"
        else:
            time.sleep(0.01)