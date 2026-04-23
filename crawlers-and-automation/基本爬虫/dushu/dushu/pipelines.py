# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import urllib.request


class DushuPipeline:
    def open_spider(self, spider):
        self.f = open('dushu.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        self.f.write(str(item))
        return item

    def close_spider(self, spider):
        self.f.close()


from scrapy.utils.project import get_project_settings


class MySqlPipeline:
    def open_spider(self, spider):
        settings = get_project_settings()

        self.host = settings['DB_HOST']
        self.port = settings['DB_PORT']
        self.user = settings['DB_USER']
        self.password = settings['DB_PASSWORD']
        self.name = settings['DB_NAME']
        self.charset = settings['DB_CHARSET']

        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                    database=self.name,
                                    charset=self.charset)
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        sql='insert into book(name,src) values ("{}","{}")'.format(item['name'],item['src'])
        self.cur.execute(sql)
        self.conn.commit()
        return item

    def close(self):
        self.cur.close()
        self.conn.close()