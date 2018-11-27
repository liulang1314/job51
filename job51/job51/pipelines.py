# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql
from scrapy.exceptions import DropItem
class Job51Pipeline(object):
    def open_spider(self, spider):
        self.file = open('qiancheng.json', 'a')

    def process_item(self, item, spider):
        # 数据处理的主要方法，在这里定义了对数据的主要操作
        # 将item强制转化为字典
        dict_data = dict(item)
        # 将字典转化为json字符串cii=False) + ',\n'
        #         # 写入文件
        str_data = json.dumps(dict_data, ensure_ascii=False) + ',\n'
        self.file.write(str_data)
        return item

    # 在停止爬虫时清理
    def close_spider(self, spider):
        self.file.close()

class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['jobname'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['jobname'])  ##这里换成你自己的item["#"]
            return item

class MysqlPipeline(object):
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password = crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into job51(%s) values (%s)' %(keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item



