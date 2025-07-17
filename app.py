import streamlit as st
import requests
import xml.etree.ElementTree as ET

def get_watchlist_from_rss(username):
    url = f"https://letterboxd.com/{username}/watchlist/rss/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        raise Exception("Watchlist non trovata (forse privata o username errato).")
    elif response.status_code != 200:
        raise Exception(f"Errore HTTP {response.status_code} durante la richiesta.")

    try:
        root = ET.fromstring(response.content)
        titles = set()
        for item in root.findall(".//item"):
            title = item.find("title").text
            if title:
                titles.add(title.strip())
        if not titles:
            raise Exception("Nessun film trovato nella watchlist (forse è vuota o privata).")
        return titles
    except ET.ParseError:
        raise Exception("Impossibile leggere il feed RSS. Forse la watchlist è privata.")

st.title("🎬 Confronta Watchlist Letterboxd")

user1 = st.text_input("👤 Username 1")
user2 = st.text_input("👤 Username 2")

if st.button("Confronta") and user1 and user2:
    try:
        wl1 = get_watchlist_from_rss(user1.strip())
        wl2 = get_watchlist_from_rss(user2.strip())
        in_comune = wl1 & wl2

        if in_comune:
            st.success(f"🎉 {len(in_comune)} film in comune:")
            for title in sorted(in_comune):
                st.write(f"• {title}")
        else:
            st.warning("Nessun film in comune trovato.")
    except Exception as e:
        st.error(f"Errore: {str(e)}")
