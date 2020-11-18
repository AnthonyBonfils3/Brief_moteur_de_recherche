# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import logging
import pymongo
from Bot_Scrap_Offre.items import BotScrapOffreItem

class BotScrapOffrePipeline(object):

    collection_name = 'offres'

    def __init__(self, mongo_db):
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
    	## pull the information for settings.py
    	return cls(
    	    mongo_db = crawler.settings.get('MONGO_DATABASE')
            )   

    def open_spider(self, spider):
        ## intitializing spider opening db connection
        self.client = pymongo.MongoClient()
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()


    def process_item(self, item, spider):
        ## how to handle each post
        self.db[self.collection_name].find_one_and_update(
            {"guid": item["guid"]},
            {"$set": dict(item)},           
            upsert=True
        )
        logging.debug ("Post added to MongoDB")
        return item
