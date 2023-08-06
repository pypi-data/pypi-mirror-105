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
    def get_store_product_marketplace_limit(self, server_url='', token='', marketplace_id='', store_id='', offset=0, status=None):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'
        status_list = ['pending_register_product', 'done']

        url = "/storeProductsMarketplace/"

        if store_id and marketplace_id:
            if '?' in url:
                url += f'&marketplaceId={marketplace_id}&storeId={store_id}'
            else:
                url += f'?marketplaceId={marketplace_id}&storeId={store_id}'
        if status and status in status_list:
            if '?' in url:
                url += f'&statusProcessing={status}'
            else:
                url += f'?statusProcessing={status}'

        LIMIT = 20
        params = {
            "offset": offset,
            "limit": LIMIT
        }

        response = requests.get(
            f"{server_url}{url}",
            headers=headers,
            params=params
        )

        if response.status_code != 200:
            logging.error(f"/storeProductsMarketplace/ ERROR - {response.status_code} - {response.content if not 'html' in str(response.content) else 'Error'} - {status if status else ''}")
            return []

        if json.loads(response.content)['total'] == 0:
            logging.info(f"/storeProductsMarketplace/ is empty - {status if status else ''}")
            return []

        return json.loads(response.content)

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