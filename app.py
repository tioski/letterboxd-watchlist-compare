import streamlit as st
import requests
import xml.etree.ElementTree as ET

def get_watchlist_from_rss(username):
    url = f"https://letterboxd.com/{username}/watchlist/rss/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Utente non trovato o watchlist privata.")
    
    root = ET.fromstring(response.content)
    titles = set()
    for item in root.findall(".//item"):
        title = item.find("title").text
        if title:
            titles.add(title.strip())
    return titles

st.title("🎬 Confronta Watchlist Letterboxd")

user1 = st.text_input("👤 Username 1")
user2 = st.text_input("👤 Username 2")

if st.button("Confronta") and user1 and user2:
    try:
        wl1 = get_watchlist_from_rss(user1)
        wl2 = get_watchlist_from_rss(user2)
        in_comune = wl1 & wl2

        if in_comune:
            st.success(f"🎉 {len(in_comune)} film in comune:")
            for title in sorted(in_comune):
                st.write(f"• {title}")
        else:
            st.warning("Nessun film in comune trovato.")
    except Exception as e:
        st.error(f"Errore: {str(e)}")
