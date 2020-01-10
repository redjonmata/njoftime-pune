#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
# from scrapy.loader import ItemLoader
# from njoftime.items import Njoftime


class NjoftimeSpider(scrapy.Spider):
    name = 'notifs'
    start_urls = ['http://www.njoftime.com/forumdisplay.php?14-ofroj-vende-pune']

    def parse(self, response):
        # for title in response.css('.inner > h3'):
        #     yield {
        #         'title': title.css('a ::text').get(),
        #         'date': title.xpath('dl/dd[2]/text()').get().replace(', ', '') + " " + title.xpath('dl/dd[2]/span/text()').get()
        #     }

        for notif in response.css('.inner > h3'):
            url = notif.xpath('a/@href').get()

            yield scrapy.Request("http://www.njoftime.com/" + url, self.parse_notification)

        for next_page in response.css('.prev_next > a'):
            yield response.follow(next_page, self.parse)

    def parse_notification(self, response):
        date = response.css('.date')
        datetime = date.css('span ::text').get().strip().replace(',','') + " " + date.css('span > span ::text').get().strip()
        employer = response.css('.username > strong ::text').get().strip()
        title = response.css('head > title ::text').get().strip()
        description = response.css('.postcontent').get().strip()

        yield {
            'url': response.url,
            'time': datetime,
            'employer' : employer,
            'title': title,
            'description': description
        }
        # notification = ItemLoader(item=Njoftime(), response=response)
        #
        # for title in response.css('.inner > h3'):
        #     yield {'title': title.css('a ::text').get(), 'date': title.xpath('dl/dd[2]/text()').get().replace(', ','')
        #            + " " + title.xpath('dl/dd[2]/span/text()').get()}
        #
        # notification.add_value('url', response.url)
        # notification.add_value('title', title.css('a ::text').get())
        # notification.add_value('date', title.xpath('dl/dd[2]/text()').get().replace(', ', ''))
        # notification.add_value('description', title.css('a ::text').get())
        # notification.add_value('employer', title.css('a ::text').get())
        # notification.add_value('employer_image', title.css('a ::text').get())
        # notification.add_value('employer_contact', title.css('a ::text').get())
        #
        # yield notification
