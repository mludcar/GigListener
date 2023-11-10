import spotipy
import logging
from spotipy.oauth2 import SpotifyOAuth
from constraints import SPOTIFY_CLIENT_ID, SPOTIFY_SECRET_ID, SPOTIFY_REDIRECT_URI

def main():
    sp = get_spotify_authentication()
    spotify_empty_list = create_spotify_list(sp, reproduction_list_name)
    song_to_search = ['karma police radiohead']
    song_uri = search_list_spotify(sp, song_to_search)
    add_songs_to_list(sp, song_uri, spotify_empty_list)
    logging.info("SUCCESS!!!")

# Create spotify connection
def get_spotify_authentication():
    logging.info("Connecting with Spotify...")
    sp_oauth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_SECRET_ID, redirect_uri=SPOTIFY_REDIRECT_URI, scope="playlist-modify-private")
    return spotipy.Spotify(auth_manager=sp_oauth)

# Reproduction List Name only for testing pourpose
reproduction_list_name = 'Magical List from Mike The Sorcerer'

#TODO automatic name list creator

# Spotify reproduction list creator
def create_spotify_list(spotify_connection, list_name):
    logging.info("Creating Spotify List...")
    empty_list = spotify_connection.user_playlist_create(spotify_connection.me()["id"], list_name, public=False, description='Created list by Sorcerer Mike python incantation')
    return empty_list['id']

# Search song on Spotify
def search_song_spotify(spotify_connection, song_name):
    response = spotify_connection.search(q=song_name, type='track')
    if response['tracks']['items']:
        first_appareance = response['tracks']['items'][0]
        return first_appareance['uri']
    else:
        logging.info(f'{song_name} not founded')
        return ''

# Function to iterate list and search all songs
def search_list_spotify(spotify_connection, song_list):
    logging.info("Searching songs...")
    raw_list = []
    for song in song_list:
        new_song = search_song_spotify(spotify_connection, song)
        raw_list.append(new_song)
    return raw_list

# Add list of songs to reproduction list
def add_songs_to_list(spotify_connection, uri_song_list, spotify_empty_list):
    logging.info("Adding songs to list...")
    #filter list in order to avoid empty string
    filtered_song_list = [song for song in uri_song_list if song]
    spotify_connection.playlist_add_items(spotify_empty_list, filtered_song_list)

if __name__ == "__main__":
    main()
