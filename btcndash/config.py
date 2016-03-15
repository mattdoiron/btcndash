# Bitcoind RCP Settings
RPC_URN = "http://user1:YOUR_BIG_LONG_PASSWORD_HERE@127.0.0.1:8332"
NODE_PORT = 8333

# BTCnDash Settings
HEADER_TITLE = " BTCnDash: Bitcoin Node Dashboard"
DONATE_ADDRESS = "1AHT2Zq7JneADw94M8uCdKRrqVZfhrTBYM"
CACHE_TIME = 300
CACHE_TIME_LOC = 1800
SERVER_IP_LOCAL = "192.168.2.0"
SERVER_IP_PUBLIC = "detect"
SERVER_PORT = 8335
SERVER_TYPE = "wsgiref"
SERVER_LOCATION = "detect"
SERVER_LATITUDE = "detect"
SERVER_LONGITUDE = "detect"
DEBUG = False
LOG_LEVEL = 'INFO'

# Registry of pages and info about them such as which blocks to include.
PAGES = {
    'index': {'template': "index.tpl",
              'static': "index.html",
              'title': "Bitcoin Node Status",
              'tiles': [['general', 'connections', 'bandwidth'],
                        ['bandwidth_summary', 'network', 'donate']]},
    'peers': {'template': "peers.tpl",
              'static': "peers.html",
              'title': "Bitcoin Node Status - Peers",
              'tiles': [['peers']]},
    'tx':    {'template': "tx.tpl",
              'static': "tx.html",
              'title': "Bitcoin Node Status - Transactions",
              'tiles': [['tx']]},
    '404':   {'template': "404.tpl",
              'static': "404.html",
              'title': "Bitcoin Node Status - Page Not Found",
              'tiles': [['404']]},
}

# API Settings
# Select your preferred services here and customize the parameters if required.
QR_URL = "https://chart.googleapis.com/chart"
QR_PARAM = "?cht=qr&chs=186x186&chld=L|0&chl="
BLOCK_HEIGHT_URL = "https://blockchain.info/block-height/"
IP_INFO_URL = "https://blockchain.info/ip-address/"
TX_INFO_URL = "https://blockchain.info/tx/"
HASH_DIFF_URL = "https://bitcoinwisdom.com/bitcoin/difficulty"
LOC_URL = "http://ip-api.com/json/"
MAP_URL = "https://maps.google.com/maps?q={},{}&z=11"
DONATE_URL = "https://blockchain.info/address/"

# Registry of 'tiles' and the RPC commands required to populate them with data.
# Do NOT change these unless you're creating custom tiles!
TILES = {
    'general':           {'template': "general.tpl",
                          'rpc_commands': []},
    'connections':       {'template': "connections.tpl",
                          'rpc_commands': ['getinfo']},
    'bandwidth':         {'template': "bandwidth.tpl",
                          'rpc_commands': ['getnettotals']},
    'bandwidth_summary': {'template': "bandwidth_summary.tpl",
                          'rpc_commands': ['getnettotals']},
    'network':           {'template': "network.tpl",
                          'rpc_commands': ['getnetworkhashps']},
    'donate':            {'template': "donate.tpl",
                          'rpc_commands': []},
    'peers':             {'template': "peers.tpl",
                          'rpc_commands': ["getpeerinfo"]},
    'tx':                {'template': "tx.tpl",
                          'rpc_commands': ["getrawmempool"]},
    '404':               {'template': "404.tpl",
                          'rpc_commands': []}
}
