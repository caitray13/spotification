import spotipy
from spotipy.oauth2 import SpotifyOAuth

from typing import Dict, List, Any

import itertools


class SpotifyService():
    def __init__(self, scope) -> None:
        self.scope = scope
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        # TODO: put these into sub functions
        self.saved_tracks = self.current_user_saved_tracks()
        self.saved_tracks = list(itertools.chain(self.saved_tracks, self.current_user_saved_album_tracks()))

    def get_recently_played(self) -> List[Dict]:
        r = self.spotify.current_user_recently_played()
        recently_played = []
        saved_tracks = []
        for idx, item in enumerate(r['items']):
            
            track_dict = {}
            track_dict['track_name'] = item['track']['name']
            track_dict['track_id'] = item['track']['id']
            track_dict['track_uri'] = item['track']['uri']
            track_dict['artist_name'] = item['track']['artists'][0]['name']
            track_dict['artist_id'] = item['track']['artists'][0]['id']
            track_dict['artist_uri'] = item['track']['artists'][0]['uri']
            track_dict['popularity'] = item['track']['popularity']
            track_dict['duration_ms'] = item['track']['duration_ms']
            saved_tracks.append(track_dict)
            
            print(idx, track_dict['artist_name'],
                  " – ", track_dict['track_name'])
        return saved_tracks
    
    def current_user_saved_tracks(self) -> List[Dict]:
        r = self.spotify.current_user_saved_tracks(limit=50)
        saved_tracks = []
        for idx, item in enumerate(r['items']):
            track_dict = {}
            track_dict['track_name'] = item['track']['name']
            track_dict['track_id'] = item['track']['id']
            track_dict['track_uri'] = item['track']['uri']
            track_dict['artist_name'] = item['track']['artists'][0]['name']
            track_dict['artist_id'] = item['track']['artists'][0]['id']
            track_dict['artist_uri'] = item['track']['artists'][0]['uri']
            track_dict['popularity'] = item['track']['popularity']
            track_dict['duration_ms'] = item['track']['duration_ms']
            saved_tracks.append(track_dict)
        return saved_tracks
    
    def current_user_saved_album_tracks(self)-> Dict:
        r = self.spotify.current_user_saved_albums(limit=50)
        saved_tracks = []
        for idx, album in enumerate(r['items']):
            album = album['album']
            for track_idx in range(album['total_tracks']):
                track_dict = {}
                track_dict['track_id'] = album['tracks']['items'][track_idx]['id']
                track_dict['track_uri'] = album['tracks']['items'][track_idx]['uri']
                track_dict['track_name'] = album['tracks']['items'][track_idx]['name']
                track_dict['artist_name'] = album['artists'][0]['name']
                track_dict['artist_id'] = album['artists'][0]['id']
                track_dict['artist_uri'] = album['artists'][0]['uri']
                saved_tracks.append(track_dict)
        
        return saved_tracks
        
    def get_audio_analyis(self, limit=50, track_ids=None)-> Dict:
        if track_ids==None:
            track_ids = [track['track_uri'] for track in self.saved_tracks] 
            r = self.spotify.audio_features(tracks=track_ids[:limit])
            saved_tracks_audio_analysis = saved_tracks_audio_analysis = dict(zip(track_ids, r))
        else:
            r = self.spotify.audio_features(tracks=track_ids)
            saved_tracks_audio_analysis = dict(zip(track_ids, r))
        return saved_tracks_audio_analysis

    def get_saved_tracks(self):
        return self.saved_tracks
