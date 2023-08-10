import scrapy
import logging
# from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
class CountriesSpider(scrapy.Spider):
    name = "countries"
    # Never ever put the http protocol here, it won't work.
    allowed_domains = ["www.worldometers.info"]
    # Links to scrape, scrapy by default uses http.
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    # Parse the response we get back from the spider.
    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries:
            # Whenever executing a xpath against selector, always start with .//
            name = country.xpath(".//text()").get() # .get() returns the data
            link = country.xpath(".//@href").get() # .get() returns the data

            # absolute_url = f"https://www.worldometers.info{link}"
            absolute_url = response.urljoin(link)

            # When scrapy sends a request to each country link, callback will send response to the country method  
            # meta 
            yield response.follow(url=absolute_url, callback=self.parse_country, meta={'country_name':name})

    def parse_country(self,response):
        # open_in_browser(response)
        # # logging.info(response.url)
        name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            # row is of selector type.
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath("td[2]/strong/text()").get()
            yield{
                'country_name':name,
                'year':year,
                'population':population
            }