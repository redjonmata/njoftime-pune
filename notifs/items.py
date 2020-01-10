# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Njoftime(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    employer = scrapy.Field()
    employer_image = scrapy.Field()
    employer_contact = scrapy.Field()
    pass
