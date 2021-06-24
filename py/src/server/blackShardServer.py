from Handler import Handler
from Config import Config
from Database import Database

def main():
    handler = Handler(Config(), Database())
    while True:
        if handler.wait_for_client():
            print("[*] Client Connected.")
        else:
            print("[!] Client Connection Failed.")

if __name__ == "__main__":
    main()
