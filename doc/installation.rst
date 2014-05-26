===============================
Installation Guide for BTCnDash
===============================

BTCnDash is developed on and intended for use on Debian/Ubuntu linux flavours. It should work anywhere python works, but it hasn't been tested very much.

Basic summary of steps:

1. Create a user under which BTCnDash will run

2. Create a python virtualenv for BTCnDash and its dependencies

3. Install the requirements into the virtualenv along with BTCnDash itself

5. Make sure the bitcoin.conf file has the appropriate settings enabled

4. Copy init or init.d scripts and edit any values to match your system

5. Start bitcoind and BTCnDash, then test it!

Create a new User
~~~~~~~~~~~~~~~~~

It's a bad idead to run most anything as root so let's create a user just for BTCnDash.::

sudo adduser --system --group btcndash

Create virtualenv
~~~~~~~~~~~~~~~~~

To follow...

More to follow...
