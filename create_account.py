import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

salt=b'yp\x98\xa5\x1a\xcb\xe8\xd2%\xfcM\x14\xd1<!\x99'
from cryptography.fernet import Fernet

def create_account():
    match=False
    while(match==False):
        provided_password=input("Enter a password for this account: ")
        provided_password_verify=input("Re-enter the password: ")
        if(provided_password==provided_password_verify):
            match=True
        else:
            print("Passwords do not match, please try again!")

    password = provided_password.encode()

    kdf = PBKDF2HMAC(algorithm=hashes.SHA512(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())

    hashed_password = base64.urlsafe_b64encode(kdf.derive(password))
    file=open("account.txt", 'wb')
    file.write(hashed_password)
    file.close()




if __name__ == '__main__':
    create_account()
