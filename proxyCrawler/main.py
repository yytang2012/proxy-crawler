from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    crawler_process = CrawlerProcess(get_project_settings())
    crawler_process.crawl('proxy-spider')
    crawler_process.start()
    pass

if __name__ == '__main__':
    main()