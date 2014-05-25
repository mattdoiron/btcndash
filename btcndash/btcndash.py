#!/usr/bin/python
# -*- coding: utf-8 -*-

""""
Copyright (c) 2014. All rights reserved.

BTCnDash is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BTCnDash is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BTCnDash. If not, see <http://www.gnu.org/licenses/>.
"""

"""
BTCnDash: Python script to generate and server status dashboard
of a full Bitcoin node

Acknowledgments:
 * Bottle: python web framework (http://bottlepy.org)
 * bitcoinrpc: rpc library (https://github.com/jgarzik/python-bitcoinrpc)
 * Blocks: bootstrap theme (http://alvarez.is/demo/free/blocks/)

Donate Bitcoin to 1AHT2Zq7JneADw94M8uCdKRrqVZfhrTBYM

:copyright: (c) 2014 by Matt Doiron.
:license: GPL v3, see LICENSE for more details.

"""

__title__ = "BTCnDash"
__author__ = "Matt Doiron"
__copyright__ = "Copyright 2014, Matt Doiron"
__license__ = "GPL v3"
__version__ = "0.1.0"
__maintainer__ = "Matt Doiron"
__email__ = "mattdoiron@gmail.com"
__status__ = "Development"

# TODO gracefully handle what happens if the node is offline
# TODO save data transfered, uptime persistently
# TODO test init scripts (both types init.d and upstart)
# TODO clean up css files (lots of unused stuff)


# ----------------------------------------------------
# Imports
# ----------------------------------------------------

import time
import os
import threading
import atexit
import urllib
import json

from bottle import Bottle, template, static_file, TEMPLATE_PATH
from bitcoinrpc.authproxy import AuthServiceProxy
from bitcoinrpc.authproxy import JSONRPCException


# ----------------------------------------------------
# Constants
# ----------------------------------------------------

# RPC and Node settings
RPC_UNAME = 'user1'
RPC_PWORD = 'YOUR_LONG_PASSWORD_HERE'
RPC_IP = '127.0.0.1'
RPC_PORT = '8332'
RPC_URN = "http://{}:{}@{}:{}".format(RPC_UNAME, RPC_PWORD, RPC_IP, RPC_PORT)
NODE_PORT = '8333'

# General settings
DONATE_ADDRESS = '1AHT2Zq7JneADw94M8uCdKRrqVZfhrTBYM'
CACHE_TIME = 300
CACHE_TIME_LOC = 1800

# Local server settings
SERVER_IP_LOCAL = '192.168.2.x'
SERVER_IP_PUBLIC = None
SERVER_PORT = '8334'
SERVER_TYPE = 'cherrypy'
SERVER_LOCATION = None
DEBUG = False
APP_ROOT = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH.insert(0, os.path.join(APP_ROOT, 'views'))
PAGES = {'index': {'template': 'index.tpl',
                   'static': 'index.html'},
         'peers': {'template': 'peers.tpl',
                   'static': 'peers.html'},
         'tx':    {'template': 'tx.tpl',
                   'static': 'tx.html'},
         '404':   {'template': '404.tpl',
                   'static': '404.html'}}

# External API settings
QR_URL = 'https://chart.googleapis.com/chart'
QR_PARAM = '?cht=qr&chs=186x186&chld=L|0&chl='
BLOCK_HEIGHT_URL = 'https://blockchain.info/block-height/'
IP_INFO_URL = 'https://blockchain.info/ip-address/'
TX_INFO_URL = 'https://blockchain.info/tx/'
HASH_DIFF_URL = 'https://bitcoinwisdom.com/bitcoin/difficulty'
LOC_URL = 'http://freegeoip.net/json/'
MAP_URL = 'https://maps.google.com/maps?q={},{}&z=11'


# ----------------------------------------------------
# Page Cache Class
# ----------------------------------------------------

class PageCache(object):
    """Takes care of getting and caching pages of different types."""

    def __init__(self):
        """Upon init, refresh cached pages"""

        # Fetch and cache all pages
        for page in PAGES.keys():
            self.cache_page(page)

    def cache_loc(self):
        """Cache location/IP separately because they should rarely change."""
        # Refresh IP and location
        try:
            global SERVER_IP_PUBLIC
            global SERVER_LOCATION
            global MAP_URL
            loc = json.loads(urllib.urlopen(LOC_URL).read())
            SERVER_LOCATION = ', '.join([loc['city'],
                                         loc['region_code'],
                                         loc['country_name']])
            SERVER_IP_PUBLIC = loc['ip']
            MAP_URL = MAP_URL.format(loc['latitude'], loc['longitude'])
        except IOError as e:
            print 'Error: {}'.format(e)
            SERVER_IP_PUBLIC = 'n/a'
            SERVER_LOCATION = 'Unknown'
            MAP_URL = '#'

    def cache_404(self):
        """Creates a static 404 page"""
        return dict()

    def cache_index(self):
        """Takes care of getting and caching the index page."""

        # Get all the required data
        try:
            rpc = AuthServiceProxy(RPC_URN)
            info = rpc.getinfo()
            netinfo = rpc.getnettotals()
            sent = netinfo['totalbytessent']
            recv = netinfo['totalbytesrecv']
            total = sent + recv
            hashrate = rpc.getnetworkhashps()
            transactions = rpc.getrawmempool()
        except JSONRPCException as e:
            print 'Error ({}): {}'.format(e.error['code'], e.error['message'])
            return False

        # Collect, format and return the required data in a dict
        return {'cons': info['connections'],
                'hashrate': '{:,.1f}'.format(hashrate / 1.0E12),
                'block_height': '{:,}'.format(info['blocks']),
                'block_url': BLOCK_HEIGHT_URL + str(info['blocks']),
                'diff': '{:,.2f}'.format(info['difficulty']),
                'version': info['version'],
                'sent': '{:,.1f}'.format(sent / 1048576.0),
                'recv': '{:,.1f}'.format(recv / 1048576.0),
                'total': '{:,.3f}'.format(total / 1073741824.0),
                'pcnt_in': '{:,.1f}'.format(recv / float(total) * 100.0),
                'pcnt_out': '{:,.1f}'.format(sent / float(total) * 100.0),
                'tx': transactions,
                'tx_count': '{:,}'.format(len(transactions)),
                'update': time.strftime("%Y-%m-%d %H:%M:%S"),
                'ip': ':'.join([SERVER_IP_PUBLIC, NODE_PORT]),
                'loc': SERVER_LOCATION,
                'donate': DONATE_ADDRESS,
                'qr_url': QR_URL + QR_PARAM + DONATE_ADDRESS,
                'title': 'Bitcoin Node Status',
                'map_url': MAP_URL,
                'hash_diff_url': HASH_DIFF_URL}

    def cache_peers(self):
        """Takes care of getting and caching the peers page."""

        # Get all the required data
        try:
            rpc = AuthServiceProxy(RPC_URN)
            peers = rpc.getpeerinfo()
        except JSONRPCException as e:
            print 'Error ({}): {}'.format(e.error['code'], e.error['message'])
            return False

        # Collect, format and return the required data in a dict
        return {'peers': peers,
                'node_url': IP_INFO_URL,
                'title': 'Bitcoin Node Status - Peers',
                'donate': DONATE_ADDRESS}

    def cache_tx(self):
        """Takes care of getting and caching the transactions page."""

        # Get all the required data
        try:
            rpc = AuthServiceProxy(RPC_URN)
            tx = rpc.getrawmempool()
        except JSONRPCException as e:
            print 'Error ({}): {}'.format(e.error['code'], e.error['message'])
            return False

        # Collect, format and return the required data in a dict
        return {'transactions': tx,
                'tx_url': TX_INFO_URL,
                'title': 'Bitcoin Node Status - Transactions',
                'donate': DONATE_ADDRESS}

    def cache_page(self, _page):
        """Gets and caches the specfied page."""

        #Retrive the dictionary contianing info about the page
        page = PAGES.get(_page, 'index')

        # Find the last modified time of the STATIC_PAGE and the current time
        now = time.time()
        if os.path.exists(page['static']):
            modified = os.path.getmtime(page['static'])
        else:
            modified = False

        # Check if last modified time is > CACHE_TIME_LOC seconds ago
        if now - modified >= CACHE_TIME_LOC or not modified:
            
            # Refresh location and ip before checking other pages
            self.cache_loc()

        # Check if last modified time is > CACHE_TIME seconds ago
        if now - modified >= CACHE_TIME or not modified:

            # Retrieve the specified data
            data = getattr(self, 'cache_' + _page)()

            # Open the static file and write the compiled template
            if data:
                path = os.path.join(APP_ROOT, 'static', 'html', page['static'])
                with open(path, 'wb') as file:
                    file.write(template(page['template'], data=data))


# ----------------------------------------------------
# Worker Class to Refresh Page Cache in Background
# ----------------------------------------------------

class Worker(object):
    """Creates the worker thread, which refreshes the page cache"""

    def __init__(self):
        self.refreshCache(0)

    def interrupt(self):
        global workerThread
        workerThread.cancel()

    def refreshCache(self, _cache_time=False):
        global workerThread

        if not _cache_time:
            cache_time = CACHE_TIME

        # Call PageCache object to check cache freshness
        PageCache()

        try:
            # Set the next thread to start in cache_time seconds
            workerThread = threading.Timer(cache_time, self.refreshCache, ())
            workerThread.daemon = True
            workerThread.start()

            # When you kill Bottle (SIGTERM), clear the next timer
            atexit.register(self.interrupt)

        except (KeyboardInterrupt, SystemExit):
            self.interrupt()


# ----------------------------------------------------
# Create Bottle App
# ----------------------------------------------------

app = Bottle()


# ----------------------------------------------------
# Bottle Routes
# ----------------------------------------------------

@app.route('/')
@app.route('/<page>')
@app.route('/<page>/')
def index(page=None):
    """Default route to display cached status pages."""
    path = os.path.join('static', 'html', PAGES[page or 'index']['static'])
    return static_file(path, root=APP_ROOT)


@app.route('/static/<filename:path>')
def static(filename):
    root = os.path.join(APP_ROOT, 'static')
    return static_file(filename, root=root)


@app.error(404)
def error():
    path = os.path.join('static', 'html', PAGES['404']['static'])
    return static_file(path, root=APP_ROOT)

# ----------------------------------------------------
# Start your engines!
# ----------------------------------------------------

if __name__ == '__main__':

    # Create a global thread for the worker
    workerThread = threading.Thread()

    # Start the worker thread
    Worker()

    # Starts the Bottle server with the specified settings
    app.run(host=SERVER_IP_LOCAL, port=SERVER_PORT,
            server=SERVER_TYPE, debug=DEBUG)
