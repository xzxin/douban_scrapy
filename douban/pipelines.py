# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import random
from scrapy.http import Request
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
reload(sys)
sys.setdefaultencoding('utf8')

class DoubanPipeline(ImagesPipeline):

    def get_media_requests(self,item,info):
        for image_url in item['image_urls']:
            yield Request(url=image_url ,meta={'item':item})

    def file_path(self,request,response=None,info=None):
        item=request.meta['item'] #通过上面的meta传递过来item +str(random.random())
        #图片文件名，item['carname'][index]得到汽车名称，request.url.split('/')[-1].split('.')[-1]得到图片后缀jpg,png
        image_guid = item['title']+'_'+item['star']+'.'+request.url.split('/')[-1].split('.')[-1]
        #图片下载目录 此处item['country']即需要前面item['country']=''.join()......,否则目录名会变成\u97e9\u56fd\u6c7d\u8f66\u6807\u5fd7\xxx.jpg
        filename = u'full/{0}'.format(image_guid)
        return filename

    def item_completed(self,results,item,info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item


class SaveNameScore(object):
    def __init__(self):
        self.file= open('douban_top250.txt',mode='wb')


    def process_item(self, item, spider):
        line = 'The top250 movie list:'
        title = item['title']
        star = item['star']
        line = line + ' ' + title +' '
        line = line + star + '\n'
        self.file.write(line)

    def close_spider(self, spider):
        self.file.close()