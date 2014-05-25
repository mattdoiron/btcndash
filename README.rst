========
BTCnDash
========

BTCnDash: Python script to generate and server status dashboard of a full Bitcoin node

A web-based dashboard displaying information about a full bitcoin node such as current connections to the server, recent transactions forwarded, bandwidth usage, and network stats like hash rate. Most items are generated automatically or retrieved from the bitcoind server itself via RPC calls.

BTCnDash is meant to be lightweight, and with the assumption that there will be very low traffic to the dashboard. As such, it does not use a full webserver like Nginx or apache. It uses the Bottle microframework and generates static status pages on a schedule. CherryPy's server is used as the actuall webserver, but Bottle (and therefore BTCnDash) can be served by lots of different servers.

To launch the dashboard, all that is required is something like

::
python btcndash.py

Or you can use one of the example scripts in the scripts folder to start BTCnDash as a daemon.

The css is a bit of a mess and bloated for my purposes, but I hope to trim it down and clean it up as I go.

Hope you find it useful! If so, please consider donating Bitcoin to 1AHT2Zq7JneADw94M8uCdKRrqVZfhrTBYM

Author
======

Matt Doiron <mattdoiron@gmail.com>

Acknowledgments
===============

Thanks to those who make great tools like these:

* Bottle: python web framework (http://bottlepy.org)
* bitcoinrpc: rpc library (https://github.com/jgarzik/python-bitcoinrpc)
* Blocks: bootstrap theme (http://alvarez.is/demo/free/blocks/)
* CherryPy: btcndash uses the webserver from cherrypy (http://cherrypy.org/)

.. image:: doc/btcndash_screenshot.png