# Encrypted Password Manager

This is a local password manager that stores encrypted usernames and passwords in PostgreSQL.
Fields are encrypted using the AES-256 encryption standard, and user authentication is provided with SHA-512


## Requirements

**Python3** and **PostgreSQL 9.6.8** are required on the system

Python Modules:

psycopg2 2.8.5  
cryptography 2.9.2  

## Config
Two config.ini files are used for connecting to PostgreSQL. Please edit the "username" and "password" sections corresponding to your PostgreSQL server.


## Setup:  
To create the necessary databases and tables:\
``python3 setup.py``  

To run an instance of the application:\
``python3 app.py``

