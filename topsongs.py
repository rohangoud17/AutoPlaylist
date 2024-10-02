from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = "7aeac8b14fdb472faddaa8cfcc79c6b8"
client_secret = "fd33b5e917d846e49ed675e6403575e1"

date = input("which year do you want to travel to? Type in the date in this format yyyy-mm-dd")



response = requests.get("https://www.billboard.com/charts/hot-100/" + date)





soup = BeautifulSoup(response.text,"html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [(song.get_text().strip()) for song in song_names_spans]


spotify_endpoint = "https://api.spotify.com/v1/users/smedjan/playlists"
playlist_param = {
    "name": "New Playlist",
    "public": False
}

data_json = playlist_param
spot_res = requests.post(url=spotify_endpoint,json=playlist_param)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username="Rohan", 
    )
)
user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
