import streamlit as st
from datetime import date
from sqlalchemy import text

st.title("Datenbank")

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# User input fields
username = st.text_input("Username")
timestamp = st.date_input("Timestamp", date.today())
distance = st.number_input("Distance (in meters)", min_value=0.0, format="%.2f")
photo_id = st.text_input("Photo ID")

# Function to insert data into the database
def insert_data(username, timestamp, distance, photo_id):
    insert_query = text(
        'INSERT INTO "KAFotoFinder-Scoreboard" (username, timestamp, distance, photo_id) '
        'VALUES (:username, :timestamp, :distance, :photo_id)'
    )
    
    # Execute the insert query
    with conn.session as s:
        s.execute(insert_query, {
            'username': username,
            'timestamp': timestamp,
            'distance': distance,
            'photo_id': photo_id
        })
        s.commit()
    
    st.success("Data inserted successfully!")
    st.rerun()

# Button to submit the data
if st.button("Submit"):
    if username and photo_id:  # Basic validation to ensure fields are filled
        insert_data(username, timestamp, distance, photo_id)
    else:
        st.warning("Please fill in all fields.")

# Perform query.
df = conn.query('SELECT * FROM "KAFotoFinder-Scoreboard";', ttl="10m")
st.write(df)