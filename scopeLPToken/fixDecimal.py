import pandas as pd
from classes.Web3Call import Web3Call
from utils.db import contract

contract = contract['bsc']
list_token = [
"0x469e0d351b868cb397967e57a00dc7de082542a3",
"0x3286a3f5de8b52ee9c967c7f82e1f9d158895e99",
"0x30e3a76f435908414d42a92505497b3681f5504a",
"0x4e94e170b17bd4b457e690ecb21a63d28510e920",
"0xdf3df1caac971ebea3d1e606bd7fb4a12b5ada96",
"0x94af1370e498ac2b695d7e56512fd2805e707828",
"0x31eded84f47458941f7b25c27fe96a923fdd38ac",
"0xf8c33277db4c5ec53e0145cb8b9a62801e23a753",
"0xe52be9828d4e555eedf6aac6afc35084b6c0a4ae",
"0xe6c0dc3fafbdb5edd1cbbe39982728864cdc7abf",
"0x9b1c23fccc05ad8a2f78b92cfc243ac03d1ad0a2",
"0x4de4988d844394905ff1eeb5b42dd34128ca7802",
"0x8bb5d992daa3186385a9fa1cec71f8fe852bd36a",
"0x8f35e10ae6e56f85e21ba9453de78a8436d87c07",
"0xacf1715c2225fd16f66750f450d47e900b121cbf",
"0x8f741a40ecdd61685d3266f14ff76f63db28cb84",
"0x26959a440fe864124fcb9afb12b71fc3bfbf2a85",
"0xae55b4baf1828b1e9bb28f11d3a4cdc1f15fd09b",
"0xd166bb5fdf745e51d68ec27c45c725d91213106a",
"0x3b9d0be995b10600b1f10248173283d512f85e09",
"0x8f1d683b3bc33ed2ab7a11ae9f72bf869819eb3d",
"0xa8d7f4a540884d8245fe24ec3970480c4a6ca97b",
"0xe7698afc8cf3e5ab051767e6c814cbbc47abb6f0",
"0x8885013f8a64889c7228bbb6de747a291eb6663d",
"0x7364919f0ee9fb8defc88d0cc4cec18387e898e5",
"0x7e4b8c9593319dd351c4d26e85a7a792ede7939e",
"0xdf50678e65dbf3842854207a05ff626783f73614",
"0xe7cf56a19b2e76dfbdd10a7cd953317ec9860e86",
"0xd9f4b92ba1e3c589a93ab24841c53bc9d27025c0",
"0x86cc9e446da2e3777702073bf4f6eb349fc76bea",
"0xbeaacd47480679b754bfe62aed4b151aae887bcd",
"0x69b5f70857800b236c7329bf9067797bfb7d1c46",
"0xcf39b3bf82cdda2ae208729e6dfa8abc68729561",
"0x0fabba0a03879e1b5a114214fbbe1485dec5e4f9",
"0x63c562e78e7c0fc568e41f3921d78f2446b4567d",
"0x56c2723807c398a5d263c698d660165802f104a8",
"0xf589ad858f165a4a8026a54c5aafd2f2867919fa",
"0xb1ed20709fb0a9b95cc00f9a8e003666961a0657",
"0x535c18be97593241194541f029176e14363cff20",
"0x93f44bc6007dc3773d6d292d0a801c5dd98fd238",
"0x31fdf4333d2edcadcebd25edd7dabcb73b27e851",
"0x8494961ffd40ece6747a3f83745a3e40c403277d",
"0x83a5b89f8da7517d91498224b5ec8c4c040b3ff8",
"0x2233f23615a3429c5b2437628f6b66b59809ce11",
"0xb69a3ae9ad8cab85b8aa96be952550c9172722fd",
"0xbb478f66a4bcbdaea738be8fa95e105e48918b06",
"0xc115f337130aaae97f4ab34751ee2854d2795958",
"0xcf064bb27af87ff677c7da084ce879559a8400db",
"0xcadf38af5c327f0c36888149d56cf53497f895e1",
"0xf62f72bc967f9b1db922373d25ad23be6e3e72d3",
"0x205938aed42d920a639bd20e29237e1e717e9d59",
"0xff0307b4a7d2b4c04e6b7e29f1fad39e99a0396f",
"0xcc47d752d57a1836d8ac61aed7e09e04c38be83e",
"0x92ade4d5fab9b060de19a3ff74fcca4ef0ba8a4e",
"0x4b78401b64165746725bf6d367e44e8d335ea436",
"0x6dc93f3c6a03df3b264dbe5c096d53110b836752",
"0x81b3e23aae7cba1041d308e8dfdba5e074867cc3",
"0xdd9114597217125d60f67ebf099f0e9570954f46",
"0x98c8fcf5e49d383718fec8bdf0c78d4a9cae80f9",
"0x6cd4814a9ac460d89c390d2c871ef884152c2638",
"0x84c182aa7daba78f61f90f2e62981fd88eb3946d",
"0x76944c37c4931ddfbf2f248d777b659af390c72d",
"0x8bb5d992daa3186385a9fa1cec71f8fe852bd36a",
"0x5799f88ac03eb0f77ea56e101ae1e15b38b2d643",
"0xcc50baa6d6d6141c4de98d9cbac5a8ba6eacd0a8",
"0xb93c7d48e0799b07b5c639bfb8ddffa1f5d88654",
"0xcdc98e886fc1226ca3cc791d9814bfc6672e37e2",
"0x66f65c995b729a349a5c74342ebf26bb7d232e4c",
"0x4e48810bb734f7f104718e3b5517d0e815c7a037",
"0x4567e803804474b565cae615597b852373ff51b7",
"0xc78153b15ccc931205c62af311aebbb9751d354e",
"0xc325c5e6379f37dec4dece94752d17ab9836a750",
"0x44047cdef4cef8469af65832a56040f3f62795d3",
"0x6684e13fab047b97b59ee34d9975945c61a4014f",
"0x03ae26ba78b92ef0fe62178fe3d4ee003e328e51",
"0x7efbaabc514590cb6d5584dc5b4b215c0f92dc38",
"0xb99400ff63d4fa6cd444701219c66ecb2aafc9de",
"0xd11d2ba2d10eb01fd5d1c1837f811210cae59d14",
"0x8c2cbeabf0834589eb0ca69df446ec97e0a63689",
]
list_data = []
data = contract.find({"address": {"$in": list_token}})
for _lp_data in data:
    lpAddress = _lp_data['address']
    underlying0 = _lp_data['underlying'][0]['token_address']
    decimal0 = _lp_data['underlying'][0]['decimal']
    underlying1 = _lp_data['underlying'][1]['token_address']
    decimal1 = _lp_data['underlying'][1]['decimal']
    contract1 = Web3Call('bsc', underlying1)
    decimal1_web3 = contract1.callBlock('decimals', block_id = 26474870)
    contract0 = Web3Call('bsc', underlying0)
    decimal0_web3 = contract0.callBlock('decimals', block_id = 26474870)
    list_data.append({
        'lpaddress': lpAddress,
        'underlying0': underlying0,
        'underlying1': underlying1,
        'decimal0': decimal0,
        'decimal1': decimal1,
        'decimal0_web3': decimal0_web3,
        'decimal1_web1': decimal1_web3,
    })
pd.DataFrame(list_data).to_csv('fixdecimal.csv')
print()




