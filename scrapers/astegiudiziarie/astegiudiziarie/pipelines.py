# Define your item pi
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from itemadapter import ItemAdapter
from itemadapter import ItemAdapter
import pymongo
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
import gridfs
from pymongo.errors import WriteError

class AstegiudiziariePipeline:
    def process_item(self, item, spider):
        return item
class MongoDBPipeline(object):

    def __init__(self,MONGODB_uri,MONGODB_DB):
        self.MONGODB_uri = "mongodb://Tuasta:Aurnowac9737%23@116.203.206.106:27017/admin"
        # self.MONGODB_PORT = MONGODB_PORT
        self.MONGODB_DB = "data"
        connection = pymongo.MongoClient(
           self.MONGODB_uri
           
        )
        self.db = connection[self.MONGODB_DB]
       
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            #MONGODB_uri=crawler.settings.get('MONGODB_uri'),
            MONGODB_uri="mongodb://Tuasta:Aurnowac9737%23@116.203.206.106:27017/admin",
            #
            #MONGODB_PORT=crawler.settings.get('MONGODB_PORT'),
            #MONGODB_DB=crawler.settings.get('MONGODB_DB'),
            MONGODB_DB="data",
           
        )
    def process_item(self, item, spider):

        collection = self.db[spider.name]
        # Remove any existing documents with the same 'numero_inserzione'
        collection.delete_many({'numero_inserzione': item['numero_inserzione']})
        
        # Insert the new item
        #item['numero_inserzione'] = int(item['numero_inserzione'])
        collection.insert_one(dict(item))
