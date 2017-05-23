# -*- coding: utf-8 -*-
import scrapy
from jianshu.items import JianshuItem
# from scrapy.http import Request, FormRequest


class Jianshu(scrapy.Spider):
    name='jianshu'   # 运行时这个爬虫的名字
    allowed_domains = ["jianshu.com"]
    # url = 'http://www.jianshu.com'
    start_urls = [
    	'http://www.jianshu.com'
    ]

    #重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
    def start_requests(self):
    	print 'start_requests:'
    	re = scrapy.Request("http://www.jianshu.com",
    		headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'},
    		)
    	yield re


    def parse(self, response):
    	item = JianshuItem()
    	# print 'responseInfo:'+response.body
        selector = scrapy.Selector(response)
        articles = selector.xpath('//ul[@class="note-list"]')
        # print 'selector:'+str(selector)
        print 'articles.count:'+str(len(articles))
        for article in articles:
        	# print 'article:'+str(article)
        	titles = article.xpath('//a[@class="title"]/text()').extract()
        	print 'titles.count:'+str(len(titles))
        	for  title in titles:
        		# title = title.xpath('///div/a/text()').extract()	
	       		print 'title:'+title
	       		item['title'] = title
        		yield item
		next_link = selector.xpath('//a[@class="load-more"]').extract()
	print 'next_link:'+str(len(next_link))


        if len(next_link)==1 :

            next_link = self.url+ str(next_link[0])
            print "----"+next_link
            yield Request(next_link,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'},callback=self.parse)

		