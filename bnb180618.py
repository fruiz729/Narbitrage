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

symbols = ['BNBBTC', 'ETHBTC', 'BNBETH']

#enter the theoretical liquid capital available

liquid = 1.1 #minimum is 1 BNB; tradiing 1.1

t0 = time.time()
order_books = {}
for coin in symbols:
    order_books[coin] = client.get_order_book(symbol=coin)

t_book = time.time()

##################################################################
#BID PRICE FOR BNBBTC MARKET - MUST MATCH WHEN TRADING BNB -> BTC

price_btcbnb0 = float(order_books['BNBBTC']['bids'][0][0])
price_btcbnb1 = float(order_books['BNBBTC']['bids'][1][0])
price_btcbnb2 = float(order_books['BNBBTC']['bids'][2][0])

qty_btcbnb0 = float(order_books['BNBBTC']['bids'][0][1])       
qty_btcbnb1 = float(order_books['BNBBTC']['bids'][1][1])
qty_btcbnb2 = float(order_books['BNBBTC']['bids'][2][1])

if qty_btcbnb0 >= liquid:
    wprice_btcbnb = price_btcbnb0
    tot_qty_btcbnb = qty_btcbnb0
elif (qty_btcbnb0 + qty_btcbnb1) >= liquid:
    wprice_btcbnb = np.average([price_btcbnb0,price_btcbnb1],
                    weights = [qty_btcbnb0, (liquid-qty_btcbnb0)])                                                 
    tot_qty_btcbnb = qty_btcbnb0 + qty_btcbnb1
elif (qty_btcbnb0 + qty_btcbnb1 + qty_btcbnb2) >= liquid:

    wprice_btcbnb = np.average([price_btcbnb0,price_btcbnb1,price_btcbnb2],
                    weights = [qty_btcbnb0,qty_btcbnb1,(liquid - (qty_btcbnb0 + qty_btcbnb1])
    tot_qty_btcbnb = qty_btcbnb0 + qty_btcbnb1 + qty_btcbnb2
else:
    wprice_btcbnb = price_btcbnb0
    tot_qty_btcbnb = 0.0
    print ('FUCK IT - not enough quantity in BTCBNB Bids to go BNB --> BTC')
    
###########################################################################################################################################
#ASK PRICE FOR BNBBTC MARKET - MUST MATCH WHEN TRADING BTC -> BNB

price_bnbbtc0 = float(order_books['BNBBTC']['asks'][0][0])
price_bnbbtc1 = float(order_books['BNBBTC']['asks'][1][0])
price_bnbbtc2 = float(order_books['BNBBTC']['asks'][2][0])

qty_bnbbtc0 = float(order_books['BNBBTC']['asks'][0][1])       
qty_bnbbtc1 = float(order_books['BNBBTC']['asks'][1][1])
qty_bnbbtc2 = float(order_books['BNBBTC']['asks'][2][1])

if qty_bnbbtc0 >= liquid:
    wprice_bnbbtc = price_bnbbtc0
    tot_qty_bnbbtc = qty_bnbbtc0
elif (qty_bnbbtc0 + qty_bnbbtc1) >= liquid:
    wprice_bnbbtc = np.average([price_bnbbtc0,price_bnbbtc1],
                    weights = [qty_bnbbtc0,(liquid - qty_bnbbtc0)])
    tot_qty_bnbbtc = qty_bnbbtc0 + qty_bnbbtc1
elif (qty_bnbbtc0 + qty_bnbbtc1 + qty_bnbbtc2) >=  liquid:
    wprice_bnbbtc = np.average([price_bnbbtc0,price_bnbbtc1,price_bnbbtc2],
                    weights = [qty_bnbbtc0,qty_bnbbtc1,(liquid -(qty_bnbbtc0 + qty_bnbbtc1)])

    tot_qty_bnbbtc = qty_bnbbtc0 + qty_bnbbtc1 + qty_bnbbtc2
else:
    wprice_bnbbtc = price_bnbbtc0
    tot_qty_bnbbtc = 0.0
    print ('FUCK IT - not enough quantity in BNBBTC ASKS to go BTC --> BNB')
#############################################################################################################################
##BID PRICES FOR BNBETH MARKET - MUST MATCH WHEN TRADING BNB -> ETH

price_ethbnb0 = float(order_books['BNBETH']['bids'][0][0])
price_ethbnb1 = float(order_books['BNBETH']['bids'][1][0])
price_ethbnb2 = float(order_books['BNBETH']['bids'][2][0])

qty_ethbnb0 = float(order_books['BNBETH']['bids'][0][1])
qty_ethbnb1 = float(order_books['BNBETH']['bids'][1][1])
qty_ethbnb2 = float(order_books['BNBETH']['bids'][2][1])

if qty_ethbnb0 >= liquid:
    wprice_ethbnb = price_ethbnb0
    tot_qty_ethbnb = qty_ethbnb0
elif (qty_ethbnb0 + qty_ethbnb1) >= liquid:
    wprice_ethbnb = np.average([price_ethbnb0,price_ethbnb1],
                               weights = [qty_ethbnb0, (liquid - qty_ethbnb0)])
    tot_qty_ethbnb = qty_ethbnb0 + qty_ethbnb1
elif (qty_ethbnb0 + qty_ethbnb1 + qty_ethbnb2) >=  liquid:
    wprice_ethbnb = np.average([price_ethbnb0,price_ethbnb1,price_ethbnb2],
                    weights = [qty_ethbnb0,qty_ethbnb1,(liquid - (qty_ethbnb0 + qty_ethbnb1))])

    tot_qty_ethbnb = qty_ethbnb0 + qty_ethbnb1 + qty_ethbnb2
else:
    wprice_ethbnb = price_ethbnb0
    tot_qty_ethbnb = 0.0
    print ('FUCK IT - not enough quantity in ethbnb ASKS to go BNB --> ETH')


############################################################################################################################
##ASK PRICES FOR BNBETH MARKET - MUST MATCH WHEN TRADING ETH -> BNB

price_ethbnb0 = float(order_books['BNBETH']['asks'][0][0])
price_ethbnb1 = float(order_books['BNBETH']['asks'][1][0])
price_ethbnb2 = float(order_books['BNBETH']['asks'][2][0])

qty_ethbnb0 = float(order_books['BNBETH']['asks'][0][1])
qty_ethbnb1 = float(order_books['BNBETH']['asks'][1][1])
qty_ethbnb2 = float(order_books['BNBETH']['asks'][2][1])

if qty_ethbnb0 >= liquid/price_ethbnb0:
    wprice_ethbnb = price_ethbnb0
    tot_qty_ethbnb = qty_ethbnb0
elif (qty_ethbnb0 + qty_ethbnb1) >= liquid/np.average([price_ethbnb0,price_ethbnb1],
                    weights = [qty_ethbnb0, (liquid - (qty_ethbnb0*price_ethbnb0))/price_ethbnb1]):
    wprice_ethbnb = np.average([price_ethbnb0,price_ethbnb1],
                    weights = [qty_ethbnb0,(liquid - (qty_ethbnb0*price_ethbnb0))/price_ethbnb1])

    tot_qty_ethbnb = qty_ethbnb0 + qty_ethbnb1
elif (qty_ethbnb0 + qty_ethbnb1 + qty_ethbnb2) >=  liquid/np.average([price_ethbnb0,price_ethbnb1,price_ethbnb2],
                    weights = [qty_ethbnb0,qty_ethbnb1,(liquid - (qty_ethbnb0*price_ethbnb0) + (qty_ethbnb1*price_ethbnb1))/price_ethbnb2]):
    wprice_ethbnb = np.average([price_ethbnb0,price_ethbnb1,price_ethbnb2],
                    weights = [qty_ethbnb0,qty_ethbnb1, (liquid - (qty_ethbnb0*price_ethbnb0) + (qty_ethbnb1*price_ethbnb1))/price_ethbnb2])

    tot_qty_ethbnb = qty_ethbnb0 + qty_ethbnb1 + qty_ethbnb2
else:
    wprice_ethbnb = price_ethbnb0
    tot_qty_ethbnb = 0.0
    print ('FUCK IT - not enough quantity in ethbnb ASKS to go ETH --> BNB')

############################################################################################################################
#BID PRICE FOR ETHBTC MARKET - MUST MATCH WHEN TRADING BTC -> ETH

price_btceth0 = float(order_books['ETHBTC']['bids'][0][0])
price_btceth1= float(order_books['ETHBTC']['bids'][1][0])
price_btceth2 = float(order_books['ETHBTC']['bids'][2][0])

qty_btceth0 = float(order_books['ETHBTC']['bids'][0][1])
qty_btceth1 = float(order_books['ETHBTC']['bids'][1][1])
qty_btceth2 = float(order_books['ETHBTC']['bids'][2][1])

if qty_btceth0*price_btceth0 >= liquid/wprice_bnbbtc:
    wprice_btceth = price_btceth0
    tot_qty_btceth = qty_btceth0
elif (qty_btceth0+qty_btceth1)*np.average([price_btceth0, price_btceth1],weights = [qty_btceth0*price_btceth0, (liquid/wprice_bnbbtc)-(qty_btceth0*price_btceth0)])>= liquid/wprice_bnbbtc:
    wprice_btceth = np.average([price_btceth0,price_btceth1], weights = [qty_btceth0*price_btceth0, (liquid/wprice_bnbbtc)-(qty_btceth0*price_btceth0)])
    tot_qty_btceth = qty_btceth0 + qty_btceth1                                          
elif (qty_btceth0 + qty_btceth1 + qty_btceth2)*np.average([price_btceth0, price_btceth1, price_btceth2], weights = [qty_btceth0*price_btceth0,qty_btceth1*price_btceth1, liquid/wprice_bnbbtc-(qty_btceth0*price_btceth0 + qty_btceth1*price_btceth1)]) >= liquid/wprice_bnbbtc:

    wprice_btceth = np.average([price_btceth0,price_btceth1,price_btceth2],
                    weights = [qty_btceth0,qty_btceth1,liquid/wprice_bnbbtc - (qty_btceth0*price_btceth0 + qty_btceth1*price_btceth1)])

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

if qty_ethbtc0 >= (liquid/wprice_bnbeth):
    wprice_ethbtc = price_ethbtc0
    tot_qty_ethbtc = qty_ethbtc0
elif (qty_ethbtc0 + qty_ethbtc1) >= (liquid/wprice_bnbeth):
    wprice_ethbtc = np.average([price_ethbtc0,price_ethbtc1],
                    weights = [qty_ethbtc0,(liquid/wprice_bnbeth)-qty_ethbtc0])

    tot_qty_ethbtc = qty_ethbtc0 + qty_ethbtc1
elif (qty_ethbtc0 + qty_ethbtc1 + qty_ethbtc2)>=(liquid/wprice_bnbeth):
    wprice_ethbtc = np.average([price_ethbtc0,price_ethbtc1,price_ethbtc2],
                    weights = [qty_ethbtc0,qty_ethbtc1,(liquid/wprice_bnbeth) - (qty_ethbtc0+qty_ethbtc1)])
    tot_qty_ethbtc = qty_ethbtc0 + qty_ethbtc1 + qty_ethbtc2
else:
    wprice_ethbtc = price_ethbtc0
    tot_qty_ethbtc = 0.0
    print ('FUCK IT - not enough quantity in ethbtc ASKS to go ETH --> BTC')

t_calc = time.time()

#f_btc = wprice_bnbeth/wprice_ethbtc
#f_eth = wprice_bnbbtc*wprice_btceth
#d_btc = f_btc - wprice_bnbbtc
#d_eth = f_eth - wprice_bnbeth

f_btc_liquid = ((liquid/wprice_bnbeth)*wprice_ethbtc)*wprice_btcbnb
f_eth_liquid = ((liquid/wprice_bnbbtc)/wprice_btceth)*wprice_ethbnb


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


####Simulated Orders with fee to determine whether transaction is profitable####

simbalance_bnbe1 = 0
simbalance_bnbb1 = 0

if f_eth_liquid >= f_btc_liquid:
    ## BNB -> BTC -> ETH -> BNB
    simbalance_btc = liquid/wprice_bnbbtc
    simfee_btc = simbalance_btc*0.001
    simbalance_btc -= simfee_btc
    simbalance_btc = float(truncate(simbalance_btc,6))
    
    simbalance_eth = simbalance_btc/wprice_btceth
    simfee_eth = simbalance_eth * 0.001
    simbalance_eth -= simfee_eth
    simbalance_eth = float(truncate(simbalance_eth, 5))

    simbalance_bnb = simbalance_eth*wprice_ethbnb
    simfee_bnb = simbalance_bnb * 0.001
    simbalance_bnb -= simfee_bnb
    simbalance_bnbb1 = float(truncate(simbalance_bnb, 2))

simbalance_eth = 0
simbalance_btc = 0
simbalance_bnb = 0

if f_eth_liquid < f_btc_liquid:
    ## BNB -> ETH -> BTC -> BNB
    simbalance_eth = liquid/wprice_bnbeth
    simfee_eth = simbalance_eth*0.001
    simbalance_eth -= simfee_eth
    simbalance_eth = float(truncate(simbalance_eth, 5))

    simbalance_btc = simbalance_eth*wprice_ethbtc
    simfee_btc = simbalance_btc * 0.001
    simbalance_btc -= simfee_btc
    simbalance_btc = float(truncate(simbalance_btc, 6)) 

    simbalance_bnb = simbalance_btc*wprice_btcbnb
    simfee_bnb = simbalance_bnb * 0.001
    simbalance_bnb -= simfee_bnb
    simbalance_bnbe1 = float(truncate(simbalance_bnb, 2))


balance_bnb0 = client.get_asset_balance(asset = 'BNB')
balance_bnb0 = float(balance_bnb0[u'free'])
balance_bnb = balance_bnb0

error_msg = ''
trade_dir = ''


if  simbalance_bnbe1 <= liquid and simbalance_bnbb1 <= liquid:
    balance_bnb = balance_bnb0
    balance_btc = float(client.get_asset_balance(asset='BTC')[u'free'])
    balance_eth = float(client.get_asset_balance(asset='ETH')[u'free'])
    error_msg = 'Trading not profitable'

    profitlist = [t0, error_msg, 0, liquid, balance_bnb0, balance_bnb, simbalance_bnbe1, simbalance_bnbb1, balance_eth, balance_btc]
    profitopen = open('/home/ubuntu/Narbitrage/data_files/profit_real.csv', 'a')
    profitout = csv.writer(profitopen)
    profitout.writerow(profitlist)
    profitopen.close()

    print(error_msg)
    sys.exit()
    
if tot_qty_bnbbtc <= 0 or tot_qty_btcbnb <= 0 or tot_qty_ethbtc <= 0 or tot_qty_btceth <= 0 or tot_qty_bnbeth <= 0 or tot_qty_ethbnb <= 0:
    balance_bnb = balance_bnb0
    balance_btc = float(client.get_asset_balance(asset='BTC')[u'free'])
    balance_eth = float(client.get_asset_balance(asset='ETH')[u'free'])
    error_msg = "Not enough quantity in first three orders"

    profitlist = [t0, error_msg, 0, liquid, balance_bnb0, balance_bnb, simbalance_bnbe1, simbalance_bnbb1, balance_eth, balance_btc]
    profitopen = open('/home/ubuntu/Narbitrage/data_files/profit_real.csv', 'a')
    profitout = csv.writer(profitopen)
    profitout.writerow(profitlist)
    profitopen.close()
    
    print(error_msg)
    sys.exit()

elif simbalance_bnbe1 > simbalance_bnbb1:
    trade_dir = 'Trading BNB->ETH->BTC->BNB'
    client.ping()

#### FIRST ORDER START TIMER ####
    time_order_start = time.time()

#### ORDER ETH WITH BNB ####

    order_bnb_eth = client.order_market_buy(symbol='BNBETH', quantity= float(truncate(liquid/wprice_bnbeth,5)))

    time_order1 = time.time()
    
    min_eth = 10.0/wprice_bnbeth #minimum trade value is 10 BNB
    balance_eth = min_eth
    while balance_eth <= min_eth:
        balance_eth = float(client.get_asset_balance(asset='ETH')[u'free'])
                
    time_balance1 = time.time()
    
#### ORDER BTC WITH ETH ####
    order_eth_btc = client.order_market_sell(symbol='ETHBTC', quantity= float(truncate(balance_eth*wprice_ethbtc,3)))

    time_order2 = time.time()

    min_btc = 10.0/wprice_bnbeth #minimum trade value is 10 BNB
    balance_btc = min_btc
    while balance_btc <= min_btc:
        balance_btc = float(client.get_asset_balance(asset = 'BTC')[u'free'])

    time_balance2 = time.time()
    
#### ORDER BNB WITH BTC ####

    order_btc_bnb = client.order_market_sell(symbol='BNBBTC', quantity = float(truncate(balance_btc,6)))

    time_order3 = time.time()
    
    time.sleep(5.0)

    balance_bnb = float(client.get_asset_balance(asset = 'BNB')[u'free'])
          
elif simbalance_bnbb1 > simbalance_bnbe1:
    trade_dir = 'Trading BNB->BTC->ETH->BNB'

    client.ping()
#### Timer Start ####
    time_order_start = time.time()
#### ORDER BTC WITH BNB ####
    order_bnb_btc = client.order_market_buy(symbol='BNBBTC', quantity= float(truncate(liquid/wprice_bnbbtc,6)))

    time_order1 = time.time()
    
    min_btc = 10.0/wprice_bnbbtc
    balance_btc = min_btc
    while balance_btc <= min_btc:
        balance_btc = float(client.get_asset_balance(asset = 'BTC')[u'free'])

    time_balance1 = time.time()

#### ORDER ETH WITH BTC ####
    order_btc_eth = client.order_market_buy(symbol='ETHBTC', quantity = float(truncate(balance_btc/wprice_btceth,3)))

    time_order2 = time.time()

    min_eth = 10.0/wprice_bnbeth

    balance_eth = min_eth
    while balance_eth <= min_eth:
        balance_eth = float(client.get_asset_balance(asset = 'ETH')[u'free'])

    time_balance2 = time.time()
        
#### ORDER BNB WITH ETH ####
    order_eth_bnb = client.order_market_sell(symbol='BNBETH',quantity = float(truncate(balance_eth,5)))

    time_order3 = time.time()
    
    time.sleep(5.0)

    balance_bnb = float(client.get_asset_balance(asset = 'BNB')[u'free'])
    
t_order_final = time.time()

t_order1_elapsed = time_order1 - time_start
t_balance1_elapsed = time_balance1 - time_order1
t_order2_elapsed = time_order2 - time_balance1
t_balance2_elapsed = time_balance2 - time_order2
t_ordder3_elapsed = time_order3 - time_balance2

t_book_el = t_book-t0
t_calc_el = t_calc-t_book

####Exporting data to a CSV####

priceqtylist = [price_bnbbtc0, price_bnbbtc1, price_bnbbtc2, qty_bnbbtc0, qty_bnbbtc1, qty_bnbbtc2,
                price_btcbnb0, price_btcbnb1, price_btcbnb2, qty_btcbnb0, qty_btcbnb1, qty_btcbnb2,
                price_ethbnb0, price_ethbnb1, price_ethbnb2, qty_ethbnb0, qty_ethbnb1, qty_ethbnb2,
                price_bnbeth0, price_bnbeth1, price_bnbeth2, qty_bnbeth0, qty_bnbeth1, qty_bnbeth2,
                price_btceth0, price_btceth1, price_btceth2, qty_btceth0, qty_btceth1, qty_btceth2,
                price_ethbtc0, price_ethbtc1, price_ethbtc2, qty_ethbtc0, qty_ethbtc1, qty_ethbtc2,
                t_book_el, t_calc_el, t_order1_elapsed, t_balance1_elapsed, t_order2_elapsed, t_balance2_elapsed, t_order3_elapsed]

weightedavglist = [wprice_bnbbtc, wprice_btcbnb, wprice_bnbeth, wprice_ethbnb, wprice_btceth,wprice_ethbtc]

profitlist = [t0, error_msg, trade_dir, liquid, balance_bnb0, balance_bnb, simbalance_bnbe1, simbalance_bnbb1, balance_eth, balance_btc]

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
