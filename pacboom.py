from web3 import Web3
import requests
from eth_account import Account as EthereumAccount
from loguru import logger as ll
from config import abi, headers, proxies
import random
import time


class Pacboom():
    def __init__(self, private_key):
        self.private_key = private_key
        self.w3 = Web3(Web3.HTTPProvider("https://rpc.blast.io"))
        self.account = EthereumAccount.from_key(self.private_key)
        self.contract_address = self.w3.to_checksum_address("0x3743E1dFC5D91BA60c8B9561A436982f92866843")
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=abi)
        self.headers = headers
        self.proxy = {
            'http': proxies[0]
        }
        ll.debug(self.proxy)

    def take_jwt(self):
        url = 'https://pacboom.com/create-jwt'
        body = {
            'userAddress': self.account.address
        }
        response = requests.post(url=url, headers=headers, proxies=self.proxy, json=body)
        self.headers['Authorization'] = response.json().get('token')

    def send_points(self):
        ll.info(headers)
        response = requests.post(url='https://pacboom.com/initialize-score', headers=self.headers, proxies=self.proxy)

        if response.status_code == 401:
            ll.error(f'Initialize score: STATUS {response.status_code} | Response {response.json()}')
            time.sleep(10)
            return False
        else:
            ll.info(f'Initialize score: STATUS {response.status_code} | Response {response.json()}')

        choise = random.randint(1, 1000)
        if choise >= 1 and choise <= 300:
            score = random.randint(1000, 10000)
            score = int(round(score / 10000, 2) * 10000)
            ll.info(f'Score will be {score}')
            sleep = random.randint(60, 100)
            ll.info(f"Sleep {sleep} sec")
            time.sleep(sleep)
        elif choise >= 301 and choise <= 650:
            score = random.randint(10000, 30000)
            score = int(round(score / 100000, 3) * 100000)
            ll.info(f'Score will be {score}')
            sleep = random.randint(180, 340)
            ll.info(f"Sleep {sleep} sec")
            time.sleep(sleep)
        elif choise >= 651 and choise <= 850:
            score = random.randint(30000, 50000)
            score = int(round(score / 100000, 3) * 100000)
            ll.info(f'Score will be {score}')
            sleep = random.randint(340, 580)
            ll.info(f"Sleep {sleep} sec")
            time.sleep(sleep)
        elif choise >= 851 and choise <= 950:
            score = random.randint(50000, 110000)
            score = int(round(score / 100000, 3) * 100000)
            ll.info(f'Score will be {score}')
            sleep = random.randint(580, 1000)
            ll.info(f"Sleep {sleep} sec")
            time.sleep(sleep)
        elif choise >= 951 and choise <= 1000:
            score = random.randint(100000, 120000)
            score = int(round(score / 1000000, 4) * 1000000)
            ll.info(f'Score will be {score}')
            sleep = random.randint(1000, 1240)
            ll.info(f"Sleep {sleep} sec")
            time.sleep(sleep)

        body = {
            'address': self.account.address,
            'score': score
        }
        response = requests.post(url="https://pacboom.com/saveScore", headers=headers, proxies=self.proxy, json=body)
        ll.info(f"Save score: STATUS {response.status_code}")
        time.sleep(random.randint(1, 5))
        body = {
            'score': score
        }
        response = requests.post(url='https://pacboom.com/getSignature', headers=headers, proxies=self.proxy, json=body)
        ll.info(f"Get Signature: {response.json()} ")
        return response.json().get('signature'), response.json().get('timestamp'), score

    def send_transaction(self, data):
        claim_points = self.contract.functions.claimPoints(data[2], data[1], data[0]).build_transaction({
            'from': self.account.address,
            'gas': random.randint(220000, 260000),
            'gasPrice': self.w3.to_wei(random.randint(1, 10) / 10, 'gwei'),
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
        })

        # Sign swap tx and send to blockchain
        sign_tx = self.w3.eth.account.sign_transaction(claim_points, private_key=self.private_key)
        buy_tx = self.w3.eth.send_raw_transaction(sign_tx.raw_transaction)
        ll.info("Txn sent, awaiting for response.")

        # Await for result
        tx_result = self.w3.eth.wait_for_transaction_receipt(buy_tx)

        # Transaction status verification
        # If status == 1: Swap success.
        if tx_result['status'] == 1:
            ll.success("Success! TX:", self.w3.to_hex(buy_tx))
            return True
        else:
            ll.error("Error! TX:", self.w3.to_hex(buy_tx))
            return False

    def pacboom(self):
        x = 0
        self.take_jwt()
        while x != 3:
            while True:
                try:
                    data = self.send_points()
                    self.send_transaction(data)
                    sleep = random.randint(10, 30)
                    ll.info(f"Sleep: {sleep} sec")
                    x = 0
                except requests.RequestException as err:
                    ll.warning(err)
                    break
                except Exception as err:
                    ll.warning(err)
                    self.take_jwt()
                    break
            x = x + 1
