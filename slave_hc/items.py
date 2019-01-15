# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class HcItemItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = Field()
    name = Field()
    contacts = Field()
    # tel = Field()
    tel1 = Field()
    tel2 = Field()
    tag = Field()
    city = Field()

# class HcItem(Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     link = Field()
#     name = Field()
#     contacts = Field()
#     tel = Field()
#     Fixed_tel = Field()
#     city = Field()

