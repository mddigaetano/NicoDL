# NicoDL
Python script that lets you download Videos from NicoNico

## About
The script is made of several steps:
1. fetch `SONGS_COUNT` tweets from `TWITTER_USERNAME`'s timeline;
1. downloads the video
    1. first it fetches the video pages to obtain the needed cookies
    1. then, it opens the video link and starts the download
1. creates the mp3
   1. to do so, the script calls `ffmpeg` to convert the video
   1. if the song title is not the one you want thanks to OS constraints in naming files, the `corrections` dict switches it
   1. finally, it sets the right mp3 tags, with `Vocaloid` as album entry

Every tweet is written following a specific format:
* `\[author 1 & author 2 & ... & final author feat. vocalist 1 & ... & final vocalist\] song title http://link.to.song \#smXXXXX`  
where the http link is optional and the hashtag is the video id.

## Run from Docker
To run the container with docker just copy:
```sh
docker run -it --rm \
     --name niconicontainer \
     --mount type=bind,source=(pwd)/Music,target=/app/Music \
     --mount type=bind,source=(pwd)/Video,target=/app/Video \
     -e TWITTER_USERNAME=<your_twitter_id> \
     -e SONGS_COUNT=<how_many_songs_to_download> \
     -e OAUTH_TOKEN=<your_token> \
     -e OAUTH_TOKEN_SECRET=<your_token> \
     -e APP_KEY=<your_token> \
     -e APP_SECRET=<your_token> \
     mddigaetano/niconicoload:v1.0
```
where:
* `OAUTH_TOKEN`
* `OAUTH_TOKEN_SECRET`
* `APP_KEY`
* `APP_SECRET`  
are the four tokens the Twitter API needs (the app just needs read-only permissions).

If you want to run it in detached mode just type `-d` instead of `-it`  
To change the location of the downloaded videos and converted songs edit the `source=` parameters after `--mount`  
You could also omit the Video mount, but doing so means it will always fetch already downloaded videos

## Compile from source
If you want to build the docker image, `cd` into the repo and type:
```sh
docker build -t niconicoload .
```

If you just want to use the script without a container, install the python dependencies and ffmpeg and run the script.  
