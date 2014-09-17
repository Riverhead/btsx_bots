##  This is a very simple bot based on the Market Maker bot for BitSharesX. This takes logic started by "toast" and massaged by Riverhead.
##  
##  IT IS HIGHLY RECOMMENDED YOU SETUP A BOT WALLET/ACCOUNT WITH LIMITED FUNDS. IF YOU RUN THIS AGAINST YOUR PRIMARY WALLET REALLY "BAD THINGS" COULD HAPPEN.
##  
##  The purpose of this bot is: 1) Create a simple bot as a base to create more complex bots 2) Generate traffic in the bitUSD:BTSX market
##  
##  SETUP:
##  
##  Modify the config.json to reference your own RPC configutarion.
##  Fund your bot account with at least 501 BTSX
##  create a logs directory in the same directory as the python source
##  

import time

class MarketSpeculator():
    def __init__(self, client, feeds, bot_config, log):
        self.log = log
        self.client = client
        if not "bot_type" in bot_config or bot_config["bot_type"] != "market_speculator":
            raise Exception("Bad bot configuration object")
        self.config = bot_config
        self.name = self.config["account_name"]
        self.base_symbol = bot_config["asset_pair"][0]
        self.quote_symbol = bot_config["asset_pair"][1]

    def execute(self):
        SPREAD = self.config["spread_percent"]
        sec_since_update = 0
        last_price = self.client.get_last_fill(self.base_symbol, self.quote_symbol)
        start_btsx = float(self.client.get_balance(self.name, self.quote_symbol))

        btsx_balance = self.client.get_balance(self.name, self.quote_symbol)
        usd_balance = self.client.get_balance(self.name, self.base_symbol)
        new_price   = last_price

        if usd_balance > 10:
            self.client.submit_bid(self.name, 0.3*(usd_balance / new_price), self.quote_symbol, new_price * (1+SPREAD), self.base_symbol)
            sec_since_update = 0
        if btsx_balance > 500:
            self.client.submit_ask(self.name, 0.3*btsx_balance, self.quote_symbol, new_price * (1-SPREAD), self.base_symbol)
            sec_since_update = 0
        while True:
            new_price   = self.client.get_last_fill(self.base_symbol, self.quote_symbol)

            usd_balance = self.client.get_balance(self.name, self.base_symbol)
            btsx_balance = self.client.get_balance(self.name, self.quote_symbol)

            if usd_balance > 10:
               self.client.submit_bid(self.name, 0.3*(usd_balance / new_price), self.quote_symbol, new_price * (1+SPREAD), self.base_symbol)
               sec_since_update = 0
            if btsx_balance > 500:
               self.client.submit_ask(self.name, 0.3*btsx_balance, self.quote_symbol, new_price * (1-SPREAD), self.base_symbol)
               sec_since_update = 0


            self.log("Seconds since last action: %i USD %f BTSX %f started %f" % (sec_since_update, usd_balance, btsx_balance, start_btsx))

            time.sleep(2)
            sec_since_update += 2

            if new_price > 0:
                if (abs(new_price - last_price) / last_price) > (SPREAD / 3):
                   self.log("Price moved -  old:  %f   new:  %f" % (last_price, new_price))
                  
                   sec_since_update = 0
    
                   self.client.cancel_all_orders(self.name, self.base_symbol, self.quote_symbol)
                   self.client.wait_for_block()

                   usd_balance = self.client.get_balance(self.name, self.base_symbol) 
                   btsx_balance = self.client.get_balance(self.name, self.quote_symbol) 


                   if usd_balance > 10:
                      self.client.submit_bid(self.name, 0.3*(usd_balance / new_price), self.quote_symbol, new_price * (1+SPREAD), self.base_symbol)
                   if btsx_balance > 500:
                      self.client.submit_ask(self.name, 0.3*btsx_balance, self.quote_symbol, new_price * (1-SPREAD), self.base_symbol)
                last_price = new_price

