from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

#while True:
process = CrawlerProcess(get_project_settings())

process.crawl("pvp")
process.start()
