# Bitcoind RCP Settings
RPC_URN = "http://user1:YOUR_BIG_LONG_PASSWORD_HERE@127.0.0.1:8332"
NODE_PORT = 8333

# BTCnDash Settings
DONATE_ADDRESS = "1AHT2Zq7JneADw94M8uCdKRrqVZfhrTBYM"
CACHE_TIME = 300
CACHE_TIME_LOC = 1800
SERVER_IP_LOCAL = "192.168.2.0"
SERVER_IP_PUBLIC = "detect"
SERVER_PORT = 8334
SERVER_TYPE = "cherrypy"
SERVER_LOCATION = "detect"
SERVER_LATITUDE = "detect"
SERVER_LONGITUDE = "detect"
DEBUG = False
LOG_LEVEL = 'INFO'
PAGES = {'index': {'template': "index.tpl",
                   'static': "index.html",
                   'title': "Bitcoin Node Status"},
         'peers': {'template': "peers.tpl",
                   'static': "peers.html",
                   'title': "Bitcoin Node Status - Peers"},
         'tx':    {'template': "tx.tpl",
                   'static': "tx.html",
                   'title': "Bitcoin Node Status - Transactions"},
         '404':   {'template': "404.tpl",
                   'static': "404.html",
                   'title': "Bitcoin Node Status - Page Not Found"}}

# API Settings
QR_URL = "https://chart.googleapis.com/chart"
QR_PARAM = "?cht=qr&chs=186x186&chld=L|0&chl="
BLOCK_HEIGHT_URL = "https://blockchain.info/block-height/"
IP_INFO_URL = "https://blockchain.info/ip-address/"
TX_INFO_URL = "https://blockchain.info/tx/"
HASH_DIFF_URL = "https://bitcoinwisdom.com/bitcoin/difficulty"
LOC_URL = "http://ip-api.com/json/"
MAP_URL = "https://maps.google.com/maps?q={},{}&z=11"
DONATE_URL = "https://blockchain.info/address/"

# Dash Block Registry
DASH_BLOCK_REGISTRY = {
    'index': {'rpc_commands': ["getinfo", "getnettotals", "getnetworkhashps", "getrawmempool"]},
    'peers': {'rpc_commands': ["getpeerinfo"]},
    'tx':    {'rpc_commands': ["getrawmempool"]},
    '404':   {'rpc_commands': ["getinfo"]}
}
