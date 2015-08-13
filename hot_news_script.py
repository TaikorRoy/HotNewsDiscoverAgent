__author__ = 'Taikor'

import hot_news_picker_lib
import mysql_updater_baseClass
import pool_lib
import time


class HotNewsDiscoverAgent(object):
    def __init__(self, _news_pool_file_path, _obsolete_pool_file_path, _kw_pool_file_path, _interval):
        self.news_pool_file_path = _news_pool_file_path
        self.obsolete_pool_file_path = _obsolete_pool_file_path
        self.kw_pool_file_path = _kw_pool_file_path
        self.interval = _interval

    def run_one_job(self):
        discarded_news_queue = pool_lib.update_news_pool(self.news_pool_file_path)
        pool_lib.update_obsolete_pool(self.obsolete_pool_file_path, discarded_news_queue)
        pool_lib.update_kw_pool(self.kw_pool_file_path)

        hot_news_and_kws = hot_news_picker_lib.select_hot_news(self.news_pool_file_path, self.obsolete_pool_file_path, self.kw_pool_file_path)

        mysql_updater = mysql_updater_baseClass.MySQLUpdater()
        for item in hot_news_and_kws:
            mysql_updater.query(item)
        mysql_updater.clean_up()
        return 0

    def run_batch(self):
        while True:
            self.run_one_job()
            time.sleep(self.interval)

if __name__ == "__main__":
    news_pool_file_path = r"news_pool_cache"
    obsolete_pool_file_path = r"obsolete_pool_cache"
    kw_pool_file_path = r"kw_pool_cache"
    interval = 1*3600
    agent = HotNewsDiscoverAgent(news_pool_file_path, obsolete_pool_file_path, kw_pool_file_path, interval)
    agent.run_batch()





