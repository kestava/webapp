..
    Hierarchy of section markers:
    
    = with overline, for title
    =, for sections
    ^, for subsections
    -, for subsubsections

============
Installation
============

Setup Cloud Server
==================

1. Follow the Rackspace guide to setting up an Ubuntu server (http://cloudservers.rackspacecloud.com/index.php/Ubuntu\_-_Setup).

#. If you don't already have one on your local workstation, create a RSA
   public/private key pair for use with the new server.

::

    mkdir ~/.ssh
    chmod 700 ~/.ssh
    ssh-keygen -t rsa

#. Copy public key to the new server::

    ssh-copy-id <username>@<host>

Setup User Accounts and Groups
==============================

Create a *kestava-users* group for use in assigning privileges to parts of the
filesystem (e.g. the log file directory)::

    sudo addgroup kestava-users

Create a system user to run Kestava applications.

::

    sudo adduser --system kestava
    sudo usermod --append --groups kestava-users kestava

Install Required Packages
=========================

::

    sudo apt-get install build-essential
    sudo apt-get install python-dev
    sudo apt-get install libxml2-dev libxslt-dev
    sudo apt-get install libpq-dev
    sudo apt-get install python-software-properties
    sudo apt-get install python-setuptools

Other useful packages::

    sudo apt-get install bash-completion
    
Install PostgreSQL
==================

Install the latest version of PostgreSQL::

    sudo apt-get install postresql

Create a superuser account to use for administrative purposes::

    sudo -u postgres createuser --superuser <admin username>
    sudo -u postgres psql

Assign the administrative account a password::

    postgres=# \password <admin username>

Create a regular user account to access Kestava database(s)::

    createuser kestava
    Shall the new role be a superuser? (y/n) n
    Shall the new role be allowed to create databases? (y/n) n
    Shall the new role be allowed to create more new roles? (y/n) n

.. note::

    No database is created at this time.  First we need to obtain the Kestava
    source, which contains the database setup scripts.

.. rubric:: Resources:

1. Server Administration Chapter from the PostgreSQL 8.4 Documentation:
   http://www.postgresql.org/docs/8.4/static/admin.html
   
#. The Ubuntu Community page on PostgreSQL:
   https://help.ubuntu.com/community/PostgreSQL

Install PostGIS
===============

Add UbuntuGIS "stable" PPA to the system's software sources list.  This let's us
install a newer version of PostGIS than the one normally found in Ubuntu's
software repositories.

::

    sudo add-apt-repository ppa:ubuntugis/ppa
    cd /etc/apt/sources.list.d

There should be a file in this directory named something like
ubuntugis-ppa-maverick.list, which we need to edit.  At the time of this
writing, there was no repository for Maverick, so we need to set it to look at
Lucid's.

::

    sudo nano ubuntugis-ppa-maverick.list

Change the two references to "maverick" to say "lucid" instead.

Synchronize local pack index files::

    sudo apt-get update

Install PostGIS::

    sudo apt-get install postgresql-8.4-postgis
    
.. rubric:: Resources:

1. PostGIS Documentation Chapter on Installation:
   http://postgis.refractions.net/documentation/manual-1.5/ch02.html

Install git
===========

::

    sudo add-apt-repository ppa:git-core/ppa
    sudo apt-get update
    sudo apt-get install git-core

Create a RSA public/private key pair
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There may already be a ~/.ssh directory present.  If not then create it with the
following commands::

    mkdir ~/.ssh
    chmod 700 ~/.ssh

Create the key pair.

::

    ssh-keygen -t rsa

Make note of the passphrase you assigned to the private key.

Copy and paste the public key to Github::

    cat ~/.ssh/id_rsa.pub

Copy and paste this in the Account Settings page at Github, naming the key
something indicating the remote server and username on that server
(e.g jacob on washoe).

Download the Web Application Source
===================================

Clone the git repository for the web application with the following commands::

    mkdir -p ~/documents/git-repos/kestava
    cd ~/documents/git-repos/kestava
    git clone git@github.com:kestava/webapp.git

Run Database Setup Script
=========================

::

    /usr/bin/python ~/documents/git-repos/kestava/webapp/src/database/scripts/complete.py \
    -n kestava \
    -m ~/documents/git-repos/kestava/webapp/src/database/scripts/complete.manifest \
    -s ~/documents/git-repos/kestava/webapp/src/database/scripts
    

Setup Python Virtual Environment
================================

Install virtualenv using easy_install::

    sudo easy_install virtualenv

Create the virtual environment::

    sudo mkdir /usr/local/pythonenv
    cd /usr/local/pythonenv
    sudo virtualenv --no-site-packages KESTAVA-WEBAPP

These requirements should be installed in a Python virtual environment:

1. cherrypy

   ::
   
        sudo KESTAVA-WEBAPP/bin/pip install cherrypy

#. lxml

   Install the latest stable version.  At the time of this writing, version
   2.2.8 is the most current.

   ::

        sudo KESTAVA-WEBAPP/bin/pip install lxml==2.2.8

#. psycopg2

   ::

        sudo KESTAVA-WEBAPP/bin/pip install psycopg2==2.3.2

#. python-openid

   ::
   
        sudo KESTAVA-WEBAPP/bin/pip install python-openid

#. geopy (check this!)

#. mox (only on development box)

Setup nginx
===========

::

    sudo add-apt-repository ppa:nginx/stable
    sudo apt-get update
    sudo apt-get install nginx

Configure nginx

::

    cd /etc/nginx/sites-available
    sudo nano kestava

Enter these contents into the file.  The example below is for test.kestava.org.
You should supply the hostname that is appropriate for the current environment.

::

    server {
        server_name test.kestava.org;
        
        location / {
            proxy_pass http://127.0.0.1:21850/;
        }
    }

Create a symbolic link to the file in the nginx/sites-enabled directory.

::

    cd /etc/nginx/sites-enabled
    sudo ln -s ../sites-available/kestava

Start (or restart) nginx.

::

    sudo /etc/init.d/nginx start

or

::

    sudo /etc/init.d/nginx restart

If you try to access the website in your browser now, you should see a
**502 Bad Gateway** message from nginx.
    
Setup the Web Application
=========================

Create the log file directory::

    sudo mkdir /var/log/kestava
    sudo chown root:kestava-users /var/log/kestava/
    sudo chmod 775 /var/log/kestava/

Create the session data directory::

    sudo mkdir /var/kestava-session-data
    sudo chown root:kestava-users /var/kestava-session-data/
    sudo chmod 775 /var/kestava-session-data/

Create the OpenID filestore directory::

    sudo mkdir /var/kestava-openid-filestore
    sudo chown root:kestava-users /var/kestava-openid-filestore/
    sudo chmod 775 /var/kestava-openid-filestore/

Create settings.py for the web application::

    cd ~/documents/git-repos/kestava/webapp/src/www/
    cp settings.py.sample settings.py
    nano settings.py

.. rubric:: Settings:
    
* Set socket_host to 127.0.0.1, since we'll be using nginx to proxy requests.

* Set socket_port to 21850.

* Set access_log_when and error_log_when to 'midnight'.

* Set appSettings/siteName as appropriate.

* Set appSettings/siteHostname as appropriate.

Start the Web Application
=========================

::

    cd ~/git-repos/kestava/webapp/src/www
    sudo -u kestava /usr/local/pythonenv/KESTAVA-WEBAPP/bin/python app.py

Create Upstart Script
=====================

The Kestava webapp project contains a file called kestava-webapp.conf, which is
a sample Upstart script for managing the application process as a service.
Copy this file to /etc/init and modify it with the correct path(s) for your
system (e.g. where the application's app.py file resides).

From then on, the application should start when the server boots, and you can
manage the process with the initctl commands.