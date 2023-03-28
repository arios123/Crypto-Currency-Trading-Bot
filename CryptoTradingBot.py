import cbpro
import requests
import time
import logging
from datetime import datetime

#Removed the credentials for security and privacy reasons
auth_client =  cbpro.AuthenticatedClient("")
public_client = cbpro.PublicClient()
##################################################
def gettingMACD():
   indicator = "rsi"
   endpoint = "https://api.taapi.io/macd"
   parameters = {
   #Removed the credentials for security and privacy reasons
       'secret': '',
       'exchange': 'binance',
       'symbol': 'BTC/USDT',
       'interval': '1h'
       } 
   response = requests.get(url = endpoint, params = parameters)
   result = response.json() 
   return(result)
####################################################
def getUSDBalance():
   checko1 = True
   while(checko1):
      try:
      #Removed the credentials for security and privacy reasons
         usd = auth_client.get_account('')
         checko1 = False
      except:
         print("Problem using cbpro")
         time.sleep(1)
   checko1 = True
   usd_string = str(usd['available'])
   return str(usd_string[:usd_string.index(".")+3])
####################################################
def getBTCBalance():
   checko2 = True
   while(checko2):
      try:
      #Removed the credentials for security and privacy reasons
         btc = auth_client.get_account('')
         checko2 = False
      except:
         print("Problem using cbpro")
         time.sleep(1)
   checko2 = True
   btc_string = str(btc['available'])
   return str(btc_string[:10])
#####################################################
def macd():
   checko3 = True
   print("Gotta wait 15 seconds")

   while(checko3):
      try:
         macd_info = gettingMACD()
         blue_line = float(macd_info["valueMACD"])
         yellow_line = float(macd_info["valueMACDSignal"])
         checko3 = False
         return float(blue_line), float(yellow_line)
      except:
        auhijkasdf=1
#####################################################
def buy(bp):
   usd_balance = getUSDBalance()
   order = auth_client.place_market_order(product_id="BTC-USD", side="buy", funds=usd_balance)
   print(order)
   the_order_num = str(order['id'])
   print(the_order_num)
   file1 = open("resume.txt", "r+")
   test = file1.readlines()
   test[0] = "True\n"
   test[1] = "False\n"
   test[2] = str(bp)+"\n"
   file1.close()
   file2 = open("resume.txt", "w")
   file2.writelines(test)
   file2.close()
#####################################################
def sell(yl):
   btc_balance = getBTCBalance()
   order = auth_client.place_market_order(product_id="BTC-USD", side="sell", size=btc_balance)
   print(order)
   the_order_num = str(order['id'])
   print(the_order_num)
   file1 = open("resume.txt", "r+")
   test = file1.readlines()
   test[0] = "False\n"
   test[1] = "True\n"
   test[4] = str(yl)
   file1.close()
   file2 = open("resume.txt", "w")
   file2.writelines(test)
   file2.close()
#####################################################
def price():
    checko4 = True
    while(checko4):
        try:
            p = float(public_client.get_product_ticker(product_id="BTC-USD")['price'])
            checko4 = False
            return p
        except:
            print("Trying to get price from coinbase")
#####################################################
def macddifference(ys,yl):
    if(ys - yl > 75):
        return True
    else:
        return False
#####################################################
def startup():
    file1 = open("resume.txt", "r+")
    test = file1.readlines()
    test[0] = bool(test[0])
    test[1] = bool(test[1])
    test[2] = float(test[2])
    test[3] = bool(test[3])
    test[4] = float(test[4])
    file1.close()
    return test
#####################################################
print("Starting now")

info = startup()

selling = True#info[0]
buying = False#info[1]
bought_price = info[2]
selling_check = info[3]
yellow_start = info[4] # gotta do something about this here
macd_difference = 0.0

print(selling)
print(buying)
print(bought_price)
print(selling_check)
print(yellow_start)


while(True):
   
   blue_line, yellow_line = macd()
   current_price = price()
    ##########################
   if(selling):
   
      print("Trying to sell...")

      if(current_price >= bought_price * 1.015):
        if(yellow_line >= blue_line):
            print("Selling rn")
            sell(yellow_line)  
            selling = False
            buying = True
            yellow_start = yellow_line
      if(current_price <= bought_price*0.97):
        print("Selling rn")
        sell(yellow_line)  
        selling = False
        buying = True
        yellow_start = yellow_line
     #probably should add failsafe here       
     
    ##############################     
   if(buying):
   
      print("Trying to buy...")
      
      if(yellow_line <= blue_line):
        macd_diff = macddifference(yellow_start, yellow_line)
        if(macd_diff): 
            print("buying rn")
            buy(current_price)
            bought_price = current_price
            selling = True
            buying = False
        elif( not(macd_diff)):
            if(yellow_start - yellow_line < 50):
                print("You the actual person here have to check because something weird is happening.")