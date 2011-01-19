============
Installation
============

Setup Cloud Server
==================

1. Follow the instructions found at: http://cloudservers.rackspacecloud.com/index.php/Ubuntu_-_Setup

#. If you don't already have one on your local workstation, create a RSA
   public/private key pair for use with the new server.

::

    mkdir ~/.ssh
    chmod 700 ~/.ssh
    ssh-keygen -t rsa

#. Copy public key to the new server::

    ssh-copy-id <username>@<host>

Requirements
============

Install PostgreSQL
------------------

Blah

Install PostGIS
---------------

Blah

Python virtualenv
-----------------

1. Create a Python virtual environment tailored to the script.

   Install python-setuptools and virtualenv.

::

    sudo apt-get install python-setuptools
    sudo easy_install virtualenv

   Create the virtual environment

::

    sudo mkdir /usr/local/pythonenv
    cd /usr/local/pythonenv
    sudo virtualenv --no-site-packages KESTAVA

Some things needed in order to compile software later

::

    sudo apt-get install build-essential
    sudo apt-get install python-dev
    sudo apt-get install libxml2-dev libxslt-dev
    sudo apt-get install libpq-dev
    sudo apt-get install python-software-properties

Create a RSA public/private key pair for use with Github.  There may already be
a ~/.ssh directory present, if it was created to support ssh access to the host.

::

    mkdir ~/.ssh
    chmod 700 ~/.ssh
    ssh-keygen -t rsa

Jot down the passphrase you assigned to the private key somewhere.

Install git so we can work with source control.

::

    sudo add-apt-repository ppa:git-core/ppa
    sudo apt-get update
    sudo apt-get install git-core

These requirements should be installed in a Python virtual environment::

    1. cherrypy
    
    #. lxml (latest stable version), e.g.::
    
        sudo KESTAVA/bin/pip install lxml==2.2.8
    
    #. psycopg2
    
    ::
    
        sudo KESTAVA/bin/pip install psycopg2
    
    #. geopy (check this!)
    
    #. mox (only on development box)
    
Setup User Account
==================

Create a *kestava* group for use in assigning privileges to parts of the
filesystem (e.g. the log file directory)::

    sudo addgroup kestava

Create a system user for the web application to run as.  *pyuser* is a reasonable account name.

::

    sudo adduser --system pyuser
    sudo usermod --append -G kestava pyuser

Setup the database
==================

Install PostgreSQL

::

    sudo apt-get install postgresql

Change the postgres user's PostgreSQL password::

    sudo -u postgres psql postgres
    \password postgres

Setup Ident authentication for administrative user and pyuser.

::

    

Setup nginx
===========

::

    sudo add-apt-repository ppa:nginx/development
    sudo apt-get update
    sudo apt-get install nginx

Configure nginx

::

    cd /etc/nginx/sites-available
    sudo nano kestava.test

Place the following contents in the file::

    server {
        server_name test.kestava.org;
        
        location / {
            proxy_pass http://127.0.0.1:21850/;
        }
    }

Create a symbolic link to the file in the nginx/sites-enabled directory.

::

    cd /etc/nginx/sites-enabled
    sudo ln -s ../sites-available/kestava.test

Setup the Web Application
=========================

Create the log file directory::

    sudo mkdir /var/log/kestava
    sudo chown root:kestava /var/log/kestava/
    sudo chmod 775 /var/log/kestava/

Create the session data directory::

    sudo mkdir /var/kestava-session-data
    sudo chown root:kestava /var/kestava-session-data/
    sudo chmod 775 /var/kestava-session-data/

Create the OpenID filestore directory::

    sudo mkdir /var/kestava-openid-store
    sudo chown root:kestava /var/kestava-openid-store/
    sudo chmod 775 /var/kestava-openid-store/

Clone the git repository for the web application.

::

    mkdir -p ~/git-repos/kestava
    cd ~/git-repos/kestava
    git clone git@github.com:kestava/webapp.git

Copy settings.py.sample to create settings.py and modify as appropriate for the
new host.

1. Set socket_host to 127.0.0.1, since we'll be using nginx to proxy requests.

#. Set socket_port to 21850.

Start the Web Application

::

    cd ~/git-repos/kestava/webapp/src/www
    sudo -u pyuser /usr/local/pythonenv/KESTAVA/bin/python app.py
