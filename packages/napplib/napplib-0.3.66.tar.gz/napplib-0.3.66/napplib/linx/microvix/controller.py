import requests, json, logging
from xml.etree import ElementTree

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")

url = 'http://webapi.microvix.com.br/1.0/api/integracao'

class MicrovixController:

	@classmethod
	def get_stock(self, user, password, method, chave, cnpjEmp, data_inicio='NULL', data_fim='NULL', cod_produto='NULL', referencia='NULL', type='XML'):
		logging.info(f"Coletando estoque dos produtos da API... para o seller: {cnpjEmp}")

		payload=f"<?xml version='1.0' encoding='utf-8' ?>\r\n\r\n<LinxMicrovix>\r\n\r\n<Authentication user=\"{user}\" password=\"{password}\" />\r\n\r\n<Command><Name>{method}</Name>\r\n\r\n<Parameters>\r\n<Parameter id=\"chave\">{chave}</Parameter>\r\n<Parameter id=\"cnpjEmp\">{cnpjEmp}</Parameter>\r\n<Parameter id='Data_mov_ini'>{data_inicio}</Parameter>\r\n<Parameter id=\"data_mov_fim\">{data_fim}</Parameter>\r\n<Parameter id=\"cod_produto\">{cod_produto}</Parameter>\r\n<Parameter id=\"referencia\">{referencia}</Parameter>\r\n\r\n</Parameters>\r\n\r\n</Command>\r\n\r\n</LinxMicrovix>"
		headers = {
		  'Content-Type': 'application/xml'
		}

		r = requests.post(url, headers=headers, data=payload)

		string_xml = r.content
		tree = ElementTree.fromstring(string_xml)
		stocks = tree.find('ResponseData').findall('R')
		
		stock_upload = []

		for stk in stocks:
			codProd = str(stk.findall('D')[2].text).strip()
			ean = str(stk.findall('D')[3].text).strip()
			
			if not stk.findall('D')[6].text:
				price = 0
			else:
				price = round(float(str(stk.findall('D')[6].text).strip()),2)

			if not stk.findall('D')[4].text:
				qty = 0
			else:
				qty = int(float(str(stk.findall('D')[4].text).strip()))

			stock_upload.append([codProd, ean, qty, price])

		return stock_upload

	@classmethod
	def get_products(self, user, password, method, chave, cnpjEmp,  data_inicio='NULL', data_fim='NULL', type='XML'):
		logging.info(f"Coletando os produtos da API... para o seller: {cnpjEmp}")

		payload=f"<?xml version='1.0' encoding='utf-8' ?>\r\n\r\n<LinxMicrovix>\r\n\r\n<Authentication user=\"{user}\" password=\"{password}\" />\r\n\r\n<Command><Name>{method}</Name>\r\n\r\n<Parameters>\r\n<Parameter id=\"chave\">{chave}</Parameter>\r\n<Parameter id=\"cnpjEmp\">{cnpjEmp}</Parameter>\r\n<Parameter id='Dt_update_inicio'>{data_inicio}</Parameter>\r\n<Parameter id=\"Dt_update_fim\">{data_fim}</Parameter>\r\n\r\n</Parameters>\r\n\r\n</Command>\r\n\r\n</LinxMicrovix>"
		headers = {
		  'Content-Type': 'application/xml'
		}

		r = requests.post(url, headers=headers, data=payload)

		string_xml = r.content
		tree = ElementTree.fromstring(string_xml)
		products = tree.find('ResponseData').findall('R')

		products_upload = []

		for prd in products:
			product = prd.findall('D')
			codProd = str(product[1].text).strip()
			ean = str(product[2].text).strip()
			nome = str(product[3].text).strip()
			referencia = str(product[6].text).strip()
			unidade = str(product[8].text).strip()
			cor = str(product[9].text).strip()
			tamanho = str(product[10].text).strip()
			setor = str(product[11].text).strip()
			linha = str(product[12].text).strip()
			marca = str(product[13].text).strip()
			colecao = str(product[14].text).strip()
			peso = str(product[23].text).strip()
			cest = str(product[5].text).strip()
			ncm = str(product[4].text).strip()

			products_upload.append([codProd, ean, nome, referencia, unidade,
					cor, tamanho, setor, linha, marca, colecao, peso, cest, ncm])

		return products_upload
		
	@classmethod
	def parsed_items():
		pass

	@classmethod
	def get_images_vtex():
		pass