# -*- coding: utf-8 -*-
import os
import scrapy

class PItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()


class MeizituSpider(scrapy.Spider):
    name = "meizitu"
    allowed_domains = ["meizitu.com"]
    start_urls = ( 'http://www.meizitu.com/a/list_1_1.html',)

    def parse(self, response):
        exp = u'//div[@id="wp_page_numbers"]//a[text()="下一页"]/@href'
        _next = response.xpath(exp).extract_first()
        next_page = os.path.join(os.path.dirname(response.url), _next)
        yield scrapy.FormRequest(next_page, callback=self.parse)
        for p in response.xpath('//li[@class="wp-item"]//a/@href').extract():
            yield scrapy.FormRequest(p, callback=self.parse_item)

    def parse_item(self, response):
        item=PItem()
        urls = response.xpath("//div[@id='picture']//img/@src").extract()
        item['image_urls'] = urls 
        return item

