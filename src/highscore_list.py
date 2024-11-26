import pandas as pd
from datetime import datetime

def update_highscore_list(hs_list, user_name, distance, photo_id):
    """Manuelles Update mit dem neuen Wert, um nicht auf Latenz der Datenbank angewiesen zu sein"""

    df = hs_list
    df['new_flag'] = "old"
    df_unique = df.loc[df.groupby('username')['distance'].idxmin()]

    ### Neuen Versuch eintragen
    new_entry = pd.DataFrame({'username': user_name,
                              'timestamp': datetime.now().date(),
                              'distance': distance,
                              'photo_id': photo_id,
                              'device_id': [None],
                              'new_flag': "new"
                              })

    df_updated = pd.concat([df_unique, new_entry], ignore_index=True)

    ### Formatieren
    df_renamed = df_updated.rename(columns={'username': 'Name', 'timestamp': 'Zeit', 'distance': 'Score'})
    df_sorted = df_renamed.sort_values(by='Score', ascending=True)
    df_sorted['Platz'] = range(1, len(df_sorted) + 1)
    df_sorted = df_sorted[['Platz', 'Name', 'Zeit', 'Score', 'new_flag']]
    
    return df_sorted

def calculate_rank(highscore_list):
    """Berechne die Platzierung innerhalb der Einträge der Liste"""
    df = highscore_list
    filtered_df = df[df['new_flag'] == 'new']
    min_score_index = filtered_df['Score'].idxmin()
    platz_min_score = filtered_df.loc[min_score_index, 'Platz']
    return platz_min_score

def style_highscore(highscore_list):
    df = highscore_list
    df['Score'] = df['Score'].astype(int)
    styled_df = df.style.apply(
        lambda row: ['font-weight: bold; background-color: red' if row['new_flag'] == 'new' else '' for _ in row],
        axis=1  # Zeilenweise anwenden
    )
    return styled_df