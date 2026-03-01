import spotipy
import sys
import os
from spotipy.oauth2 import SpotifyOAuth


SPOTIPY_CLIENT_ID=''
SPOTIPY_CLIENT_SECRET=''
SPOTIPY_REDIRECT_URI='http://127.0.0.1:9090'

def auth_spotipy_for_liked():
    scope = "user-library-read"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                     client_id=SPOTIPY_CLIENT_ID,
                                                     client_secret=SPOTIPY_CLIENT_SECRET,
                                                     redirect_uri=SPOTIPY_REDIRECT_URI))

def auth_spotipy():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
                                                     client_id=SPOTIPY_CLIENT_ID,
                                                     client_secret=SPOTIPY_CLIENT_SECRET,
                                                     redirect_uri=SPOTIPY_REDIRECT_URI))

def dump_playlist(sp:spotipy.Spotify, playlist):
    offset = 0
    if os.path.exists(f"dump/{playlist["name"]}.dump"):
        print(f"{playlist["name"]} has been previously dumped")
        return
    playlist_id = playlist["id"]
    total_tracks = playlist['tracks']['total']
    all_items = []
    items = sp.playlist_items(playlist_id, limit=50, offset=offset)['items']
    while len(items) > 0:
        print(f"    offset: {offset}, tracks in batch/tracks left:{len(items)}/{total_tracks-offset}")
        all_items += items
        offset += 50
        items = sp.playlist_items(playlist_id, limit=50, offset=offset)['items']
    playlist["items"] = all_items
    with open(f'dump/{playlist["name"]}.dump', 'w', encoding='utf-8') as file:
        file.write(str(playlist))
    print(f"    wrote {len(all_items)}/{total_tracks}")

def get_liked_tracks():
    if os.path.exists(f"dump/saved.dump"):
        print("Liked tracks have been previously dumped (to saved.dump)")
    else:
        sp = auth_spotipy_for_liked()
        liked_songs = sp.current_user_saved_tracks(limit=50)
        items = liked_songs['items']
        all_items = []
        offset = 0
        while len(items) > 0:
            all_items += items
            offset += 50
            items = liked_songs = sp.current_user_saved_tracks(limit=50, offset=offset)['items']
        with open(f'dump/saved.dump', 'w', encoding='utf-8') as file:
            file.write(str(all_items))

def get_playlist_by_id(sp:spotipy.Spotify, playlist_id):
    playlist = sp.playlist(playlist_id)
    dump_playlist(sp, playlist)

def get_all_playlists():
    sp = auth_spotipy()
    pl_offset = 0
    playlists = sp.current_user_playlists(limit=10, offset=pl_offset)
    i = 0
    while len(playlists["items"]) > 0:
        print(f"pl_offset: {pl_offset}")
        for playlist in playlists["items"]:
            i += 1
            print(f"{i}/{playlists["total"]}: {playlist["name"]}; {playlist["tracks"]["total"]} tracks; id={playlist["id"]}")
            dump_playlist(sp, playlist)
        pl_offset += 10
        playlists = sp.current_user_playlists(limit=10, offset=pl_offset)


if __name__ == "__main__":
    if not os.path.exists("./dump"):
        os.makedirs("./dump")

    if len(sys.argv) < 2:
        get_liked_tracks()
        get_all_playlists()

    args = sys.argv[1:]
    sp = auth_spotipy_for_liked()
    for id in args:
        get_playlist_by_id(sp, id)
