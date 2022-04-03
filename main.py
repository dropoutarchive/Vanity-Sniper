import os
import sys
import ctypes
import requests
from time import time
from itertools import cycle
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

if sys.platform == "linux":
    os.system("clear")
else:
    os.system("cls")

class Discord():

    def __init__(self):
        ctypes.windll.kernel32.SetConsoleTitleW("vanity sniper")
        self.timestamp = lambda: str(datetime.fromtimestamp(time())).split(" ")[1]

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }

        with open("proxies.txt", encoding="utf-8") as f:
            self.proxies = [i.strip() for i in f]

        self.proxy = cycle(self.proxies)
        self.attempts = 0
        self.sniping = True

        self.token = None
        self.guild = None
        self.vanity = None

        self.magic = True

    def log(self, text: str, value: str):
        print("\x1b[38;2;73;73;73m[\x1b[0m%s\x1b[38;2;73;73;73m]\x1b[0m %s \x1b[38;2;73;73;73m%s\x1b[0m" % (self.timestamp(), text, value))

    def get_session(self):
        session = requests.Session()
        session.proxies.update({
            "https": "http://%s" % (next(self.proxy))
        })
        return session

    def claim(self):
        headers = {
            "authorization": self.token,
            "content-type": "application/json",
        }

        response = requests.patch("https://ptb.discord.com/api/v9/guilds/%s/vanity-url" % (self.guild), json={"code": self.vanity}, headers=headers)
        if response.status_code == 200:
            self.log("Successfully claimed", self.vanity)
            return sys.exit()
        else:
            self.log("Failed to update vanity.", "")

    def worker(self):
        while self.sniping:
            session = self.get_session()
            response = session.get("https://ptb.discord.com/api/v9/invites/%s" % (self.vanity))
            if response.status_code == 200:
                self.attempts += 1
                if not self.attempts % 100:
                    self.log("Vanity still unavailable after", "%s\x1b[0m requests." % (self.attempts))
            elif response.status_code == 404:
                self.sniping = False
                if self.magic:
                    self.magic = False
                    self.claim()
                return

    def run(self):
        self.token = input("\x1b[38;2;73;73;73m[\x1b[0m%s\x1b[38;2;73;73;73m]\x1b[0m Token\x1b[38;2;73;73;73m:\x1b[0m " % (self.timestamp()))
        self.guild = input("\x1b[38;2;73;73;73m[\x1b[0m%s\x1b[38;2;73;73;73m]\x1b[0m Guild\x1b[38;2;73;73;73m:\x1b[0m " % (self.timestamp()))
        self.vanity = input("\x1b[38;2;73;73;73m[\x1b[0m%s\x1b[38;2;73;73;73m]\x1b[0m Vanity\x1b[38;2;73;73;73m:\x1b[0m " % (self.timestamp()))

        print()

        with ThreadPoolExecutor(max_workers=10_000) as executor:
            for x in range(5_000):
                executor.submit(self.worker)

if __name__ == "__main__":
    Discord().run()
