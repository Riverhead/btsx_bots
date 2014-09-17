

# if you derive from Bot, it will play nice with the configuration and bot settings
class ExampleBot():

    def __init__(self, client, feeds, bot_config, log):  
        # executes after client is connected and config is loaded

        self.log = log
        self.client = client
        if not "bot_type" in bot_config or bot_config["bot_type"]:
            raise Exception("Bad bot configuration object")
        if bot_config["bot_type"] !=  "  Bot type name I expect  ":
            raise Exception("Bad bot configuration object")
        self.config = bot_config

        self.name = self.config["account_name"]
        init_balance = self.client.get_balance("BTSX")
        self.log("initialized bot")


    # This is executed *often* - you are responsible for caching (except feeds) and short-circuiting
    def execute(self)
        external_price = self.feeds["usd_per_btsx"].fetch()

        #   self.make_money()
