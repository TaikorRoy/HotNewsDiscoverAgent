# -*- coding: utf-8 -*-
__author__ = 'Taikor'

import news_crawler
import time
import codecs
import json


def load_pool_file(file_path):
    try:
        with codecs.open(file_path, "r", encoding="utf8") as f:
            content = f.read()
            news_pool = json.loads(content)
        return news_pool
    except:
        with codecs.open(file_path, "w", encoding="utf8") as f:
            pool_void = dict()
            str_buffer = json.dumps(pool_void)
            f.write(str_buffer)
        return pool_void


def update_pool_file(pool, file_path):
    with codecs.open(file_path, "w", encoding="utf8") as f:
        content = json.dumps(pool, ensure_ascii=False)
        f.write(content)
    return 0


def update_news_pool(file_path):
    Engine = {"Baidu"}
    news_pool_file_path = file_path

    news_pool = load_pool_file(news_pool_file_path)
    ct = int(time.time())
    ot_pool = list()
    ot_threshold = 2*24*3600
    obsolete_receive_queue = list()
    for news in news_pool.keys():
        if (ct - news_pool[news]) > ot_threshold:
            ot_pool.append(news)
    for news in ot_pool:
        obsolete_receive_queue.append(news)
        news_pool.pop(news)
    # need to push merge ot_pool with obsolete_pool

    news_set = news_crawler.fetch_news_master(Engine)
    for news in news_set:
        if news not in news_pool.keys():
            news_pool[news] = ct
    update_pool_file(news_pool, news_pool_file_path)
    return obsolete_receive_queue


def update_obsolete_pool(obsolete_pool_file_path, _queue):
    obsolete_pool = load_pool_file(obsolete_pool_file_path)
    ct = int(time.time())
    ot_pool = list()
    ot_threshold = 7*24*3600
    for news in obsolete_pool.keys():
        if (ct - obsolete_pool[news]) > ot_threshold:
            ot_pool.append(news)
    for news in ot_pool:
        obsolete_pool.pop(news)

    for news in _queue:
        obsolete_pool[news] = ct  # receive the discarded news from news_pool

    update_pool_file(obsolete_pool, obsolete_pool_file_path)


def update_kw_pool(kw_pool_file_path):
    kw_pool = load_pool_file(kw_pool_file_path)
    ct = int(time.time())
    ot_pool = list()
    ot_threshold = 2*24*3600
    for news in kw_pool.keys():
        if (ct - kw_pool[news]) > ot_threshold:
            ot_pool.append(news)
    for news in ot_pool:  # pop news that are ot
        kw_pool.pop(news)

    update_pool_file(kw_pool, kw_pool_file_path)

