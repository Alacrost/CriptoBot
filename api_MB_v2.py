
import hashlib
import hmac
import json
from typing import OrderedDict

from http import client
from urllib.parse import urlencode
from pprint import pprint


from parametros import *

params1 = {
    'tapi_method': 'list_orderbook',
    'coin_pair': 'BRLXRP'
}
params2 = {
    'tapi_method': 'get_account_info',
    'tapi_nonce': '1'
}


params3 = {
    'tapi_method': 'list_orders',
    'tapi_nonce': '1',
    'coin_pair': 'BRLXRP',
    'status_list': '[1, 2, 3, 4]',
    'has_fills': True
}

params1 = urlencode(params1)
params2 = urlencode(params2)
params3 = urlencode(params3)


def valores_API_MB(params=params1, moeda='BRLXRP'):

    params1 = {
        'tapi_method': 'list_orderbook',
        'coin_pair': moeda
    }

    params2 = {
        'tapi_method': 'get_account_info',
        'tapi_nonce': '1'
    }

    params3 = {
        'tapi_method': 'list_orders',
        'tapi_nonce': '1',
        'coin_pair': moeda,
        'status_list': '[1, 2, 3, 4]',
        'has_fills': True
    }

    params1 = urlencode(params1)
    params2 = urlencode(params2)
    params3 = urlencode(params3)

    # Constantes
    MB_TAPI_ID = 'MB_TAPI_ID'
    MB_TAPI_SECRET = 'MB_TAPI_SECRET'
    REQUEST_HOST = 'www.mercadobitcoin.net'
    REQUEST_PATH = '/tapi/v3/'

    # Gerar MAC
    params_string = REQUEST_PATH + '?' + params
    H = hmac.new(bytes(MB_TAPI_SECRET, encoding='utf8'),
                 digestmod=hashlib.sha512)
    H.update(params_string.encode('utf-8'))
    tapi_mac = H.hexdigest()

    # Gerar cabeçalho da requisição
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'TAPI-ID': MB_TAPI_ID,
        'TAPI-MAC': tapi_mac
    }

    # Realizar requisição POST

    try:
        conn = client.HTTPSConnection(REQUEST_HOST)
        conn.request("POST", REQUEST_PATH, params, headers)

        # Print response data to console
        response = conn.getresponse()
        response = response.read()

        response_json = json.loads(response)
        # print('status: {}'.format(response_json['status_code']))

        if params == params1:  # ORDERBOOK
            global list_orderBook_ASKS
            global list_orderBook_BIDS
            global list_orderBook_TIME
            list_orderBook_ASKS = response_json['response_data']['orderbook']['asks']
            list_orderBook_BIDS = response_json['response_data']['orderbook']['bids']
            list_orderBook_TIME = float(response_json['server_unix_timestamp'])
            pprint(list_orderBook_ASKS)
            pprint(list_orderBook_BIDS)
            pprint(f'Time: {list_orderBook_TIME}')

        if params == params2:  # ACCOUNT INFO
            global get_account_info_BALANCE
            global get_account_info_WITHDRAWAL
            global get_account_info_TIME
            get_account_info_BALANCE = response_json['response_data']['balance']
            get_account_info_WITHDRAWAL = response_json['response_data']['withdrawal_limits']
            get_account_info_TIME = float(
                response_json['server_unix_timestamp'])
            pprint(get_account_info_BALANCE['brl'])
            # pprint(get_account_info_BALANCE)
            # pprint(get_account_info_WITHDRAWAL)
            # pprint(f'Time: {get_account_info_TIME}')
        # LIST ORDERS (1 : pending,2 : open,3 : canceled, 4 : filled )
        if params == params3:
            global list_orders
            global list_orders_TIME
            list_orders = response_json['response_data']['orders']
            list_orders_TIME = response_json['server_unix_timestamp']
            pprint(list_orders)
            pprint(list_orders_TIME)

    finally:
        if conn:
            conn.close()


valores_API_MB(params=params2)
