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
print('f_eth_liquid= ' +str(f_eth_liquid))
print('f_btc_liquid= ' +str(f_btc_liquid))

####Simulated Orders with fee to determine whether transaction is profitable####

simbalance_usdte1 = 0
simbalance_usdtb1 = 0

if f_eth_liquid >= f_btc_liquid:
    ## USDT -> BTC -> ETH -> USDT
    simbalance_btc = liquid/wprice_usdtbtc
    simfee_btc = simbalance_btc*0.001
    simbalance_btc -= simfee_btc
    simbalance_btc = round(simbalance_btc,6)
    print('btc= ' + str(simbalance_btc))
    print('btc in usdt= ' +str(simbalance_btc*wprice_btcusdt))
    simbalance_eth = simbalance_btc/wprice_btceth
    simfee_eth = simbalance_eth * 0.001
    simbalance_eth -= simfee_eth
    simbalance_eth = round(simbalance_eth, 5)
    print('eth= ' + str(simbalance_eth))
    print('eth in usdt= ' + str(simbalance_eth*wprice_ethusdt))
    simbalance_usdt = simbalance_eth*wprice_ethusdt
    simfee_usdt = simbalance_usdt * 0.001
    simbalance_usdt -= simfee_usdt
    simbalance_usdtb1 = round(simbalance_usdt, 2)
    print('Potential Profit USDT -> BTC -> ETH -> USDT ' +str(simbalance_usdtb1))
    print('\t')

simbalance_eth = 0
simbalance_btc = 0
simbalance_usdt = 0
if f_eth_liquid < f_btc_liquid:
    ## USDT -> ETH -> BTC -> USDT
    simbalance_eth = liquid/wprice_usdteth
    simfee_eth = simbalance_eth*0.001
    simbalance_eth -= simfee_eth
    simbalance_eth = round(simbalance_eth, 5)
    print('eth= ' + str(simbalance_eth))
    print('eth in usdt = ' + str(simbalance_eth*wprice_ethusdt))

    simbalance_btc = simbalance_eth*wprice_ethbtc
    simfee_btc = simbalance_btc * 0.001
    simbalance_btc -= simfee_btc
    simbalance_btc = round(simbalance_btc, 6)
    print('btc =' + str(simbalance_btc))
    print('btc in usdt= ' +str(simbalance_btc*wprice_btcusdt)) 

    simbalance_usdt = simbalance_btc*wprice_btcusdt
    simfee_usdt = simbalance_usdt * 0.001
    simbalance_usdt -= simfee_usdt
    simbalance_usdte1 = round(simbalance_usdt, 2)
    print('fee_USDT= ' +str(simfee_usdt))
    print('Potential Profit USDT-> ETH ->BTC -> USDT ' + str(simbalance_usdte1))
    print('\t')


#Syntax get balance:
#balance = client.get_asset_balance(asset='BTC')

#Syntax market order:
#order = client.order_market_buy(
#        symbol='BNBBTC',
#        quantity=100)
        

#order = client.order_market_sell(
#       symbol='BNBBTC',
#        quantity=100

#Syntax Check Order Status
#order = client.get_order(
#       symbol='BNBBTC',
#       orderId='orderId')


balance_usdt = liquid
error_msg = ''
trade_dir = ''
if  simbalance_usdte1 <= liquid and simbalance_usdtb1 <= liquid:
    balance_usdt = liquid
    balance_btc = client.get_asset_balance(asset='BTC')
    balance_eth = client.get_asset_balance(asset='ETH')
    error_msg = 'Trading not profitable'
    print(error_msg)
    sys.exit()
    
if tot_qty_usdtbtc <= 0 or tot_qty_btcusdt <= 0 or tot_qty_ethbtc <= 0 or tot_qty_btceth <= 0 or tot_qty_usdteth <= 0 or tot_qty_ethusdt <= 0:
    balance_usdt = liquid
    balance_btc = client.get_asset_balance(asset='BTC')
    balance_eth = client.get_asset_balance(asset='ETH')
    error_msg = "Not enough quantity in first three orders"
    print(error_msg)
    sys.exit()

elif simbalance_usdte1 > simbalance_usdtb1:
    trade_dir = 'Trading USDT->ETH->BTC->USDT'
    print(trade_dir)

    client.ping()

#### ORDER ETH WITH USDT ####    
    order_usdt_eth = client.create_test_order(symbol='ETHUSDT',side=SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET, quantity= round((liquid/wprice_usdteth),5))

    balance_eth = client.get_asset_balance(asset='ETH')

    min_eth = 10.0/wprice_usdteth #minimum trade value is 10 USDT

    try:
        balance_eth >= min_eth
    except None:
        time.sleep(0.2)

    try:
        balance_eth >= min_eth
    except None:
        balance_usdt = liquid
        error_msg = 'Too much time getting ethereum balance'
        print(error_msg)
        sys.exit()

#### ORDER BTC WITH ETH ####
                
    order_eth_btc = client.create_test_order(symbol='ETHBTC',side=SIDE_SELL,
                    type=Client.ORDER_TYPE_MARKET, quantity= round((balance_eth*wprice_ethbtc),3))

    balance_btc = client.get_asset_balance(asset='BTC')

    min_btc = 10.0/wprice_usdteth #minimum trade value is 10 USDT

    try:
        balance_btc >= min_btc
    except None:
        time.sleep(0.2)

    try:
        balance_btc >= min_btc
    except None:
        balance_usdt = liquid
        error_msg = 'Too much time getting ethereum balance'
        print(error_msg)
        sys.exit()

#### ORDER USDT WITH BTC ####

    order_btc_usdt = client.create_test_order(symbol='BTCUSDT', side = SIDE_SELL,
                    type=Client.ORDER_TYPE_MARKET, quantity = balance_btc)

    balance_usdt = client.get_asset_balance(asset = 'USDT')

    time.sleep(2.0)

    balance_usdt = client.get_asset_balance(asset = 'USDT')
    
           
elif simbalance_usdtb1 > simbalance_usdte1:
    trade_dir = 'Trading USDT->BTC->ETH->USDT'
    print(trade_dir)

    client.ping()
#### ORDER BTC WITH USDT ####
    order_usdt_btc = client.create_test_order(symbol='BTCUSDT', side = SIDE_BUY,
                     type=Client.ORDER_TYPE_MARKET,quantity= round((liquid/wprice_usdtbtc),6))

    balance_btc = client.get_asset_balance(asset = 'BTC')
    
    min_btc = 10.0/wprice_usdtbtc
    
    try:
        balance_btc >= min_btc
    except None:
        time.sleep(0.2)

    balance_btc = client.get_asset_balance(asset = 'BTC')
 
    try:
        balance_btc >= min_btc
    except None:
        balance_usdt = liquid
        error_msg = 'Too much time getting ethereum balance'
        print(error_msg)
        sys.exit()

#### ORDER ETH WITH BTC ####
    order_btc_eth = client.create_test_order(symbol='ETHBTC', side = SIDE_BUY,
                    type = Client.ORDER_TYPE_MARKET, quantity = round((balance_btc/wprice_btceth),3))

    balance_eth = client.get_asset_balance(asset = 'ETH')
        
    try:
        balance_eth >= min_eth
    except None:
        time.sleep(0.2)

    try:
        balance_eth >= min_eth
    except None:
        balance_usdt = liquid
        print('Too much time getting ethereum balance')
        sys.exit()
    
#### ORDER USDT WITH ETH ####
    order_eth_usdt = client.create_test_order(symbol='ETHUSDT', side=SIDE_SELL,
                    type = Client.ORDER_TYPE_MARKET,quantity = balance_eth)


    balance_usdt = client.get_asset_balance(asset = 'USDT')

    time.sleep(2.0)

    balance_usdt = client.get_asset_balance(asset = 'USDT')
    
t_order = time.time()

t_book_el = t_book-t0
t_calc_el = t_calc-t_book
t_order_el = t_order-t_calc


####Exporting data to a CSV####

priceqtylist = [price_usdtbtc0, price_usdtbtc1, price_usdtbtc2, qty_usdtbtc0, qty_usdtbtc1, qty_usdtbtc2,
                price_btcusdt0, price_btcusdt1, price_btcusdt2, qty_btcusdt0, qty_btcusdt1, qty_btcusdt2,
                price_ethusdt0, price_ethusdt1, price_ethusdt2, qty_ethusdt0, qty_ethusdt1, qty_ethusdt2,
                price_usdteth0, price_usdteth1, price_usdteth2, qty_usdteth0, qty_usdteth1, qty_usdteth2,
                price_btceth0, price_btceth1, price_btceth2, qty_btceth0, qty_btceth1, qty_btceth2,
                price_ethbtc0, price_ethbtc1, price_ethbtc2, qty_ethbtc0, qty_ethbtc1, qty_ethbtc2,
                t_book_el, t_calc_el, t_order_el]

weightedavglist = [wprice_usdtbtc, wprice_btcusdt, wprice_usdteth, wprice_ethusdt, wprice_btceth,wprice_ethbtc]

profitlist = [liquid, balance_usdt, simbalance_usdte1, simbalance_usdtb1, balance_eth, balance_btc]

orderopen = open('/home/ubuntu/Narbitrage/data_files/orderbook.csv', 'a')
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
