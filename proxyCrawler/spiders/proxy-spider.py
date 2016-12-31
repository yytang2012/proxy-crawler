# -*- coding: utf-8 -*-
import os

import scrapy
from scrapy import Selector
from scrapy.conf import settings

from proxyCrawler.libs.misc import save_to_json


class ProxySpider(scrapy.Spider):
    name = "proxy-spider"
    start_urls = [
        'https://incloak.com/proxy-list/?type=h#list',
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root_dir = os.path.expanduser(settings['ROOT_DIR'])
        self.proxy_file = os.path.join(root_dir, settings['PROXY_FILE'])

    def parse(self, response):
        sel = Selector(response)
        proxy_info_selector = sel.xpath('//tbody/tr/td[@class="tdl"]/..')
        proxy_info_list = [item.xpath('td/text()').extract() for item in proxy_info_selector]
        save_to_json(proxy_info_list, self.proxy_file)