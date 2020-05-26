import base64
import psycopg2
from os import path

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from config import config_live
from generate_key import generate_key
from create_account import create_account


def verify():
    """
    User authentication; hashes the provided password and compares it to the stored hash.
    Hashing is done using a salt for further security.
    :return: Return True if hashes match, otherwise return false
    """

    salt=b'yp\x98\xa5\x1a\xcb\xe8\xd2%\xfcM\x14\xd1<!\x99'
    try:
        file=open("account.txt", 'rb')
    except FileNotFoundError as e:
        print(e)
    else:
        hashed=file.read()
        file.close()

    password_provided=input("Please enter your password: ")
    password=password_provided.encode()

    kdf = PBKDF2HMAC(algorithm=hashes.SHA512(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())

    hashed_password = base64.urlsafe_b64encode(kdf.derive(password))

    if hashed==hashed_password:
        return True
    return False


def getKey():
    """
    Retrieves key from "key.txt"
    :return: key string from the file
    """
    try:
        file=open("key.txt", 'rb')
    except FileNotFoundError as e:
        print(e)
    else:
        key=file.read()
        file.close()
        return key


def getInfo(key):
    """
    Takes in user input, encodes and encrypts the strings, stores into a dictionary
    :param key: key used from encrypting
    :return: returns dictionary of service, encrypted username and encrypted password
    """
    cipher=Fernet(key)

    source=input("Enter website/source: ")
    user=input("Enter username: ")
    password=input("Enter password: ")

    encoded_user=user.encode()
    encrypted_user=cipher.encrypt(encoded_user)
    storage_user=encrypted_user.decode()

    encoded_password=password.encode()
    encrypted_password=cipher.encrypt(encoded_password)
    storage_password=encrypted_password.decode()

    block={"Service":source,"User":storage_user, "Password":storage_password}
    print("Encrypting...")
    print(source, storage_user, storage_password)
    print("Successfully stored!")

    return block

def store(info):
    """
    Stores information into postgreSQL
    :param info: dictionary of encrypted information
    """

    sql="""INSERT INTO storage(service, username, password) VALUES(%s,%s,%s)"""
    conn=None

    try:
        params=config_live()
        conn=psycopg2.connect(**params)
        cur=conn.cursor()

        cur.execute(sql,(info["Service"], info["User"],info["Password"],))
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print (error)
    finally:
        if conn is not None:
            conn.close()

def retrieve(service):
    """
    Retrieves the desired service
    :param service: string of name of service needing to be retrieved
    :return: returns the row from postgreSQL in the form of a tuple
    """

    sql="""SELECT service, username, password FROM storage where service=%s"""
    conn=None

    try:
        params=config_live()
        conn=psycopg2.connect(**params)
        cur=conn.cursor()

        cur.execute(sql, (service,))
        row=cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print (error)
    finally:
        if conn is not None:
            conn.close()
    return row

def display(row):
    """
    Decryptes the information and displays it to the user
    :param row: tuple of retrieved row from postgreSQL
    """
    key=getKey()
    cipher=Fernet(key)

    encoded_username=row[1].encode()
    encoded_password=row[2].encode()
    username=cipher.decrypt(encoded_username).decode()
    password=cipher.decrypt(encoded_password).decode()
    print("Amazon username: [{}]".format(username))
    print("Amazon password: [{}]".format(password))


def list_services():
    """
    Displays stored services in postgreSQL, and asks user for the desired account
    :return: Returns a string of the choice of the user
    """
    sql = """SELECT service FROM storage"""
    conn = None

    try:
        params = config_live()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(sql)
        rows = cur.fetchall()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    list_of_services=[]
    for x in rows:
        print(x[0])
        list_of_services.append(x[0])

    choice=input("Which account would you like to unlock?")

    return choice

def menu():
    """
    Main menu; displays options for the user
    :return: returns an integer representing the users selection
    """
    print('Welcome')
    print('1. Store')
    print('2. Retrieve')
    print('3. Exit')
    selection=int(input("Enter choice: "))
    return selection

def main():
    """
    main program:
    - checks if account and key is present; otherwise allows user to generate them
    - verifys user
    - displays the menu
    - calls appropirate function to either store or retrieve information
    """
    account=False
    while account==False:
        if path.exists("key.txt") and path.exists("account.txt"):
            account=True
        else:
            generate_key()
            create_account()

    a=verify()
    while a is False:
        a=verify()

    x=menu()
    while x is not 3:
        if x==1:
            key=getKey()
            info=getInfo(key)
            store(info)
        if x==2:
            choice=list_services()
            result=retrieve(choice)
            display(result)
        x=menu()

if __name__ == '__main__':
    main()
