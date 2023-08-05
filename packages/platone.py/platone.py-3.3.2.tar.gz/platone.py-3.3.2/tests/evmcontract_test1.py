from hexbytes import HexBytes
from platone import Web3, HTTPProvider
from platone.platone import Platone
from platone.packages.platone_keys.utils import bech32, address
from platone.packages.eth_utils import to_checksum_address

true = True
false = False

# w3 = Web3(HTTPProvider("http://10.1.1.5:6789"))
# platon = PlatON(w3)
# print(w3.isConnected())
#
# from_address = "lax1yjjzvjph3tw4h2quw6mse25y492xy7fzwdtqja"
# print(from_address)
#
# send_privatekey = "16e80ad4079462cc7f9748af2f9cf03e8f7384bed597c086db4f11a98c3b08f0"
w3 = Web3(HTTPProvider(" http://58.251.94.108:56789"))  # 含有国密链的节点
# w3 = Web3(HTTPProvider("http://10.1.1.2:6789"))
platone = Platone(w3)
print(w3.isConnected())

from_address = "lax1uqug0zq7rcxddndleq4ux2ft3tv6dqljphydrl"
print(from_address)

send_privatekey = "983759fe9aac227c535b21d78792d79c2f399b1d43db46ae6d50a33875301557"


def contract_deploy(bytecode, fromAddress):
    bytecode = bytecode
    transactionHash = platone.sendTransaction(
        {
            "from": fromAddress,
            "gas": 1000000,
            "gasPrice": 1000000000,
            "data": bytecode,
        }
    )
    transactionHash = HexBytes(transactionHash).hex().lower()
    return transactionHash


bytecode = '608060405234801561001057600080fd5b50600060019080600181540180825580915050906001820390600052602060002001600090919290919091505550600060029080600181540180825580915050906001820390600052602060002001600090919290919091505550600060039080600181540180825580915050906001820390600052602060002001600090919290919091505550600060049080600181540180825580915050906001820390600052602060002001600090919290919091505550600060059080600181540180825580915050906001820390600052602060002001600090919290919091505550610153806101016000396000f3fe608060405234801561001057600080fd5b506004361061002b5760003560e01c8063853255cc14610030575b600080fd5b61003861004e565b6040518082815260200191505060405180910390f35b60007323346584d341c839148cd0b1166a16394074a1746387fbcc7760006040518263ffffffff1660e01b8152600401808060200182810382528381815481526020019150805480156100c057602002820191906000526020600020905b8154815260200190600101908083116100ac575b50509250505060206040518083038186803b1580156100de57600080fd5b505af41580156100f2573d6000803e3d6000fd5b505050506040513d602081101561010857600080fd5b810190808051906020019092919050505090509056fea265627a7a72315820971387e8880e897ea84556392fddbf14557ac01fec2b059cec87e9e436b79e2f64736f6c634300050d0032'

abi = [{"inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor"},
       {"constant": true, "inputs": [], "name": "sum",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": false,
        "stateMutability": "view", "type": "function"}]
tx = contract_deploy(bytecode, from_address)
print(tx)
tx_receipt = platone.waitForTransactionReceipt(tx)
print(tx_receipt)
contractAddress = tx_receipt.contractAddress
print(contractAddress)


# hrpgot, data = bech32.decode("lax", from_address)
# address = to_checksum_address(bytes(data))
# print('qqq')
# print(address)

def SendTxn(txn):
    signed_txn = platone.account.signTransaction(txn, private_key=send_privatekey)
    res = platone.sendRawTransaction(signed_txn.rawTransaction).hex()
    txn_receipt = platone.waitForTransactionReceipt(res)
    print(res)
    return txn_receipt


contract_instance = platone.contract(address=contractAddress, abi=abi)

txn = contract_instance.functions.ifControl(20).buildTransaction(
    {
        'chainId': 102,
        'nonce': platone.getTraensactionCount(from_address),
        'gas': 1000000,
        'value': 0,
        'gasPrice': 1000000000,
    }
)
print(SendTxn(txn))

result = contract_instance.functions.sum().call()
print(result)
