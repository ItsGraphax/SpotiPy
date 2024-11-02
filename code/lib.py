import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = '397b52223fb74badb14f507606fbe859'
SPOTIPY_CLIENT_SECRET = '71d3541cdcf649338631a98d23082470'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

DEFAULT_FALLBACK = {
    "device": {
        "id": "string",
        "is_active": False,
        "is_private_session": False,
        "is_restricted": False,
        "name": "-",
        "type": "-",
        "volume_percent": 0,
        "supports_volume": False
    },
    "repeat_state": "string",
    "shuffle_state": False,
    "context": {
        "type": "string",
        "href": "string",
        "external_urls": {
            "spotify": "string"
        },
        "uri": "string"
    },
    "timestamp": 0,
    "progress_ms": 0,
    "is_playing": False,
    "item": {
        "album": {
            "album_type": "-",
            "total_tracks": 0,
            "available_markets": [],
            "external_urls": {
                "spotify": "string"
            },
            "href": "string",
            "id": "2up3OPMp9Tb4dAKM2erWXQ",
            "images": [
                {
                    "url": "DEFAULT",
                    "height": 300,
                    "width": 300
                }
            ],
            "name": "Nothing Playing",
            "release_date": "-",
            "release_date_precision": "-",
            "restrictions": {
                "reason": "market"
            },
            "type": "album",
            "uri": "-",
            "artists": [
                {
                    "external_urls": {
                        "spotify": "string"
                    },
                    "href": "string",
                    "id": "string",
                    "name": "-",
                    "type": "artist",
                    "uri": "string"
                }
            ]
        },
        "artists": [
            {
                "external_urls": {
                    "spotify": "string"
                },
                "href": "string",
                "id": "string",
                "name": "-",
                "type": "artist",
                "uri": "string"
            }
        ],
        "available_markets": ["string"],
        "disc_number": 0,
        "duration_ms": 0,
        "explicit": False,
        "external_ids": {
            "isrc": "string",
            "ean": "string",
            "upc": "string"
        },
        "external_urls": {
            "spotify": "string"
        },
        "href": "string",
        "id": "string",
        "is_playable": False,
        "linked_from": {
        },
        "restrictions": {
            "reason": "string"
        },
        "name": "Nothing Playing",
        "popularity": 0,
        "preview_url": "string",
        "track_number": 0,
        "type": "track",
        "uri": "string",
        "is_local": False
    },
    "currently_playing_type": "string",
    "actions": {
        "interrupting_playback": False,
        "pausing": False,
        "resuming": False,
        "seeking": False,
        "skipping_next": False,
        "skipping_prev": False,
        "toggling_repeat_context": False,
        "toggling_shuffle": False,
        "toggling_repeat_track": False,
        "transferring_playback": False
    }
}

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                                            client_id=SPOTIPY_CLIENT_ID,
                                            client_secret=SPOTIPY_CLIENT_SECRET,
                                            redirect_uri=SPOTIPY_REDIRECT_URI,
                                            scope='user-read-playback-state user-modify-playback-state'))

def update():
        playback = sp.current_playback()
        if playback:
                return playback
        else:
                return DEFAULT_FALLBACK

def playpause():
    playing = sp.current_playback()['is_playing']
    if playing:
        sp.pause_playback()
    else:
        sp.start_playback()
        
def next():
    sp.next_track()
