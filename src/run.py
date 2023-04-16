from web3 import Web3
import os
import time
import datetime
import pandas as pd
from config import futures_manager_abi, futures_manager_address, proxy_abi, market_abi

def run():
    URL = os.getenv('infura')

    # create a Web3 instance that points to the POA network
    w3 = Web3(Web3.HTTPProvider(URL))

    # check if the connection was successful by getting the latest block number
    latest_block = w3.eth.block_number

    futures_manager_contract = w3.eth.contract(address=futures_manager_address, abi=futures_manager_abi)
    futures_contracts = futures_manager_contract.functions.allMarkets().call()



    rates = pd.DataFrame()

    while True:
        perps_funding_rates = {}
        ts = datetime.datetime.utcnow()
        for i in futures_contracts:
            try:
                proxy_tmp = w3.eth.contract(address=i, abi=proxy_abi).functions.getAllTargets().call()[1]
                perps_funding_rates[i] = w3.eth.contract(address=proxy_tmp, abi=market_abi).functions.currentFundingRate().call() / 10**18 / 24 * 100
            except:
                pass

            
            entry = pd.DataFrame(perps_funding_rates, index=[0]).T.reset_index().rename(columns={'index': 'address', 0: 'funding_rate'})
            entry['ts'] = ts
            rates = pd.concat([rates, entry])
        print(rates)
        time.sleep(60)

if __name__ == '__main__':
    run()