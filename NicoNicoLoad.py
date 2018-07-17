#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, urllib3
import twitter

class NicoNicoLoad:
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

    def __init__(self, ak, as, oat, oats, username, songs_count):
        self.APP_KEY = ak
        self.app_SECRET = as
        self.OAUTH_TOKEN = oat
        self.OAUTH_TOKEN_SECRET = oats
        self.username = username
        self.songs_count = songs_count

    def linkExtractor(self, song_id):
        http = urllib3.PoolManager()
        request = http.request('GET','http://www.nicovideo.jp/watch/' + song_id)
        page = request.data.decode('utf-8')
        index = page.find("smileInfo&quot;:{&quot;url&quot;:&quot;http:") + 39
        videoLink = page[index : page.find("&quot;", index)]
        return videoLink.replace("\\", "")


    def tweetFetcher(self):
        api = twitter.Api(APP_KEY,
                          APP_SECRET,
                          OAUTH_TOKEN,
                          OAUTH_TOKEN_SECRET)

        json = api.GetUserTimeline(screen_name = self.username,
                                   count = self.songs_count)
        for tweet in json:
            yield tweet

    def videoConverter(self):
        pass

    def tagEditor(self):
        pass

if __name__ == "__main__":
    ak = os.environ['APP_KEY']
    as = os.environ['APP_SECRET']
    oat = os.environ['OAUTH_TOKEN']
    oats = os.environ['OAUTH_TOKEN_SECRET']
    username = os.environ['TWITTER_USERNAME']
    songs_count = os.environ['SONGS_COUNT']

    nnl = NicoNicoLoad(ak, as, oat, oats, username, songs_count)

