# -*- coding:utf-8 -*-
# ☯ Author: Jingyq
# ☯ Email: woshijingyongqiang@163.com
# ☯ Date: 2023/8/21 15:21
# ☯ Notes:

import pymongo


class CreateConnect(object):

    def __init__(self, collection_name):
        # 创建一个mongo客户端
        self.mongo_client = pymongo.MongoClient(f'mongodb://root:GAOhuang2023@152.136.126.114:17000/',
        serverSelectionTimeoutMS=5000,
        socketTimeoutMS=5000)

        self.db = self.mongo_client["job_leap"]
        self.collection = self.db[collection_name]

    def mongo_db_find_one(self, data):

        ret =self.collection.find_one(data)
        return ret

    def mongo_db_insert_one(self, data):

        ret = self.collection.insert_one(data)
        return ret

    def mongo_db_update_one(self, data_index, data):
        ret = self.collection.replace_one(data_index, data)
        return ret

    def close_connect(self):
        self.mongo_client.close()
