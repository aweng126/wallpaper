# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from wallpaper.items import WallpaperItem

class ZolpaperSpider(scrapy.Spider):
    name = 'zolpaper'
    # allowed_domains = ['www.zol.com.cn']
    # zol_start_url='http://desk.zol.com.cn/meinv/'

    num=0
    zol_kind_hot_url='http://desk.zol.com.cn/{kind}/hot_1.html'
    album_list={'dongman','mingxing','chuangyi',  'jianzhu', 'jingwu', 'dongwu', 'tiyu','pinpai','meishi','qita'}

    def start_requests(self):
        for kind in self.album_list:
            yield Request(self.zol_kind_hot_url.format(kind=kind), self.parse_zol_page)

    def parse_zol_page(self, response):
        album_list_url = response.css('.top-main .main ul .photo-list-padding a::attr(href)').extract()
        for album_per_url in album_list_url:
            yield Request('http://desk.zol.com.cn'+album_per_url,self.parse_per_pic)

        next_page_url = response.css('.top-main .main .pagecon .page a[id=pageNext]::attr(href)').extract_first()
        print('next_page_url', next_page_url)
        if next_page_url and self.num < 4:
            self.num += 1
            yield Request('http://desk.zol.com.cn' + next_page_url, self.parse_zol_page)

    def parse_per_pic(self, response):
        item = WallpaperItem()
        pic_urls = response.css('.wrapper .photo div  img[id=bigImg]::attr(src)').extract()
        pic_name=response.css('.photo-tit h3 a::text').extract_first()
        for href in response.css('.photo-set .photo-set-list .photo-list-box .clearfix li a::attr(href)').extract():
            yield Request('http://desk.zol.com.cn'+ href,self.parse_per_pic)
        item['image_urls'] = pic_urls
        item['name'] = pic_name
        yield item
