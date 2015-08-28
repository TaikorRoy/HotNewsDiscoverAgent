# -*- coding: utf-8 -*-
__author__ = 'Taikor'

import requests
import re
import time


def extract_news(_body, _Engine):
    if _Engine == "Sougou":
        pattern = r'<a .+?(?:business_headline|business_newslist).+? title="(.+?)"'
        _news = re.findall(pattern, _body, flags=re.DOTALL)
    elif _Engine == "Baidu":
        _news = list()
        div_pattern = r'<div class="middle-focus-news">(.+?)</div>'
        title_pattern = r'target="_blank">(.+?)</a>'
        div_match = re.findall(div_pattern, _body, flags=re.DOTALL)
        section_selected = [0, 1]
        i = 0
        for div_value in div_match:
            if i in section_selected:
                title_match = re.findall(title_pattern, div_value, flags=re.DOTALL)
                _news = _news + title_match
            i += 1

    news_buffer = list()
    for item in _news:
        if len(item) > 6 and item.find("<") == -1:
            news_buffer.append(item)
    news_buffer[0] = "!!!" + news_buffer[0]  # marking first news (bold)
    return news_buffer


def fetch_news(_Engine):
    URL = {"Sougou": r"http://news.sogou.com/business.shtml", "Baidu": r"http://finance.baidu.com/"}
    r = requests.get(URL[_Engine])
    while True:
        if r.status_code == requests.codes.ok:
            if _Engine is "Baidu":
                r.encoding = "gbk"
            html_body = r.text
            _news = extract_news(html_body, _Engine)
            break
        else:
            time.sleep(5)  # if request failed, then program sleep 5 s and retry
            r = requests.get(URL[_Engine])
    return _news


def fetch_news_master(Engines):
    news = list()
    for engine in Engines:
        newslist_buffer = fetch_news(engine)
        news = news + newslist_buffer
    news_set = set(news)
    return news_set


def query_search_result(_news_title):
    url = "http://news.baidu.com/ns"
    ct = int(time.time())
    secs_per_day = 3600*24
    bt = ct - secs_per_day
    et = ct
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.52 Safari/537.36',
        'Host': 'news.baidu.com'
    }
    paras = {'word': _news_title,
             'bt': bt,
             'et': et,
             'ct': '1',
             'rn': '20',
             'ie': 'utf-8'}
    while True:   # Either request failed or succeed, the crawler sleep for 0.1 s, loop breaks when crawler succeed
        r = requests.get(url, params=paras)
        print(r.url)
        html_body = r.text
        pattern = r'<span class="nums">.+?([0-9]*?,?[0-9]*?).</span>'
        match = re.findall(pattern, html_body)
        if len(match) > 0:   # pattern found, request succeed !
            num = int(match[0].replace(",", ""))
            if _news_title.find("!!!") > 0:
                num += 999999999999
            time.sleep(0.1)
            break
        else:  # pattern not found, request failed, crawler retry this request
            print("Error Page Returned")
            time.sleep(0.1)
    return num


def query_search_result_batch(_news_title_set):
    news_num_query_result = list()
    for _title in _news_title_set:
        news_title = _title
        news_num = query_search_result(_title)
        news_num_query_result.append([news_title, news_num])
    news_num_query_result.sort(key=lambda news_result: news_result[1], reverse=True)
    return news_num_query_result

