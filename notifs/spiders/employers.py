#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from slugify import slugify
from notifs.items import Employer
from scrapy.loader import ItemLoader


class EmployersSpider(scrapy.Spider):
    name = 'employers'
    start_urls = ['http://www.njoftime.com/forumdisplay.php?14-ofroj-vende-pune']

    def parse(self, response):
        for notif in response.css('.inner > h3'):
            url = notif.xpath('a/@href').get()

            yield scrapy.Request("http://www.njoftime.com/" + url, self.parse_url_employer)

        for next_page in response.css('.prev_next > a'):
            yield response.follow(next_page, self.parse)

    def parse_url_employer(self, response):
        employer = response.css('.username')
        employer_url = "http://njoftime.com/" + employer.xpath('@href').get().strip()
        name = response.css('.username > strong ::text').get().strip()

        yield scrapy.Request(employer_url, self.parse_employer, meta={'name':name})

    def parse_employer(self, response):
        employer = ItemLoader(item=Employer(), response=response)

        details = response.css('#view-aboutme > div:nth-child(2) > div')
        image = 'http://njoftime.com/' + response.css('.avatarcontainer > img::attr(src)').extract_first().strip()
        dls = {}
        employer_details = {}

        for detail in details.css('dl'):
            key = detail.css('dt').extract_first().strip().replace('<dt>','').replace('</dt>','')
            dls[key] = detail.css('dd').extract_first().strip().replace('<dd>','').replace('</dd>','')

        employer_details['name'] = response.meta.get('name').replace("'",'').replace('"',"")
        employer_details['slug'] = slugify(response.meta.get('name').replace("'",'').replace('"',""))

        if 'Qyteti:' in dls.keys():
            employer_details['city'] = dls['Qyteti:']
        else:
            employer_details['city'] = ''

        if 'Shteti:' in dls.keys():
            employer_details['country'] = dls['Shteti:']
        else:
            employer_details['country'] = ''

        if 'Adresa:' in dls.keys():
            employer_details['address'] = dls['Adresa:'].replace("'",'').replace('"',"")
        else:
            employer_details['address'] = ''

        if 'Telefon:' in dls.keys():
            employer_details['phone'] = dls['Telefon:']
        else:
            employer_details['phone'] = ''

        if 'Fax:' in dls.keys():
            employer_details['fax'] = dls['Fax:']
        else:
            employer_details['fax'] = ''

        if 'Celular/Mobil:' in dls.keys():
            employer_details['mobile_phone'] = dls['Celular/Mobil:']
        else:
            employer_details['mobile_phone'] = ''

        if 'Rubrika/fusha e aktivitetit:' in dls.keys():
            employer_details['category'] = dls['Rubrika/fusha e aktivitetit:']
        else:
            employer_details['category'] = ''

        employer.add_value('name', employer_details['name'])
        employer.add_value('slug', employer_details['slug'])
        employer.add_value('city', employer_details['city'])
        employer.add_value('country', employer_details['country'])
        employer.add_value('address', employer_details['address'])
        employer.add_value('phone', employer_details['phone'])
        employer.add_value('mobile_phone', employer_details['mobile_phone'])
        employer.add_value('fax', employer_details['fax'])
        employer.add_value('category', employer_details['category'])
        employer.add_value('image', image)

        yield employer.load_item()
