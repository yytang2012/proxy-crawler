# -*- coding: utf-8 -*-
import os

import scrapy
from scrapy import Selector
from scrapy.conf import settings

from proxyCrawler.libs.misc import *


class ProxySpider(scrapy.Spider):
    name = "proxy-spider"
    start_urls = [
        'https://incloak.com/proxy-list/?type=h#list',
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root_dir = os.path.expanduser(settings['ROOT_DIR'])
        self.proxy_file = os.path.join(root_dir, settings['PROXY_FILE'])

    def parse(self, response):
        start_page = False if 'flag' in response.meta else True
        sel = Selector(response)
        proxy_info_selector = sel.xpath('//tbody/tr/td[@class="tdl"]/..')
        new_proxy_info_list = [item.xpath('td/text()').extract() for item in proxy_info_selector]
        if start_page:
            proxy_info_list = []
        else:
            proxy_info_list = load_from_json(self.proxy_file)
        proxy_info_list += new_proxy_info_list
        save_to_json(proxy_info_list, self.proxy_file)

        next_page_selector = sel.xpath('//ul/li[@class="arrow__right"]/a/@href').extract()
        if len(next_page_selector) != 0:
            next_page_url = sel.xpath('//ul/li[@class="arrow__right"]/a/@href').extract()[0]
            request = scrapy.Request(response.urljoin(next_page_url), callback=self.parse)
            request.meta['flag'] = True
            yield request
        else:
            print("This is the last page")

