import scrapy
from scrapy_splash import SplashRequest

class QuotesSpiderSpider(scrapy.Spider):
    name = "quotes_spider"
    allowed_domains = ["quotes.toscrape.com"]
    # start_urls = ["https://www.quotes.toscrape.com/js/"]

    script='''
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(0.5))
        return splash:html()
    end
    '''        

    def start_requests(self):
        yield SplashRequest("http://quotes.toscrape.com/", callback=self.parse, endpoint="execute", args={'lua_source':self.script})

    def parse(self, response):
        for singleQuote in response.xpath("//div[@class='quote']"):
            yield{
                'quote': singleQuote.xpath('.//span[@class="text"]/text()').get(),
                'author': singleQuote.xpath(".//small[@class='author']/text()").get(),
                'tags': singleQuote.xpath(".//div[@class='tags']/a/text()").getall()
            }
        next = response.xpath("//li[@class='next']/a/@href").get()
        if next:
            absolute_url=f"http://quotes.toscrape.com/js{next}"
            yield SplashRequest(url=absolute_url, callback=self.parse, endpoint="execute", args={
                'lua_source':self.script
            })
