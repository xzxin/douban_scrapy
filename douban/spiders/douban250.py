# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class Douban250Spider(scrapy.Spider):
    name = 'douban250'
    # allowed_domains = ['https://movie.douban.com/']
    start_urls = ['https://movie.douban.com/top250']




    def parse(self, response):
        for sel in response.xpath('//div[@class="item"]'):
            item = DoubanItem()
            item['title'] = sel.xpath('div[@class="info"]/div[@class="hd"]/a/span/text()').extract()[0]
            item['star'] = sel.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]\
            /span[@class="rating_num"]/text()').extract()[0]
            item['image_urls'] = sel.xpath('div[@class="pic"]/a/img/@src').extract()           # .extract()[0]
            # print star,title
            yield item
        nextPage = sel.xpath('//div[@class="paginator"]/\
                             span[@class="next"]/a/@href').extract()[0].strip()
        if nextPage:
            next_url = 'https://movie.douban.com/top250'+nextPage
            yield scrapy.http.Request(next_url,callback=self.parse,dont_filter=True)

