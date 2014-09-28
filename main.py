import os
import sys
import urllib2
import json
import time

from mylog import logger
log = logger.log

from btsx import BTSX

from config import read_config
from bots import MarketMaker
from bots import MarketSpeculator

from feeds import BterFeeds, BTC38Feeds, Average, Feed


if len(sys.argv) < 2:
    print "Usage:  main.py config_path"
    sys.exit(1)

conf = read_config(sys.argv[1])

print conf

client = BTSX(
    conf["client"]["rpc_user"],
    conf["client"]["rpc_password"],
    conf["client"]["rpc_port"]
)

bter = BterFeeds()
btc38 = BTC38Feeds()
feeds = {}
feeds["bter_usd_per_btsx"] = Feed.from_func(bter.avg_usd_per_btsx)
feeds["btc38_usd_per_btsx"] = Feed.from_func(btc38.last_usd_per_btsx)
feeds["usd_per_btsx"] = Average({k: feeds[k] for k in ["bter_usd_per_btsx", "btc38_usd_per_btsx"]})

# fetch them all once to cache
for key, feed in feeds.iteritems():
    print key
    print feed.fetch()

bots = []
for botconfig in conf["bots"]:
    bot_type = botconfig["bot_type"]
    print bot_type
    if bot_type == "market_maker":
        bots.append(MarketMaker(client, feeds, botconfig, log))
    else: 
        if bot_type == "market_speculator":
           bots.append(MarketSpeculator(client, feeds, botconfig, log))
        else:
           raise Exception("unknown bot type")

while True:
    for bot in bots:
        bot.execute()
    time.sleep(10)
