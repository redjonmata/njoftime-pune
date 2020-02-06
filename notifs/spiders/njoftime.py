#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from slugify import slugify
from datetime import date
from datetime import datetime
from notifs.items import Njoftime
from scrapy.loader import ItemLoader
import html


class NjoftimeSpider(scrapy.Spider):
    name = 'notifs'
    start_urls = ['http://www.njoftime.com/forumdisplay.php?14-ofroj-vende-pune']

    def parse(self, response):
        notif = ItemLoader(item=Njoftime(), response=response)
        for notif in response.css('.inner > h3'):
            url = notif.xpath('a/@href').get()

            yield scrapy.Request("http://www.njoftime.com/" + url, self.parse_notification)

        for next_page in response.css('.prev_next > a'):
            yield response.follow(next_page, self.parse)

    def parse_notification(self, response):
        notif = ItemLoader(item=Njoftime(), response=response)

        html_date = response.css('.date')
        job_date = html_date.css('span ::text').get().strip().replace(',','')
        job_date_arr = job_date.split('.')
        job_date = '-'.join([job_date_arr[2], job_date_arr[1], job_date_arr[0]])
        job_time = " " + html_date.css('span > span ::text').get().strip() + ":00"

        employer = slugify(response.css('.username > strong ::text').get().strip())

        title = response.css('head > title ::text').get().strip()
        slug = slugify(title)

        today = date.today().strftime("%Y-%m-%d")
        now = datetime.now().strftime("%H:%M:%S")
        description = html.escape(response.css('.postcontent').get().strip())

        # yield {
        #     'url': response.url,
        #     'employer' : employer,
        #     'title': title,
        #     'slug': slug,
        #     'job_date': job_date + job_time,
        #     'created_at': today + " " + now,
        #     'description': description
        # }

        notif.add_value('title',title)
        notif.add_value('slug',slug)
        notif.add_value('description',description)
        notif.add_value('employer',employer)
        notif.add_value('url',response.url)
        notif.add_value('job_date',job_date + job_time)
        notif.add_value('created_at',today + " " + now)

        yield notif.load_item()
