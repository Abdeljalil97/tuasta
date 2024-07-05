# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
import gridfs
from pymongo.errors import WriteError

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
            MONGODB_uri="mongodb://Tuasta:Aurnowac9737%23@116.203.206.106:27017/admin",
            #MONGODB_PORT=crawler.settings.get('MONGODB_PORT'),
            MONGODB_DB="data",
           
        )
    def process_item(self, item, spider):
        collection = self.db[spider.name]
        if collection.find_one({'numero_inserzione': item['numero_inserzione']}) is None:
            collection.insert_one(dict(item))
        else :
            print(f"product with numero_inserzione: {item['numero_inserzione']} exist .")
            filter = { 'numero_inserzione': item['numero_inserzione'] }
            newvalues = { "$set": dict(item) }
            try:
                collection.update_one(filter,newvalues)
            except WriteError as e :
                print(f"error : {e}")
                pass
        valid = True
        # for data in item:
        #     if not data:
        #         valid = False
        #         raise DropItem("Missing {0}!".format(data))
        # if valid:
        #     collection.insert_one(dict(item))
        #     for file in item['files']:
        #         #Open the image in read-only format.
        #         fs = gridfs.GridFS(self.db)
        #         with open(f"files/{file['path']}", 'rb') as f:
        #             contents = f.read()

        #         #Now store/put the image via GridFs object.
        #         name_file = file['path'].split('/')[len(file['path'].split('/'))-1]
        #         fs.put(contents, filename=name_file)
            
        return item

class MongoFiles(FilesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        
        # media_guid = request.url.split('/')[len(request.url.split('/'))-2]+request.url.split('/')[len(request.url.split('/'))-1]
        
        # if "pdf" in media_guid:
        #     return f"full/{media_guid.replace('.pdf','_')}.pdf"
        # if "jpg" in media_guid:
        #     return f"full/{media_guid.replace('.jpg','_')}.jpg"
        pass
    
