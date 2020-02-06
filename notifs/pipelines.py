# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.utils.project import get_project_settings
from notifs.items import Notification
from notifs.items import Employer
from scrapy.exceptions import DropItem
from slugify import slugify
import string
import random


def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class NotificationsPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        host = settings.get('MYSQL_HOST')
        user = settings.get('MYSQL_USER')
        password = settings.get('MYSQL_PASS')
        db = settings.get('MYSQL_DB')

        self.connection = pymysql.connect(host, user, password, db)
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        if isinstance(item, Notification):
            return self.handle_notification(item, spider)
        if isinstance(item, Employer):
            return self.handle_employer(item, spider)

    def close_spider(self):
        self.cursor.close()
        self.connection.close()

    def handle_notification(self, item, spider):
        select_query = "SELECT id FROM employers WHERE slug = '" + item['employer'][0] + "'"
        rows_count = self.cursor.execute(select_query)

        if rows_count > 0:
            employer_id = self.cursor.fetchone()

            self.add_job_notification(employer_id[0], item)
        else:
            raise DropItem("Job notification has no employer")

    def handle_employer(self, item, spider):
        category_id = 1

        if item['category'][0] != '':
            select_query = "SELECT id FROM categories WHERE slug = '" + slugify(item['category'][0]) + "'"
            rows_count = self.cursor.execute(select_query)

            if rows_count > 0:
                category_id = self.cursor.fetchone()

                self.add_employer(category_id[0], item)
            else:
                self.cursor.execute("INSERT INTO categories (name, slug) VALUES ('%s', '%s')" % (item['category'][0], slugify(item['category'][0])))
                self.connection.commit()

                select_query = "SELECT id FROM categories WHERE slug = '" + slugify(item['category'][0]) + "'"
                self.cursor.execute(select_query)
                category_id = self.cursor.fetchone()

                self.add_employer(category_id[0], item)
        else:
            self.add_employer(category_id, item)

    def add_job_notification(self, employer_id, item):
        random_string = id_generator()

        query = """INSERT INTO notifications (title, slug, description, employer_id, url, job_date, created_at)
                    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
                % (item['title'][0], item['slug'][0] + "-" + random_string, item['description'][0], employer_id, item['url'][0],
                   item['job_date'][0], item['created_at'][0])
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except pymysql.IntegrityError:
            raise DropItem("Duplicate entry error for job %s" % item['title'][0])

    def add_employer(self, category_id, item):
        query = """INSERT INTO employers (name, slug, city, country, address, phone, mobile_phone, fax, category_id, image)
                                    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s')""" \
                % (item['name'][0], item['slug'][0], item['city'][0], item['country'][0], item['address'][0],
                   item['phone'][0], item['mobile_phone'][0], item['fax'][0], category_id, item['image'][0])
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except pymysql.IntegrityError:
            raise DropItem("Duplicate entry error for employer %s" % item['name'][0])
