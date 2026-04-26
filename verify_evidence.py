import hashlib
import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

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

def hash_evidence(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

try:
    file_to_check = "sample_evidence.txt"
    print(f"\n🔍 Scanning Evidence File: {file_to_check}")

    # Step 1: Hash the file on our computer right now
    current_fingerprint = hash_evidence(file_to_check)
    print(f" Current File Hash: {current_fingerprint}")

    print(" Asking the Blockchain if this hash exists...")
    
    is_valid, timestamp = contract.functions.verifyEvidence(current_fingerprint).call()

    if is_valid:
        print(f"\n SYSTEM VERIFIED: This exact file is authentic!")
        print(f" It was securely logged at Blockchain Timestamp: {timestamp}\n")

except Exception as e:
    print(f"\n ALERT: INTEGRITY FAILURE!")
    print(f"This file has been TAMPERED with, or it was never logged.")
    print(f"Details: {e}\n")