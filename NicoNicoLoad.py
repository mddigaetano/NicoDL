#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

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

    APP_KEY = os.environ['APP_KEY']
    APP_SECRET = os.environ['APP_SECRET']
    OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET = os.environ['OAUTH_TOKEN_SECRET']

    def linkExtractor(self, url, name):
        return ""

    def tweetFetcher(self):
        return ""

    def videoConverter(self):
        return ""

    

if __name__ == "__main__":
    nnl = NicoNicoLoad()

