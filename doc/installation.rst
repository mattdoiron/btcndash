===============================
Installation Guide for BTCnDash
===============================

BTCnDash is developed on and intended for use on Debian/Ubuntu linux flavours. It should work anywhere python works, but it hasn't been tested very much. This guide assumes you have bitcoind already installed. There are various tutorials on the web on how to do this.

Basic summary of steps:

1. Create a user under which BTCnDash will run

2. Install dependencies

3. Create a python virtualenv for BTCnDash and its dependencies

4. Download BTCnDash to newly created virtualenv.

5. Install requirements to new virtualenv.

6. Make sure the bitcoin.conf file has the appropriate settings enabled

7. Copy init or init.d scripts and edit any values to match your system

8. Set correct permissions

9. Open the required ports on your firewall.

10. Start bitcoind and BTCnDash, then test it!

Create a new User
~~~~~~~~~~~~~~~~~

It's a bad idead to run most anything as root so let's create a user just for BTCnDash.

    sudo adduser --system --group btcndash

Install Dependencies
~~~~~~~~~~~~~~~~~~~~

Various bits and pieces required by BTCnDash.

    sudo apt-get install python-pip python-virtualenv

Create virtualenv and Install Python requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Technically, this step is optional, but it's highly recommended to ensure updates to other Python files/libraries later don't break BTCnDash.

    cd /home/btcndash
    mkvirtualenv btcndash
    source btcndash/bin/activate

Get files for BTCnDash
~~~~~~~~~~~~~~~~~~~~~~

Download the latest version of BTCnDash

    wget https://bitbucket.org/mattdoiron/btcndash/get/57542ca054d3.zip
    
If you have mercurial installed you can also do:

    hg clone https://bitbucket.org/mattdoiron/btcndash
    
Install other requirements into virtualenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use pip to install the requirements as per the supplied requirements.txt file

    pip install -r requirements.txt
    
Configure bitcoind
~~~~~~~~~~~~~~~~~~

Take a loot at the supplied bitcoin.conf to see how to configure bitcoind to accept RPC requests. This will primarily involve providing a username and password (good ones).

Create startup scripts for BTCnDash
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the provided startup scripts (one or the other) and change any values near the top of the file to match your system and the location of various files.

Permisisons
~~~~~~~~~~~

Use the following command to make sure the files that will be used by BTCnDash are owned by the user created in step one.

    sudo chown -R btcndash:btcndash /path/to/virtualenv


Open firewall ports
~~~~~~~~~~~~~~~~~~~

Make sure you open the port for the BTCnDash webserver so that you can access it over your network and the internet. Note this is NOT the same as the RPC port. The RPC port should NOT be exposed unless you intend to run the BTCnDash program on a computer other than the one running bitcoind. You may need to open the webserver port on your router as well (similarly to how you would have opened a port for bitcoind to get it working).

Start it and test it
~~~~~~~~~~~~~~~~~~~~

Start BTCnDash with:

    sudo start btcndash
    
or

    sudo service btcndash start

