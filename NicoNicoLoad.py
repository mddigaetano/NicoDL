#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

from requests import Session
from twitter import Twitter, OAuth

from mutagen.mp3 import MP3
from mutagen.id3 import TIT2, TPE1, TALB


class NicoNicoLoad:

    CHUNK_SIZE = 1024
    corrections = {
        u"1-6 -out of the gravity-": u"1/6 -out of the gravity-",
        u"World - Lampshade": u"World·Lampshade",
        u"Heart \' Palette": u"Heart＊Palette",
        u"Re-flection": u"Re:flection",
        u"\'Hello, Planet": u"*Hello, Planet",
        u"Vaicarious": u"√aicarious",
        u"The Flower of Raison d\'Etre": u"The Flower of Raison d\'Être"}

    def __init__(self, username, songs_count, oat, oats, ak, asecret, nicouser, nicopass):
        self.username = username
        self.songs_count = songs_count

        self.api = Twitter(auth=OAuth(oat, oats, ak, asecret))
        self.http = Session()
        self.nicoLogin(nicouser, nicopass)

    def nicoLogin(self, username, password):
        payload = {
            'mail_tel': username,
            'password': password
        }
        self.http.post('https://account.nicovideo.jp/login', data=payload)

    def linkExtractor(self, song_id):
        page = self.http.get('http://www.nicovideo.jp/watch/' + song_id)
        page = page.text
        index = page.find("smileInfo&quot;:{&quot;url&quot;:&quot;http:") + 39
        videoLink = page[index: page.find("&quot;", index)].replace("\\", "")
        if videoLink[-3:] == "low":
            raise Exception("Low quality video!")
        return videoLink

    def videoDownloader(self, filename, song_id):
        url = self.linkExtractor(song_id)
        request = self.http.get(url, stream=True)
        with open("./Video/" + filename + ".mp4", 'wb') as download:
            for chunk in request.iter_content(chunk_size=self.CHUNK_SIZE):
                download.write(chunk)

    def videoConverter(self, filename):
        subprocess.run("ffmpeg -i ./Video/\"" + filename + ".mp4\" "
                       "-vn ./Music/\"" + filename + ".mp3\" "
                       ">/dev/null 2>&1",
                       shell=True)

    def tagEditor(self, filename):
        mp3 = MP3("./Music/" + filename + ".mp3")
        if mp3.tags == None:
            mp3.add_tags()
        name = filename.split("] ")
        artists = name[0]
        title = name[1]
        artists = artists[1:] \
            .replace(" feat.", ";") \
            .replace(" &", ";") \
            .replace("'", "*")
        try:
            title = self.corrections[title]
        except KeyError:
            pass

        mp3.tags.add(TIT2(encoding=3, text=title))
        mp3.tags.add(TALB(encoding=3, text=u"Vocaloid"))
        mp3.tags.add(TPE1(encoding=3, text=artists))
        mp3.save(v1=2)

    def tweetParser(self, tweet):
        split = tweet['text'].split(" https")
        if len(split) == 1:
            split = tweet['text'].split(" #sm")
        filename = split[0].replace("&amp;", "&")
        song_id = tweet['entities']['hashtags'][0]['text']
        return filename, song_id

    def start(self):
        tweets = self.api.statuses.user_timeline(screen_name=self.username,
                                                 count=self.songs_count)
        to_convert = []
        for tweet in tweets:
            filename, song_id = self.tweetParser(tweet)
            try:
                if not os.path.isfile("./Video/"+filename+".mp4"):
                    self.videoDownloader(filename, song_id)
                    to_convert.append(filename)
                else:
                    raise Exception("Already downloaded!")
            except Exception as e:
                print(str(e) + " " + filename)

        for filename in to_convert:
            self.videoConverter(filename)
            self.tagEditor(filename)

if __name__ == "__main__":
    username = os.environ['TWITTER_USERNAME']
    songs_count = int(os.environ['SONGS_COUNT'])

    oat = os.environ['OAUTH_TOKEN']
    oats = os.environ['OAUTH_TOKEN_SECRET']
    ak = os.environ['APP_KEY']
    asecret = os.environ['APP_SECRET']

    nicouser = os.environ['NICONICO_USERNAME']
    nicopass = os.environ['NICONICO_PASSWORD']

    nnl = NicoNicoLoad(username, songs_count, oat, oats, ak, asecret, nicouser, nicopass)
    nnl.start()
