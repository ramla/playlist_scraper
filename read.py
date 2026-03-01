import ast
import csv
import os
import sys

filenames = []
if len(sys.argv) < 2:
    f = os.listdir("./dump")
    filenames = ["./dump/" + filename for filename in os.listdir("./dump") if filename[-5:] == ".dump"]
else:
    filenames = sys.argv[1:]

for filename in filenames:
    dump = None
    with open(filename, "r", encoding="utf-8") as file:
        dump = file.readline()

    dump = ast.literal_eval(dump)    

    playlist_name = "saved" # default: liked songs, list of items
    itemcontainer = dump
    data = []
    keys = []

    if type(dump) == dict:
        # playlist dump
        # playlist_keys: ['collaborative', 'description', 'external_urls', 'followers', 'href', 'id', 'images',
        #                 'name', 'owner', 'primary_color', 'public', 'snapshot_id', 'tracks', 'items', 'type', 'uri']
        playlist_name = dump["name"]
        itemcontainer = dump["items"]

    print("==========================================================")
    print("playlist name:", playlist_name)
    print("==========================================================")
    for item in itemcontainer:
        # item_keys = ['added_at', 'added_by', 'is_local', 'primary_color', 'track', 'item', 'video_thumbnail']
        # track_keys = ['preview_url', 'available_markets', 'explicit', 'type', 'episode', 'track', 'album', 'artists',
        #               'disc_number', 'track_number', 'duration_ms', 'external_ids', 'external_urls', 'href', 'id',
        #               'name', 'popularity', 'uri', 'is_local']
        # artist_keys = ['external_urls', 'href', 'id', 'name', 'type', 'uri']
        # album_keys = ['available_markets', 'type', 'album_type', 'href', 'id', 'images', 'name', 'release_date',
        #               'release_date_precision', 'uri', 'artists', 'external_urls', 'total_tracks']
        trackname = item["track"]["name"]
        artistnames = [artist["name"] for artist in item["track"]["artists"]]
        albumname = item["track"]["album"]["name"]
        release_date = item["track"]["album"]["release_date"]
        if release_date is not None:
            year = release_date.split("-")[0]
        else:
            year = ""
        print(f"{artistnames[0]} - {trackname} ({albumname}, {year})")
        
        data.append(",".join(
                [trackname] + \
                [artistnames[0]] + \
                [",".join(["; ".join((artistnames[1:]) if len(artistnames) > 1 else "")])] + \
                [albumname] + \
                [year]
            )
        )

    keys = ["Track", "Artist", "Other artists", "Album", "Year"] 

    if not os.path.exists("./csv"):
        os.makedirs("./csv")

    with open(f"csv/{playlist_name}.csv", "w", newline="", encoding="utf-8") as csvfile:
        f = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        f.writerow(",".join(keys))
        for row in data:
            f.writerow(row)
