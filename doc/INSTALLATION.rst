============
Installation
============

Requirements
============

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
    sudo KESTAVA/bin/pip install psycopg2==2.2.2

These requirements should be installed in a Python virtual environment::

    1. cherrypy
    
    #. lxml (version 2.2.8)
    
    #. psycopg2 (version 2.2.2)
    
    #. geopy (check this!)
    
    #. mox
    
User Account
============

Create a system user for the web application to run as.  *pyuser* is a reasonable account name.

::

    sudo useradd -r pyuser