# import required module
from cryptography.fernet import Fernet
import maskpass
import hashlib
import os

Path = input("Path to save files to >> ")

# Generate a key
key = Fernet.generate_key()
 
# Store the key in a file
with open(os.path.join(Path, 'key.key'), 'wb') as filekey:
   filekey.write(key)
   filekey.close()

# Open the key file
with open(os.path.join(Path, 'key.key'), 'rb') as filekey:
    key = filekey.read()
    filekey.close()
 
# using the generated key
fernet = Fernet(key)

Passwd = str(hashlib.md5(maskpass.advpass(prompt = "Password to encrypt >> ", mask = "*").encode()).hexdigest())

# Open the file in write mode and write the unencrypted data to it
with open(os.path.join(Path, 'pass.txt'), 'w') as unencrypted_file:
    unencrypted_file.write(Passwd)
    unencrypted_file.close()
 
# Open the password file to encrypt
with open(os.path.join(Path, 'pass.txt'), 'rb') as file:
    original = file.read()
    file.close()
     
# Encrypt the password file
encrypted = fernet.encrypt(original)
 
# Open the file in write mode and write the encrypted data to it
with open(os.path.join(Path, 'pass.txt'), 'wb') as encrypted_file:
    encrypted_file.write(encrypted)
    encrypted_file.close()

print("MD5: " + Passwd)
print("Encrypted MD5: " + str(encrypted))
