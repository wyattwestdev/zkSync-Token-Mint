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

            tx = None

            if (option.isnumeric()):

                if (int(option) == 1):
                    amount = input('\nChoose the amount to be minted: ')
                    tx = mint(account, contract, amount)            
                elif (int(option) == 2):
                    amount = input('\nChoose the amount to be burned: ')
                    tx = burn(account, contract, amount)
                elif (int(option) == 3):
                    amount = input('\nChoose the amount to be burned from the supply: ')
                    tx = burnSupply(account, contract, amount)   
                elif (int(option) == 4):
                    amount = input('\nChoose the amount to be added to the supply: ')
                    tx = increaseSupply(account, contract, amount)   

                total_fee = totalFeeCalculator(active_chain, tx)

                if tx != None:
                    
                    print(f'Total tx fee = {total_fee}.')     

        except ValueError as exception:

            print(exception)

def mint(account, contract, amount):

    return contract.mint(amount, {"from": account})

def burn(account, contract, amount):

    return contract.burn(amount, {"from": account})

def burnSupply(account, contract, amount):
    
    return contract.burnSupply(amount, {"from": account})

def increaseSupply(account, contract, amount):
    
    return contract.increaseSupply(amount, {"from": account})

def totalFeeCalculator(active_chain, tx) -> int:

    total_fee = 0

    if tx != None:

        gas_price = web3.eth.getTransaction(tx.txid).gasPrice
        gas_used = web3.eth.getTransactionReceipt(tx.txid).gasUsed
        l1_fee = Web3.toInt(hexstr=web3.eth.getTransactionReceipt(tx.txid).l1Fee) if (active_chain == 'Scroll' or active_chain == 'Base') else 0

        total_fee = int(l1_fee + (gas_price * gas_used) / (10 ** 26))
    
    return total_fee

# brownie run scripts/interact.py --network zkSync
def main():

    active_chain = network.show_active()
    account = Utils.get_account(active_chain)  
    contract = get_contract()
    menu(account, contract, active_chain)