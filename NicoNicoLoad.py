#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from requests import Session
from twitter import Twitter, OAuth

class NicoNicoLoad:

    CHUNK_SIZE = 1024
    corrections = {
        "names":
            [u"1-6 -out of the gravity-",
             u"World - Lampshade",
             u"Heart \' Palette",
             u"Re-flection",
             u"\'Hello, Planet",
             u"Vaicarious",
             u"The Flower of Raison d\'Etre"],
        "titles":
            [u"1/6 -out of the gravity-",
             u"World·Lampshade",
             u"Heart＊Palette",
             u"Re:flection",
             u"*Hello, Planet",
             u"√aicarious",
             u"The Flower of Raison d\'Être"]
    }

    def __init__(self, username, songs_count, oat, oats, ak, asecret):
        self.username = username
        self.songs_count = songs_count

        self.api = Twitter(auth = OAuth(oat, oats, ak, asecret))
        self.http = Session()

    def linkExtractor(self, song_id):
        page = self.http.get('http://www.nicovideo.jp/watch/' + song_id)
        page = page.text
        index = page.find(u"smileInfo&quot;:{&quot;url&quot;:&quot;http:") + 39
        videoLink = page[index : page.find("&quot;", index)]
        return videoLink.replace("\\", "")

    def videoDownloader(self, filename, song_id):
        if not os.path.isfile("./Video/"+filename+".mp4"):
            url = self.linkExtractor(song_id)
            if(url[-3:] == "low"):
                raise Exception("Low quality video!")

            request = self.http.get(url, stream = True)
            with open( "./Video/" + filename + ".mp4", 'wb') as download:
                for chunk in request.iter_content(chunk_size=self.CHUNK_SIZE):
                    download.write(chunk)
        else:
            raise Exception("Already downloaded!")

    def videoConverter(self, to_convert):
        pass

    def tagEditor(self, to_tag):
        pass

    def start(self):
        tweets = self.api.statuses.user_timeline(screen_name = self.username,
                                                 count = self.songs_count)
        to_convert = []
        for tweet in tweets:
            split = tweet['text'].split(" https")
            if len(split) == 1:
                split = tweet['text'].split(" #sm")
            filename = split[0].replace("&amp;", "&")
            song_id = tweet['entities']['hashtags'][0]['text']

            try:
                self.videoDownloader(filename, song_id)
                to_convert.append(filename)
            except Exception as e:
                print(str(e) + " " + filename)

        self.videoConverter(to_convert)
        self.tagEditor(to_convert)

if __name__ == "__main__":
    username = os.environ['TWITTER_USERNAME']
    songs_count = os.environ['SONGS_COUNT']

    oat = os.environ['OAUTH_TOKEN']
    oats = os.environ['OAUTH_TOKEN_SECRET']
    ak = os.environ['APP_KEY']
    asecret = os.environ['APP_SECRET']

    nnl = NicoNicoLoad(username, songs_count, oat, oats, ak, asecret)
    nnl.start()

