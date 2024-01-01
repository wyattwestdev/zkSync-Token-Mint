from brownie import network, config, Westoken
from scripts.utils import LOCAL_ENVIRONMENT_NETWORKS

def get_contract() -> Westoken:
    active_network = network.show_active()
    if active_network in LOCAL_ENVIRONMENT_NETWORKS:
        print(f'This operation requires a testnet network.')
        return None
    return Westoken.at(config["networks"][active_network].get("contracts")[-1])