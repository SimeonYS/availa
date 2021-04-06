import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import AavailaItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class AavailaSpider(scrapy.Spider):
	name = 'availa'
	start_urls = ['https://www.availa.bank/about/news/archive/']

	def parse(self, response):
		post_links = response.xpath('//ul[@class="results-list news-list"]/li/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//p[@class="date-line"]//text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="gen-content"]//text()[not (ancestor::p[@class="date-line"])]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=AavailaItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
