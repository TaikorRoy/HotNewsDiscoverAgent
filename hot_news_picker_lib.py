# -*- coding: utf-8 -*-
__author__ = 'Taikor'

import news_crawler
import pool_lib
import extract_news_kws_lib
import time


def rearrange(eles):
    # TODO: need further development
    def bog(str):
        return set(str.split(" "))

    eles = set(eles)
    groups = list()
    list_length = len(eles)
    for ele in eles:
        if len(bog(eles[i][1]) & bog(eles[i+j][1])) >= 1:
            buffer = list()
            buffer.append(eles[i])
            buffer.append(eles[i+j])
            groups.append(buffer)
            eles[i] = None  # remove similar items but remains the seat
            eles[i+j] = None
    return eles


def match_topic(topic_pos_buffer, topic_pos):
    topic_pos_list = topic_pos.split(" ")
    topic_pos_set = set(topic_pos_list)

    match_result = False
    for pos in topic_pos_buffer:
        pos_list = pos.split(" ")
        pos_set = set(pos_list)
        if len(pos_set & topic_pos_set) >= 2:
            match_result = True
            break
        else:
            pass
    return match_result


def select_hot_news(news_pool_file_path, obsolete_pool_file_path, kw_pool_file_path):
    volume_of_selection = 10
    ct = int(time.time())

    news_pool_dictionary = pool_lib.load_pool_file(news_pool_file_path)
    obsolete_pool_dictionary = pool_lib.load_pool_file(obsolete_pool_file_path)
    kw_pool_dictionary = pool_lib.load_pool_file(kw_pool_file_path)

    news_pool_title_set = set(news_pool_dictionary.keys())
    query_result = news_crawler.query_search_result_batch(news_pool_title_set)

    topic_candidates = list()
    for topic, query_result_quantity in query_result:
        if topic not in obsolete_pool_dictionary.keys():
            topic_candidates.append([topic, query_result_quantity])

    topic_candidates_titles_and_kws = [[x[0], extract_news_kws_lib.extract_news_kws(x[0])] for x in topic_candidates]

    topics_picked = list()
    counter = 0
    for ele in topic_candidates_titles_and_kws:
        if counter < volume_of_selection:
            if not match_topic(kw_pool_dictionary.keys(), ele[1]):
                topics_picked.append(ele)
                kw_pool_dictionary[ele[1]] = ct
                counter += 1

    for ele in topics_picked:
        try:
            news_pool_dictionary.pop(ele[0])
            obsolete_pool_dictionary[ele[0]] = ct
        except:
            print("Pop Dict Key Error")

    # topics_picked = rearrange(topics_picked)

    pool_lib.update_pool_file(news_pool_dictionary, news_pool_file_path)
    pool_lib.update_pool_file(obsolete_pool_dictionary, obsolete_pool_file_path)
    pool_lib.update_pool_file(kw_pool_dictionary, kw_pool_file_path)

    return topics_picked


if __name__ == "__main__":
    elses = [['日本韩国', '日本 韩国'], ['新加坡中国', '新加坡 中国'], ['不不不', '我 事'], ['不不不', '我 事'], ['不不不', '我 事'], ['不不不', '我 事'], ['不不不', '我 事'], ['不不不', '我 事'], ['不不不', '我 事'], ['不不不', '我 事']]
    print(elses)
    a = rearrange(elses)
    print(a)

