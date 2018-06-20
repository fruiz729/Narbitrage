import numpy as np
import time
import math
import csv
from binance.enums import *
from binance.client import Client
import sys

api_key = 'sPk9hkYh1NWH30fVsmDJccUb0xhSK02h2xOCL4Rjm8Splw3cveN95f2BrYyzXlwa'
api_secret = 'Gdc47Iq3fi2WpN52LGivX5UnSX4oEfyfF4qDa9TfZ5daVOqNdwcKqHRb0ZFu3j3G'
client = Client(api_key, api_secret)
time_res = client.get_server_time()

symbols = ['BTCUSDT', 'ETHBTC', 'ETHUSDT']

#enter the theoretical liquid capital available
#liquid = 100.00 #keep decimal to make it a float

liquid = 15.00 # minimum trading is 10 USD; trading 15

t0 = time.time()
order_books = {}
for coin in symbols:
    order_books[coin] = client.get_order_book(symbol=coin)

t_book = time.time()

##################################################################
#BID PRICE FOR BTCUSDT MARKET - MUST MATCH WHEN TRADING USDT -> BTC

price_usdtbtc0 = float(order_books['BTCUSDT']['bids'][0][0])
price_usdtbtc1 = float(order_books['BTCUSDT']['bids'][1][0])
price_usdtbtc2 = float(order_books['BTCUSDT']['bids'][2][0])

qty_usdtbtc0 = float(order_books['BTCUSDT']['bids'][0][1])       
qty_usdtbtc1 = float(order_books['BTCUSDT']['bids'][1][1])
qty_usdtbtc2 = float(order_books['BTCUSDT']['bids'][2][1])

if qty_usdtbtc0 >= liquid/price_usdtbtc0:
    wprice_usdtbtc = price_usdtbtc0
    tot_qty_usdtbtc = qty_usdtbtc0
elif (qty_usdtbtc0 + qty_usdtbtc1) >= liquid/np.average([price_usdtbtc0,price_usdtbtc1],
                    weights = [qty_usdtbtc0,(qty_usdtbtc1)]):
    wprice_usdtbtc = np.average([price_usdtbtc0,price_usdtbtc1],
                    weights = [qty_usdtbtc0, (liquid-(qty_usdtbtc0*price_usdtbtc0))/price_usdtbtc1])                                                 
    tot_qty_usdtbtc = qty_usdtbtc0 + qty_usdtbtc1
elif (qty_usdtbtc0 + qty_usdtbtc1 + qty_usdtbtc2) >= liquid/np.average([price_usdtbtc0,price_usdtbtc1,price_usdtbtc2],
      weights = [qty_usdtbtc0,qty_usdtbtc1, (liquid - (qty_usdtbtc0/price_usdtbtc0)+(qty_usdtbtc1/price_usdtbtc1))/price_usdtbtc2]):

    wprice_usdtbtc = np.average([price_usdtbtc0,price_usdtbtc1,price_usdtbtc2],
                    weights = [qty_usdtbtc0,qty_usdtbtc1,(liquid - (qty_usdtbtc0/price_usdtbtc0)+(qty_usdtbtc1/price_usdtbtc1))/price_usdtbtc2])
    tot_qty_usdtbtc = qty_usdtbtc0 + qty_usdtbtc1 + qty_usdtbtc2
else:
    wprice_usdtbtc = price_usdtbtc0
    tot_qty_usdtbtc = 0.0
    print ('FUCK IT - not enough quantity in BTCUSDT Bids to go USDT --> BTC')
    
###########################################################################################################################################
#ASK PRICE FOR BTCUSDT MARKET - MUST MATCH WHEN TRADING BTC -> USDT

price_btcusdt0 = float(order_books['BTCUSDT']['asks'][0][0])
price_btcusdt1 = float(order_books['BTCUSDT']['asks'][1][0])
price_btcusdt2 = float(order_books['BTCUSDT']['asks'][2][0])

qty_btcusdt0 = float(order_books['BTCUSDT']['asks'][0][1])       
qty_btcusdt1 = float(order_books['BTCUSDT']['asks'][1][1])
qty_btcusdt2 = float(order_books['BTCUSDT']['asks'][2][1])

if qty_btcusdt0 >= liquid/price_btcusdt0:
    wprice_btcusdt = price_btcusdt0
    tot_qty_btcusdt = qty_btcusdt0
elif (qty_btcusdt0 + qty_btcusdt1) >= liquid/np.average([price_btcusdt0,price_btcusdt1],
                    weights = [qty_btcusdt0,(liquid-(qty_btcusdt0*price_btcusdt0))/price_btcusdt1]):
    wprice_btcusdt = np.average([price_btcusdt0,price_btcusdt1],
                    weights = [qty_btcusdt0,(liquid-(qty_btcusdt0*price_btcusdt0))/price_btcusdt1])
    
    tot_qty_btcusdt = qty_btcusdt0 + qty_btcusdt1
elif (qty_btcusdt0 + qty_btcusdt1 + qty_btcusdt2) >=  liquid/np.average([price_btcusdt0,price_btcusdt1,price_btcusdt2],
                    weights = [qty_btcusdt0,qty_btcusdt1,(liquid - (qty_btcusdt0*price_btcusdt0)+(qty_btcusdt1*price_btcusdt1))/price_btcusdt2]):
    wprice_btcusdt = np.average([price_btcusdt0,price_btcusdt1,price_btcusdt2],
                    weights = [qty_btcusdt0,qty_btcusdt1,(liquid -(qty_btcusdt0*price_btcusdt0)+(qty_btcusdt1*price_btcusdt1))/price_btcusdt2])

    tot_qty_btcusdt = qty_btcusdt0 + qty_btcusdt1 + qty_btcusdt2
else:
    wprice_btcusdt = price_btcusdt0
    tot_qty_btcusdt = 0.0
    print ('FUCK IT - not enough quantity in BTCUSDT ASKS to go BTC --> USDT')
#############################################################################################################################
##BID PRICES FOR ETHUSDT MARKET - MUST MATCH WHEN TRADING USDT -> ETH

price_usdteth0 = float(order_books['ETHUSDT']['bids'][0][0])
price_usdteth1 = float(order_books['ETHUSDT']['bids'][1][0])
price_usdteth2 = float(order_books['ETHUSDT']['bids'][2][0])

qty_usdteth0 = float(order_books['ETHUSDT']['bids'][0][1])
qty_usdteth1 = float(order_books['ETHUSDT']['bids'][1][1])
qty_usdteth2 = float(order_books['ETHUSDT']['bids'][2][1])

if qty_usdteth0 >= liquid/price_usdteth0:
    wprice_usdteth = price_usdteth0
    tot_qty_usdteth = qty_usdteth0
elif (qty_usdteth0 + qty_usdteth1) >= liquid/np.average([price_usdteth0,price_usdteth1],
                    weights = [qty_usdteth0,(liquid - (qty_usdteth0*price_usdteth0))/price_usdteth1]):
    wprice_usdteth = np.average([price_usdteth0,price_usdteth1],
                    weights = [qty_usdteth0, (liquid -(qty_usdteth0*price_usdteth0))/price_usdteth1])
   
    tot_qty_usdteth = qty_usdteth0 + qty_usdteth1
elif (qty_usdteth0 + qty_usdteth1 + qty_usdteth2) >=  liquid/np.average([price_usdteth0,price_usdteth1,price_usdteth2],
                    weights = [qty_usdteth0,qty_usdteth1,(liquid-(qty_usdteth0*price_usdteth0)+(qty_usdteth1*price_usdteth1))/price_usdteth2]):
    wprice_usdteth = np.average([price_usdteth0,price_usdteth1,price_usdteth2],
                    weights = [qty_usdteth0,qty_usdteth1,(liquid - (qty_usdteth0*price_usdteth0) + (qty_usdteth1*price_usdteth1))/price_usdteth2])


    tot_qty_usdteth = qty_usdteth0 + qty_usdteth1 + qty_usdteth2
else:
    wprice_usdteth = price_usdteth0
    tot_qty_usdteth = 0.0
    print ('FUCK IT - not enough quantity in usdteth ASKS to go USDT --> ETH')


############################################################################################################################
##ASK PRICES FOR ETHUSDT MARKET - MUST MATCH WHEN TRADING ETH -> USDT

price_ethusdt0 = float(order_books['ETHUSDT']['asks'][0][0])
price_ethusdt1 = float(order_books['ETHUSDT']['asks'][1][0])
price_ethusdt2 = float(order_books['ETHUSDT']['asks'][2][0])

qty_ethusdt0 = float(order_books['ETHUSDT']['asks'][0][1])
qty_ethusdt1 = float(order_books['ETHUSDT']['asks'][1][1])
qty_ethusdt2 = float(order_books['ETHUSDT']['asks'][2][1])

if qty_ethusdt0 >= liquid/price_ethusdt0:
    wprice_ethusdt = price_ethusdt0
    tot_qty_ethusdt = qty_ethusdt0
elif (qty_ethusdt0 + qty_ethusdt1) >= liquid/np.average([price_ethusdt0,price_ethusdt1],
                    weights = [qty_ethusdt0, (liquid - (qty_ethusdt0*price_ethusdt0))/price_ethusdt1]):
    wprice_ethusdt = np.average([price_ethusdt0,price_ethusdt1],
                    weights = [qty_ethusdt0,(liquid - (qty_ethusdt0*price_ethusdt0))/price_ethusdt1])

    tot_qty_ethusdt = qty_ethusdt0 + qty_ethusdt1
elif (qty_ethusdt0 + qty_ethusdt1 + qty_ethusdt2) >=  liquid/np.average([price_ethusdt0,price_ethusdt1,price_ethusdt2],
                    weights = [qty_ethusdt0,qty_ethusdt1,(liquid - (qty_ethusdt0*price_ethusdt0) + (qty_ethusdt1*price_ethusdt1))/price_ethusdt2]):
    wprice_ethusdt = np.average([price_ethusdt0,price_ethusdt1,price_ethusdt2],
                    weights = [qty_ethusdt0,qty_ethusdt1, (liquid - (qty_ethusdt0*price_ethusdt0) + (qty_ethusdt1*price_ethusdt1))/price_ethusdt2])

    tot_qty_ethusdt = qty_ethusdt0 + qty_ethusdt1 + qty_ethusdt2
else:
    wprice_ethusdt = price_ethusdt0
    tot_qty_ethusdt = 0.0
    print ('FUCK IT - not enough quantity in ethusdt ASKS to go ETH --> USDT')

############################################################################################################################
#BID PRICE FOR ETHBTC MARKET - MUST MATCH WHEN TRADING BTC -> ETH

price_btceth0 = float(order_books['ETHBTC']['bids'][0][0])
price_btceth1= float(order_books['ETHBTC']['bids'][1][0])
price_btceth2 = float(order_books['ETHBTC']['bids'][2][0])

qty_btceth0 = float(order_books['ETHBTC']['bids'][0][1])
qty_btceth1 = float(order_books['ETHBTC']['bids'][1][1])
qty_btceth2 = float(order_books['ETHBTC']['bids'][2][1])

if qty_btceth0*price_btceth0 >= liquid/wprice_usdtbtc:
    wprice_btceth = price_btceth0
    tot_qty_btceth = qty_btceth0
elif (qty_btceth0+qty_btceth1)*np.average([price_btceth0, price_btceth1],weights = [qty_btceth0*price_btceth0, (liquid/wprice_usdtbtc)-(qty_btceth0*price_btceth0)])>= liquid/wprice_usdtbtc:
    wprice_btceth = np.average([price_btceth0,price_btceth1], weights = [qty_btceth0*price_btceth0, (liquid/wprice_usdtbtc)-(qty_btceth0*price_btceth0)])
    tot_qty_btceth = qty_btceth0 + qty_btceth1                                          
elif (qty_btceth0 + qty_btceth1 + qty_btceth2)*np.average([price_btceth0, price_btceth1, price_btceth2], weights = [qty_btceth0*price_btceth0,qty_btceth1*price_btceth1, liquid/wprice_usdtbtc-(qty_btceth0*price_btceth0 + qty_btceth1*price_btceth1)]) >= liquid/wprice_usdtbtc:

    wprice_btceth = np.average([price_btceth0,price_btceth1,price_btceth2],
                    weights = [qty_btceth0,qty_btceth1,liquid/wprice_usdtbtc - (qty_btceth0*price_btceth0 + qty_btceth1*price_btceth1)])

    tot_qty_btceth = qty_btceth0 + qty_btceth1 + qty_btceth2
else:
    wprice_btceth = price_btceth0
    tot_qty_btceth = 0.0
    print ('FUCK IT - not enough quantity in btceth ASKS to go BTC --> ETH')

################################################################################################################################
#ASK PRICES FOR ETHBTC MARKET - MUST MATCH WHEN TRADING ETH -> BTC

price_ethbtc0 = float(order_books['ETHBTC']['asks'][0][0])
price_ethbtc1= float(order_books['ETHBTC']['asks'][1][0])
price_ethbtc2 = float(order_books['ETHBTC']['asks'][2][0])

qty_ethbtc0 = float(order_books['ETHBTC']['asks'][0][1])
qty_ethbtc1 = float(order_books['ETHBTC']['asks'][1][1])
qty_ethbtc2 = float(order_books['ETHBTC']['asks'][2][1])

if qty_ethbtc0 >= (liquid/wprice_usdteth):
    wprice_ethbtc = price_ethbtc0
    tot_qty_ethbtc = qty_ethbtc0
elif (qty_ethbtc0 + qty_ethbtc1) >= (liquid/wprice_usdteth):
    wprice_ethbtc = np.average([price_ethbtc0,price_ethbtc1],
                    weights = [qty_ethbtc0,(liquid/wprice_usdteth)-qty_ethbtc0])

    tot_qty_ethbtc = qty_ethbtc0 + qty_ethbtc1
elif (qty_ethbtc0 + qty_ethbtc1 + qty_ethbtc2)>=(liquid/wprice_usdteth):
    wprice_ethbtc = np.average([price_ethbtc0,price_ethbtc1,price_ethbtc2],
                    weights = [qty_ethbtc0,qty_ethbtc1,(liquid/wprice_usdteth) - (qty_ethbtc0+qty_ethbtc1)])
    tot_qty_ethbtc = qty_ethbtc0 + qty_ethbtc1 + qty_ethbtc2
else:
    wprice_ethbtc = price_ethbtc0
    tot_qty_ethbtc = 0.0
    print ('FUCK IT - not enough quantity in ethbtc ASKS to go ETH --> BTC')

t_calc = time.time()

#f_btc = wprice_usdteth/wprice_ethbtc
#f_eth = wprice_usdtbtc*wprice_btceth
#d_btc = f_btc - wprice_usdtbtc
#d_eth = f_eth - wprice_usdteth

f_btc_liquid = ((liquid/wprice_usdteth)*wprice_ethbtc)*wprice_btcusdt
f_eth_liquid = ((liquid/wprice_usdtbtc)/wprice_btceth)*wprice_ethusdt


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


####Simulated Orders with fee to determine whether transaction is profitable####

simbalance_usdte1 = 0
simbalance_usdtb1 = 0

if f_eth_liquid >= f_btc_liquid:
    ## USDT -> BTC -> ETH -> USDT
    simbalance_btc = liquid/wprice_usdtbtc
    simfee_btc = simbalance_btc*0.001
    simbalance_btc -= simfee_btc
    simbalance_btc = float(truncate(simbalance_btc,6))
    
    simbalance_eth = simbalance_btc/wprice_btceth
    simfee_eth = simbalance_eth * 0.001
    simbalance_eth -= simfee_eth
    simbalance_eth = float(truncate(simbalance_eth, 5))

    simbalance_usdt = simbalance_eth*wprice_ethusdt
    simfee_usdt = simbalance_usdt * 0.001
    simbalance_usdt -= simfee_usdt
    simbalance_usdtb1 = float(truncate(simbalance_usdt, 2))

simbalance_eth = 0
simbalance_btc = 0
simbalance_usdt = 0

if f_eth_liquid < f_btc_liquid:
    ## USDT -> ETH -> BTC -> USDT
    simbalance_eth = liquid/wprice_usdteth
    simfee_eth = simbalance_eth*0.001
    simbalance_eth -= simfee_eth
    simbalance_eth = float(truncate(simbalance_eth, 5))

    simbalance_btc = simbalance_eth*wprice_ethbtc
    simfee_btc = simbalance_btc * 0.001
    simbalance_btc -= simfee_btc
    simbalance_btc = float(truncate(simbalance_btc, 6)) 

    simbalance_usdt = simbalance_btc*wprice_btcusdt
    simfee_usdt = simbalance_usdt * 0.001
    simbalance_usdt -= simfee_usdt
    simbalance_usdte1 = float(truncate(simbalance_usdt, 2))


balance_usdt0 = client.get_asset_balance(asset = 'USDT')
balance_usdt0 = float(balance_usdt0[u'free'])
balance_usdt = balance_usdt0

error_msg = ''
trade_dir = ''


if  simbalance_usdte1 <= liquid and simbalance_usdtb1 <= liquid:
    balance_usdt = balance_usdt0
    balance_btc = float(client.get_asset_balance(asset='BTC')[u'free'])
    balance_eth = float(client.get_asset_balance(asset='ETH')[u'free'])
    error_msg = 'Trading not profitable'

    profitlist = [t0, error_msg, 0, liquid, balance_usdt0, balance_usdt, simbalance_usdte1, simbalance_usdtb1, balance_eth, balance_btc]
    profitopen = open('/home/ubuntu/Narbitrage/data_files/profit_real.csv', 'a')
    profitout = csv.writer(profitopen)
    profitout.writerow(profitlist)
    profitopen.close()

    print(error_msg)
    sys.exit()
    
if tot_qty_usdtbtc <= 0 or tot_qty_btcusdt <= 0 or tot_qty_ethbtc <= 0 or tot_qty_btceth <= 0 or tot_qty_usdteth <= 0 or tot_qty_ethusdt <= 0:
    balance_usdt = balance_usdt0
    balance_btc = float(client.get_asset_balance(asset='BTC')[u'free'])
    balance_eth = float(client.get_asset_balance(asset='ETH')[u'free'])
    error_msg = "Not enough quantity in first three orders"

    profitlist = [t0, error_msg, 0, liquid, balance_usdt0, balance_usdt, simbalance_usdte1, simbalance_usdtb1, balance_eth, balance_btc]
    profitopen = open('/home/ubuntu/Narbitrage/data_files/profit_real.csv', 'a')
    profitout = csv.writer(profitopen)
    profitout.writerow(profitlist)
    profitopen.close()
    
    print(error_msg)
    sys.exit()

elif simbalance_usdte1 > simbalance_usdtb1:
    trade_dir = 'Trading USDT->ETH->BTC->USDT'
    client.ping()

#### FIRST ORDER START TIMER ####
    time_order_start = time.time()

#### ORDER ETH WITH USDT ####

    order_usdt_eth = client.order_market_buy(symbol='ETHUSDT', quantity= float(truncate(liquid/wprice_usdteth,5)))

    time_order1 = time.time()
    
    min_eth = 10.0/wprice_usdteth #minimum trade value is 10 USDT
    balance_eth = min_eth
    while balance_eth <= min_eth:
        balance_eth = float(client.get_asset_balance(asset='ETH')[u'free'])
                
    time_balance1 = time.time()
    
#### ORDER BTC WITH ETH ####
    order_eth_btc = client.order_market_sell(symbol='ETHBTC', quantity= float(truncate(balance_eth*wprice_ethbtc,3)))

    time_order2 = time.time()

    min_btc = 10.0/wprice_usdteth #minimum trade value is 10 USDT
    balance_btc = min_btc
    while balance_btc <= min_btc:
        balance_btc = float(client.get_asset_balance(asset = 'BTC')[u'free'])

    time_balance2 = time.time()
    
#### ORDER USDT WITH BTC ####

    order_btc_usdt = client.order_market_sell(symbol='BTCUSDT', quantity = float(truncate(balance_btc,6)))

    time_order3 = time.time()
    
    time.sleep(5.0)

    balance_usdt = float(client.get_asset_balance(asset = 'USDT')[u'free'])
          
elif simbalance_usdtb1 > simbalance_usdte1:
    trade_dir = 'Trading USDT->BTC->ETH->USDT'

    client.ping()
#### Timer Start ####
    time_order_start = time.time()
#### ORDER BTC WITH USDT ####
    order_usdt_btc = client.order_market_buy(symbol='BTCUSDT', quantity= float(truncate(liquid/wprice_usdtbtc,6)))

    time_order1 = time.time()
    
    min_btc = 10.0/wprice_usdtbtc
    balance_btc = min_btc
    while balance_btc <= min_btc:
        balance_btc = float(client.get_asset_balance(asset = 'BTC')[u'free'])

    time_balance1 = time.time()

#### ORDER ETH WITH BTC ####
    order_btc_eth = client.order_market_buy(symbol='ETHBTC', quantity = float(truncate(balance_btc/wprice_btceth,3)))

    time_order2 = time.time()

    min_eth = 10.0/wprice_usdteth

    balance_eth = min_eth
    while balance_eth <= min_eth:
        balance_eth = float(client.get_asset_balance(asset = 'ETH')[u'free'])

    time_balance2 = time.time()
        
#### ORDER USDT WITH ETH ####
    order_eth_usdt = client.order_market_sell(symbol='ETHUSDT',quantity = float(truncate(balance_eth,5)))

    time_order3 = time.time()
    
    time.sleep(5.0)

    balance_usdt = float(client.get_asset_balance(asset = 'USDT')[u'free'])
    
t_order_final = time.time()

t_order1_elapsed = time_order1 - time_start
t_balance1_elapsed = time_balance1 - time_order1
t_order2_elapsed = time_order2 - time_balance1
t_balance2_elapsed = time_balance2 - time_order2
t_ordder3_elapsed = time_order3 - time_balance2

t_book_el = t_book-t0
t_calc_el = t_calc-t_book

####Exporting data to a CSV####

priceqtylist = [price_usdtbtc0, price_usdtbtc1, price_usdtbtc2, qty_usdtbtc0, qty_usdtbtc1, qty_usdtbtc2,
                price_btcusdt0, price_btcusdt1, price_btcusdt2, qty_btcusdt0, qty_btcusdt1, qty_btcusdt2,
                price_ethusdt0, price_ethusdt1, price_ethusdt2, qty_ethusdt0, qty_ethusdt1, qty_ethusdt2,
                price_usdteth0, price_usdteth1, price_usdteth2, qty_usdteth0, qty_usdteth1, qty_usdteth2,
                price_btceth0, price_btceth1, price_btceth2, qty_btceth0, qty_btceth1, qty_btceth2,
                price_ethbtc0, price_ethbtc1, price_ethbtc2, qty_ethbtc0, qty_ethbtc1, qty_ethbtc2,
                t_book_el, t_calc_el, t_order1_elapsed, t_balance1_elapsed, t_order2_elapsed, t_balance2_elapsed, t_order3_elapsed]

weightedavglist = [wprice_usdtbtc, wprice_btcusdt, wprice_usdteth, wprice_ethusdt, wprice_btceth,wprice_ethbtc]

profitlist = [t0, error_msg, trade_dir, liquid, balance_usdt0, balance_usdt, simbalance_usdte1, simbalance_usdtb1, balance_eth, balance_btc]

orderopen = open('/home/ubuntu/Narbitrage/data_files/orderbook_real.csv', 'a')
orderout = csv.writer(orderopen)
orderout.writerow(priceqtylist)
orderopen.close()

avgopen = open('/home/ubuntu/Narbitrage/data_files/weightedaverage_real.csv', 'a')
avgout = csv.writer(avgopen)
avgout.writerow(weightedavglist)
avgopen.close()

profitopen = open('/home/ubuntu/Narbitrage/data_files/profit_real.csv', 'a')
profitout = csv.writer(profitopen)
profitout.writerow(profitlist)
profitopen.close()
