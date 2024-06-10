#######################################################################
#                                                                    #
#                       VERSÃO 0.4  DATA FROM API REST KEY           #
#                                       ACTIONS                      #
#                                                                    #
#                                                                    #
######################################################################

from logging import error
from time import sleep
import requests
from pprint import pprint
from datetime import datetime
from requests.api import get
from rich import print
from rich.table import Table
# from utilidades import apresentacao
from rich.console import Console
import os
import hashlib
import hmac
import json
from http import client
from urllib.parse import urlencode
from binance import set as Client_bnb
# from binance.enums import *
# from binance.exceptions import BinanceAPIException, BinanceOrderException


table = Table(title='PAINEL')
console = Console()

log_data = 'registro_data'
log_actions = 'registro_acoes'

# CRIAR ARQUIVO TXT COM INFORMAÇÕES E REGISTRA


def registro_log(nome_arquivo='log', registro=''):
    with open(f'{nome_arquivo}.txt', 'a', newline='') as arquivo:
        arquivo.write(f'{registro}' + os.linesep)
##########################################################


# CHAMA JSON API FREE BINANCE
def chamando_moedaBNB(moeda_BNB=''):
    valor = requests.get(
        f'https://api.binance.com/api/v3/ticker/24hr?symbol={moeda_BNB}')
    moeda = valor.json()
    global date_Binance
    date_Binance = round(float(moeda['closeTime']), 3)
##########################################################


# CHAMA JSON API FREE MERCADO BITCOIN
def chamando_moedaMB(moeda_MB='XRP'):
    valor = requests.get(
        f'https://www.mercadobitcoin.net/api/{moeda_MB}/ticker/')
    moeda = valor.json()
    global date_MB
    date_MB = round(float(moeda['ticker']['date']), 3)
##########################################################


# TAXAS DE CORRETORAS
def taxas():
    global taxa_compraBNB_Maker
    taxa_compraBNB_Maker = 0.075

    global taxa_vendaBNB_Maker
    taxa_vendaBNB_Maker = 0.075

    global taxa_compraMB_Maker
    taxa_compraMB_Maker = 0.7

    global taxa_vendaMB_Maker
    taxa_vendaMB_Maker = 0.7


# LÓGICA PARA COMPRA E VENDA MAKER
def calculo_MAKER(moeda='', porcentagem=0):

    global porcentagem_diferenca
    aumento = 0.2/100
    if venda_BNB > list_orderBook_BIDS:
        diferenca = venda_BNB - list_orderBook_BIDS
        porcentagem_diferenca = round(
            ((diferenca*100)/venda_BNB) - taxa_compraBNB_Maker - taxa_vendaMB_Maker, 3)

        if porcentagem_diferenca > porcentagem:
            registro_log(nome_arquivo=log_data, registro=f'{porcentagem_diferenca} // {oportunidade} //{hora} \n ORDEM de COMPRA {moeda} no MB por {round(list_orderBook_BIDS + (
                list_orderBook_BIDS*aumento), 4)} e ORDEM de VENDA no BNB por {round(venda_BNB - (venda_BNB*aumento), 4)}, diferença de {porcentagem_diferenca} % ')
            print(f'ORDEM de COMPRA {moeda} no MB por [orange]{round(list_orderBook_BIDS + (list_orderBook_BIDS*aumento), 4)}[/] e ORDEM de VENDA no BNB por {
                  round(venda_BNB - (venda_BNB*aumento), 4)}, diferença de [green]{porcentagem_diferenca} %[/] ')
        elif porcentagem_diferenca < porcentagem:
            print(f'Não comprar {moeda} no MB, diferença de [red]{
                  porcentagem_diferenca} %[/] ')

    if list_orderBook_ASKS > compra_BNB:
        diferenca = list_orderBook_ASKS - compra_BNB
        porcentagem_diferenca = round(
            ((diferenca*100)/list_orderBook_ASKS) - taxa_compraMB_Maker - taxa_vendaBNB_Maker, 3)

        if porcentagem_diferenca > porcentagem:

            registro_log(nome_arquivo=log_data,
                         registro=f'{porcentagem_diferenca} // {oportunidade} //{hora} \n ORDEM de COMPRA {moeda} na BNB por {round(compra_BNB + (compra_BNB*aumento), 4)} e vender no MB por {round(list_orderBook_ASKS(list_orderBook_ASKS*aumento), 4)}, diferença de {porcentagem_diferenca}% ')
            print(f'ORDEM de COMPRA {moeda} na BNB por {round(compra_BNB + (compra_BNB*aumento), 4)} e vender no MB por {
                  round(list_orderBook_ASKS(list_orderBook_ASKS*aumento), 4)}, diferença de {porcentagem_diferenca}% ')
        elif porcentagem_diferenca < porcentagem:
            print(f'Não comprar {moeda} na BNB, diferença de [red]{
                  porcentagem_diferenca} %[/] ')
###########################################################


# LÓGICA PARA COMPRA E VENDA TAKER
def calculo_TAKER(moeda='', porcentagem=0):

    global porcentagem_diferencaBNB
    global porcentagem_diferencaMB
    porcentagem_diferencaBNB = 0
    porcentagem_diferencaMB = 0
    diferencaBNB = 0.0
    diferencaMB = 0.0
    try:
        if venda_BNB < list_orderBook_BIDS:  # se tiver compradorMB > vendaBNB

            diferencaBNB = float(list_orderBook_BIDS - venda_BNB)
            porcentagem_diferencaBNB = (
                (diferencaBNB*100)/list_orderBook_BIDS) - taxa_compraBNB_Maker - taxa_vendaMB_Maker

            if porcentagem_diferencaBNB >= porcentagem:
                registro_log(nome_arquivo=log_data, registro=f'{porcentagem_diferencaBNB} // {oportunidade} //{hora} \n COMPRA TAKER ({moeda} na BNB por {
                             round(venda_BNB, 4)} e vender TAKER na MB por {round(list_orderBook_BIDS, 4)}, diferença de {porcentagem_diferencaBNB}% ')
                print(f'{porcentagem_diferencaBNB} // {oportunidade} //{hora} \n COMPRA TAKER ({moeda} na BNB por {round(
                    venda_BNB, 4)} e vender TAKER na MB por {round(list_orderBook_BIDS, 4)}, diferença de {porcentagem_diferencaBNB}% ')
            elif porcentagem_diferencaBNB <= porcentagem:
                print(f'Não comprar {moeda} no MB, diferença de [red]{
                      porcentagem_diferencaBNB} %[/] ')
        else:
            print('Nada em BNB')
            porcentagem_diferencaBNB = 0
    except:
        print('erro porcentagem')
        porcentagem_diferencaBNB = 0
    try:
        if list_orderBook_ASKS < compra_BNB:  # se tiver compradorBNB > vendaMB
            diferencaMB = 0.0
            diferencaMB = float(float(compra_BNB) - float(list_orderBook_ASKS))
            porcentagem_diferencaMB = (
                (diferencaMB*100)/compra_BNB) - taxa_compraMB_Maker - taxa_vendaBNB_Maker

            if porcentagem_diferencaMB >= porcentagem:
                registro_log(nome_arquivo=log_data, registro=f'{porcentagem_diferencaMB} // {oportunidade} //{hora} \n COMPRA TAKER ({moeda} no MB por {
                             round(list_orderBook_ASKS, 4)} e vender TAKER no BNB por {round(compra_BNB, 4)}, diferença de {porcentagem_diferencaMB}% ')
                print(f'{porcentagem_diferencaMB} // {oportunidade} //{hora} \n COMPRA TAKER ({moeda} no MB por {round(
                    list_orderBook_ASKS, 4)} e vender TAKER no MB por {round(compra_BNB, 4)}, diferença de {porcentagem_diferencaMB}% ')
            elif porcentagem_diferencaMB <= porcentagem:
                print(f'Não comprar {moeda} na BNB, diferença de [red]{
                      porcentagem_diferencaMB} %[/] ')
        else:
            print('Nada em MB')
            porcentagem_diferencaMB = 0
    except:
        print('erro porcentagem 2')
        porcentagem_diferencaMB = 0
 ##################################################

 ###############                                        ###############
 ###############                                        ###############
        ###     API REST BINANCE    ###
 ###############                                        ###############
 ###############                                        ###############


client_binance = Client_bnb(apiKey='apiKey',
                            secret='secret')


def get_orderbook(ultimas_ordens=0):

    info = client_binance.get_order_book(symbol='XRPBRL')

    global venda_BNB
    global compra_BNB
    venda_BNB = float(info['asks'][ultimas_ordens][0])
    compra_BNB = float(info['bids'][ultimas_ordens][0])
    # pprint(venda_BNB)
    # pprint(compra_BNB)


def get_my_orders(moeda='XRPBRL'):
    orders = client_binance.get_all_orders(symbol=moeda)
    pprint(orders)


def get_my_trades(moeda='XRPBRL'):
    trades = client_binance.get_my_trades(symbol=moeda)
    pprint(trades)


def get_order(quant, preco):
    client_binance.create_order(
        symbol='XRPBRL',
        side='SELL',
        type='LIMIT',
        timeInForce='GTC',
        quantity=quant,
        price=preco)


def ordem_market_sell(moeda='XRPBRL', quant=30):
    client_binance.order_market_sell(symbol=moeda, quantity=quant)


def ordem_market_buy(moeda='XRPBRL', quant=30):
    client_binance.order_market_buy(symbol=moeda, quantity=quant)


def ordem_limit_buy(moeda, quant, preco):
    client_binance.order_limit_buy(
        symbol=moeda,
        quantity=quant,
        price=preco)


def ordem_limit_sell(moeda, quant, preco):
    client_binance.order_limit_sell(
        symbol=moeda,
        quantity=quant,
        price=preco)
#####################################################################
#####################################################################
#####################################################################
#####################################################################


# IMPRIME HORA ATUAL DO SISTEMA
def imprimir_hora_atual():
    global hora
    global hora_timestamp
    hora = datetime.now()
    time_res = client_binance.get_server_time()
    hora_timestamp = datetime.timestamp(hora)
    hora = datetime.__format__(hora, "%H:%M:%S")
    print(f'############ {hora} ############')
##########################################################

# CHAMA TODA A LÓGICA


def chamando_exchanges(moeda=''):

    try:
        # chamando_moedaBNB(f'{moeda}BRL')
        # chamando_moedaMB(f'{moeda}')
        valores_API_MB(params=list_orderBook, moeda='BRLXRP')
        get_orderbook(0)  # get valores
        taxas()
        calculo_TAKER(moeda=f'{moeda}', porcentagem=0)

    except:
        print(error)
        print('*********  DEU RUIM.... tentando novamente ************')
##########################################################

# CRIAR UM TABELA NA TELA


def func_table():
    table.add_column('[bold]     XRP   [/]')
    table.add_column('[on white][black]   COMPRA [/]  ')
    table.add_column('[on white][black]   VENDA  [/]')
    table.add_row(('[on yellow][black][bold][center]   Binance   [/]'),
                  f'   {compra_BNB}', f'   {venda_BNB}')
    table.add_row('[on blue][black][bold] M. Bitcoin  [/]',
                  f'   {list_orderBook_BIDS}', f'   {list_orderBook_ASKS}')
    return table
##########################################################


###############                                        ###############
###############                                        ###############
    ###     API REST MERCADO BITCOIN    ###
###############                                        ###############
###############                                        ###############
moedaMB = ''
precoMB = ''
quantidadeMB = ''

list_orderBook = {
    'tapi_method': 'list_orderbook',
    'coin_pair': "BRLXRP"
}
info_account = {
    'tapi_method': 'get_account_info',
    'tapi_nonce': '1'
}


list_orders = {
    'tapi_method': 'list_orders',
    'tapi_nonce': '1',
    'coin_pair': moedaMB,
    'status_list': '[1, 2, 3, 4]',
    'has_fills': False
}

place_limit_sell = {'tapi_method': 'place_sell_order',
                    'tapi_nonce': '1',
                    'coin_pair': moedaMB,
                    'quantity': quantidadeMB,
                    'limit_price': precoMB,
                    'async': 'true'
                    }
place_limit_buy = {'tapi_method': 'place_buy_order',
                   'tapi_nonce': '1',
                   'coin_pair': moedaMB,
                   'quantity': quantidadeMB,
                   'limit_price': precoMB,
                   'async': 'true'
                   }

list_orderBook = urlencode(list_orderBook)
info_account = urlencode(info_account)
list_orders = urlencode(list_orders)
place_limit_sell = urlencode(place_limit_sell)
place_limit_buy = urlencode(place_limit_buy)


def valores_API_MB(params=list_orderBook):

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
        print('status: {}'.format(response_json['status_code']))

        if params == list_orderBook:  # ORDERBOOK
            global list_orderBook_ASKS
            global list_orderBook_BIDS
            global list_orderBook_TIME
            list_orderBook_ASKS = float(
                response_json['response_data']['orderbook']['asks'][0]['limit_price'])
            list_orderBook_BIDS = float(
                response_json['response_data']['orderbook']['bids'][0]['limit_price'])
            list_orderBook_TIME = float(response_json['server_unix_timestamp'])
            # pprint (list_orderBook_ASKS)
            # pprint (list_orderBook_BIDS)
            # pprint (f'Time: {list_orderBook_TIME}')

        if params == info_account:  # ACCOUNT INFO
            global get_account_info_BALANCE
            global get_account_info_WITHDRAWAL
            global get_account_info_TIME
            get_account_info_BALANCE = response_json['response_data']['balance']
            get_account_info_WITHDRAWAL = response_json['response_data']['withdrawal_limits']
            get_account_info_TIME = float(
                response_json['server_unix_timestamp'])
            # pprint(get_account_info_BALANCE)
            # pprint(get_account_info_WITHDRAWAL)
            # pprint(f'Time: {get_account_info_TIME}')
        # LIST ORDERS (1 : pending,2 : open,3 : canceled, 4 : filled )
        if params == list_orders:
            global list_ordersMB
            global list_orders_TIME
            list_ordersMB = response_json['response_data']['orders']
            list_orders_TIME = response_json['server_unix_timestamp']
            pprint(list_ordersMB)
            # pprint(list_orders_TIME)
        if params == place_limit_sell:
            pprint(response_json)

    finally:
        if conn:
            conn.close()
#####################################################################
#####################################################################
#####################################################################
#####################################################################

# VERIFICA SALDO EM MOEDA E FIAT


def check_saldo(saldoXRP=30, saldoBRL=200):
    try:
        saldoBNB_XRP = round(
            float(client_binance.get_asset_balance(asset='XRP')['free']), 5)
        saldoBNB_BRL = float(
            client_binance.get_asset_balance(asset='BRL')['free'])
        print(f' BNB  Saldo BRL: R$ {saldoBNB_BRL}')
        print(f' BNB  Saldo XRP: xrp {saldoBNB_XRP}')
        valores_API_MB(params=list_orderBook)
        saldoMB_XRP = round(
            float(get_account_info_BALANCE['xrp']['available']), 5)
        saldoMB_BRL = float(get_account_info_BALANCE['brl']['available'])
        print(f'  MB    Saldo BRL: R$ {saldoMB_BRL}')
        print(f'  MB    Saldo XRP: xrp {saldoMB_XRP}')
        if saldoBNB_XRP > saldoXRP and saldoMB_BRL > saldoBRL:
            return True
        else:
            return False
    except:
        print(error)
######################################################

# VERIFICA OPORTUNIDADE %


def diferenca_buysell(porcent=2):
    if porcentagem_diferencaMB >= porcent or porcentagem_diferencaBNB >= porcent:
        return True
    else:
        return False


# INICIA O PROGRAMA
if __name__ == '__main__':

    # apresentacao()
    oportunidade = 0

while True:
    try:
        # chamando_exchanges('XRP')
        # imprimir_hora_atual()
        # diferenca1 = date_MB - (date_Binance/1000)
        # registro_log(registro=f'diferença entre corretoras {diferenca1}', nome_arquivo='registro_time')

        # chamando_exchanges('XRP')
        list_orderBook = {
            'tapi_method': 'list_orderbook',
            'coin_pair': "BRLXRP"
        }
        list_orderBook = urlencode(list_orderBook)

        valores_API_MB(params=list_orderBook)
        get_orderbook(0)  # get valores
        taxas()
        imprimir_hora_atual()
        calculo_TAKER(moeda='XRP', porcentagem=0.5)
        quantidadeMoedas = '2'
        precoMB = str(list_orderBook_ASKS)
        quantidadeMB = '2'

        place_limit_buy = {'tapi_method': 'place_buy_order',
                           'tapi_nonce': '1',
                           'coin_pair': "BRLXRP",
                           'quantity': quantidadeMB,
                           'limit_price': precoMB,
                           'async': 'true'
                           }
        place_limit_buy = urlencode(place_limit_buy)
        info_ac = valores_API_MB(params=info_account)

        checkSaldo = check_saldo(saldoXRP=1, saldoBRL=7)
        check_diferenca = diferenca_buysell(porcent=0.1)
        if checkSaldo == True and check_diferenca == True:
            print('True')
            get_order(quant=quantidadeMoedas, preco=compra_BNB)  # venda BNB
            valores_API_MB(params=place_limit_buy)  # compra MB
            registro_log(nome_arquivo=log_actions, registro=f' XRP comprado R$ {
                         precoMB} e vendido R$ {compra_BNB} - {hora}')
            # print(get_order())

        else:
            print('False')

        console.print(func_table())
        table = None
        table = Table()

        sleep(3)
    except:
        print(error)
        print('Não deu....')
        sleep(3)

# valores_API_MB(params=place_limit_sell,moeda='BRLXRP',preco='6.0',quant='1.0')
# sleep(3)
''' try:
    sell_limit = client_binance.create_order(
        symbol='XRPBRL',
        side='SELL',
        type='LIMIT',
        timeInForce='GTC',
        quantity=5,
        price=7)
    print(sell_limit)
except BinanceAPIException as e:
    # error handling goes here
    print(e)
except BinanceOrderException as e:
    # error handling goes here
    print(e)
 '''
