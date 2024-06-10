#######################################################################
#                                                                    #
#           VERSÃO 0.1 REQUEST API VIA HTTP SIMPLES                  #
#                                                                    #
#                                                                    #
######################################################################

from logging import error
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

lista_moedaBNB= 'XRPUSDT','SOLUSDT','SHIBUSDT','LUNAUSDT','FILUSDT','ETHUSDT','DYDXUSDT','DOTUSDT','DOGEUSDT','BTCUSDT','ADAUSDT'
lista_moedaHB= 'xrpusdt','solusdt','shibusdt','lunausdt','filusdt','ethusdt','dydxusdt','dotusdt','dogeusdt','btcusdt','adausdt'
set_moeda = 10
select_moedaBNB = lista_moedaBNB[set_moeda]
select_moedaHB = lista_moedaHB[set_moeda]


##  ########################################################    
def chamando_moeda(moedaBNB = '', moedaHB = ''):
    # VARIAVEIS

    global venda_BNB
    global compra_BNB
    global timestamp_BNB
    
    global venda_HB
    global compra_HB
    global timestamp_HB
    
    valor_BNB = requests.get(f'https://api.binance.com/api/v3/ticker/24hr?symbol={moedaBNB}')
    ticker_BNB = valor_BNB.json()
    venda_BNB = float(ticker_BNB['askPrice'])
    compra_BNB = float(ticker_BNB['bidPrice'])
    #print('venda_BNB')
    #print(compra_BNB)
    
    
    valor_HB = requests.get(f'https://api.huobi.pro/market/detail/merged?symbol={moedaHB}')
    ticker_HB = valor_HB.json()
    venda_HB = float(ticker_HB['tick']['ask'][0])
    compra_HB = float(ticker_HB['tick']['bid'][0]) 
    #pprint(venda_HB)
    #print(compra_HB)
    
    
##########################################################      
log_data = 'registro_dataBNBHB'
log_actions = 'registro_acoesBNBHB'

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
             
    global taxa_compraHB_Maker
    taxa_compraHB_Maker = 0.2   
    
    global taxa_vendaHB_Maker
    taxa_vendaHB_Maker = 0.2  
    
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
    
    
    if exchanges=='BNB_HB':
        try:
            if venda_BNB < compra_HB:  ##  se tiver compradorHB > vendaBNB 
            
                diferencaBNB = float(compra_HB - venda_BNB)
                porcentagem_diferencaBNB = ((diferencaBNB*100)/compra_HB) - taxa_compraBNB_Maker - taxa_vendaHB_Maker
                
                if porcentagem_diferencaBNB >= porcentagem:
                    imprimir_hora_atual()
                    registro_log(nome_arquivo= log_data,registro = f'{porcentagem_diferencaBNB} // {hora} \n COMPRA TAKER ({moeda} na BNB por {round(venda_BNB,4)} e vender TAKER na HB por {round(compra_HB,4)}, diferença de {porcentagem_diferencaBNB}% ')
                    print(f'COMPRA TAKER ({moeda} na BNB por {round(venda_BNB,4)} e vender TAKER na HB por {round(compra_HB,4)}, diferença de {porcentagem_diferencaBNB}% ')
                elif porcentagem_diferencaBNB <= porcentagem:
                    print(f'DIFERENÇA BNB-HB [red]{porcentagem_diferencaBNB} %[/] ')   
            else: 
                print('Nada em BNB')   
                porcentagem_diferencaBNB  = 0 
        except: 
            print('erro porcentagem')
            porcentagem_diferencaBNB  = 0  
        try:     
            if venda_HB < compra_BNB: ## se tiver compradorBNB > vendaHB
                diferencaHB =0.0
                diferencaHB =  float(compra_BNB - venda_HB)
                porcentagem_diferencaHB = ((diferencaHB*100)/compra_BNB )- taxa_compraHB_Maker - taxa_vendaBNB_Maker
                
                if porcentagem_diferencaHB >= porcentagem:
                    imprimir_hora_atual()
                    registro_log(nome_arquivo= log_data, registro = f'{porcentagem_diferencaHB}  // {hora} \n COMPRA TAKER ({moeda} no HB por {round(venda_HB,4)} e vender TAKER no BNB por {round(compra_BNB,4)}, diferença de {porcentagem_diferencaHB}% ')
                    print( f' COMPRA TAKER ({moeda} no HB por {round(venda_HB,4)} e vender TAKER no HB por {round(compra_BNB,4)}, diferença de {porcentagem_diferencaHB}% ')
                elif porcentagem_diferencaHB <= porcentagem:
                    print(f'DIFERENÇA BNB-HB [red]{porcentagem_diferencaHB} %[/] ') 
            else: 
                print('Nada em HB')
                porcentagem_diferencaHB = 0
        except:
            print('erro porcentagem 2')
            porcentagem_diferencaHB = 0          
    ##################################################
            
##########################################################
  
      
##########################################################

##########################################################       
def func_table(moeda = ''):
    table.add_column(f'[bold]    {select_moedaBNB}  [/]')
    table.add_column('[on white][black]   COMPRA [/]  ')
    table.add_column('[on white][black]   VENDA  [/]')
    table.add_row(('[on yellow][black][bold][center]   Binance   [/]'), f'   {compra_BNB}',f'   {venda_BNB}')
    table.add_row('[white][bold] Huobi  [/]', f'   {compra_HB}',f'   {venda_HB}')
    
    return table



if __name__=='__main__':
    
       
       
    #apresentacao()
   
    
    while True:
            try:
                
                
                chamando_moeda(moedaBNB=f'{select_moedaBNB}', moedaHB=f'{select_moedaHB}')
                taxas()
                imprimir_hora_atual()
                print('')
                calculo_TAKER(moeda= f'{select_moedaBNB}', porcentagem = 0,exchanges='BNB_HB')
                console.print(func_table())
              
                table = None
                table = Table()
                sleep(3)
            except: 
                print(error)
                print('Não deu....')
  
 