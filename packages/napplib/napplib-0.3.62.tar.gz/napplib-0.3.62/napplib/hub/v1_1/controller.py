import requests, json, datetime, sys, logging
from .utils import Utils

from .models.product import InventoryList

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")

class HubController:
	@classmethod
	def authenticate(self, server_url='', user='', passwd=''):
		# create headers
		headers = dict()
		headers['Content-Type'] = 'application/json'

		# authenticate payload
		payload = dict()
		payload['username'] = user
		payload['password'] = passwd

		# do login request
		r = requests.post(f'{server_url}/signin/', headers=headers, data=json.dumps(payload))


		# catch error
		if r.status_code != 200:
			raise Exception(f'Failed to login on NappHUB...try again... {r.content.decode("utf-8")}')

		# get and return token
		token = json.loads(r.content.decode('utf8'))['token']

		return token

	@classmethod
	def inventory_list(self, server_url='', token='', store_id='', marketplace_id='', inventory_list=''):
		headers = dict()
		headers['Authorization'] = f'Bearer {token}'

		payload = json.dumps(inventory_list)

		r = requests.patch(f'{server_url}/updateInventory/{store_id}/{marketplace_id}', headers=headers, data=payload)

		return r

	@classmethod
	def get_store_product_marketplace_limit(self, server_url='', token='', marketplace_id='', store_id=''):
		# create headers
		headers = dict()
		headers['Authorization'] = f'Bearer {token}'

		store_products_mkt_all = []
		url = "/storeProductsMarketplace/"

		if store_id and marketplace_id:
			url = f'/storeProductsMarketplace/?marketplaceId={marketplace_id}&storeId={store_id}'

		count = 0
		LIMIT = 20

		params = {
			"offset": count,
			"limit": LIMIT
		}

		response = requests.get(
			f"{server_url}{url}",
			headers=headers,
			params=params
		)
		total = json.loads(response.content)['total']
		if total == 0:
			logging.info("/storeProductsMarketplace/ is empty.")
			return []

		store_products_mkt_all.extend(json.loads(response.content)['data'])

		pages = int(total / LIMIT)
		if pages == 0:
			return store_products_mkt_all

		for i in range(0, pages, 1):
			count += LIMIT

			params["offset"] = count

			response = requests.get(
				f"{server_url}{url}",
				headers=headers,
				params=params
			)

			store_products_mkt_all.extend(json.loads(response.content)['data'])

		return store_products_mkt_all


	@classmethod
	def store_product_marketplace_update_list(self, server_url, token, storeProducts):
		headers = dict()
		headers['Authorization'] = f'Bearer {token}'

		payload = json.dumps(storeProducts)

		r = requests.patch(f'{server_url}/storeProductsMarketplace/?list=true', headers=headers, data=payload)

		return r

	@classmethod
	def create_products(self, server_url, token, store_id='', marketplace_id='', products=[]):
		headers = dict()
		headers['Authorization'] = f'Bearer {token}'

		payload = json.dumps(products)
		
		r = requests.post(f'{server_url}/integrateProducts/{store_id}/{marketplace_id}', headers=headers, data=payload)

		return r