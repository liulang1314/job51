# -*- coding: utf-8 -*-
import scrapy
from job51.items import Job51Item
import time
class Job51spiderSpider(scrapy.Spider):
    name = 'job51spider'
    allowed_domains = ['www.51job.com']
    start_urls = ['http://search.51job.com/']
    #start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,%2B,2,3.html?lang=c&amp;stype=1&amp;postchannel=0000&amp;workyear=99&amp;cotype=99&amp;degreefrom=99&amp;jobterm=99&amp;companysize=99&amp;lonlat=0%2C0&amp;radius=-1&amp;ord_field=0&amp;confirmdate=9&amp;fromType=&amp;dibiaoid=0&amp;address=&amp;line=&amp;specialarea=00&amp;from=&amp;welfare=']
    page = 0
    headers = {}

    def parse(self, response):
        nodes = response.xpath('//div[@class="dw_table"]/div[@class="el"]')
        for node in nodes:
            item = Job51Item()
            jobname = node.xpath('./p//a/@title').extract_first()
            company = node.xpath('./span[@class="t2"]/a/text()').extract_first()
            location = node.xpath('./span[@class="t3"]/text()').extract_first()
            salary = node.xpath('./span[@class="t4"]/text()').extract_first()

            item['jobname'] = jobname
            item['company'] = company
            item['location'] = location
            item['salary'] = salary
            yield item

        next_url = response.xpath('//li[@class="bk"]/a/@href').extract()
        self.page += 1
        print("51job page:" + str(self.page))
        time.sleep(3)
        if next_url:
            url = response.urljoin(next_url[-1])
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
        else:
            print("退出")

