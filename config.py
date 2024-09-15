import json
import fake_useragent



with open('abi.json', 'r') as file:
    abi = json.load(file)

blast_address = "0xb1a5700fA2358173Fe465e6eA4Ff52E36e88E2ad"
UA = fake_useragent.UserAgent()
headers = {
    "Authorization": '',
    'User-Agent': UA.random,
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'connection': 'keep-alive',
    'content-type': 'application/json',
    'host': 'pacboom.com',
    'origin': 'https://pacboom.com',
    'referer': 'https://pacboom.com/index.html',
    'sec-ch-ua': 'Chromium;v=128, Not;A=Brand;v=24, Google Chrome;v=128',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
}

with open('proxy.txt', 'r') as file:
    proxies = [row.strip() for row in file]


