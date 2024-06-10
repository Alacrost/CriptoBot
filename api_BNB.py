from binance import Client      
from pprint import pprint
from binance.enums import*

client = Client(api_key= '******************************',api_secret= '********************************',testnet= False)



def get_orderbook(ultimas_ordens = 0):
    info = client.get_order_book(symbol='XRPBRL')
    
    global venda_BNB 
    global compra_BNB 
    venda_BNB = float(info['asks'][ultimas_ordens][0])
    compra_BNB = float(info['bids'][ultimas_ordens][0])
    pprint(venda_BNB)
    pprint(compra_BNB)

def get_order(moeda='',side='',type='',quantidade=0):
        client.create_test_order(
        symbol = moeda,
        side = side,
        type = type,
        quantity = quantidade
        )

def get_my_orders():
    orders = client.get_all_orders(symbol='XRPBRL')
    pprint(orders)

def get_my_trades():
    trades = client.get_my_trades(symbol='XRPBRL')
    pprint(trades)


def check_saldo():
    saldoBNB_XRP = client.get_asset_balance(asset='BNB')['free']
    saldoBNB_BRL = client.get_asset_balance(asset='BRL')['free']
    print(f' Saldo BRL: R$ {saldoBNB_BRL}')
    print(f' Saldo XRP: xrp {saldoBNB_XRP}')
    
check_saldo()

