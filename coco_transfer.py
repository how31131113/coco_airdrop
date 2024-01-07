"""
1. 安装python，如果不会可以百度

2. 在终端依次执行
    pip install requests
    pip3 install web3==5.31.1
    
from_private_key 填入要发放空投的私钥
from_address 填入要发放空投的地址
transfer_addresses 填入要接收空头的地址
count 填入每人要发放多少币空投，1000个币等于1张


备注：地址持有coco，将不会获得空投
执行方式，在脚本所在路径的文件夹空白处打开终端，输入
python coco_transfer.py
"""
import requests
from web3 import Web3



# 输入你的私钥
from_private_key = ''
# 输入你的地址
from_address = ''
# 输入空投名单,替换掉以下示例
transfer_addresses = [
    '0xd6fa5B2c8D6A242944433C14F3f00B005F6C1eEf',
    '0xebdc0c73f8b0d38f3971cfbad42acc16066718ae',
    '0x6732D38E58f9Badd512A2d30b7e2b75Cd0037D21',
    '0xd797a7fcc9a046a0bf26bcd97c60b485b1fdd22d',
    '0xF22f2F9a57CFBf1D14226Fc2aCc6Ecd1E01AdBEe',
    '0x3caBf176B3F1c8D74F59834Fd4c96dC6e68Fe453',
    '0xd453b1c25bccd92add92d197e1d87a677d4e111e',
    '0x19fa59339dC1200820A065dd3ca911a17eba02BF',
    '0xEF19834596fc8fD524f483c8098577EFBb41efe2',
    '0x7E39ad71C8bf7848f728456E22160633b83B2aF6'
]
# 输入每个空投多少币，1000个币等于1张
count = 100



"""
以下不用改动
以下不用改动
以下不用改动
"""


def createHexData(count):
    data = 'data:,{"p":"core-20","op":"transfer","tick":"coco","amt":"%s"}' % (count)
    utf8_bytes = data.encode('utf-8')
    hex_str = utf8_bytes.hex()
    return "0x" + hex_str


def hasCoco(address):
    headers = {'accept': 'application/json, text/plain, */*'}
    params = {'address': address}
    response = requests.get('https://api.corescriptions.com/api/core-20/address', params=params, headers=headers)
    response_json = response.json()
    token_list = response_json['data']
    for token in token_list:
        tick = token['tick']

        if tick == 'coco':
            return True

    return False


def sendAirdrop(from_private_key, from_address, to_address, count):
    rpc_url = "https://rpc-core.icecreamswap.com"
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    from_address = Web3.toChecksumAddress(from_address)
    to_address = Web3.toChecksumAddress(to_address)
    nonce = web3.eth.get_transaction_count(from_address)
    gas_price = int(web3.eth.gas_price * 1.25)  # 看网络情况调高调低gas倍数，默认1.25
    hex_data = createHexData(count)

    tx = {
        'nonce': nonce,
        'chainId': 1116,
        'from': from_address,
        'to': to_address,
        'data': hex_data,
        'gasPrice': gas_price,
        'value': Web3.toWei(0, 'ether')
    }
    try:
        gas = web3.eth.estimateGas(tx)
        tx['gas'] = gas
        signed_tx = web3.eth.account.sign_transaction(tx, from_private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=10)
        if receipt.status == 1:
            print(f"Airdrop send successfully! {to_address}")
        else:
            print("Airdrop send failed!")
    except Exception as e:
        print(f"send failed,{e}")


if __name__ == '__main__':
    for address in transfer_addresses:

        if hasCoco(address):
            print(f"此地址已有coco，跳过 {address}")
            continue

        sendAirdrop(from_private_key=from_private_key,
                    from_address=from_address,
                    to_address=address,
                    count=count)
