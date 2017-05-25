Taxifares

Taxifares is taxi call-taker order application developed in Flask (Python framework) and JQuery. It uses flask as the web framework and MySQL for its database.
 
Instructions for Deployment on an Ubuntu VPS

•	Set up apache server to host the flask app.
•	Set up an instance of MySQL on your server. Enter the password taxi for mysql database root user. Do not confuse it with the server root user password.

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install apache2 mysql-client mysql-server
sudo apt-get install libapache2-mod-wsgi
sudo a2enmod wsgi
 
•	Set up the Flask environment.

cd /var/www/

•	Make the Flask environment directory:

mkdir taxifares
cd taxifares

•	Make the actual application directory:

mkdir taxifares
cd taxifares/

Note: By now, your app directory should look like this: /var/www/taxifares/taxifares

•	Download the repository from GitHub:

git clone https://github.com/agd1967/taxifares_app.git;

•	Install the required python modules:

sudo apt-get install python-mysql.connector

•	Install and Setup the Virtual Environment for Flask to run Python and the application:

sudo apt-get install python-pip
sudo pip install virtualenv
sudo virtualenv venv
source venv/bin/activate

•	Install Flask within the Virtual Environment

sudo pip install Flask

•	Set up the Flask configuration file:

 sudo nano /etc/apache2/sites-available/taxifares.conf

•	Include this code in the configuration file:
               
<VirtualHost *:80>
                ServerName IP address
				ServerAdmin myemail@gmail.com
				WSGIScriptAlias / /var/www/taxifares/taxifares.wsgi
				<Directory /var/www/taxifares/taxifares/>
				        Order allow,deny
						Allow from all
				</Directory>
				Alias /static /var/www/taxifares/taxifares/static
				<Directory /var/www/taxifares/taxifares/static/>
				        Order allow,deny
						Allow from all
				</Directory>
				ErrorLog ${APACHE_LOG_DIR}/error.log
				LogLevel warn
				CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>


•	Enable the server: 

sudo a2ensite taxifares
service apache2 reload

•	Configure the WSGI file:

cd /var/www/taxifares
nano taxifares.wsgi

•	Enter in the taxifares.wsgi file, followed by Save and Exit:

#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/taxifares/")

from taxifares import app as application
application.secret_key = 'taxifares-key-2017'

•	Restart apache

service apache2 restart

•	Install the required python modules and restart apache:

sudo apt-get install python-mysql.connector
service apache2 restart

•	Import the taxifares MySql database:

mysql -u root -ptaxi taxi < /var/www/taxifares/taxifares/data/taxi_client.sql
mysql -u root -ptaxi taxi < /var/www/taxifares/taxifares/data/taxi_fares.sql
mysql -u root -ptaxi taxi < /var/www/taxifares/taxifares/data/taxi_routines.sql



For more detailed information on how to deploy a flask application on an ubuntu vps, visit:
https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
 

