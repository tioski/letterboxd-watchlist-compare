import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_watchlist(username):
    url = f"https://letterboxd.com/{username}/watchlist/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    films = soup.select('li.poster-container')
    titles = [film['data-film-slug'].strip('/').replace('-', ' ').title() for film in films]
    return set(titles)

st.title("🎬 Confronta Watchlist Letterboxd")

user1 = st.text_input("👤 Username 1")
user2 = st.text_input("👤 Username 2")

if st.button("Confronta") and user1 and user2:
    try:
        wl1 = get_watchlist(user1)
        wl2 = get_watchlist(user2)
        in_comune = wl1 & wl2

        if in_comune:
            st.success(f"🎉 {len(in_comune)} film in comune:")
            for title in sorted(in_comune):
                st.write(f"• {title}")
        else:
            st.warning("Nessun film in comune trovato.")
    except Exception as e:
        st.error(f"Errore: {str(e)}")
