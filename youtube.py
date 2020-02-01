#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import cached_url
import yaml
import re
import time
import traceback as tb
from telegram_util import matchKey, isCN

def getList(pivot, text):
    for m in re.finditer(pivot, text):
        tmp = text[m.end(): m.end() + 40]
        tmp = tmp.replace('\\"', '')
        x = tmp.find('"')
        yield tmp[:x]


def videoFilter(title, v_len, author, _, raw):
    if matchKey(title, ['镇魂', '白宇', '朱一龙']) and v_len > 60 * 20:
        return False
    if matchKey(title, ['丁毅', '聰明的一休', '準提咒']):
        return False
    if matchKey(author, ['sunfirekiss', '丁毅', 'YaleUniversity']):
        return False
    if matchKey(raw, ['Human Behavioral Biology']):
        return False
    if matchKey(author, ['bach', 'piano']) or matchKey(title, ['bach', 'piano']):
        return False
    if v_len > 10 * 60:
        return False
    if isCN(title):
        return False
    return True

def getPiece(b, e, text):
    if text.find(b) == -1 or text.find(e) == -1:
        return ''
    return text[text.find(b) + len(b): text.find(e)].strip()[:-1]

with open('setting.yaml') as f:
    setting = yaml.load(f, Loader=yaml.FullLoader)

lists_url = 'https://www.youtube.com/user/%s/playlists' % setting['user']
list_url = 'https://www.youtube.com/playlist?list='
video_url = 'https://www.youtube.com/watch?v='

list_pivot = 'playlist\?list='
video_pivot = '"videoId":"'
length_pivot = '"lengthSeconds":"'
title_pivot = '","title":"'
author_pivot = ',"author":"'
json_pivot = 'window["ytInitialData"] = '
json_end = 'window["ytInitialPlayerResponse"]'

lists_html = cached_url.get(lists_url)

# for p in getList(list_pivot, lists_html):
#     for v in getList(video_pivot, cached_url.get(list_url + p)):
#         with open('videos.txt', 'a') as f:
#             f.write(v + '\n')

with open('videos.txt') as f:
    videos = f.read().split()

video_info = []
titles = set()
for v in set(videos):
    try:
        v_html = cached_url.get(video_url + v)
        v_len = int(next(getList(length_pivot, v_html)))
        title = next(getList(title_pivot, v_html))
        if title in titles:
            continue
        titles.add(title)
        author = next(getList(author_pivot, v_html))
        video_info.append((title, v_len, author, video_url + v, v_html))
        with open('video_info.txt', 'a') as f:
            f.write('%s\t%d\t%s\t%s\n' % (title, v_len, author, video_url + v))
    except Exception as e:
        # pass
        print(e)
        tb.print_exc()


video_info = [x for x in video_info if videoFilter(*x)]
video_info = sorted(video_info, key=lambda x: x[1])
with open('video_info.txt', 'w') as f:
    f.write('Title\tLength\tAuthor\tUrl\n')
    for x in video_info:
        f.write('%s\t%d\t%s\t%s\n' % x[:-1])
