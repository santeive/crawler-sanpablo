import scrapy
from scrapy.linkextractors import LinkExtractor
import csv
import time
import calendar
from datetime import datetime, date
from ..items import SanpabloItem
from collections import defaultdict
from scrapy.crawler import CrawlerProcess

class SanPablo(scrapy.Spider):
	name = 'sanpablo'
	allowed_domains = ["www.farmaciasanpablo.com.mx"]

	#Corremos así
	#scrapy crawl sanpablo -o sanpablo.csv
	#Posteriormente correr celdas_vacias.py, para limpiar datos
	
	def start_requests(self):
		urls = [
		"https://www.farmaciasanpablo.com.mx/medicamentos/antimicoticos/Aerosoles0/c/060010001",
		"https://www.farmaciasanpablo.com.mx/medicamentos/antimicoticos/Cremas-antimicoticas0/c/060010002",
		"https://www.farmaciasanpablo.com.mx/medicamentos/antimicoticos/Geles0/c/060010003",
		"https://www.farmaciasanpablo.com.mx/medicamentos/antimicoticos/Polvos-y-talcos0/c/060010004",
		"https://www.farmaciasanpablo.com.mx/medicamentos/antimicoticos/Pomadas0/c/060010005",
		"https://www.farmaciasanpablo.com.mx/medicamentos/antimicoticos/Soluciones0/c/060010006",
		"https://www.farmaciasanpablo.com.mx/medicamentos/antimicoticos/Unguentos0/c/060010007",

		"https://www.farmaciasanpablo.com.mx/medicamentos/dermatologicos/Capilares0/c/060020001",
		"https://www.farmaciasanpablo.com.mx/medicamentos/dermatologicos/Cicatrizantes0/c/060020002",
		"https://www.farmaciasanpablo.com.mx/medicamentos/dermatologicos/Dermatitis0/c/060020003",
		"https://www.farmaciasanpablo.com.mx/medicamentos/dermatologicos/Gel-dermatologico0/c/060020004",
		"https://www.farmaciasanpablo.com.mx/medicamentos/dermatologicos/Jabones1/c/060020005",
		"https://www.farmaciasanpablo.com.mx/medicamentos/dermatologicos/Tratamientos-antiacne0/c/060020006",
		"https://www.farmaciasanpablo.com.mx/medicamentos/dermatologicos/Tratamientos-dermatologicos0/c/060020007",

		"https://www.farmaciasanpablo.com.mx/medicamentos/dolor/Analgesicos0/c/060030001",
		"https://www.farmaciasanpablo.com.mx/medicamentos/dolor/Analgesicos-Infantil0/c/060030002",
		"https://www.farmaciasanpablo.com.mx/medicamentos/dolor/Anestesicos0/c/060030003",
		"https://www.farmaciasanpablo.com.mx/medicamentos/dolor/Colicos0/c/060030004",
		"https://www.farmaciasanpablo.com.mx/medicamentos/dolor/Hemorroides0/c/060030005",
		"https://www.farmaciasanpablo.com.mx/medicamentos/dolor/Musculares-y-desinflamatorios0/c/060030006",

		"https://www.farmaciasanpablo.com.mx/medicamentos/especialidades-medicas/A-B0/c/060040001",
		"https://www.farmaciasanpablo.com.mx/medicamentos/especialidades-medicas/C-D0/c/060040002",
		"https://www.farmaciasanpablo.com.mx/medicamentos/especialidades-medicas/E-F0/c/060040003",
		"https://www.farmaciasanpablo.com.mx/medicamentos/especialidades-medicas/G-H0/c/060040004",
		"https://www.farmaciasanpablo.com.mx/medicamentos/especialidades-medicas/I-J0/c/060040005",
		"https://www.farmaciasanpablo.com.mx/medicamentos/especialidades-medicas/K-L0/c/060040006",
		"https://www.farmaciasanpablo.com.mx/medicamentos/especialidades-medicas/M-N0/c/060040007",
		"https://www.farmaciasanpablo.com.mx/medicamentos/especialidades-medicas/O-P0/c/060040008",
		"https://www.farmaciasanpablo.com.mx/medicamentos/especialidades-medicas/Q-R0/c/060040009",
		"https://www.farmaciasanpablo.com.mx/medicamentos/especialidades-medicas/S-T0/c/060040010",
		"https://www.farmaciasanpablo.com.mx/medicamentos/especialidades-medicas/U-V0/c/060040011",
		"https://www.farmaciasanpablo.com.mx/medicamentos/especialidades-medicas/X-Y-Z0/c/060040012",

		"https://www.farmaciasanpablo.com.mx/medicamentos/estomacal/Antiacidos0/c/060050001",
		"https://www.farmaciasanpablo.com.mx/medicamentos/estomacal/Antidiarreicos0/c/060050002",
		"https://www.farmaciasanpablo.com.mx/medicamentos/estomacal/Antiulcerosos0/c/060050003",
		"https://www.farmaciasanpablo.com.mx/medicamentos/estomacal/Digestivos0/c/060050004",
		"https://www.farmaciasanpablo.com.mx/medicamentos/estomacal/Dolor-y-malestar0/c/060050005",
		"https://www.farmaciasanpablo.com.mx/medicamentos/estomacal/Higiene-anal0/c/060050006",
		"https://www.farmaciasanpablo.com.mx/medicamentos/estomacal/Laxantes0/c/060050007",
		"https://www.farmaciasanpablo.com.mx/medicamentos/estomacal/Parasitos0/c/060050008",
		"https://www.farmaciasanpablo.com.mx/medicamentos/estomacal/Reductores-de-peso0/c/060050009",
		"https://www.farmaciasanpablo.com.mx/medicamentos/estomacal/Sueros-orales0/c/060050010",

		"https://www.farmaciasanpablo.com.mx/medicamentos/genericos/A-B-C-D0/c/060060001",
		"https://www.farmaciasanpablo.com.mx/medicamentos/genericos/E-F-G-H0/c/060060002",
		"https://www.farmaciasanpablo.com.mx/medicamentos/genericos/I-J-K-L0/c/060060003",
		"https://www.farmaciasanpablo.com.mx/medicamentos/genericos/M-N-O-P0/c/060060004",
		"https://www.farmaciasanpablo.com.mx/medicamentos/genericos/Q-R-S-T0/c/060060005",
		"https://www.farmaciasanpablo.com.mx/medicamentos/genericos/V-W-X-Y-Z0/c/060060006",

		"https://www.farmaciasanpablo.com.mx/medicamentos/gripe-y-tos/Antialergicas0/c/060070001",
		"https://www.farmaciasanpablo.com.mx/medicamentos/gripe-y-tos/Antigripales0/c/060070002",
		"https://www.farmaciasanpablo.com.mx/medicamentos/gripe-y-tos/Aparatos-de-diagnosticos0/c/060070003",
		"https://www.farmaciasanpablo.com.mx/medicamentos/gripe-y-tos/Descongestionantes0/c/060070004",
		"https://www.farmaciasanpablo.com.mx/medicamentos/gripe-y-tos/Garganta-Irritada0/c/060070005",
		"https://www.farmaciasanpablo.com.mx/medicamentos/gripe-y-tos/Humidificadores0/c/060070006",
		"https://www.farmaciasanpablo.com.mx/medicamentos/gripe-y-tos/Inhaladores0/c/060070007",
		"https://www.farmaciasanpablo.com.mx/medicamentos/gripe-y-tos/Nebulizadores0/c/060070008",
		"https://www.farmaciasanpablo.com.mx/medicamentos/gripe-y-tos/Tos0/c/060070009",

		"https://www.farmaciasanpablo.com.mx/medicamentos/oftalmicos/Higiene-lentes-de-contacto0/c/060080001",
		"https://www.farmaciasanpablo.com.mx/medicamentos/oftalmicos/Inflamacion-infeccion0/c/060080002",
		"https://www.farmaciasanpablo.com.mx/medicamentos/oftalmicos/Lentes-para-lectura0/c/060080004",
		"https://www.farmaciasanpablo.com.mx/medicamentos/oftalmicos/Lagrimas-artificiales0/c/060080003",
		"https://www.farmaciasanpablo.com.mx/medicamentos/oftalmicos/Lubricantes-oculares0/c/060080005",
		"https://www.farmaciasanpablo.com.mx/medicamentos/oftalmicos/Oftalmologicos0/c/060080006",
		"https://www.farmaciasanpablo.com.mx/medicamentos/oftalmicos/Preparacion-lentes-contacto0/c/060080007",
		"https://www.farmaciasanpablo.com.mx/medicamentos/oftalmicos/Taollitas-humedas0/c/060080008",
		"https://www.farmaciasanpablo.com.mx/medicamentos/oftalmicos/Tonicos-vitaminas0/c/060080009",

		"https://www.farmaciasanpablo.com.mx/medicamentos/pruebas-antidoping/Test-antidoping0/c/060090001",

		"https://www.farmaciasanpablo.com.mx/medicamentos/relajantes/Antitabaquismo0/c/060100001",
		"https://www.farmaciasanpablo.com.mx/medicamentos/relajantes/Relajantes1/c/060100002",

		"https://www.farmaciasanpablo.com.mx/medicamentos/supervision-medica/D-E-F0/c/060110002",
		"https://www.farmaciasanpablo.com.mx/medicamentos/supervision-medica/G-H-I0/c/060110003",
		"https://www.farmaciasanpablo.com.mx/medicamentos/supervision-medica/J-K-L0/c/060110004",
		"https://www.farmaciasanpablo.com.mx/medicamentos/supervision-medica/M-N-O0/c/060110005",
		"https://www.farmaciasanpablo.com.mx/medicamentos/supervision-medica/P-Q-R0/c/060110006",
		"https://www.farmaciasanpablo.com.mx/medicamentos/supervision-medica/S-T-U0/c/060110007",
		"https://www.farmaciasanpablo.com.mx/medicamentos/supervision-medica/V-W-X0/c/060110008",
		"https://www.farmaciasanpablo.com.mx/medicamentos/supervision-medica/Y-Z0/c/060110009",

		"https://www.farmaciasanpablo.com.mx/medicamentos/varices/Cuidado-de-piernas0/c/060120001",

		"https://www.farmaciasanpablo.com.mx/equipo-y-botiquin/aparatos-de-medicion/Baumanometros0/c/050010001",
		"https://www.farmaciasanpablo.com.mx/equipo-y-botiquin/aparatos-de-medicion/Detector-preventivo0/c/050010002",
		"https://www.farmaciasanpablo.com.mx/equipo-y-botiquin/aparatos-de-medicion/Glucometros0/c/050010003",
		"https://www.farmaciasanpablo.com.mx/equipo-y-botiquin/aparatos-de-medicion/Termometros0/c/050010004",
		"https://www.farmaciasanpablo.com.mx/equipo-y-botiquin/aparatos-de-medicion/Tiras-y-lancetas0/c/050010005",

		"https://www.farmaciasanpablo.com.mx/equipo-y-botiquin/baterias-alcalinas/Pilas0/c/050020001",

		"https://www.farmaciasanpablo.com.mx/equipo-y-botiquin/material-de-curacion/algodones-y-pads/c/050030001",
		"https://www.farmaciasanpablo.com.mx/equipo-y-botiquin/material-de-curacion/Antisep-alcohol-agua-oxigen.0/c/050030002",
		"https://www.farmaciasanpablo.com.mx/equipo-y-botiquin/material-de-curacion/Jeringas-y-agujas0/c/050030003",
		"https://www.farmaciasanpablo.com.mx/equipo-y-botiquin/material-de-curacion/Otros-accesorios-de-curacion0/c/050030004",
		"https://www.farmaciasanpablo.com.mx/equipo-y-botiquin/material-de-curacion/Parches-y-telas-adhesivas0/c/050030005",
		"https://www.farmaciasanpablo.com.mx/equipo-y-botiquin/material-de-curacion/Vendas-y-gasas0/c/050030006",

		"https://www.farmaciasanpablo.com.mx/equipo-y-botiquin/ortopedia/accesorios-de-ortopedia/c/050040001",

		"https://www.farmaciasanpablo.com.mx/salud-natural/salud-natural/alimentos-saludables/c/070010001",
		"https://www.farmaciasanpablo.com.mx/salud-natural/salud-natural/aromaterapia/c/070010002",
		"https://www.farmaciasanpablo.com.mx/salud-natural/salud-natural/bebidas-organicas-y-naturales/c/070010016",
		"https://www.farmaciasanpablo.com.mx/salud-natural/salud-natural/botanas-saludables/c/070010013",
		"https://www.farmaciasanpablo.com.mx/salud-natural/salud-natural/cuidado-personal/c/070010014",
		"https://www.farmaciasanpablo.com.mx/salud-natural/salud-natural/cuidados-del-bebe/c/070010015",
		"https://www.farmaciasanpablo.com.mx/salud-natural/salud-natural/endulzantes-naturales/c/070010003",
		"https://www.farmaciasanpablo.com.mx/salud-natural/salud-natural/flores-de-bach/c/070010004",
		"https://www.farmaciasanpablo.com.mx/salud-natural/salud-natural/medicamentos-herbolarios/c/070010005",
		"https://www.farmaciasanpablo.com.mx/salud-natural/salud-natural/medicamentos-homeopaticos/c/070010006",
		"https://www.farmaciasanpablo.com.mx/salud-natural/salud-natural/remedios-herbolarios/c/070010007",
		"https://www.farmaciasanpablo.com.mx/salud-natural/salud-natural/superfoods/c/070010008",
		"https://www.farmaciasanpablo.com.mx/salud-natural/salud-natural/dulces-y-chocolates-sin-azucar/c/070010009",
		"https://www.farmaciasanpablo.com.mx/salud-natural/salud-natural/tes/c/070010011",
		"https://www.farmaciasanpablo.com.mx/salud-natural/salud-natural/vitaminas-y-minerales-naturale/c/070010012",

		"https://www.farmaciasanpablo.com.mx/vitaminas-y-suplementos/suplementos-alimenticios/suplementos-y-complementos/c/090010001",

		"https://www.farmaciasanpablo.com.mx/vitaminas-y-suplementos/vitaminicos/calcios/c/090020001",
		"https://www.farmaciasanpablo.com.mx/vitaminas-y-suplementos/vitaminicos/colageno/c/090020002",
		"https://www.farmaciasanpablo.com.mx/vitaminas-y-suplementos/vitaminicos/colesterol/c/090020003",
		"https://www.farmaciasanpablo.com.mx/vitaminas-y-suplementos/vitaminicos/complementos-vitaminicos/c/090020004",
		"https://www.farmaciasanpablo.com.mx/vitaminas-y-suplementos/vitaminicos/naturistas/c/090020006",
		"https://www.farmaciasanpablo.com.mx/vitaminas-y-suplementos/vitaminicos/multivitaminicos/c/090020005",
		"https://www.farmaciasanpablo.com.mx/vitaminas-y-suplementos/vitaminicos/osteoartritis/c/090020007",
		"https://www.farmaciasanpablo.com.mx/vitaminas-y-suplementos/vitaminicos/vitaminas-y-minerales/c/090020009",


		"https://www.farmaciasanpablo.com.mx/dermocosmeticos/dermocosmeticos/cosmeticos-clinicos/c/040010001",
		"https://www.farmaciasanpablo.com.mx/dermocosmeticos/dermocosmeticos/cremas/c/040010002",
		"https://www.farmaciasanpablo.com.mx/dermocosmeticos/dermocosmeticos/dermatologicos/c/040010003",
		"https://www.farmaciasanpablo.com.mx/dermocosmeticos/dermocosmeticos/desodorantes/c/040010004",
		"https://www.farmaciasanpablo.com.mx/dermocosmeticos/dermocosmeticos/emolientes/c/040010005",
		"https://www.farmaciasanpablo.com.mx/dermocosmeticos/dermocosmeticos/exfoliantes/c/040010006",
		"https://www.farmaciasanpablo.com.mx/dermocosmeticos/dermocosmeticos/geles-o-lociones-de-limpieza/c/040010007",
		"https://www.farmaciasanpablo.com.mx/dermocosmeticos/dermocosmeticos/higiene-intima/c/040010009",
		"https://www.farmaciasanpablo.com.mx/dermocosmeticos/dermocosmeticos/hidratantes/c/040010008",
		"https://www.farmaciasanpablo.com.mx/dermocosmeticos/dermocosmeticos/kits-y-promocionales/c/040010010",
		"https://www.farmaciasanpablo.com.mx/dermocosmeticos/dermocosmeticos/lociones-anticaida/c/040010011",
		"https://www.farmaciasanpablo.com.mx/dermocosmeticos/dermocosmeticos/nutricosmeticos/c/040010012",
		"https://www.farmaciasanpablo.com.mx/dermocosmeticos/dermocosmeticos/protectores-solares/c/040010013",
		"https://www.farmaciasanpablo.com.mx/dermocosmeticos/dermocosmeticos/reafirmantes-corporales/c/040010014",
		"https://www.farmaciasanpablo.com.mx/dermocosmeticos/dermocosmeticos/shampoos%2C-acondicionadores-y-t/c/040010015",


		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/accesorios-de-pies-y-manos/Alicates0/c/030010001",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/accesorios-de-pies-y-manos/Bisturi0/c/030010002",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/accesorios-de-pies-y-manos/Corta-callos0/c/030010003",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/accesorios-de-pies-y-manos/Corta-Unas0/c/030010004",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/accesorios-de-pies-y-manos/Limas0/c/030010005",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/accesorios-de-pies-y-manos/Pies0/c/030010006",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/accesorios-de-pies-y-manos/Tijeras0/c/030010007",

		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/afeitado/After-shave-para-hombre0/c/030020001",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/afeitado/Cartucho-para-hombre0/c/030020002",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/afeitado/Cartucho-para-mujer0/c/030020003",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/afeitado/Depilatorio-para-mujer0/c/030020004",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/afeitado/Espuma-para-afeitar-hombre0/c/030020005",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/afeitado/Espuma-para-afeitar-mujer0/c/030020006",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/afeitado/Gel-para-afeitar-hombre0/c/030020007",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/afeitado/Gel-para-afeitar-mujer0/c/030020008",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/afeitado/Rastrillo-para-hombre0/c/030020009",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/afeitado/Rastrillo-para-mujer0/c/030020010",

		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cosmeticos/Delineadores0/c/030030001",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cosmeticos/Esmaltes0/c/030030002",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cosmeticos/Labiales0/c/030030003",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cosmeticos/Maquillajes0/c/030030004",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cosmeticos/Mascaras0/c/030030005",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cosmeticos/Polvos0/c/030030006",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cosmeticos/Rubores0/c/030030007",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cosmeticos/Sombras0/c/030030008",

		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-bucal/Accesorios-dentales0/c/030040001",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-bucal/Cepillos-dentales0/c/030040002",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-bucal/Enjuagues-bucales0/c/030040003",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-bucal/Especializados0/c/030040004",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-bucal/Hilos-dentales0/c/030040005",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-bucal/Ortodoncia0/c/030040006",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-bucal/Pastas-dentales0/c/030040007",

		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-de-la-piel/Corporal0/c/030050002",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-de-la-piel/Contorno-Ojos0/c/030050001",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-de-la-piel/Faciales0/c/030050003",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-de-la-piel/Pies-y-manos0/c/030050004",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-de-la-piel/Protectores-para-labios0/c/030050006",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-de-la-piel/Talcos-y-colonias0/c/030050007",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-de-la-piel/Toallitas-desmaquillantes0/c/030050008",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-de-la-piel/Toallitas-exfoliantes0/c/030050009",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-de-la-piel/Toallitas-limpiadoras0/c/030050010",

		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-del-cabello/Acondicionadores0/c/030060001",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-del-cabello/Cremas-para-peinar0/c/030060002",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-del-cabello/Fijadores0/c/030060003",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-del-cabello/Shampoos0/c/030060004",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-del-cabello/Tintes0/c/030060005",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/cuidado-del-cabello/Tratamientos-capilares0/c/030060006",

		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/desodorante/Barra-hombre0/c/030070001",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/desodorante/Barra-mujer0/c/030070002",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/desodorante/Barra-unisex0/c/030070003",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/desodorante/Roll-on-hombre0/c/030070004",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/desodorante/Roll-on-mujer0/c/030070005",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/desodorante/Roll-on-unisex0/c/030070006",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/desodorante/Spray-hombre0/c/030070007",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/desodorante/Spray-mujer0/c/030070008",

		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/higiene-y-proteccion-femenina/Higiene-femenina0/c/030080001",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/higiene-y-proteccion-femenina/Pantiprotectores0/c/030080002",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/higiene-y-proteccion-femenina/Tampones0/c/030080003",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/higiene-y-proteccion-femenina/Toallas-femeninas0/c/030080004",

		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/incontinencia/Ropa-interior-desechable0/c/030090001",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/incontinencia/Salvacamas0/c/030090002",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/incontinencia/Toallas-para-incontinencia0/c/030090003",

		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/jabones/Geles-antibacteriales0/c/030100001",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/jabones/Jabones-en-barra0/c/030100002",
		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/jabones/Jabones-liquidos0/c/030100003",

		"https://www.farmaciasanpablo.com.mx/cuidado-personal-y-belleza/papel-higienico-y-panuelos/papel-higienico-y-panuelos/c/030110001",

		"https://www.farmaciasanpablo.com.mx/bebes/accesorios-para-bebe/Aspiradores-nasales0/c/020010001",
		"https://www.farmaciasanpablo.com.mx/bebes/accesorios-para-bebe/Biberones0/c/020010002",
		"https://www.farmaciasanpablo.com.mx/bebes/accesorios-para-bebe/Chupones0/c/020010003",
		"https://www.farmaciasanpablo.com.mx/bebes/accesorios-para-bebe/Cosas-para-bebe0/c/020010004",
		"https://www.farmaciasanpablo.com.mx/bebes/accesorios-para-bebe/Protectores-de-pezones0/c/020010005",
		"https://www.farmaciasanpablo.com.mx/bebes/accesorios-para-bebe/Tetinas0/c/020010006",

		"https://www.farmaciasanpablo.com.mx/bebes/alimentos-para-bebes/Aguas-para-bebes0/c/020020001",
		"https://www.farmaciasanpablo.com.mx/bebes/alimentos-para-bebes/Cereales0/c/020020002",
		"https://www.farmaciasanpablo.com.mx/bebes/alimentos-para-bebes/Jugos0/c/020020003",
		"https://www.farmaciasanpablo.com.mx/bebes/alimentos-para-bebes/Papillas0/c/020020004",
		"https://www.farmaciasanpablo.com.mx/bebes/alimentos-para-bebes/Yogurts0/c/020020005",

		"https://www.farmaciasanpablo.com.mx/bebes/cuidados-del-bebe/Aceites0/c/020030001",
		"https://www.farmaciasanpablo.com.mx/bebes/cuidados-del-bebe/Aplicadores0/c/020030002",
		"https://www.farmaciasanpablo.com.mx/bebes/cuidados-del-bebe/Cremas-de-bebe0/c/020030003",
		"https://www.farmaciasanpablo.com.mx/bebes/cuidados-del-bebe/Pomadas-y-unguentos0/c/020030004",
		"https://www.farmaciasanpablo.com.mx/bebes/cuidados-del-bebe/Shampoo-y-jabones0/c/020030005",
		"https://www.farmaciasanpablo.com.mx/bebes/cuidados-del-bebe/Talcos0/c/020030006",
		"https://www.farmaciasanpablo.com.mx/bebes/cuidados-del-bebe/Toallitas-humedas0/c/020030007",

		"https://www.farmaciasanpablo.com.mx/bebes/dermopediatria/Cremas-para-bebe0/c/020040001",
		"https://www.farmaciasanpablo.com.mx/bebes/dermopediatria/Cremas-para-sol0/c/020040002",
		"https://www.farmaciasanpablo.com.mx/bebes/dermopediatria/Especiales-para-mamas0/c/020040003",
		"https://www.farmaciasanpablo.com.mx/bebes/dermopediatria/Geles-y-jabones0/c/020040004",
		"https://www.farmaciasanpablo.com.mx/bebes/dermopediatria/Lociones-y-aguas-de-tocador0/c/020040005",
		"https://www.farmaciasanpablo.com.mx/bebes/dermopediatria/Repelente-de-mosquitos0/c/020040006",
		"https://www.farmaciasanpablo.com.mx/bebes/dermopediatria/Shampoos-para-bebe0/c/020040007",
		"https://www.farmaciasanpablo.com.mx/bebes/dermopediatria/Talcos-y-aceites0/c/020040008",
		"https://www.farmaciasanpablo.com.mx/bebes/dermopediatria/Toallitas-humedas-bebe0/c/020040009",

		"https://www.farmaciasanpablo.com.mx/bebes/formulas-infantiles/Especializadas0/c/020050001",
		"https://www.farmaciasanpablo.com.mx/bebes/formulas-infantiles/Regulares-etapa-10/c/020050002",
		"https://www.farmaciasanpablo.com.mx/bebes/formulas-infantiles/Regulares-etapa-20/c/020050003",
		"https://www.farmaciasanpablo.com.mx/bebes/formulas-infantiles/Regulares-etapa-30/c/020050004",
		"https://www.farmaciasanpablo.com.mx/bebes/formulas-infantiles/Regulares-etapa-40/c/020050005",

		"https://www.farmaciasanpablo.com.mx/bebes/panales/Nina-etapa-30/c/020060001",
		"https://www.farmaciasanpablo.com.mx/bebes/panales/Nina-etapa-40/c/020060002",
		"https://www.farmaciasanpablo.com.mx/bebes/panales/Nina-etapa-50/c/020060003",
		"https://www.farmaciasanpablo.com.mx/bebes/panales/Nina-etapa-60/c/020060004",
		"https://www.farmaciasanpablo.com.mx/bebes/panales/Nino-etapa-30/c/020060005",
		"https://www.farmaciasanpablo.com.mx/bebes/panales/Nino-etapa-40/c/020060006",
		"https://www.farmaciasanpablo.com.mx/bebes/panales/Nino-etapa-50/c/020060007",
		"https://www.farmaciasanpablo.com.mx/bebes/panales/Nino-etapa-60/c/020060008",
		"https://www.farmaciasanpablo.com.mx/bebes/panales/Unisex-etapa-10/c/020060009",
		"https://www.farmaciasanpablo.com.mx/bebes/panales/Unisex-etapa-20/c/020060010",
		"https://www.farmaciasanpablo.com.mx/bebes/panales/Unisex-etapa-30/c/020060011",
		"https://www.farmaciasanpablo.com.mx/bebes/panales/Unisex-etapa-40/c/020060012",
		"https://www.farmaciasanpablo.com.mx/bebes/panales/Unisex-etapa-50/c/020060013",
		"https://www.farmaciasanpablo.com.mx/bebes/panales/Unisex-etapa-60/c/020060014",
		"https://www.farmaciasanpablo.com.mx/bebes/panales/Unisex-etapa-70/c/020060015",

		"https://www.farmaciasanpablo.com.mx/bebes/revista/revistas/c/020070001",

		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/alimentos-saludables/Galletas-cereales-y-granolas0/c/010010001",
		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/alimentos-saludables/Leches-de-soya0/c/010010002",
		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/alimentos-saludables/Sal0/c/010010003",
		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/alimentos-saludables/Snacks0/c/010010004",

		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/alimentos-sin-azucar/Cereales-galletas-y-granolas0/c/010020001",
		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/alimentos-sin-azucar/Dulces-y-chocolates0/c/010020002",
		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/alimentos-sin-azucar/Otros-alimentos-sin-azucar0/c/010020003",
		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/alimentos-sin-azucar/Suplementos-alimenticios0/c/010020004",
		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/alimentos-sin-azucar/Sustitutos-de-azucar0/c/010020005",

		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/bebidas/Aguas-purificadas0/c/010030001",
		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/bebidas/Aguas-saborizadas0/c/010030002",
		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/bebidas/Bebidas-isotonicas0/c/010030003",
		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/bebidas/Jugos-y-nectares0/c/010030004",

		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/cafe-y-chocolate-en-polvo/Cafe-soluble0/c/010040001",
		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/cafe-y-chocolate-en-polvo/Chocolates-en-polvo0/c/010040002",

		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/Leches-en-polvo0/c/010060001",
		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/Leches-liquidas0/c/010060002",

		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/galletas%2C-dulces-y-chocolates/chocolates/c/010050001",
		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/galletas%2C-dulces-y-chocolates/Dulces0/c/010050002",
		"https://www.farmaciasanpablo.com.mx/alimentos-y-bebidas/galletas%2C-dulces-y-chocolates/Galletas0/c/010050003",

		"https://www.farmaciasanpablo.com.mx/salud-sexual/bienestar-sexual/accesorios-y-juguetes/c/080010001",
		"https://www.farmaciasanpablo.com.mx/salud-sexual/bienestar-sexual/Lubricantes-vaginales0/c/080010002",
		"https://www.farmaciasanpablo.com.mx/salud-sexual/bienestar-sexual/Preservativos0/c/080010003",
		"https://www.farmaciasanpablo.com.mx/salud-sexual/bienestar-sexual/Pruebas0/c/080010004",
		"https://www.farmaciasanpablo.com.mx/salud-sexual/bienestar-sexual/Vigorizantes0/c/080010005"
		]
		#Entramos a cada una de las URL's
		for i in urls:
			yield scrapy.Request(url=i, callback=self.parse)

	def parse(self, response):
		#Link a cada producto
		items = SanpabloItem()

		#Entramos al link del producto
		for href in response.xpath('//div[@class="col-xs-5 col-sm-5 col-md-12 img-wrap"]/a/@href'):
			url = response.urljoin(href.extract())
			urls = href.extract()

			#En el ultimo parametro pasamos el link del producto
			yield scrapy.Request(url, callback = self.parse_dir_contents, dont_filter = True, meta={'link':urls})

		#Hacemos link en página siguiente si es que hay
		next_page = response.xpath('//ul[@class="pagination pull-right"]/li/a[@class="next"]/@href').get()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse, dont_filter = True)

	def parse_dir_contents(self, response):

		#Nombre, precio, descuento, envio, fabricante, url, categoria
		items = SanpabloItem()

		#Preparamos la fecha
		x = datetime.now()
		dia = str(x.strftime("%d"))
		mes = str(x.strftime("%m"))
		anio = str(x.year)

		nombre = response.xpath('normalize-space(//div[@class="hidden-sm hidden-xs"]/h1/text())').extract()
		original = response.xpath('normalize-space(//*[@id="body-main-container"]/div[4]/div[2]/div[2]/div[1]/p/del/text())').extract()
		descuento = response.xpath('normalize-space(//*[@id="body-main-container"]/div[4]/div[2]/div[2]/div[1]/p/text())').extract()
		fabricante = response.xpath('normalize-space(//dl[@class="dl-left"]/dd[last()-1]/text())').extract()
		envio = response.xpath('normalize-space(//*[@id="body-main-container"]/div[4]/div[2]/div[2]/div[1]/span)').extract()
		categoria = response.xpath('normalize-space(//ol[@class="breadcrumb"]/li[last()-1])').extract()
		url = response.meta.get('link')
		fecha = dia + '-' + mes + '-' + anio

		#//*[@id="body-main-container"]/div[4]/div[2]/div[2]/div[1]/p/text()

		items['nombre'] = nombre
		items['original'] = original
		items['descuento'] = descuento
		items['fabricante'] = fabricante
		items['envio'] = envio
		items['categoria'] = categoria
		items['url'] = "https://www.farmaciasanpablo.com.mx"+url
		items['fecha'] = fecha

		yield items