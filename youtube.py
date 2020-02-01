#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import cached_url
import yaml

with open('setting.yaml') as f:
    setting = yaml.load(f, Loader=yaml.FullLoader)
playlists_url = 'https://www.youtube.com/user/%s/playlists' % setting['user']

soup = BeautifulSoup(cached_url.get(playlists_url), 'html.parser')
