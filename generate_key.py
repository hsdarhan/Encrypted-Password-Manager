from cryptography.fernet import Fernet

def generate_key():
    """
    Generates a key used for encryption and decryption (AES-256)
    :return:
    """
    key=Fernet.generate_key()
    print(key)
    fkey=open("key.txt", 'wb')
    fkey.write(key)
    fkey.close()
