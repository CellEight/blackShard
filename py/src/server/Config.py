from os.path import isfile, expanduser
import yaml

class Config():
    def __init__(self, config_loc = expanduser("~/.config/blackshard/bs_server_conf.yaml")):
        self.config_loc = config_loc
        if isfile(config_loc):
            self.load_config()
        else:
            print("[!] Server has not yet been configured! Please run setup script.")
            exit(1)

    def load_config(self):
        """ Open configuration file, parse and set variables """
        with open(self.config_loc, 'r') as config_fd:
            config = yaml.safe_load(config_fd.read())
        self.server_ip = config['server_ip']
        self.server_port = config['server_port']
        self.db_ip = config['db_ip']
        self.db_port = config['db_port']
        self.db_user = config['db_user']
        self.db_password = config['db_password']
        self.db_name = config['db_name']
        self.header = config['header']
