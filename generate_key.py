from cryptography.fernet import Fernet

def generate_key():
    key=Fernet.generate_key()
    print(key)
    fkey=open("key.txt", 'wb')
    fkey.write(key)
    fkey.close()
