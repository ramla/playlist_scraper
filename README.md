# Quick Spotify Playlist Scraper

Spotify announced changes to the API effective **March 9th** including removal of current_user_playlists method so I made this scraper to do the deed in case it's more difficult later. I didn't want to decide on filtering or formatting at the moment so I just save the data as is so I can decide later. Thus this scraper **saves all the metadata available** in the API from the tracks (no, it's not as comprehensive as in Anna's backup but you have everything you need to reference to it later). My playlists came down to 72MB of dump files.

It turned out that some of my later created playlists weren't fetched with that method anyhow and I had to scrape the rest by playlist id (the whole share url works here) anyway.

To use the scraper insert your own secrets in scrape.py and start blastin'. Here's one writeup on how to get your own secrets. [https://stevesie.com/docs/pages/spotify-client-id-secret-developer-api](https://stevesie.com/docs/pages/spotify-client-id-secret-developer-api)

### Usage examples:
> `python ./scrape.py` fetch all playlists spotify agrees to list for you with current_user_playlists<br>
> `python ./scrape.py playlist_url playlist_id`<br>
> `python ./read.py` batch process all files in ./dump/<br>
> `python ./read.py dump/songs.dump dump/playlist.dump`<br>
