# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import time
import calendar
from datetime import datetime, date
from scrapy.exporters import CsvItemExporter

def getFecha():
	#Traemos la fecha
		x = datetime.now()
		dia = str(x.strftime("%d"))
		mes = str(x.strftime("%m"))
		anio = str(x.year)
		hora = str(x.strftime("%H"))
		date = dia + '-' + mes + '-' + anio
		
		return date

class SanpabloPipeline(object):

	def __init__(self):
		date = getFecha()
		fileName = "sanpablo-" + date + ".csv"
		
		self.file = open(fileName, 'wb')
		self.exporter = CsvItemExporter(self.file, str)
		self.exporter.fields_to_export = ["nombre", "original", "descuento", "fabricante", "categoria", "envio", "url", "fecha"]
		self.exporter.start_exporting()

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.file.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item
