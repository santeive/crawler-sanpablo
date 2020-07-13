# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SanpabloItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nombre = scrapy.Field()
    original = scrapy.Field()
    descuento = scrapy.Field()
    categoria = scrapy.Field()
    fabricante = scrapy.Field()
    envio = scrapy.Field()
    url = scrapy.Field()
    fecha = scrapy.Field()
