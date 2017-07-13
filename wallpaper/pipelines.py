# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class WallpaperPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img_url in item['image_urls']:
            yield Request(img_url, meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        album_name = item['name']
        image_guid = request.url.split('/')[-1]
        return 'full/%s/%s' % (album_name, image_guid)

