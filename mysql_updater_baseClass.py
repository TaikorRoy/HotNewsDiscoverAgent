# -*- coding: utf-8 -*-
__author__ = 'Taikor'

import MySQLdb
import time


class MySQLUpdater(object):
    HOST = "180.153.177.252"
    USER = "palas"
    PASSWD = "lapas"
    DB = "Palas_V5"

    def __init__(self):
        self.db = MySQLdb.Connect(
            host=MySQLUpdater.HOST,
            user=MySQLUpdater.USER,
            passwd=MySQLUpdater.PASSWD,
            db=MySQLUpdater.DB,
        )
        self.db.query('SET NAMES utf8')
        self.cursor = self.db.cursor()
        self.counter = 0

    def get_formated_time(self):
        struct_time = time.localtime()
        year = struct_time.tm_year
        month = struct_time.tm_mon
        day = struct_time.tm_mday
        hour = struct_time.tm_hour
        min = struct_time.tm_min
        sec = struct_time.tm_sec
        formated_time = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(min) + ":" + str(sec)
        return formated_time, int(time.time())

    def query(self, topic_title_and_kw):
        topic_title_and_kw[1] = topic_title_and_kw[1].replace(" ", "+")
        topic_title_and_kw[0] = topic_title_and_kw[0].strip("!!!")
        formated_time, time_stamp = self.get_formated_time()
        id = self.counter + time_stamp
        sql = r"INSERT INTO HeatTopic (HeatTopicID, HeatTopicName, IssueID, QueryRule, CreateTime) VALUES ('%s', '%s', '%s', '%s', '%s')" % (id, topic_title_and_kw[0], "Reader", topic_title_and_kw[1], formated_time)
        sql = sql.encode('utf8')
        self.cursor.execute(sql)
        self.db.commit()
        self.counter += 1

    def clean_up(self):
        self.db.close()



