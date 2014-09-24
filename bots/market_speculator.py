##  This is a very simple bot based on the Market Maker bot for BitSharesX. This takes logic started by toast and massaged by Riverhead.
##  
##  IT IS HIGHLY RECOMMENDED YOU SETUP A BOT WALLET/ACCOUNT WITH LIMITED FUNDS. IF YOU RUN THIS AGAINST YOUR PRIMARY WALLET REALLY "BAD THINGS" COULD HAPPEN.
##  
##  The purpose of this bot is: 1) Create a simple bot as a base to create more complex bots 2) Generate traffic in the bitUSD:BTSX market

import time

class MarketSpeculator():
    def __init__(self, client, feeds, bot_config, log):
        self.log = log
        self.client = client
        if not "bot_type" in bot_config or bot_config["bot_type"] != "market_speculator":
            raise Exception("Bad bot configuration object")
        self.config = bot_config
        self.name = self.config["account_name"]
        self.quote_symbol = bot_config["asset_pair"][0]
        self.base_symbol = bot_config["asset_pair"][1]
        self.min_balance = self.config["min_balance"]
        self.last_bid = 0
        self.last_ask = 0

    def execute(self):
        self.log("Executing bot:  %s" % self.name)
        SPREAD = self.config["spread_percent"]
        BEAT_BUY_BY = 0.005
        BEAT_ASK_BY = 0.005

        median = self.client.get_median(self.quote_symbol)

        #Get the ratio of the last filled order
        last_price = self.client.get_last_fill(self.base_symbol, self.quote_symbol)

        #Get the ratio of the lowest ask price
        lowest_ask  = self.client.get_lowest_ask(self.quote_symbol, self.base_symbol)

        usd_balance = self.client.get_balance(self.name, self.quote_symbol) 
        btsx_balance = self.client.get_balance(self.name, self.base_symbol) 

        #If the market has moved.
        if ((abs(self.last_ask - last_price) / last_price) > (SPREAD / 3)) and self.last_ask != 0 :
           self.client.cancel_all_orders(self.name, self.base_symbol, self.quote_symbol)
           self.client.wait_for_block() 

        if ((abs(self.last_bid - last_price) / last_price) > (SPREAD / 3)) and self.last_bid != 0 :
           self.client.cancel_all_orders(self.name, self.base_symbol, self.quote_symbol)
           self.client.wait_for_block() 

        #bid just below the lowest ask 

        if usd_balance > 10:
           self.client.submit_bid(self.name, ((usd_balance-1) / (lowest_ask *(1-(BEAT_ASK_BY*2)))), self.base_symbol, lowest_ask * (1-(BEAT_ASK_BY*2)) , self.quote_symbol)
           self.last_bid = lowest_ask * (1-BEAT_ASK_BY*2)
           self.last_ask = 0


        #For selling we just want to sell a few Larimers less to make sure we're the cheapest

        if btsx_balance > 50:
           self.client.submit_ask(self.name, btsx_balance-(self.min_balance-50), self.base_symbol, lowest_ask * (1-BEAT_ASK_BY), self.quote_symbol)
           self.last_bid = 0



