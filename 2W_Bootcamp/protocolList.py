def getListProtocolName(_chain):  
    if _chain == 'avax':      
        list_protocol = [
        'Pangolin',
        'SushiSwap',
        'Synapse',
        'TraderJoe']
    elif _chain == 'eth':
        list_protocol = ['1inch',
        'Arrakis Finance',
        'Balancer',
        'Curve Finance',
        'DODO',
        'Frax',
        'KyberSwap',
        'KyberSwap Elastic',
        'PancakeSwap',
        'Saddle',
        'ShibaSwap',
        'SushiSwap',
        'Synapse',
        'UniSwap',
        'Uniswap V3']
    elif _chain == 'bsc':
        list_protocol = ['1inch',
        'ApeSwap',
        'BiSwap',
        'Ellipsis',
        'KyberSwap',
        'KyberSwap Elastic',
        'MDEX',
        'PancakeSwap',
        'Synapse',
        'Wault']
    return list_protocol
