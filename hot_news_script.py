__author__ = 'Taikor'

import hot_news_picker_lib
import mysql_updater_baseClass
import pool_lib
import time


class HotNewsDiscoverAgent(object):
    def __init__(self, _news_pool_file_path, _obsolete_pool_file_path, _kw_pool_file_path, _times_to_update, _pool_update_freq):
        self.news_pool_file_path = _news_pool_file_path
        self.obsolete_pool_file_path = _obsolete_pool_file_path
        self.kw_pool_file_path = _kw_pool_file_path
        self.times_to_update = _times_to_update
        self.pool_update_freq = _pool_update_freq

    def update_pools(self):
        discarded_news_queue = pool_lib.update_news_pool(self.news_pool_file_path)
        pool_lib.update_obsolete_pool(self.obsolete_pool_file_path, discarded_news_queue)
        pool_lib.update_kw_pool(self.kw_pool_file_path)

    def update_db(self):
        hot_news_and_kws = hot_news_picker_lib.select_hot_news(self.news_pool_file_path, self.obsolete_pool_file_path, self.kw_pool_file_path)

        mysql_updater = mysql_updater_baseClass.MySQLUpdater()
        for item in hot_news_and_kws:
            mysql_updater.query(item)
        mysql_updater.clean_up()
        print("Db Updated !")
        return 0

    def time_match(self, times):
        ct = time.localtime()
        hour = ct.tm_hour
        min = ct.tm_min
        result = False
        for time_to_update in times:
            if time_to_update["hour"] == -99:  # debug use only, always return True
                result = True
                break
            if time_to_update["hour"] == -1:  # for pool update frequence, disable hour by set its value to -1
                hour = -1
            if hour == time_to_update["hour"] and min == time_to_update["min"]:
                result = True
                break
            else:
                result = False
        return result

    def update_db_when_time_is_right(self):
        test = self.time_match(self.times_to_update)
        if test:
            self.update_db()
            return 0
        else:
            return -1

    def update_pool_when_time_is_right(self):
        test = self.time_match(self.pool_update_freq)
        if test:
            self.update_pools()
            return 0
        else:
            return -1

    def run_batch(self):
        while True:  # loop every
            return_code_db = self.update_db_when_time_is_right()
            return_code_pool = self.update_pool_when_time_is_right()
            if return_code_db == 0:
                time.sleep(61)
            if return_code_pool == 0:
                time.sleep(61)
            time.sleep(1)

if __name__ == "__main__":
    news_pool_file_path = r"news_pool_cache"
    obsolete_pool_file_path = r"obsolete_pool_cache"
    kw_pool_file_path = r"kw_pool_cache"
    times_to_update = [{"hour": 9, "min": 35}, {"hour": 16, "min": 35}]
    pool_update_freq = [{"hour": -1, "min": 0}]
    agent = HotNewsDiscoverAgent(news_pool_file_path, obsolete_pool_file_path, kw_pool_file_path, times_to_update, pool_update_freq)
    agent.run_batch()





