This folder contains functional files, helping to make certain requests or extracting additional metadata

Some of the codes contain API requests, for which a key is requested. For that a Spotify developer account is required. 

The json files `category.json` and `hub_category.json` define how playlists and hubs have been coded into categories.

`create_db.js` was a first try towards extracting information by scraping in the console of the Spotify web application; it could not be used to automate the data collection since the content in the web application differed to the mobile application data

`playlist.py` can help requesting playlist information !!!! only the first 50 titles for now

with `previous_listening.py` the user's listening history can be requested