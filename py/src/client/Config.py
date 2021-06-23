class Config():
    def __init__(self, config_loc = "~/.blackShard.cfg"):
        self.config_loc = config_loc
        self.load_config()

    def load_config(self):
        """ Open configuration file, parse and set variables """
        # Will write code later, just hard coding variables for now
        self.text_editor = "vim"
