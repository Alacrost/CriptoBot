import abc
import hashlib
import hmac
import json
from typing import OrderedDict
import requests
from http import client
from urllib.parse import urlencode
from pprint import pprint
from datetime import datetime
from pytz import timezone
from requests.api import post
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
    MB_TAPI_ID = ' MB_TAPI_ID'
    MB_TAPI_SECRET = 'MB_TAPI_SECRET'
    REQUEST_HOST = 'https://api.novadax.com'
    REQUEST_PATH = 'v1/common/symbols'

    # Nonce
    # Para obter variação de forma simples
    # timestamp pode ser utilizado:
    #     import time
    #     tapi_nonce = str(int(time.time()))

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
        print('status: {}'.format(response_json['status_code']))

    finally:
        if conn:
            conn.close()
