import scrapy

class DmozSpider(scrapy.Spider):  
    name = "dmoz"  
    # allowed_domains = ["javachen.com"]  
    # start_urls = [  
    #     "http://blog.javachen.com/2014/06/08/using-scrapy-to-cralw-zhihu.html"
    # ]  
    
    def start_requests(self):
    	# re = super(DmozSpider,self).start_requests()
    	re = scrapy.Request("http://www.jianshu.com",
    		headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'},
    		)
    		# cookies={'signin_redirect':'http%3A%2F%2Fwww.jianshu.com%2F',
      #                 'path': '/',
      #                '_session_id':'cGFXV2s0dFE0WkxOSEsvVnhZU0ZvWDRUZjdZNzV4UldzTW4veXd6L1Q3eG1XOUxMMHVrWEVrMkNyVWJjTDZSN3JWK3ZQdldrOXQwNFRINnVpREJ3Z1ZDaEk0ejRsK2luaDdzTFlOM1VZWS9JYXNvZ1J5YVJUQW5HdnhaUW1qK2NHb2dCNTVSK0xDMFVxY0xQM0tpb2I5TXdlZGdhMjRSOHNvOFZvNWR4dkRya2ZNT1pwQTZPenJnV3FTVW9qTUZNU3JCWFZmZnFpdFcyd2JTR25yOVBpQktBSzBVZFZWN2lLSWxoa3JDSkZDKzVpNGk0MSszSEtLT1pMYXZwa1kwNS0tcG1SY003b05zVXNFa3M5REtQRms1QT09--3faf168b2bda1f46a2b189a3fab9a13fd65c0552',
      #                 'path': '/'
      #                 })
    	# re.setCookies = {
    	# 		's':'dd',
    	# }
    	print 'requestInfo:'+str(re.headers)
    	yield re

    def parse(self, response):  
    	print 'response success:'
        # filename = response.url.split("/")[-2]  
        # open(filename, 'wb').write(response.body)  