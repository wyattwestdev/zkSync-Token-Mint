import scripts.utils as Utils
from scripts.contract import get_contract
from web3 import Web3
from brownie import network, config, web3

def menu(account, contract, active_chain):

    option = ''

    while (option != 'q'):

        print("\n**************************************************")
        print(  "*                      MENU                      *")
        print(  "*                                                *")
        print(  "* 1) Mint Token                                  *")
        print(  "* 2) Burn Token                                  *")
        print(  "* 3) Burn Token Supply                           *")
        print(  "* 4) Increase Token Supply                       *")
        print(  "* q) Exit the program                            *")
        print(  "*                                                *")
        print(  "**************************************************")
        print(f"\n  {contract.symbol()} Available Supply: {int(contract.getAvailableSupply() / (10 ** contract.decimals()))}")
        print(f"  {contract.symbol()} Max Supply: {int(contract.getMaxSupply() / (10 ** contract.decimals()))}")
        print(f"  {contract.symbol()} Wallet Supply: {int(contract.getBalance({'from': account}) / (10 ** contract.decimals()))}")
        option = input('\nChoose a menu option: ')

        try:
            if (option.isnumeric()):
                if (int(option) == 1):
                    amount = input('\nChoose the amount to be minted: ')
                    mint(account, contract, amount)            
                elif (int(option) == 2):
                    amount = input('\nChoose the amount to be burned: ')
                    burn(account, contract, amount)
                elif (int(option) == 3):
                    amount = input('\nChoose the amount to be burned from the supply: ')
                    burnSupply(account, contract, amount)   
                elif (int(option) == 4):
                    amount = input('\nChoose the amount to be added to the supply: ')
                    increaseSupply(account, contract, amount)        
        except ValueError as exception:
            print(exception)

def mint(account, contract, amount):

    contract.mint(amount, {"from": account})

def burn(account, contract, amount):

    contract.burn(amount, {"from": account})

def burnSupply(account, contract, amount):
    
    contract.burnSupply(amount, {"from": account})

def increaseSupply(account, contract, amount):
    
    contract.increaseSupply(amount, {"from": account})

def main():

    active_chain = network.show_active()
    account = Utils.get_account(active_chain)  
    contract = get_contract()
    menu(account, contract, active_chain)