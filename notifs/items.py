# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Njoftime(scrapy.Item):
    title = scrapy.Field()
    slug = scrapy.Field()
    description = scrapy.Field()
    employer = scrapy.Field()
    url = scrapy.Field()
    job_date = scrapy.Field()
    created_at = scrapy.Field()


class Employer(scrapy.Item):
    name = scrapy.Field()
    slug = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    mobile_phone = scrapy.Field()
    fax = scrapy.Field()
    category = scrapy.Field()
    image = scrapy.Field()
