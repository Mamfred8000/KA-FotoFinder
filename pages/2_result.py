import streamlit as st
import src.database
import src.highscore_list

def main():
    st.session_state.highscore_list = src.highscore_list.update_highscore_list(
        st.session_state.hs_list,
        st.session_state.user_name,
        st.session_state.distance,
        st.session_state.photo_id
        )
    
    st.session_state.rank = src.highscore_list.calculate_rank(
        st.session_state.highscore_list
        )


    st.markdown(f"<h2 style='text-align: center;'>{st.session_state.distance:.0f}m</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>{st.session_state.rank}. Platz für dich!</p>", unsafe_allow_html=True)

    st.write("### Dein Score:")
    map_obj = src.map.generate_map(show_result=True)

    st.write("### Highscore Liste:")
    st.dataframe(
        src.highscore_list.style_highscore(st.session_state.highscore_list),
        hide_index=True,
        column_order=("Platz", "Name", "Zeit", "Score")
        )

##main
if 'init_flag' in st.session_state:
    main()
else:
    st.write("Initialization failed. Read QR-Code to resume.")

# Output für Entwicklung
#st.write(st.session_state)