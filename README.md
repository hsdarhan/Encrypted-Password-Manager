# Encrypted Password Manager

This is a local password manager that stores your encrypted usernames and passwords in PostgreSQL.
Fields are encrypted using the AES-256 encryption standard, and user authentication is provided with SHA-512 hashing object. 


Requirements:

PostgreSql 9.6.8  
psycopg2 2.8.5  
cryptography 2.9.2  


Setup:  
Run setup.py first to create the neccessary databases+tables

