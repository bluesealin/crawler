from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule
from t66y.items import T66YItem
from blog.models import Blog
import re
from scrapy.utils.url import urljoin_rfc
import scrapy

class Fid7Spider(CrawlSpider):
    name = "fid7"
    allowed_domains = ["cl.zondem.com",]
    
    start_urls = [
        #"http://cl.clceo.xyz",
        #"http://cl.clceo.xyz/index.php",
	"http://cl.zondem.com/index.php",
        #"http://cl.clceo.xyz/thread0806.php?fid=7",
	"http://cl.zondem.com/thread0806.php?fid=7",
        #"http://cl.clceo.xyz/htm_data/7/1512/1766000.html",
    ] 
   
    custom_settings={
        "USER_AGENT":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.101 Chrome/45.0.2454.101 Safari/537.36",
    } 

    rules=(
        Rule(LinkExtractor(allow=r'http://cl\.ewcl\.me/thread0806\.php\?fid\=7$'),
            callback="parse_url",follow=True),
        Rule(LinkExtractor(allow=r'\&search\=\&page\=[1-5]$'),
             callback="parse_url",follow=True),
        
       
        
    )
    
   
   #********************************
    Blog.objects.all().delete()
   #********************************
    def parse_blog(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        #from scrapy.shell import inspect_response
       # inspect_response(response, self)
        #self.logger.info('Parse function called on %s', response.url)
        
        item = T66YItem()
        item['title'] = response.xpath('//h4/text()').extract()
        item['href']=[]
        item['href'].append(response.url)
        item['author'] =response.xpath('//th[@class="r_two"]/font/b/text()').extract()
        item['date_str'] =re.compile(r'Posted:(\d+-\d+-\d+ \d+:\d+)').findall(response.body) 
        item['commentnum'] =re.compile(r'page=(\d+)').findall( response.xpath('//a[@id="last"]/@href').extract()[0])
        item['content']=response.xpath('//div[@class="tpc_content do_not_catch"]').extract()
        yield item
        
    def parse_url(self,response):
        print 'ok!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1'
        print response.url
        requests=[]
        hrefs=response.xpath('//tr/td/h3/a/@href').extract()
        for href in hrefs:
            url='http://cl.zondem.com/'+href
            #print 'ok!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1'
            #print url
            yield scrapy.Request(url,callback=self.parse_blog)
        
        
        
        
        
