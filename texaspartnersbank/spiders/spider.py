import scrapy

from scrapy.loader import ItemLoader

from ..items import TexaspartnersbankItem
from itemloaders.processors import TakeFirst


class TexaspartnersbankSpider(scrapy.Spider):
	name = 'texaspartnersbank'
	start_urls = ['https://www.thebankofaustin.com/news/',
	              'https://www.thebankofsa.com/blog/',
	              ]

	def parse(self, response):
		post_links = response.xpath('//a[@class="btn btn-blue"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[text()="Next >"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="main-content"]//text()[normalize-space() and not(ancestor::h1 | ancestor::h6 | ancestor::a)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@id="info"]/h6/text()').get()

		item = ItemLoader(item=TexaspartnersbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
