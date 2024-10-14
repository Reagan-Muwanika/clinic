This is the final (third) year project for Reagan Muwanika. A student at 
Kyambogo University doing a Bachelors Degree in Infomation Technology
and Computing (BITC). The project is about a computerized clinic/ hospital data 
management system with the case study of JB Medical Services located along
Kira-Bulindo road
****************************Packages Used********************************
1. Flask; This is a python framework
2. mysql-connector-python; This is a mysql connector for connecting to the database
3. WTForms; This is used to design forms that capture data in the frontend
4. Jinja; This is used to design html
*************************************************************************

**********************Setting up virtual environment*********************
Change to the working directory using the cd command
Create the python virtual environment
command:	python -m venv virtualenv
Activate the virtual environment
command:	virtualenv/Scripts/Activate
Install flask using pip package installer
command:	pip install flask
Install mysql-connector-python using pip package installer
command:	pip install mysql-connector-python
Install WTForms using pip package installer
command:	pip install wtforms
*************************************************************************

**************************Running the Application************************
Still in the activated virtual environment, enter the command below to run
the application.
command:	flask --app jbm --debug run
After running the application, use the browser and enter the url below to
access the computerized clinic management system.
URL:	127.0.0.1:5000/staff/login
Use the credentials below to access the admin panel
Username:	admin
Password:	mure647reagan
************************************************************************* 

********************************Creating the Database********************
The database of this application was developed using Server Query Language 
(SQL).
The server used in the development of the application is MySQL Server 8.0.39.
The app comprises of a file/ sql module called schema.sql which contains 
the sql statements for creating the various database tables and relationships.
There also other sql statements with in the python modules consisted in the 
application which were used in their respective needs.
Endeavour to create a database with the name 'clinic' on the MySQL server 
using the create database command ie 'CREATE DATABASE IF NOT EXISTS clinic;'.
After creating the above mentioned database, initialize the database tables 
and relationships between them using the command below in the activated 
virtual environment
command:	flask --app jbm initialize-database
Note: The above command is only executed once when that application/ system is 
run on the server for the first time
**************************************************************************