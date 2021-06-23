import threading
from Session import Session
from Network import Network

class Handler():
    """ The Handler class is responsible for orchestrating the ongoing connections
        by waiting for clients connect and then when they do establishing the 
        connection and creating a session object in a new thread to manage the session. """
    # Will implement a inefficient faux multi-threading approach for the moment as it's faster to set up
    def __init__(self, config, db):
        self.config = config
        self.db = db

    def create_thread(self, net):
        """ Creates session and new thread for a given connection. """
        session = Session(self.config, net, self.db)
        thread = threading.Thread(target=session_thread, args=(session,))        

    def wait_for_client(self):
        """ Creates a network object which listens for an incoming connection 
            and when it receives one calls create_thread to manage session creation """
        # This is not an optimal solution as issues could arise from multiple clients
        # attempting simultaneous connection. Could it be handled by altering client code
        # so that it reattempts connection until successful?
        net = Network(config)
        if net.listen_for_client():
            return self.create_thread(net)
        else:
            return False
        
    
def session_thread(session):
    while result:
       result = session.listen_for_cmd()

