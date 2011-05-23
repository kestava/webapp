..
    Hierarchy of section markers:
    
    = with overline, for title
    =, for sections
    ^, for subsections
    -, for subsubsections

============
Installation
============

Create an RSA public/private key pair
=====================================

#. If you don't already have one on your local workstation, create a RSA
   public/private key pair for use with the new server.

::

    mkdir ~/.ssh
    chmod 700 ~/.ssh
    ssh-keygen -t rsa
    
Make note of the passphrase you assigned to the private key.
    
Setup Cloud Server
==================

1. Follow the Rackspace guide to setting up an Ubuntu server (http://cloudservers.rackspacecloud.com/index.php/Ubuntu\_-_Setup).

   Install Ubuntu 10.04 LTS Lucid Lynx.

#. Copy your public key to the new server::

    ssh-copy-id <username>@<host>

Create System Account
=====================

Create a system user to run Unsilo applications::

    sudo adduser --system unsilo

Install Required Packages
=========================

::

    sudo apt-get install build-essential
    sudo apt-get install python-dev (python2.7-dev on Lucid)
    sudo apt-get install libxml2-dev libxslt-dev
    sudo apt-get install libpq-dev
    sudo apt-get install python-software-properties
    sudo apt-get install python-setuptools

.. note::

    libpq-dev contains the header files for the PostgreSQL C client library.  It
    is a dependency of psycopg2.

Other useful packages::

    sudo apt-get install bash-completion
    
Install PostgreSQL
==================

Install the latest version of PostgreSQL.

::

    sudo apt-get install postresql
    
Change the *postgres* user's PostgreSQL password.

::

    sudo -u postgres psql postgres
    \password postgres

Create a superuser account to use for administrative purposes.  Here,
*<admin username>* should be the same as an existing system user account.

::

    sudo -u postgres createuser --superuser <admin username>

.. note::

    From now on, we'll use the PostgreSQL user account created above to issue
    commands.  No password should be required as long as you're logged into the
    system as that OS user.
    
Create a database for the user.  Issuing the *createdb* command with no
arguments creates a database with the same name as the current user.

::

    createdb

Create a regular user account to access Unsilo database(s)::

    createuser unsilo
    Shall the new role be a superuser? (y/n) n
    Shall the new role be allowed to create databases? (y/n) n
    Shall the new role be allowed to create more new roles? (y/n) n

.. note::

    No database is created at this time.  First we need to obtain the
    application source, which contains the database setup scripts.
    
.. note::

    When using pgAdmin, it is possible to connect to the PostgreSQL database
    using a local UNIX socket by leaving the "host" field black, when setting
    up the connection.  This is advantageous because this type of connection
    is set to use Ident authorization by default.

.. rubric:: Resources:

1. Server Administration Chapter from the PostgreSQL 8.4 Documentation:
   http://www.postgresql.org/docs/8.4/static/admin.html
   
#. The Ubuntu Community page on PostgreSQL:
   https://help.ubuntu.com/community/PostgreSQL

Install PostGIS
===============

.. note:: Need to determine if we really need to install from the PPA

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

Copy and paste your public key to Github.

::

    cat ~/.ssh/id_rsa.pub

Copy and paste this in the Account Settings page at Github, naming the key
something indicating the remote server and username on that server
(e.g jacob on washoe).

.. note:: For additional initial setup information, view the Github Help pages.

Download the Source
===================

Clone the git repository for the web application with the following commands::

    mkdir -p ~/repos/unsilo
    cd ~/repos/unsilo
    git clone git@github.com:kestava/wurfl-service.git
    git clone git@github.com:kestava/webapp.git
    git clone git@github.com:kestava/main-db.git

Run Database Setup Script
=========================

::

    cd ~/repos/unsilo/main-db/scripts
    psql -f complete.sql

Setup Python Virtual Environment
================================

Execute...
   
    ::

        which virtualenv
        
...to see if Python virtualenv is already installed.  If not, then install
virtualenv using easy_install::

    sudo easy_install virtualenv
        
Create the virtual environment::

    sudo mkdir /usr/local/pythonenv
    cd /usr/local/pythonenv
    sudo virtualenv --no-site-packages --python=python2.7 UNSILO-WEBAPP
    
.. note::

    We're using Python 2.7 here.  Make sure both Python 2.7 and the Python 2.7
    with development headers are installed on your system.
    
    ::

        sudo apt-get install python2.7 python2.7-dev
        
.. note::
    
    As of Ubuntu 11.04, Python 2.7 is installed by default.  However, on version
    10.10, it is still necessary to install python2.7 and python2.7-dev
    separately.

These requirements should be installed in a Python virtual environment:

1. cherrypy

   ::
   
        sudo UNSILO-WEBAPP/bin/pip install cherrypy

#. psycopg2

   ::

        sudo UNSILO-WEBAPP/bin/pip install psycopg2
        
   .. note::    psycopg2's latest published version is often a beta version.  In
                that case, it's probably better to explicitly install the latest
                production version.  For example::
                
                    sudo UNSILO-WEBAPP/bin/pip install psycopg2==2.4

#. python-openid

   ::
   
        sudo UNSILO-WEBAPP/bin/pip install python-openid
        
#. setproctitle

   ::
   
        sudo UNSILO-WEBAPP/bin/pip install setproctitle
        
#. jinja2

    ::
    
        sudo UNSILO-WEBAPP/bin/pip install jinja2

#. sphinx (on development box)

#. geopy (check this!)

Setup nginx
===========

::

    sudo add-apt-repository ppa:nginx/stable
    sudo apt-get update
    sudo apt-get install nginx

Configure nginx

::

    cd /etc/nginx/sites-available
    sudo nano unsilo

There is a sample nginx configuration file in the root of the webapp project
called nginx.conf.  You can use its contents to populate the new configuration
file.

Create a symbolic link to the file in the nginx/sites-enabled directory.

::

    sudo ln -s /etc/nginx/sites-available/unsilo /etc/nginx/sites-enabled/unsilo

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

    sudo mkdir -p /var/log/unsilo/webapp
    sudo chown unsilo /var/log/unsilo/webapp/

Create the session data directory::

    sudo mkdir /var/unsilo-session-data
    sudo chown unsilo /var/unsilo-session-data/

Create the OpenID filestore directory::

    sudo mkdir /var/unsilo-openid-filestore
    sudo chown unsilo /var/unsilo-openid-filestore/

Create config file for the web application.  Copy src/www/config.ini.sample and
edit as needed.  Specify this to the --config option when running the web
application.

Start the Web Application (Development mode)
============================================

It's good to create a script to manually start the application.  See src/www/README
for information on running the application from the command line.

Create Upstart Script (Production)
==================================

The project contains a file called share/webapp.conf, which is
a sample Upstart script for managing the application process as a service.
Copy this file to /etc/init and modify it with the correct path(s) for your
system (e.g. where the application's app.py file resides).

From then on, the application should start when the server boots, and you can
manage the process with the initctl commands.
