#######################################################################
#                                                                    #
#           VERSÃO 0.1 REQUEST API VIA HTTP SIMPLES                  #
#                                                                    #
#                                                                    #
######################################################################

from time import sleep
from tkinter.constants import NONE, S
import requests
from pprint import pprint
from datetime import datetime
from requests.api import get 
from rich import print
from rich.table import Table
#from utilidades import apresentacao
from rich.console import Console
import os


table = Table(title= 'PAINEL') 
console = Console()




##  ########################################################    
def chamando_moeda(moeda = ''):
    # VARIAVEIS

    global venda_BNB
    global compra_BNB
    global timestamp_BNB

    global venda_MB
    global compra_MB
    global timestamp_MB

    global venda_DAX
    global compra_DAX
    global timestamp_DAX
    
    global venda_HB
    global compra_HB
    global timestamp_HB
    
    valor_BNB = requests.get(f'https://api.binance.com/api/v3/ticker/24hr?symbol={moeda}BRL')
    ticker_BNB = valor_BNB.json()
    venda_BNB = float(ticker_BNB['askPrice'])
    compra_BNB = float(ticker_BNB['bidPrice'])
    #print(venda_BNB)
    #print(compra_BNB)
    
    valor_MB = requests.get(f'https://www.mercadobitcoin.net/api/{moeda}/ticker/')
    ticker_MB = valor_MB.json()
    venda_MB = float(ticker_MB['ticker']['sell'])
    compra_MB = float(ticker_MB['ticker']['buy'])
    #print(venda_MB)
    #print(compra_MB)
    
    valor_DAX = requests.get(f'https://api.novadax.com/v1/market/ticker?symbol={moeda}_BRL')
    ticker_DAX = valor_DAX.json()
    venda_DAX = float(ticker_DAX['data']['ask'])
    compra_DAX = float(ticker_DAX['data']['bid']) 
    #print(venda_DAX)
    #print(compra_DAX)
    
    valor_HB = requests.get(f'https://api.huobi.pro/market/detail/merged?symbol=xrpusdt')
    ticker_HB = valor_HB.json()
    #venda_HB = float(ticker_HB['tick']['ask'])
    #compra_HB = float(ticker_HB['tick']['bid']) 
    #print(ticker_HB)
    #print(compra_HB)
    
    
##########################################################      
log_data = 'registro_data_comparador'
log_actions = 'registro_acoes_comparador'

# CRIAR ARQUIVO TXT COM INFORMAÇÕES E REGISTRA
def registro_log(nome_arquivo = 'log', registro = ''):
    log_data = 'registro_data'
    log_actions = 'registro_acoes'

    with open(f'{nome_arquivo}.txt','a', newline='') as arquivo:
        arquivo.write(f'{registro}' + os.linesep)
##########################################################  
# IMPRIME HORA ATUAL DO SISTEMA
def imprimir_hora_atual():
    global hora 
    global hora_timestamp
    hora = datetime.now()
    #time_res = client_binance.get_server_time()
    hora_timestamp = datetime.timestamp(hora)
    hora = datetime.__format__(hora, "%H:%M:%S")
    print(f'############ {hora} ############')        
##########################################################  
########################################################## 
def taxas():
    global taxa_compraBNB_Maker
    taxa_compraBNB_Maker = 0.1    
    
    global taxa_vendaBNB_Maker
    taxa_vendaBNB_Maker = 0.1
        
    global taxa_compraMB_Maker
    taxa_compraMB_Maker = 0.7   
    
    global taxa_vendaMB_Maker
    taxa_vendaMB_Maker = 0.7    
 
    global taxa_compraDAX_Maker
    taxa_compraDAX_Maker = 0.4   
    
    global taxa_vendaDAX_Maker
    taxa_vendaDAX_Maker = 0.4   
    
##########################################################    
# LÓGICA PARA COMPRA E VENDA TAKER                        
def calculo_TAKER(moeda = '', porcentagem = 0, exchanges=''):
    # BNB_MB // BNB_DAX // MB_DAX
    
    global porcentagem_diferencaBNB 
    global porcentagem_diferencaMB 
    porcentagem_diferencaBNB  = 0  
    porcentagem_diferencaMB = 0
    diferencaBNB = 0.0
    diferencaMB = 0.0
    
    if exchanges=='BNB_MB':
        try:
            if venda_BNB < compra_MB:  ##  se tiver compradorMB > vendaBNB 
            
                diferencaBNB = float(compra_MB - venda_BNB)
                porcentagem_diferencaBNB = ((diferencaBNB*100)/compra_MB) - taxa_compraBNB_Maker - taxa_vendaMB_Maker
                
                if porcentagem_diferencaBNB >= porcentagem:
                    registro_log(nome_arquivo= log_data,registro = f'{porcentagem_diferencaBNB} // {hora} \n COMPRA TAKER ({moeda} na BNB por {round(venda_BNB,4)} e vender TAKER na MB por {round(compra_MB,4)}, diferença de {porcentagem_diferencaBNB}% ')
                    print(f'COMPRA TAKER ({moeda} na BNB por {round(venda_BNB,4)} e vender TAKER na MB por {round(compra_MB,4)}, diferença de {porcentagem_diferencaBNB}% ')
                elif porcentagem_diferencaBNB <= porcentagem:
                    print(f'DIFERENÇA BNB-MB [red]{porcentagem_diferencaBNB} %[/] ')   
            else: 
                print('Nada em BNB')   
                porcentagem_diferencaBNB  = 0 
        except: 
            print('erro porcentagem')
            porcentagem_diferencaBNB  = 0  
        try:     
            if venda_MB < compra_BNB: ## se tiver compradorBNB > vendaMB
                diferencaMB =0.0
                diferencaMB =  float(float(compra_BNB) - float(venda_MB))
                porcentagem_diferencaMB = ((diferencaMB*100)/compra_BNB )- taxa_compraMB_Maker - taxa_vendaBNB_Maker
                
                if porcentagem_diferencaMB >= porcentagem:
                    registro_log(nome_arquivo= log_data, registro = f'{porcentagem_diferencaMB}  // {hora} \n COMPRA TAKER ({moeda} no MB por {round(venda_MB,4)} e vender TAKER no BNB por {round(compra_BNB,4)}, diferença de {porcentagem_diferencaMB}% ')
                    print( f'COMPRA TAKER ({moeda} no MB por {round(venda_MB,4)} e vender TAKER no MB por {round(compra_BNB,4)}, diferença de {porcentagem_diferencaMB}% ')
                elif porcentagem_diferencaMB <= porcentagem:
                    print(f'DIFERENÇA BNB-MB [red]{porcentagem_diferencaMB} %[/] ') 
            else: 
                print('Nada em MB')
                porcentagem_diferencaMB = 0
        except:
            print('erro porcentagem 2')
            porcentagem_diferencaMB = 0
    elif exchanges=='BNB_DAX':
        try:
            if venda_BNB < compra_DAX:  ##  se tiver compradorDAX > vendaBNB 
            
                diferencaBNB = float(compra_DAX - venda_BNB)
                porcentagem_diferencaBNB = ((diferencaBNB*100)/compra_DAX) - taxa_compraBNB_Maker - taxa_vendaDAX_Maker
                
                if porcentagem_diferencaBNB >= porcentagem:
                    registro_log(nome_arquivo= log_data,registro = f'{porcentagem_diferencaBNB} // {hora} \n COMPRA TAKER ({moeda} na BNB por {round(venda_BNB,4)} e vender TAKER na DAX por {round(compra_DAX,4)}, diferença de {porcentagem_diferencaBNB}% ')
                    print(f'COMPRA TAKER ({moeda} na BNB por {round(venda_BNB,4)} e vender TAKER na DAX por {round(compra_DAX,4)}, diferença de {porcentagem_diferencaBNB}% ')
                elif porcentagem_diferencaBNB <= porcentagem:
                    print(f'DIFERENÇA BNB-DAX [red]{porcentagem_diferencaBNB} %[/] ')   
            else: 
                print('Nada em BNB')   
                porcentagem_diferencaBNB  = 0 
        except: 
            print('erro porcentagem')
            porcentagem_diferencaBNB  = 0  
        try:     
            if venda_DAX < compra_BNB: ## se tiver compradorBNB > vendaDAX
                diferencaDAX =0.0
                diferencaDAX =  float(float(compra_BNB) - float(venda_DAX))
                porcentagem_diferencaDAX = ((diferencaDAX*100)/compra_BNB )- taxa_compraDAX_Maker - taxa_vendaBNB_Maker
                
                if porcentagem_diferencaDAX >= porcentagem:
                    registro_log(nome_arquivo= log_data, registro = f'{porcentagem_diferencaDAX}  // {hora} \n COMPRA TAKER ({moeda} no DAX por {round(venda_DAX,4)} e vender TAKER no BNB por {round(compra_BNB,4)}, diferença de {porcentagem_diferencaDAX}% ')
                    print( f'COMPRA TAKER ({moeda} no DAX por {round(venda_DAX,4)} e vender TAKER no DAX por {round(compra_BNB,4)}, diferença de {porcentagem_diferencaDAX}% ')
                elif porcentagem_diferencaDAX <= porcentagem:
                    print(f'DIFERENÇA BNB-DAX [red]{porcentagem_diferencaDAX} %[/] ') 
            else: 
                print('Nada em DAX')
                porcentagem_diferencaDAX = 0
        except:
            print('erro porcentagem 2')
            porcentagem_diferencaDAX = 0 
    
    elif exchanges=='MB_DAX':
        try:
            if venda_MB < compra_DAX:  ##  se tiver compradorDAX > vendaMB 
            
                diferencaMB = float(compra_DAX - venda_MB)
                porcentagem_diferencaMB = ((diferencaMB*100)/compra_DAX) - taxa_compraMB_Maker - taxa_vendaDAX_Maker
                
                if porcentagem_diferencaMB >= porcentagem:
                    registro_log(nome_arquivo= log_data,registro = f'{porcentagem_diferencaMB} // {hora} \n COMPRA TAKER ({moeda} na MB por {round(venda_MB,4)} e vender TAKER na DAX por {round(compra_DAX,4)}, diferença de {porcentagem_diferencaMB}% ')
                    print(f'COMPRA TAKER ({moeda} na MB por {round(venda_MB,4)} e vender TAKER na DAX por {round(compra_DAX,4)}, diferença de {porcentagem_diferencaMB}% ')
                elif porcentagem_diferencaMB <= porcentagem:
                    print(f'DIFERENÇA MB-DAX [red]{porcentagem_diferencaMB} %[/] ')   
            else: 
                print('Nada em MB')   
                porcentagem_diferencaMB  = 0 
        except: 
            print('erro porcentagem')
            porcentagem_diferencaMB  = 0  
        try:     
            if venda_DAX < compra_MB: ## se tiver compradorMB > vendaDAX
                diferencaDAX =0.0
                diferencaDAX =  float(float(compra_MB) - float(venda_DAX))
                porcentagem_diferencaDAX = ((diferencaDAX*100)/compra_MB )- taxa_compraDAX_Maker - taxa_vendaMB_Maker
                
                if porcentagem_diferencaDAX >= porcentagem:
                    registro_log(nome_arquivo= log_data, registro = f'{porcentagem_diferencaDAX}  // {hora} \n COMPRA TAKER ({moeda} no DAX por {round(venda_DAX,4)} e vender TAKER no MB por {round(compra_MB,4)}, diferença de {porcentagem_diferencaDAX}% ')
                    print( f' COMPRA TAKER ({moeda} no DAX por {round(venda_DAX,4)} e vender TAKER no DAX por {round(compra_MB,4)}, diferença de {porcentagem_diferencaDAX}% ')
                elif porcentagem_diferencaDAX <= porcentagem:
                    print(f'DIFERENÇA MB-DAX [red]{porcentagem_diferencaDAX} %[/] ') 
            else: 
                print(f'Nada em DAX')
                porcentagem_diferencaDAX = 0
        except:
            print('erro porcentagem 2')
            porcentagem_diferencaDAX = 0               
    ##################################################
            
##########################################################
def imprimir_hora_atual():
    global hora
    hora = datetime.now()
    hora = datetime.__format__(hora, "%H:%M:%S")
    print(f'############ {hora} ############')    
      
##########################################################

##########################################################       
def func_table():
    table.add_column('[bold]     XRP   [/]')
    table.add_column('[on white][black]   COMPRA [/]  ')
    table.add_column('[on white][black]   VENDA  [/]')
    table.add_row(('[on yellow][black][bold][center]   Binance   [/]'), f'   {compra_BNB}',f'   {venda_BNB}')
    table.add_row('[on blue][black][bold] M. Bitcoin  [/]', f'   {compra_MB}',f'   {venda_MB}')
    table.add_row('[on white][black][bold] NovaDax  [/]', f'   {compra_DAX}',f'   {venda_DAX}')
    
    return table




if __name__=='__main__':
    
       
       
    #apresentacao()
   
      
    while True:
            try:
                chamando_moeda('XRP')
                taxas()
                imprimir_hora_atual()
                print('')
                calculo_TAKER(moeda='XRP', porcentagem = 0.1,exchanges='BNB_MB')
                print('')
                calculo_TAKER(moeda='XRP', porcentagem = 0.1,exchanges='BNB_DAX')
                print('')
                calculo_TAKER(moeda='XRP', porcentagem = 0.1,exchanges='MB_DAX')
                console.print(func_table())
              
                table = None
                table = Table()
                sleep(3)
            except: print('Não deu....')
  
 