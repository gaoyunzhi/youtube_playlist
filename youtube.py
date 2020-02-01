#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import cached_url
import yaml
import re
import time
import traceback as tb

def getList(pivot, text):
    for m in re.finditer(pivot, text):
        tmp = text[m.end(): m.end() + 40]
        tmp = tmp.replace('\\"', '')
        x = tmp.find('"')
        yield tmp[:x]

with open('setting.yaml') as f:
    setting = yaml.load(f, Loader=yaml.FullLoader)

lists_url = 'https://www.youtube.com/user/%s/playlists' % setting['user']
list_url = 'https://www.youtube.com/playlist?list='
video_url = 'https://www.youtube.com/watch?v='

list_pivot = 'playlist\?list='
video_pivot = '"videoId":"'
length_pivot = '"lengthSeconds":"'
title_pivot = '","title":"'

lists_html = cached_url.get(lists_url)

# for p in getList(list_pivot, lists_html):
#     for v in getList(video_pivot, cached_url.get(list_url + p)):
#         with open('videos.txt', 'a') as f:
#             f.write(v + '\n')

with open('videos.txt') as f:
    videos = f.read().split()

video_info = []

for v in set(videos):
    try:
        v_html = cached_url.get(video_url + v)
        v_len = int(next(getList(length_pivot, v_html)))
        title = next(getList(title_pivot, v_html))
        video_info.append((title, v_len, video_url + v))
        with open('video_info.txt', 'a') as f:
            f.write('%s\t%d\t%s\n' % (title, v_len, video_url + v))
    except Exception as e:
        pass
        # print(e)
        # tb.print_exc()

video_info = sorted(video_info, key=lambda x: x[1])
with open('video_info.txt', 'w') as f:
    for x in video_info:
        f.write('%s\t%d\t%s\n' % x)
