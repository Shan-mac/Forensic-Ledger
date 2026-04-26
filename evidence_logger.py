import hashlib
import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

if w3.is_connected():
    print(" Connected to Ganache Blockchain!")
else:
    print(" Failed to connect. Is Ganache running?")
    exit()

contract_address = os.getenv("CONTRACT_ADDRESS")

contract_abi = json.loads('''[
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_fileHash",
				"type": "string"
			}
		],
		"name": "recordEvidence",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "evidenceRegistry",
		"outputs": [
			{
				"internalType": "string",
				"name": "fileHash",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "exists",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_fileHash",
				"type": "string"
			}
		],
		"name": "verifyEvidence",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]''')

contract = w3.eth.contract(address=contract_address, abi=contract_abi)
investigator_account = w3.eth.accounts[0]

def hash_evidence(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read the file in small chunks just like real forensic tools
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


try:
    file_to_hash = "sample_evidence.txt"
    print(f"\n Analyzing Evidence: {file_to_hash}")
    digital_fingerprint = hash_evidence(file_to_hash)
    print(f" Digital Fingerprint (SHA-256): {digital_fingerprint}")
    print(" Locking evidence onto the blockchain...")
    tx_hash = contract.functions.recordEvidence(digital_fingerprint).transact({'from': investigator_account})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    print(f" SUCCESS! Evidence permanently locked in Block #{receipt.blockNumber}")
    print(f" Transaction Hash: {tx_hash.hex()}\n")

except Exception as e:
    print(f"\n Error: {e}")