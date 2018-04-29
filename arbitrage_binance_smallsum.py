import numpy as np
from binance.enums import *
from binance.client import Client
api_key = '1S7kzJ3dRAQPXKbQeURIcgNbWIDdNpNKIVUHF4HL6S8PjntVRjvIJ4bb1r8x35zl'
api_secret = 'r1ltG546t22G1dFRBZ5gAF93cxnrrbGfQPYkYyI9BKkw4RneAfokGhih8d8lrQAX'
client = Client(api_key, api_secret)
time_res = client.get_server_time()

## ONLY FOR REAL TRADING ##
##balance = client.get_asset_balance(asset='USDT')
##liquid = float(.20 * balance)


##Test Market Order
##Only uncomment for testing
##
##order = client.create_test_order(
##    symbol='BTCUSDT',
##    side=SIDE_BUY,type=Client.ORDER_TYPE_MARKET,
##    quantity=0.001)



##symbols = ['ETHBTC','LTCBTC', 'BNBBTC', 'NEOBTC', '123456', 'EOSETH','SNTETH',
##         'BNTETH', 'BCCBTC']

symbols = ['BTCUSDT', 'ETHBTC', 'ETHUSDT']


order_books = {}
for coin in symbols:
    order_books[coin] = client.get_order_book(symbol=coin)

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
##
##print('qty_ethusdt')
##print(float(order_books['ETHUSDT']['asks'][0][1]))
##print('price_ethusdt')
##print(float(order_books['ETHUSDT']['asks'][0][0]))
##
##print('\t')


#BID PRICE FOR BTCUSDT MARKET - MUST MATCH WHEN TRADING USDT -> BTC
price_usdtbtc0 = float(order_books['BTCUSDT']['bids'][0][0])

##price_usdtbtc1 = float(order_books['BTCUSDT']['bids'][1][0])
##price_usdtbtc2 = float(order_books['BTCUSDT']['bids'][2][0])

qty_usdtbtc0 = float(order_books['BTCUSDT']['bids'][0][1])       

##qty_usdtbtc1 = float(order_books['BTCUSDT']['bids'][1][1])
##qty_usdtbtc2 = float(order_books['BTCUSDT']['bids'][2][1])

          
##wprice_usdtbtc = np.average([price_usdtbtc0,price_usdtbtc1,price_usdtbtc2],
##                    weights = [qty_usdtbtc0,qty_usdtbtc1,qty_usdtbtc2])

##tot_qty_usdtbtc= sum([qty_usdtbtc0,qty_usdtbtc1,qty_usdtbtc2])


#ASK PRICE FOR BTCUSDT MARKET - MUST MATCH WHEN TRADING BTC -> USDT
price_btcusdt0 = float(order_books['BTCUSDT']['asks'][0][0])

##price_btcusdt1 = float(order_books['BTCUSDT']['asks'][1][0])
##price_btcusdt2 = float(order_books['BTCUSDT']['asks'][2][0])

qty_btcusdt0 = float(order_books['BTCUSDT']['asks'][0][1])

##qty_btcusdt1 = float(order_books['BTCUSDT']['asks'][1][1])
##qty_btcusdt2 = float(order_books['BTCUSDT']['asks'][2][1])

          
##wprice_btcusdt = np.average([price_btcusdt0,price_btcusdt1,price_btcusdt2],
##                    weights = [qty_btcusdt0,qty_btcusdt1,qty_btcusdt2])

##tot_qty_btcusdt = sum([qty_btcusdt0,qty_btcusdt1,qty_btcusdt2])

#BID PRICE FOR ETHBTC MARKET - MUST MATCH WHEN TRADING BTC -> ETH
price_btceth0 = float(order_books['ETHBTC']['bids'][0][0])

##price_btceth1= float(order_books['ETHBTC']['bids'][1][0])
##price_btceth2 = float(order_books['ETHBTC']['bids'][2][0])

qty_btceth0 = float(order_books['ETHBTC']['bids'][0][1])

##qty_btceth1 = float(order_books['ETHBTC']['bids'][1][1])
##qty_btceth2 = float(order_books['ETHBTC']['bids'][2][1])

##wprice_btceth = np.average([price_btceth0,price_btceth1,price_btceth2],
##                    weights = [qty_btceth0,qty_btceth1,qty_btceth2])

##tot_qty_btceth = sum([qty_btceth0,qty_btceth1,qty_btceth2])


#ASK PRICES FOR ETHBTC MARKET - MUST MATCH WHEN TRADING ETH -> BTC
price_ethbtc0 = float(order_books['ETHBTC']['asks'][0][0])

##price_ethbtc1= float(order_books['ETHBTC']['asks'][1][0])
##price_ethbtc2 = float(order_books['ETHBTC']['asks'][2][0])

qty_ethbtc0 = float(order_books['ETHBTC']['asks'][0][1])

##qty_ethbtc1 = float(order_books['ETHBTC']['asks'][1][1])
##qty_ethbtc2 = float(order_books['ETHBTC']['asks'][2][1])

##wprice_ethbtc = np.average([price_ethbtc0,price_ethbtc1,price_ethbtc2],
##                    weights = [qty_ethbtc0,qty_ethbtc1,qty_ethbtc2])

##tot_qty_ethbtc = sum([qty_ethbtc0,qty_ethbtc1,qty_ethbtc2])

##BID PRICES FOR ETHUSDT MARKET - MUST MATCH WHEN TRADING USDT -> ETH
price_usdteth0 = float(order_books['ETHUSDT']['bids'][0][0])

##price_usdteth1 = float(order_books['ETHUSDT']['bids'][1][0])
##price_usdteth2 = float(order_books['ETHUSDT']['bids'][2][0])

qty_usdteth0 = float(order_books['ETHUSDT']['bids'][0][1])

##qty_usdteth1 = float(order_books['ETHUSDT']['bids'][1][1])
##qty_usdteth2 = float(order_books['ETHUSDT']['bids'][2][1])

##wprice_usdteth = np.average([price_usdteth0,price_usdteth1,price_usdteth2],
##                    weights = [qty_usdteth0,qty_usdteth1,qty_usdteth2])

##tot_qty_usdteth = sum([qty_usdteth0,qty_usdteth1,qty_usdteth2])


##ASK PRICES FOR ETHUSDT MARKET - MUST MATCH WHEN TRADING ETH -> USDT
price_ethusdt0 = float(order_books['ETHUSDT']['asks'][0][0])

##price_ethusdt1 = float(order_books['ETHUSDT']['asks'][1][0])
##price_ethusdt2 = float(order_books['ETHUSDT']['asks'][2][0])

qty_ethusdt0 = float(order_books['ETHUSDT']['asks'][0][1])
##qty_ethusdt1 = float(order_books['ETHUSDT']['asks'][1][1])
##qty_ethusdt2 = float(order_books['ETHUSDT']['asks'][2][1])

##wprice_ethusdt = np.average([price_ethusdt0,price_ethusdt1,price_ethusdt2],
##                    weights = [qty_ethusdt0,qty_ethusdt1,qty_ethusdt2])

##tot_qty_ethusdt = sum([qty_ethusdt0,qty_ethusdt1,qty_ethusdt2])




liquid = 1000.0 ## available for trading in USDT
fee = 0.003*liquid ## 0.1% x amount of tradies x liquid


if tot_qty_btcusdt >= liquid:
    if tot_qty_ethusdt >= liquid/wprice_ethusdt:
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
    
if d_btc < fee and d_eth < fee:
    print('No profit because of fee')
    
elif d_btc >= d_eth:
    print('Trading USDT->ETH->BTC->USDT')

    order_usdt_eth = client.create_test_order(symbol='ETHUSDT',side=SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET, quantity= round((liquid/wprice_usdteth),3))

    balance_eth= round((liquid/wprice_usdteth),3)
    
    print('bought ethereum with USDT')
    
    order_eth_btc = client.create_test_order(symbol='ETHBTC',side=SIDE_SELL,
                    type=Client.ORDER_TYPE_MARKET, quantity= round((balance_eth*wprice_ethbtc),3))

    balance_btc = round((balance_eth*wprice_ethbtc),3)
    
    print('bought bitcoin with ehtereum')

    
    order_btc_usdt = client.create_test_order(symbol='BTCUSDT', side = SIDE_SELL,
                    type=Client.ORDER_TYPE_MARKET, quantity = balance_btc)
    
    print('Done back to USDT, final balance: ' + str(balance_btc))
    
elif d_btc < d_eth:
    print('Trading USDT->BTC->ETH->USDT')
    order_usdt_eth = client.create_test_order(symbol='BTCUSDT', side = SIDE_BUY,
                     type=Client.ORDER_TYPE_MARKET,quantity= round((liquid/wprice_usdtbtc),3))

    print('bought bitcoin with USDT')

    balance_btc = round((liquid/wprice_usdtbtc),3)
    
    order_btc_eth = client.create_test_order(symbol='ETHBTC', side = SIDE_BUY,
                    type = Client.ORDER_TYPE_MARKET, quantity = round((balance_btc/wprice_btceth),3))

    print('bought ehtereum with bitcoin')


    balance_eth = round((balance_btc/wprice_btceth),3)

    order_eth_usdt = client.create_test_order(symbol='ETHUSDT', side=SIDE_SELL,
                    type = Client.ORDER_TYPE_MARKET,quantity = balance_eth)
    
    print('Done back to USDT, final balance: ' + str(balance_eth*wprice_ethusdt))

    


