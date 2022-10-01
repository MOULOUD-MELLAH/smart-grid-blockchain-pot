"""from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def import_private_key(filename):
    with open(filename, "rb") as file:
        private_key = RSA.importKey(file.read(), 'MyPassphrase')
    return private_key

data = '2f10fe81fbf69b4f0f20e3ad11cf779508f907df1d9750e574a4109a8e7dab624adc3dcf800e007a21daf0f260089fa115bfe29a750de02cc1215054eea2081689c157d0ff4a9b4e925bf79ad64ed79565a78cd4369e83b7751a7a857da4e42c8893d7097df68f4b87def03dab166b1f801b0958a620b305124c946b0858cd46e05c1d8df227f17fd04cd0e76229abf6c4e02b4ead34277504dcfb1120dcb2656270e9c1476cd5679f46f02a93f72efcc71ba743730a4f6a24aafe58401c57b5348a7650fe782f6f96dc78bcf4c1ed9b3c6b87f4d160b037d3e25565c3ebc9573e120db37988c568c347f96d20bdc327f9ca30fd59dbeb63dbe70c582a2fba37'
data = data

private_key = import_private_key('/home/mouloud/WAN/DC1/private_key.pem')
decryptor = PKCS1_OAEP.new(private_key)
decrypted = decryptor.decrypt(data)
print(decrypted.decode())"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def import_private_key(filename):
    with open(filename, "rb") as file:
        private_key = RSA.importKey(file.read(), 'MyPassphrase')
    return private_key


def import_public_key(filename):
    with open(filename, "rb") as file:
        public_key1 = RSA.importKey(file.read())
    return public_key1

def encryption(arg_publickey, arg_cleartext):
    encryptor = PKCS1_OAEP.new(arg_publickey)
    ciphertext = encryptor.encrypt(arg_cleartext)
    return base64.b64encode(ciphertext)

def decryption(arg_privatekey, arg_b64text):
    decoded_data = base64.b64decode(arg_b64text)
    decryptor = PKCS1_OAEP.new(arg_privatekey)
    decrypted = decryptor.decrypt(decoded_data)
    return decrypted

PUBKEY = import_private_key('WAN/DC' + str(1) + '/public_key.pem')
PRIVKEY = import_private_key('WAN/DC' + str(1) + '/private_key.pem')

a = str(0.5).encode('ascii')
b = 0.5

cleartext1 = a

ciphertext = encryption(PUBKEY, cleartext1)
cleartext2 = decryption(PRIVKEY, ciphertext)


print(cleartext1)
print(ciphertext)
print(type(ciphertext))
print(cleartext2)
