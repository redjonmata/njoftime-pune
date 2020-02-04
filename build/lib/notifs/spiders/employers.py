#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
# from scrapy.loader import ItemLoader
# from njoftime.items import Njoftime
from slugify import slugify


class EmployersSpider(scrapy.Spider):
    name = 'employer'
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
        details = response.css('#view-aboutme > div:nth-child(2) > div')
        image = 'http://njoftime.com/' + response.css('.avatarcontainer > img::attr(src)').extract_first().strip()
        dls = {}
        employer_details = {}

        for detail in details.css('dl'):
            key = detail.css('dt').extract_first().strip().replace('<dt>','').replace('</dt>','')
            dls[key] = detail.css('dd').extract_first().strip().replace('<dd>','').replace('</dd>','')

        employer_details['name'] = response.meta.get('name')
        employer_details['slug'] = slugify(response.meta.get('name'))

        if 'Qyteti:' in dls.keys():
            employer_details['city'] = dls['Qyteti:']
        else:
            employer_details['city'] = ''

        if 'Shteti:' in dls.keys():
            employer_details['country'] = dls['Shteti:']
        else:
            employer_details['country'] = ''

        if 'Adresa:' in dls.keys():
            employer_details['address'] = dls['Adresa:']
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
            employer_details['field'] = dls['Rubrika/fusha e aktivitetit:']
        else:
            employer_details['field'] = ''

        if 'Specifikat/Specializimi:' in dls.keys():
            employer_details['specialized_field'] = dls['Specifikat/Specializimi:']
        else:
            employer_details['specialized_field'] = ''

        yield {
            'name': employer_details['name'],
            'slug': employer_details['slug'],
            'city': employer_details['city'],
            'country': employer_details['country'],
            'address': employer_details['address'],
            'phone': employer_details['phone'],
            'fax': employer_details['fax'],
            'mobile_phone': employer_details['mobile_phone'],
            'field': employer_details['field'],
            'specialized_field': employer_details['specialized_field'],
            'image': image
        }