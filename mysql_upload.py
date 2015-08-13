# -*- coding: utf-8 -*-

import MySQLdb
import MySQLdb.cursors
import codecs
import time
import random

query_term_file = u"upload_to_db.txt"
with codecs.open(query_term_file, "r", encoding="utf8") as f:
    query_terms = f.readlines()

query_terms_buffer = list()
for item in query_terms:
    buffer = item.split("\t")
    query_terms_buffer.append(buffer)
query_terms = query_terms_buffer

db = MySQLdb.Connect(
            host="180.153.177.252",
            user="palas",
            passwd="lapas",
            db="Palas_V5",
        )

db.query('SET NAMES utf8')
cursor = db.cursor()
for i in range(len(query_terms)):
    sql = r"INSERT INTO HeatTopic (HeatTopicID, HeatTopicName, IssueID, QueryRule, CreateTime) VALUES ('%s', '%s', '%s', '%s', '%s')" % (i*123+random.randint(30000, 50000), query_terms[i][0], "Reader", query_terms[i][1], "2015-8-10 15:00:00")
    sql = sql.encode('utf8')
    cursor.execute(sql)
    db.commit()
db.close()