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
__version__ = "0.1.1"
__maintainer__ = "Matt Doiron"
__email__ = "mattdoiron@gmail.com"
__status__ = "Development"

# TODO save data transferred, uptime persistently
# TODO test init scripts (both types init.d and upstart)
# TODO clean up css files (lots of unused stuff)
# TODO refactor to reduce duplicate code


# ----------------------------------------------------
# Imports
# ----------------------------------------------------

import time
import os
import threading
import atexit
import urllib
import json
import errno
from socket import error as socket_error

import bitcoin.rpc as rpc
from bitcoin.rpc import JSONRPCException
from bottle import Bottle, template, static_file, TEMPLATE_PATH
import config


# ----------------------------------------------------
# Create Bottle App and Set Templates Dir
# ----------------------------------------------------

app = Bottle()
APP_ROOT = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH.insert(0, os.path.join(APP_ROOT, 'views'))


# ----------------------------------------------------
# Page Cache Class
# ----------------------------------------------------

class PageCache(object):
    """Takes care of getting and caching pages of different types."""

    def __init__(self):
        """Upon init, refresh cached pages"""

        # Fetch and cache all pages
        for page in config.PAGES.keys():
            self.cache_page(page)

    @staticmethod
    def cache_loc():
        """Cache location/IP separately because they should rarely change."""

        # Refresh IP and location
        try:
            loc = json.loads(urllib.urlopen(config.LOC_URL).read())
            config.SERVER_LOCATION = ', '.join([loc['city'], loc['region'], loc['country']])
            config.SERVER_IP_PUBLIC = loc['query']
            config.MAP_URL = config.MAP_URL.format(loc['lat'], loc['lon'])
        except (IOError, ValueError) as e:
            print "Error: {}".format(e)
            config.SERVER_IP_PUBLIC = 'n/a'
            config.SERVER_LOCATION = 'Unknown'
            config.MAP_URL = '#'

    @staticmethod
    def cache_404():
        """Creates a static 404 page"""
        return {'title': 'BTCnDash: Error 404 - Page not found',
                'donate': config.DONATE_ADDRESS,
                'donate_url': config.DONATE_URL + config.DONATE_ADDRESS}

    @staticmethod
    def cache_index():
        """Takes care of getting and caching the index page."""

        # Get all the required data
        try:
            con = rpc.Proxy(service_url=config.RPC_URN)
            info = con.call('getinfo')
            netinfo = con.call('getnettotals')
            sent = netinfo['totalbytessent']
            recv = netinfo['totalbytesrecv']
            total = sent + recv
            hashrate = float(con.call('getnetworkhashps'))
            transactions = con.call('getrawmempool')
        except JSONRPCException as e:
            print 'Error ({}): {}'.format(e.error['code'], e.error['message'])
            return False
        except ValueError as e:
            if e.message == "No JSON object could be decoded":
                raise ValueError("No JSON in response. Be sure you entered the "
                                 "correct username and password")
        except socket_error as e:
            print "Unable to connect to Bitcoin RPC server: {}".format(e)
            info = {'connections': None, 'blocks': 0, 'difficulty': 0, 'version': 'n/a'}
            sent = 0
            recv = 0
            total = 0.0000001
            hashrate = 0.0
            transactions = []

        # Collect, format and return the required data in a dict
        return {'cons': info['connections'],
                'hashrate': '{:,.1f}'.format(hashrate / 1.0E12),
                'block_height': '{:,}'.format(info['blocks']),
                'block_url': config.BLOCK_HEIGHT_URL + str(info['blocks']),
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
                'ip': ':'.join([config.SERVER_IP_PUBLIC, config.NODE_PORT]),
                'loc': config.SERVER_LOCATION,
                'donate': config.DONATE_ADDRESS,
                'donate_url': config.DONATE_URL + config.DONATE_ADDRESS,
                'qr_url': config.QR_URL + config.QR_PARAM + config.DONATE_ADDRESS,
                'title': 'Bitcoin Node Status',
                'map_url': config.MAP_URL,
                'hash_diff_url': config.HASH_DIFF_URL}

    @staticmethod
    def cache_peers():
        """Takes care of getting and caching the peers page."""

        # Get all the required data
        try:
            con = rpc.Proxy(service_url=config.RPC_URN)
            peers = con.call('getpeerinfo')
        except JSONRPCException as e:
            print 'Error ({}): {}'.format(e.error['code'], e.error['message'])
            return False
        except ValueError as e:
            if e.message == "No JSON object could be decoded":
                raise ValueError("No JSON in response. Be sure you entered "
                                 "the correct username and password")
        except socket_error as e:
            print "Unable to connect to Bitcoin RPC server: {}".format(e)
            peers = []

        # Collect, format and return the required data in a dict
        return {'peers': peers,
                'node_url': config.IP_INFO_URL,
                'title': 'Bitcoin Node Status - Peers',
                'donate': config.DONATE_ADDRESS,
                'donate_url': config.DONATE_URL + config.DONATE_ADDRESS}

    @staticmethod
    def cache_tx():
        """Takes care of getting and caching the transactions page."""

        # Get all the required data
        try:
            con = rpc.Proxy(service_url=config.RPC_URN)
            tx = con.call('getrawmempool')
        except JSONRPCException as e:
            print 'Error ({}): {}'.format(e.error['code'], e.error['message'])
            return False
        except ValueError as e:
            if e.message == "No JSON object could be decoded":
                raise ValueError("No JSON in response. Be sure you entered "
                                 "the correct username and password")
        except socket_error as e:
            print "Unable to connect to Bitcoin RPC server: {}".format(e)
            tx = []

        # Collect, format and return the required data in a dict
        return {'transactions': tx,
                'tx_url': config.TX_INFO_URL,
                'title': 'Bitcoin Node Status - Transactions',
                'donate': config.DONATE_ADDRESS,
                'donate_url': config.DONATE_URL + config.DONATE_ADDRESS}

    def cache_page(self, _page):
        """Gets and caches the specified page."""

        # Retrieve the dictionary containing info about the page
        page = config.PAGES.get(_page, 'index')

        # Find the last modified time of the STATIC_PAGE and the current time
        now = time.time()
        if os.path.exists(page['static']):
            modified = os.path.getmtime(page['static'])
        else:
            modified = False

        # Check if last modified time is > CACHE_TIME_LOC seconds ago
        if now - modified >= config.CACHE_TIME_LOC or not modified:

            # Refresh location and ip before checking other pages
            self.cache_loc()

        # Check if last modified time is > CACHE_TIME seconds ago
        if now - modified >= config.CACHE_TIME or not modified:

            # Retrieve the specified data
            data = getattr(self, 'cache_' + _page)()

            # Open the static file and write the compiled template
            if data:
                path = os.path.join(APP_ROOT, 'static', 'html', page['static'])
                with open(path, 'wb') as static_page:
                    static_page.write(template(page['template'], data=data))


# ----------------------------------------------------
# Worker Class to Refresh Page Cache in Background
# ----------------------------------------------------

class Worker(object):
    """Creates the worker thread, which refreshes the page cache"""

    def __init__(self):
        """Immediately refresh the cache"""
        print 'Launching worker...'
        self.refresh_cache()

    @staticmethod
    def interrupt():
        global worker_thread
        worker_thread.cancel()

    def refresh_cache(self):
        global worker_thread

        # Call PageCache object to check cache freshness
        PageCache()

        try:
            # Set the next thread to start in cache_time seconds
            worker_thread = threading.Timer(config.CACHE_TIME, self.refresh_cache, ())
            worker_thread.daemon = True
            worker_thread.start()

            # When you kill Bottle (SIGTERM), clear the next timer
            atexit.register(self.interrupt)

        except (KeyboardInterrupt, SystemExit):
            self.interrupt()


# ----------------------------------------------------
# Bottle Routes
# ----------------------------------------------------

@app.route('/')
@app.route('/<_page>')
@app.route('/<_page>/')
def index(_page=None):
    """Default route to display cached status pages."""
    if _page == 'donate':
        return config.DONATE_ADDRESS

    page_dict = config.PAGES.get(_page or 'index', config.PAGES['404'])
    path = os.path.join('static', 'html', page_dict['static'])
    return static_file(path, root=APP_ROOT)


@app.route('favicon.ico')
def favicon():
    path = os.path.join('static', 'img', 'favicon.ico')
    return static_file(path, root=APP_ROOT)


@app.route('/static/<filename:path>')
def static(filename):
    root = os.path.join(APP_ROOT, 'static')
    return static_file(filename, root=root)


@app.error(404)
def error(page=None):
    path = os.path.join('static', 'html', config.PAGES['404']['static'])
    return static_file(path, root=APP_ROOT)


# ----------------------------------------------------
# Start your engines!
# ----------------------------------------------------

if __name__ == '__main__':

    print 'Launching BTCnDash...'

    # Make sure the html cache folder is present
    html_path = os.path.join(APP_ROOT, 'static', 'html')
    try:
        os.makedirs(html_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Create a global thread for the worker
    worker_thread = threading.Thread()

    # Start the worker thread (this also creates the first cache)
    Worker()

    try:
        # Starts the Bottle server with the specified settings
        app.run(host=config.SERVER_IP_LOCAL, port=config.SERVER_PORT,
                server=config.SERVER_TYPE, debug=config.DEBUG)
    except socket_error as e:
        print 'Unable to start server: {}'.format(e)
