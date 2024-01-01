from brownie import accounts
import yaml

from eth_abi.packed import encode_packed
from eth_abi import encode
from web3 import Web3

from rlp import encode
from web3.types import HexBytes
from web3.datastructures import AttributeDict
from eth_utils import to_bytes

#print(Web3.to_hex(text="Another message for Base.")[2:].ljust(64, '0'))

LOCAL_ENVIRONMENT_NETWORKS = ["development", "solidity-local"]
GAS_LIMIT = 300000
TOKEN_MAX_SUPPLY = 21000
NULL_ADDRESS = '0x0000000000000000000000000000000000000000'

def get_account(chain):
    if chain in LOCAL_ENVIRONMENT_NETWORKS:
        return accounts[0]
    else:
        return accounts.load("airdrop-account")
    
def add_contract(chain, address):
    with open ('brownie-config.yaml') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    taiko = data["networks"][chain]
    if (taiko["contracts"] is None):
        taiko["contracts"] = []
    if address not in taiko["contracts"]:
        taiko["contracts"].append(address)
        with open("brownie-config.yaml", "w") as file:
            yaml.dump(data, file)
    
def show_brownie_config():
    with open ('brownie-config.yaml') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    print(data)