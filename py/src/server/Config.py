class Config():
    def __init__(self, config_loc = "~/.blackShardServer.cfg"):
        self.config_loc = config_loc
        self.load_config()

    def load_config(self):
        """ Open configuration file, parse and set variables """
        # Will write code later, just hard coding variables for now
        self.header = "Welcome to my server full of wholesome pastes."
