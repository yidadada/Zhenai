# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class TruelovePipeline(object):
    def __init__(self):
        self.f = open ('zhenai.json','w')

    def process_item(self,item,spider):
        self.f.write(json.dumps(dict(item),ensure_ascii = False).encode('utf-8') + '\n')

    def close_spider(self,spider):
        self.f.close()

