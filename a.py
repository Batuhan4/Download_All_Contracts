import json
import requests
import time

# Set the number of API calls to make
num_calls = 4

# Calculate the wait time between API calls (in seconds)
wait_time = 1 / num_calls


# Your Etherscan API key
api_key = ''

# The base URL for the Etherscan API
base_url = 'https://api.etherscan.io/api'

# Open the JSON file and read the contents
with open('a.json', 'r',encoding='utf-8') as f:
    data = json.load(f)

# Extract the contract addresses and names from the JSON data
contract_addresses = [entry['ContractAddress'] for entry in data]
contract_names = [entry['ContractName'] for entry in data]

for contract_address in contract_addresses:
    time.sleep(wait_time)
    # Send a GET request to the Etherscan API to retrieve the source code
    params = {'module': 'contract', 'action': 'getsourcecode', 'address': contract_address, 'apikey': api_key}
    response = requests.get(base_url, params=params)

    # Check the response status code to make sure the request was successful
    if response.status_code == 200:
        # Parse the response data
        data = response.json()

        # Extract the source code from the response data
        source_code = data['result'][0]['SourceCode']

        # Save the source code to a file with the contract name
        contract_name = contract_names[contract_addresses.index(contract_address)]
        with open(f'{contract_name}.sol', 'w',encoding='utf-8') as f:
            f.write(source_code)
    else:
        print(f'Failed to retrieve source code for contract {contract_address}')
