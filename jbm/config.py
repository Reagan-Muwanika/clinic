'''
    This module establishes a database connection and allows 
    the creation of the tables and all the relationships
    between them by executing the sql code in schema.sql
    file
'''

import mysql.connector
from flask import current_app, g
from mysql.connector import errorcode, Error
from pathlib import Path
import click



def connect_to_database():
    '''
        establishing a database connection to world database. 
        It is an example database that is configured with mysql
    ''' 
    if 'db' not in g:
        config = {
            'user': 'root',
            'password': '',
            'host': '127.0.0.1',
            'port': 3306,
            'database': 'clinic',
            'charset': 'utf8mb4'
        }

        try:
            g.db = mysql.connector.connect(**config)
            print(f'Database connection establised')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return 'Access denied! Wrong Username or Password'
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return 'Access denied! Database does not exist'
            else:
                return f'{err}'

    return g.db



def disconnect_from_database(e = None):
    '''
        closing the database connection that was establised by
        connect_db() function
    '''
    db = g.pop('db', None)

    if db is not None:
        db.close()


        
def initialize_database():
    '''
        creating the tables that will hold the data in the database
        to create the tables, run the command below
        'flask --app jbm initialize-database'
    '''
    path = Path('jbm/schema.sql')
    with  open(path, 'r', encoding = 'utf8') as f:
        data = f.read()
        cursor = connect_to_database().cursor()
        cursor = cursor.execute(data)
        
        
        

@click.command('initialize-database')
def initialize_database_command():
    '''
        Creating cmd command that executes the sql in schema.sql file to initialize the database
    '''
    initialize_database()
    click.echo('\nDatabase initialized...!\n')
    
    
    
    
def initialize_app(app):
    '''
        Calling the disconnect_database fuction to close the database and Registering the 
        initialize_database_command
    '''
    app.teardown_appcontext(disconnect_from_database)
    app.cli.add_command(initialize_database_command)