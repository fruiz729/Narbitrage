import numpy as np
import time
import math
import csv
from binance.enums import *
from binance.client import Client
import sys
api_key = '1S7kzJ3dRAQPXKbQeURIcgNbWIDdNpNKIVUHF4HL6S8PjntVRjvIJ4bb1r8x35zl'
api_secret = 'r1ltG546t22G1dFRBZ5gAF93cxnrrbGfQPYkYyI9BKkw4RneAfokGhih8d8lrQAX'
client = Client(api_key, api_secret)
time_res = client.get_server_time()

##Test Market Order Syntax
##
##order = client.create_test_order(
##    symbol='BTCUSDT',
##    side=SIDE_BUY,type=Client.ORDER_TYPE_MARKET,
##    quantity=0.001)


##symbols = ['ETHBTC','LTCBTC', 'BNBBTC', 'NEOBTC', '123456', 'EOSETH','SNTETH',
##         'BNTETH', 'BCCBTC']

symbols = ['BTCUSDT', 'ETHBTC', 'ETHUSDT']

#enter the theoretical liquid capital available
liquid = 1000.00 #keep decimal to make it a float
fee = 0.003*liquid ## 0.1% x amount of tradies x liquid

t0 = time.time()
order_books = {}
for coin in symbols:
    order_books[coin] = client.get_order_book(symbol=coin)
t_book = time.time()
##print('qty_btcusdt')
##print(float(order_books['BTCUSDT']['asks'][0][1]))
##print('price_btcusdt')
##print(float(order_books['BTCUSDT']['asks'][0][0]))
##
##print('qty_ethbtc')
##print(float(order_books['ETHBTC']['asks'][0][1]))
##print('price_ethbtc')
##print(float(order_books['ETHBTC']['asks'][0][0]))
##
##print('qty_ethusdt')
##print(float(order_books['ETHUSDT']['asks'][0][1]))
##print('price_ethusdt')
##print(float(order_books['ETHUSDT']['asks'][0][0]))
##
##print('\t')

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
##    print('enough qty in first bid')
##    print('qty_usdtbtc0 = ' + str(qty_usdtbtc0) + '  liquid/price_usdtbtc0 = ' + str(liquid/price_usdtbtc0))
##    print('\t')
elif (qty_usdtbtc0 + qty_usdtbtc1) >= liquid/np.average([price_usdtbtc0,price_usdtbtc1],
                    weights = [qty_usdtbtc0,(qty_usdtbtc1)]):
#Finding weighted price average of first two quantities                                                        
    actprice_usdtbtc = np.average([price_usdtbtc0,price_usdtbtc1],
                    weights = [qty_usdtbtc0, qty_usdtbtc1])
#Re-weighting the average to include only the amount of qty2 that will be bought
    wprice_usdtbtc = np.average([price_usdtbtc0,price_usdtbtc1],
                    weights = [qty_usdtbtc0, (liquid/actprice_usdtbtc)-qty_usdtbtc0])                                                 
    tot_qty_usdtbtc = qty_usdtbtc0 + qty_usdtbtc1
##    print('enough qty in first & second bid')
##    print('qty_usdtbtc0 + qty_usdtbtc1 = ' + str(qty_usdtbtc0+qty_usdtbtc1) + '  liquid/wprice_usdtbtc = ' + str(liquid/wprice_usdtbtc))
##    print('\t')
elif (qty_usdtbtc0 + qty_usdtbtc1 + qty_usdtbtc2) >=  liquid/np.average([price_usdtbtc0,price_usdtbtc1,price_usdtbtc2],
                    weights = [qty_usdtbtc0,qty_usdtbtc1,qty_usdtbtc2]):
    actprice_usdtbtc = np.average([price_usdtbtc0,price_usdtbtc1,price_usdtbtc2],
                    weights = [qty_usdtbtc0,qty_usdtbtc1,qty_usdtbtc2])
    wprice_usdtbtc = np.average([price_usdtbtc0,price_usdtbtc1,price_usdtbtc2],
                    weights = [qty_usdtbtc0,qty_usdtbtc1,(liquid/actprice_usdtbtc)-(qty_usdtbtc0+qty_usdtbtc1)])
    tot_qty_usdtbtc = qty_usdtbtc0 + qty_usdtbtc1 + qty_usdtbtc2
##    print('enough qty in first & second & third bid')
##    print('qty_usdtbtc0 + qty_usdtbtc1 + qty_usdtbtc2 = ' + str(qty_usdtbtc0+qty_usdtbtc1+qty_usdtbtc2) + '  liquid/wprice_usdtbtc = ' + str(liquid/wprice_usdtbtc))
##    print('\t')
else:
    print ('FUCK IT - not enough quantity in BTCUSDT Bids to go USDT --> BTC')
    
####################################################################################################################
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
##    print('enough qty in first bid')
##    print('qty_btcusdt0 = ' + str(qty_btcusdt0) + '  liquid/price_btcusdt0 = ' + str(liquid/price_btcusdt0))
##    print('\t')
elif (qty_btcusdt0 + qty_btcusdt1) >= liquid/np.average([price_btcusdt0,price_btcusdt1],
                    weights = [qty_btcusdt0,qty_btcusdt1]):
    actprice_btcusdt = np.average([price_btcusdt0,price_btcusdt1],
                    weights = [qty_btcusdt0,qty_btcusdt1])
    wprice_btcusdt = np.average([price_btcusdt0,price_btcusdt1],
                    weights = [qty_btcusdt0,(liquid/actprice_btcusdt)-qty_btcusdt0])
    
    tot_qty_btcusdt = qty_btcusdt0 + qty_btcusdt1
##    print('enough qty in first & second bid')
##    print('qty_btcusdt0 + qtybtcusdt1 = ' + str(qty_btcusdt0+qty_btcusdt1) + '  liquid/wprice_btcusdt = ' + str(liquid/wprice_btcusdt))
##    print('\t')
elif (qty_btcusdt0 + qty_btcusdt1 + qty_btcusdt2) >=  liquid/np.average([price_btcusdt0,price_btcusdt1,price_btcusdt2],
                    weights = [qty_btcusdt0,qty_btcusdt1,qty_btcusdt2]):
    actprice_btcusdt = np.average([price_btcusdt0,price_btcusdt1,price_btcusdt2],
                    weights = [qty_btcusdt0,qty_btcusdt1,qty_btcusdt2])
    wprice_btcusdt = np.average([price_btcusdt0,price_btcusdt1,price_btcusdt2],
                    weights = [qty_btcusdt0,qty_btcusdt1,(liquid/actprice_btcusdt)-(qty_btcusdt0+qty_btcusdt1)])

    tot_qty_btcusdt = qty_btcusdt0 + qty_btcusdt1 + qty_btcusdt2
##    print('enough qty in first & second & third bid')
##    print('qty_btcusdt0 + qty_btcusdt1 + qty_btcusdt2 = ' + str(qty_btcusdt0+qty_btcusdt1+qty_btcusdt2) + '  liquid/wprice_btcusdt = ' + str(liquid/wprice_btcusdt))
##    print('\t')
else:
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
##    print('enough qty in first bid')
##    print('qty_usdteth0 = ' + str(qty_usdteth0) + '  liquid/price_usdteth0 = ' + str(liquid/price_usdteth0))
##    print('\t')
elif (qty_usdteth0 + qty_usdteth1) >= liquid/np.average([price_usdteth0,price_usdteth1],
                    weights = [qty_usdteth0,qty_usdteth1]):
    actprice_usdteth = np.average([price_usdteth0,price_usdteth1],
                    weights = [qty_usdteth0,qty_usdteth1])
    wprice_usdteth = np.average([price_usdteth0,price_usdteth1],
                    weights = [qty_usdteth0,(liquid/actprice_usdteth) - qty_usdteth0])
   
    tot_qty_usdteth = qty_usdteth0 + qty_usdteth1
##    print('enough qty in first & second bid')
##    print('qty_usdteth0 + qtyusdteth1 = ' + str(qty_usdteth0+qty_usdteth1) + '  liquid/wprice_usdteth = ' + str(liquid/wprice_usdteth))
##    print('\t')
elif (qty_usdteth0 + qty_usdteth1 + qty_usdteth2) >=  liquid/np.average([price_usdteth0,price_usdteth1,price_usdteth2],
                    weights = [qty_usdteth0,qty_usdteth1,qty_usdteth2]):
    actprice_usdteth = np.average([price_usdteth0,price_usdteth1,price_usdteth2],
                    weights = [qty_usdteth0,qty_usdteth1,qty_usdteth2])
    wprice_usdteth = np.average([price_usdteth0,price_usdteth1,price_usdteth2],
                    weights = [qty_usdteth0,qty_usdteth1,(liquid/actprice_usdteth)-(qty_usdteth0 + qty_usdteth1)])


    tot_qty_usdteth = qty_usdteth0 + qty_usdteth1 + qty_usdteth2
##    print('enough qty in first & second & third bid')
##    print('qty_usdteth0 + qty_usdteth1 + qty_usdteth2 = ' + str(qty_usdteth0+qty_usdteth1+qty_usdteth2) + '  liquid/wprice_usdteth = ' + str(liquid/wprice_usdteth))
##    print('\t')
else:
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
##    print('enough qty in first bid')
##    print('qty_ethusdt0 = ' + str(qty_ethusdt0) + '  liquid/price_ethusdt0 = ' + str(liquid/price_ethusdt0))
##    print('\t')
elif (qty_ethusdt0 + qty_ethusdt1) >= liquid/np.average([price_ethusdt0,price_ethusdt1],
                    weights = [qty_ethusdt0,qty_ethusdt1]):
    actprice_ethusdt = np.average([price_ethusdt0,price_ethusdt1],
                    weights = [qty_ethusdt0,qty_ethusdt1])
    wprice_ethusdt = np.average([price_ethusdt0,price_ethusdt1],
                    weights = [qty_ethusdt0,liquid/actprice_ethusdt - qty_ethusdt0])

    tot_qty_ethusdt = qty_ethusdt0 + qty_ethusdt1
##    print('enough qty in first & second bid')
##    print('qty_ethusdt0 + qtyethusdt1 = ' + str(qty_ethusdt0+qty_ethusdt1) + '  liquid/wprice_ethusdt = ' + str(liquid/wprice_ethusdt))
##    print('\t')
elif (qty_ethusdt0 + qty_ethusdt1 + qty_ethusdt2) >=  liquid/np.average([price_ethusdt0,price_ethusdt1,price_ethusdt2],
                    weights = [qty_ethusdt0,qty_ethusdt1,qty_ethusdt2]):
    actprice_ethusdt = np.average([price_ethusdt0,price_ethusdt1,price_ethusdt2],
                    weights = [qty_ethusdt0,qty_ethusdt1,qty_ethusdt2])
    wprice_ethusdt = np.average([price_ethusdt0,price_ethusdt1,price_ethusdt2],
                    weights = [qty_ethusdt0,qty_ethusdt1,(liquid/actprice_ethusdt) - (qty_ethusdt0 + qty_ethusdt1)])

    tot_qty_ethusdt = qty_ethusdt0 + qty_ethusdt1 + qty_ethusdt2
##    print('enough qty in first & second & third bid')
##    print('qty_ethusdt0 + qty_ethusdt1 + qty_ethusdt2 = ' + str(qty_ethusdt0+qty_ethusdt1+qty_ethusdt2) + '  liquid/wprice_ethusdt = ' + str(liquid/wprice_ethusdt))
##    print('\t')
else:
    print ('FUCK IT - not enough quantity in ethusdt ASKS to go ETH --> USDT')

############################################################################################################################
#BID PRICE FOR ETHBTC MARKET - MUST MATCH WHEN TRADING BTC -> ETH
price_btceth0 = float(order_books['ETHBTC']['bids'][0][0])
price_btceth1= float(order_books['ETHBTC']['bids'][1][0])
price_btceth2 = float(order_books['ETHBTC']['bids'][2][0])

qty_btceth0 = float(order_books['ETHBTC']['bids'][0][1])
qty_btceth1 = float(order_books['ETHBTC']['bids'][1][1])
qty_btceth2 = float(order_books['ETHBTC']['bids'][2][1])

if qty_btceth0 >= (liquid/wprice_usdtbtc)/price_btceth0:
    wprice_btceth = price_btceth0
    tot_qty_btceth = qty_btceth0
##    print('enough qty in first bid')
##    print('qty_btceth0 = ' + str(qty_btceth0) + '  liquid/price_btceth0 = ' + str(liquid/price_btceth0))
##    print('\t')
elif (qty_btceth0 + qty_btceth1) >= (liquid/wprice_usdtbtc)/np.average([price_btceth0,price_btceth1],
                    weights = [qty_btceth0,qty_btceth1]):
#Did not need intermediate weighted average; converted liquid straight to ethereum to account for weight of liquid used
    wprice_btceth = np.average([price_btceth0,price_btceth1],
                    weights = [qty_btceth0,(liquid/wprice_usdteth)-qty_btceth0])

    tot_qty_btceth = qty_btceth0 + qty_btceth1
##    print('enough qty in first & second bid')
##    print('qty_btceth0 + qtybtceth1 = ' + str(qty_btceth0+qty_btceth1) + '  liquid/wprice_btceth = ' + str(liquid/wprice_btceth))
##    print('\t')
elif (qty_btceth0 + qty_btceth1 + qty_btceth2) >=  (liquid/wprice_usdtbtc)/np.average([price_btceth0,price_btceth1,price_btceth2],
                    weights = [qty_btceth0,qty_btceth1,qty_btceth2]):
#Did not need intermediate weighted average; converted liquid straight to ethereum to account for weight of liquid used
    wprice_btceth = np.average([price_btceth0,price_btceth1,price_btceth2],
                    weights = [qty_btceth0,qty_btceth1,(liquid/wprice_usdteth)-(qty_btceth0+qty_btceth1)])

    tot_qty_btceth = qty_btceth0 + qty_btceth1 + qty_btceth2
##    print('enough qty in first & second & third bid')
##    print('qty_btceth0 + qty_btceth1 + qty_btceth2 = ' + str(qty_btceth0+qty_btceth1+qty_btceth2) + '  liquid/wprice_btceth = ' + str(liquid/wprice_btceth))
##    print('\t')
else:
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
##    print('enough qty in first bid')
##    print('qty_ethbtc0 = ' + str(qty_ethbtc0) + '  liquid/price_ethbtc0 = ' + str(liquid/price_ethbtc0))
##    print('\t')
elif (qty_ethbtc0 + qty_ethbtc1) >= (liquid/wprice_usdteth):
    wprice_ethbtc = np.average([price_ethbtc0,price_ethbtc1],
                    weights = [qty_ethbtc0,(liquid/wprice_usdteth)-qty_ethbtc0])

    tot_qty_ethbtc = qty_ethbtc0 + qty_ethbtc1
##    print('enough qty in first & second bid')
##    print('qty_ethbtc0 + qtyethbtc1 = ' + str(qty_ethbtc0+qty_ethbtc1) + '  liquid/wprice_ethbtc = ' + str(liquid/wprice_ethbtc))
##    print('\t')
elif (qty_ethbtc0 + qty_ethbtc1 + qty_ethbtc2)>=(liquid/wprice_usdteth):
    wprice_ethbtc = np.average([price_ethbtc0,price_ethbtc1,price_ethbtc2],
                    weights = [qty_ethbtc0,qty_ethbtc1,(liquid/wprice_usdteth) - (qty_ethbtc0 + qty_ethbtc1)])
    tot_qty_ethbtc = qty_ethbtc0 + qty_ethbtc1 + qty_ethbtc2
##    print('enough qty in first & second & third bid')
##    print('qty_ethbtc0 + qty_ethbtc1 + qty_ethbtc2 = ' + str(qty_ethbtc0+qty_ethbtc1+qty_ethbtc2) + '  liquid/wprice_ethbtc = ' + str(liquid/wprice_ethbtc))
##    print('\t')
else:
    print ('FUCK IT - not enough quantity in ethbtc ASKS to go ETH --> BTC')

t_calc = time.time()


f_btc = wprice_usdteth/wprice_ethbtc
f_eth = wprice_usdtbtc*wprice_btceth
d_btc = f_btc - wprice_usdtbtc
d_eth = f_eth - wprice_usdteth


print('fake bitcoin in usdt: ' + str(f_btc))
print('difference of fake bitcion and real bitcoin: '+ str(d_btc))
print('fake eth in usdt: ' + str(f_eth))
print('difference of fake ethereum and real ethereum: ' + str(d_eth))
print('\t')
    

if d_btc <= 0:
    print('Trading USDT->ETH->BTC->USDT NOT profitable')
    print('\t')
if d_eth <= 0:
    print('Trading USDT->BTC->ETH->USDT NOT profitable')
    print('\t')

#fee per coin assuming you have bought usdt amount of fake or middleman btc/eth
##fee_fake_btc= 0.003 * f_btc
##fee_fake_eth = 0.003 * f_eth
##fee_fake_btc = 0.0015*f_btc
##fee_fake_eth = 0.0015*f_eth

##if d_btc < fee_fake_btc and d_eth < fee_fake_eth:
##    print('No profit because of fee')
    
elif d_btc >= d_eth:
    print('Trading USDT->ETH->BTC->USDT')

    order_usdt_eth = client.create_test_order(symbol='ETHUSDT',side=SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET, quantity= round((liquid/wprice_usdteth),5))

    balance_eth= round((liquid/wprice_usdteth),5)
    
    fee_eth = balance_eth*0.001
    fee_eth_bnb = fee_eth/2
    
    balance_eth -= fee_eth
    balance_eth = round(balance_eth, 5)
    print('bought ethereum with USDT')
    
    order_eth_btc = client.create_test_order(symbol='ETHBTC',side=SIDE_SELL,
                    type=Client.ORDER_TYPE_MARKET, quantity= round((balance_eth*wprice_ethbtc),3))

    balance_btc = round((balance_eth*wprice_ethbtc),3)

    fee_btc = balance_btc*0.001
    fee_btc_bnb = fee_btc/2

    balance_btc -=fee_btc
    balance_btc = round(balance_btc, 3)
    print('bought bitcoin with ehtereum')

    
    order_btc_usdt = client.create_test_order(symbol='BTCUSDT', side = SIDE_SELL,
                    type=Client.ORDER_TYPE_MARKET, quantity = balance_btc)
    
    balance_usdt = round(balance_btc*wprice_btcusdt,2)

    fee_usdt = balance_usdt*0.001
    fee_usdt_bnb = fee_usdt/2

    balance_usdt -= fee_usdt
    balance_usdt = round(balance_usdt, 2)
    print('Done back to USDT, final balance: ' + str(round(balance_btc*wprice_btcusdt),2))

    
elif d_btc < d_eth:
    print('Trading USDT->BTC->ETH->USDT')
    order_usdt_eth = client.create_test_order(symbol='BTCUSDT', side = SIDE_BUY,
                     type=Client.ORDER_TYPE_MARKET,quantity= round((liquid/wprice_usdtbtc),6))

    print('bought bitcoin with USDT')

    balance_btc = round((liquid/wprice_usdtbtc),6)

    fee_btc = balance_btc*0.001
    fee_btc_bnb = fee_btc/2

    balance_btc -=fee_btc
    balance_btc = round(balance_btc, 3)
    
    order_btc_eth = client.create_test_order(symbol='ETHBTC', side = SIDE_BUY,
                    type = Client.ORDER_TYPE_MARKET, quantity = round((balance_btc/wprice_btceth),3))

    print('bought ehtereum with bitcoin')


    balance_eth = round((balance_btc/wprice_btceth),3)

    fee_eth = balance_eth*0.001
    fee_eth_bnb = fee_eth/2
    
    balance_eth -= fee_eth
    balance_eth = round(balance_eth, 5)

    order_eth_usdt = client.create_test_order(symbol='ETHUSDT', side=SIDE_SELL,
                    type = Client.ORDER_TYPE_MARKET,quantity = balance_eth)

    balance_usdt = round(balance_eth*wprice_ethusdt,2)
    fee_usdt = balance_usdt*0.001
    fee_usdt_bnb = fee_usdt/2

    balance_usdt -= fee_usdt
    balance_usdt = round(balance_usdt, 2)
    
    print('Done back to USDT, final balance: ' + str(round(balance_eth*wprice_ethusdt,2)))
    
t_order = time.time()

print ('t_book = ' + str(t_book-t0))
print ('t_calc = ' + str(t_calc-t_book))
print('t_order = ' + str(t_order-t_calc))

priceqtylist = [price_usdtbtc0, price_usdtbtc1, price_usdtbtc2, qty_usdtbtc0, qty_usdtbtc1, qty_usdtbtc2,
                price_btcusdt0, price_btcusdt1, price_btcusdt2, qty_btcusdt0, qty_btcusdt1, qty_btcusdt2,
                price_ethusdt0, price_ethusdt1, price_ethusdt2, qty_ethusdt0, qty_ethusdt1, qty_ethusdt2,
                price_usdteth0, price_usdteth1, price_usdteth2, qty_usdteth0, qty_usdteth1, qty_usdteth2,
                price_btceth0, price_btceth1, price_btceth2, qty_btceth0, qty_btceth1, qty_btceth2,
                price_ethbtc0, price_ethbtc1, price_ethbtc2, qty_ethbtc0, qty_ethbtc1, qty_ethbtc2,
                t_book, t_calc, t_order]

weightedavglist = [wprice_usdtbtc, wprice_btcusdt, wprice_usdteth, wprice_ethusdt, wprice_btceth,wprice_ethbtc]

profitlist = [balance_usdt, balance_usdt - liquid, 1-(balance_usdt/liquid), f_btc, f_eth, d_btc, d_eth]

orderopen = open('/home/ubuntu/Narbitrage/data_files/orderbooks.csv', 'a')
orderout = csv.writer(orderopen)
orderout.writerow(priceqtylist)
orderopen.close()

avgopen = open('/home/ubuntu/Narbitrage/data_files/weightedaverage.csv', 'a')
avgout = csv.writer(avgopen)
avgout.writerow(weightedavglist)
avgopen.close()

profitopen = open('/home/ubuntu/Narbitrage/data_files/profit.csv', 'a')
profitout = csv.writer(profitopen)
profitout.writerow(profitlist)
avgopen.close()
