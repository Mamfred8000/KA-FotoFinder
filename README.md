# KA-FotoFinder

## 🏙️ Beschreibung
**KA-FotoFinder** ist ein Spiel, bei dem man den Aufnahmeort eines Fotos aus Karlsruhe erraten soll. Die Fotos hängen aus und sind mit QR-Codes verknüpft, die direkt zur App führen. Dort kann man auf einer Karte den vermuteten Aufnahmeort markieren und das Ergebnis mit anderen vergleichen.

Die App verbindet Fotografie und Karteninteraktion mit einem spielerischen Ansatz.

---

## ⚙️ Funktionsweise
- **Benutzeroberfläche**: Erstellt mit [Streamlit](https://streamlit.io), einfach und interaktiv.
- **Kartenintegration**: Mit [Folium](https://python-visualization.github.io/folium/) wird eine Karte angezeigt, auf der Benutzer ihren Tipp abgeben können.
- **Datenbankanbindung**: Eine PostgreSQL-Datenbank speichert Fotos, Geopositionen und Highscores.
- **QR-Codes**: Jedes Foto hat eine spezifische ID, die beim Öffnen der App automatisch verwendet wird.
- **Highscore-System**: Ergebnisse werden in Echtzeit mit anderen Spielern verglichen.

---

## 📂 Projektstruktur
```
KA-FotoFinder/
├── app.py               # Hauptlogik der App
├── pages/
│   ├── 1_quiz.py        # Seite zur Tipp-Abgabe
│   └── 2_results.py     # Ergebnisse und Highscores
├── src/
│   ├── database.py      # Datenbankoperationen
│   ├── highscore_list.py# Highscore-Logik
│   ├── map.py           # Karte mit Folium
│   └── utils.py         # Hilfsfunktionen
├── streamlit/
│   ├── config.toml      # Streamlit Einstellungen
│   └── secrets.toml     # Datenbank Credentials
└── requirements.txt     # Abhängigkeiten
```

---

## 📚 Verwendete Bibliotheken und Technologien
- **Streamlit**: Für die Benutzeroberfläche.
- **Folium**: Darstellung interaktiver Karten.
- **Geopy**: Berechnung von Distanzen.
- **PostgreSQL**: Datenbank für Fotos und Highscores.
- **Pandas**: Verarbeitung und Anzeige der Daten.
- **SQLAlchemy**: Zugriff auf die Datenbank.
- **Streamlit-Folium**: Integration von Folium-Karten in Streamlit.
- **Streamlit-Javascript**: Erkennung von Desktop- oder Mobilmodus.

---

## 💡 Was ich dabei gelernt habe

- **Streamlit und App-Entwicklung**:  
  - Entwicklung einer interaktiven Benutzeroberfläche mit **Streamlit**, inklusive dem Einsatz von `session_state`, um Benutzereingaben und App-Zustände zwischen verschiedenen Seiten und Sessions zu verwalten.  
  - Aufbau eines mehrseitigen App-Flows mit dynamischen Seitenwechseln (`st.switch_page`).

- **Datenbankintegration mit PostgreSQL**:  
  - Einrichtung einer PostgreSQL-Datenbank auf Railway und Nutzung von **SQLAlchemy** zur Abfrage und Speicherung von Daten.  
  - Erstellen und Optimieren von SQL-Abfragen (z. B. für Highscore-Listen und Geo-Koordinaten).  
  - Implementierung von Datenbankoperationen wie das Einfügen neuer Ergebnisse (`INSERT`) und das Filtern sowie Sortieren von Highscores (`SELECT` mit Gruppierung und Filtern).

- **Geodaten und Interaktive Karten**:  
  - Arbeit mit **Folium** zur Erstellung dynamischer Karten, einschließlich Marker und Linien, um die geratene und tatsächliche Foto-Position visuell darzustellen.  
  - Implementierung von Klick-Events auf der Karte, um Benutzereingaben direkt in geografische Koordinaten umzuwandeln.  
  - Verwendung der Bibliothek **Geopy**, um Entfernungen zwischen zwei Geo-Punkten zu berechnen und die Ergebnisse in Echtzeit anzuzeigen.

- **Highscore-Mechanik und Datenverarbeitung**:  
  - Entwicklung eines Systems zur Berechnung der besten Spielergebnisse, basierend auf minimaler Distanz.  
  - Nutzung von **Pandas** zur Manipulation, Aggregation und Sortierung von Daten (z. B. Highscore-Tabellen).  
  - Erstellung eines Echtzeit-Ranking-Systems und optischer Hervorhebung aktueller Einträge mit `DataFrame.style`.

- **Gerätekompatibilität und Benutzerfreundlichkeit**:  
  - Implementierung einer automatischen Erkennung von Desktop- oder Mobilgeräten mit **streamlit-javascript**, um die Darstellung der App entsprechend anzupassen.  
  - Integration von QR-Codes zur einfachen Weiterleitung und Identifizierung spezifischer Fotos.


---

## 🛠️ Tech-Stack
- **Frontend**: Streamlit, Folium
- **Backend**: Python, PostgreSQL (gehostet auf Railway.io)
- **Datenverarbeitung**: Pandas, Geopy

---

## 🚀 So startest du die App
1. **Repository klonen**:
   ```bash
   git clone https://github.com/<username>/ka-fotofinder.git
   cd ka-fotofinder
   ```
2. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```
3. **App starten**:
   ```bash
   streamlit run app.py
   ```

---

## 🙌 Feedback
Ich freue mich über Rückmeldungen und Verbesserungsvorschläge!
