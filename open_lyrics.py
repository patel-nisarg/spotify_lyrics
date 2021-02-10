"""
Open lyrics for whatever song is currently playing on your Spotify.

"""

import re

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import spotify_client_id, spotify_client_secret, genius_token
from lyricsgenius import Genius


# manage tokens here: https://genius.com/api-clients


def clean_title(artists, song_title):
    # if artist names show up in song title, remove artist name
    for artist in artists:
        # remix = ["remix", "Remix"]
        if artist in song_title:
            song_title_fix = re.sub("[\(\[].*?[\)\]]", "", song_title)
        # if remix in song_title:
        #     song_title_fix = song_title_fix + " " + remix[0]
        else:
            song_title_fix = song_title
    return song_title_fix


class OpenSongLyrics:
    def __init__(self):
        self.sclient_id = spotify_client_id
        self.sclient_secret = spotify_client_secret
        self.redirect_uri = 'http://localhost:8080'
        self.scope = 'user-read-playback-state'
        self.username = 'username'
        self.client_credentials_manager = SpotifyOAuth(username=self.username, redirect_uri=self.redirect_uri,
                                                       scope=self.scope, client_id=self.sclient_id,
                                                       client_secret=self.sclient_secret, open_browser=False)
        self.genius_token = genius_token
        self.lyrics = None
        self.genius = Genius(client_access_token=self.genius_token, response_format='dom', verbose=True,
                             skip_non_songs=True)

    def get_song_info(self):
        sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        playback_read = sp.current_playback()
        if playback_read is not None:
            get_title = playback_read['item']['name']
            get_artists = playback_read['item']['artists']
            artists = []
            for artist in get_artists:
                name = artist['name']
                artists.append(name)
            album = playback_read['item']['album']['name']
            song_info = {'title': get_title, 'artists': artists, 'album': album}
            print(song_info)
        else:
            song_info = {}
        return song_info

    def get_current_lyrics(self):
        song_info = self.get_song_info()
        print(song_info)
        song_title = clean_title(artists=song_info['artists'], song_title=song_info['title'])
        self.lyrics = self.genius.search_song(title=song_title, artist=song_info['artists'][0]).lyrics
        # artists = " ".join(song_info['artists'])
        # term = song_title + " " + artists
        # a = genius.search_all(term, per_page=5, page=1)
        # aa = genius._get_item_from_search_response(a, term, type_='song', result_type='song_title')
        # album = genius.search_lyrics()
        return self.lyrics


osl = OpenSongLyrics()
print(osl.get_current_lyrics())
