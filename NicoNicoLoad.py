#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, urllib3
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
        self.http = urllib3.PoolManager()

    def linkExtractor(self, song_id):
        request = self.http.request('GET',
                                    'http://www.nicovideo.jp/watch/' + song_id)
        page = request.data.decode('utf-8')
        index = page.find("smileInfo&quot;:{&quot;url&quot;:&quot;http:") + 39
        videoLink = page[index : page.find("&quot;", index)]
        return videoLink.replace("\\", "")

    def videoDownloader(self, filename, song_id):
        if not os.path.isfile("./Video/"+filename+".mp4"):
            url = linkExtractor("http://www.nicovideo.jp/watch/" + song_id)
            if(url[-3:] == "low"):
                raise Exception("Low quality video!")

            request = http.request('GET', url, preload_content=False)
            with open( "./Video/\"" + filename + ".mp4\"", 'wb') as download:
                while True:
                    data = r.read(CHUNK_SIZE)
                    if not data:
                        break
                    out.write(data)
            request.release_conn()
        else:
            raise Exception("Already downloaded!")

    def videoConverter(self, to_convert):
        pass

    def tagEditor(self, to_tag):
        pass

    def start(self):
        tweets = self.api.statuses.user_timeline(screen_name = self.username,
                                                 count = self.count)
        to_convert = []
        for tweet in tweets:
            split = tweet.text.split(" https")
            if len(split) == 1:
                split = tweet.text.split(" #sm")
            filename = split[0].replace("&amp;", "&")
            song_id = tweet.hashtags[0].text

            try:
                videoDownloader(filename, song_id)
                to_convert.append(filename)
            except:
                pass

        videoConverter(to_convert)
        tag_editor(to_convert)


if __name__ == "__main__":
    username = os.environ['TWITTER_USERNAME']
    songs_count = os.environ['SONGS_COUNT']

    ak = os.environ['APP_KEY']
    asecret = os.environ['APP_SECRET']
    oat = os.environ['OAUTH_TOKEN']
    oats = os.environ['OAUTH_TOKEN_SECRET']

    nnl = NicoNicoLoad(username, songs_count, ak, asecret, oat, oats)
    nnl.start()

