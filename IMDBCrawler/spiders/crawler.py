#!/usr/bin/python
#coding:utf-8
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from IMDBCrawler.items import IMDBMovie

class IMDB(CrawlSpider):
    name = 'imdb'
    start_urls= ['http://www.imdb.com/search/title?genres=action&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2406822102&pf_rd_r=03AT236NWM2BVKCCSBPD&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_2']

    def parse(self, response):
        item=IMDBMovie()
        selector=Selector(response)
        Movies=selector.xpath('//div[@class="lister-item mode-advanced"]')
        for eachMovie in Movies:
            title=eachMovie.xpath('div[@class="lister-item-content"]/h3[@class="lister-item-header"]/a/text()').extract()
            movieInfo=eachMovie.xpath('div[@class="lister-item-content"]/p[@class="text-muted"]/text()').extract()
            year=eachMovie.xpath('div[@class="lister-item-content"]/h3[@class="lister-item-header"]/span[@class="lister-item-year text-muted unbold"]/text()').extract()
            ranking=eachMovie.xpath('div[@class="lister-item-content"]/div[@class="ratings-bar"]/div[@class="inline-block ratings-imdb-rating"]/strong/text()').extract()

            item['title']=title
            item['movieInfo']=movieInfo
            item['year']=year
            item['ranking']=ranking

            yield item

        nextLink=selector.xpath('//a[@class="lister-page-next next-page"]/@href').extract()
        if nextLink:
            nextLink='http://www.imdb.com/search/title?count=100&genres=action,comedy&num_votes=10000,&title'+nextLink[0]
            yield  Request(nextLink)



