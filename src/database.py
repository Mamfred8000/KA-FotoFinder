import streamlit as st
from sqlalchemy import text

def init_db():
    st.session_state.conn = st.connection("postgresql", type="sql")

def query_highscore_list():
    query = 'SELECT * FROM "KAFotoFinder-Scoreboard" WHERE photo_id = :photo_id;'
    df = st.session_state.conn.query(
        query,
        ttl=5,
        params = {"photo_id" : st.session_state.photo_id}
        )
    
    return df

def query_photo_position():
    df = st.session_state.conn.query('SELECT * FROM "photo-list";', ttl=0)
    if st.session_state.photo_id in df['photo_id'].values:
        lat = df.loc[df['photo_id'] == st.session_state.photo_id, 'latitude'].values[0]
        long = df.loc[df['photo_id'] == st.session_state.photo_id, 'longitude'].values[0]
    else:
        [lat, long] = [0, 0]
    return [lat, long]

def insert_score_data(username, timestamp, distance, photo_id, device_id):
    insert_query = text(
        'INSERT INTO "KAFotoFinder-Scoreboard" (username, timestamp, distance, photo_id, device_id) '
        'VALUES (:username, :timestamp, :distance, :photo_id, :device_id)'
    )

    with st.session_state.conn.session as s:
        s.execute(insert_query, {
            'username': username,
            'timestamp': timestamp,
            'distance': distance,
            'photo_id': photo_id,
            'device_id': device_id
        })
        s.commit()