import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sanpablo.spiders.spider import SanPablo

if __name__ == '__main__':
	process = CrawlerProcess(get_project_settings())

	process.crawl(SanPablo)
	process.start()