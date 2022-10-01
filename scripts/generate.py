"""script qui genere les clé pour chaque smart meter et data concentrateur 
"""

from tkinter import N
from brownie import accounts, Connexions
import random as rn 
import rsa 
import pandas as pd
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from hashlib import sha512
import base64


global grid_connexion 
grid_connexion = Connexions[-1]

def export_private_key(private_key, filename):
    with open(filename, "wb") as file:
        file.write(private_key.exportKey('PEM', 'MyPassphrase'))
        file.close()

def export_public_key(public_key1, filename):
    with open(filename, "wb") as file:
        file.write(public_key1.exportKey('PEM'))
        file.close()

def import_private_key(filename):
    with open(filename, "rb") as file:
        private_key = RSA.importKey(file.read(), 'MyPassphrase')
    return private_key


def import_public_key(filename):
    with open(filename, "rb") as file:
        public_key1 = RSA.importKey(file.read())
    return public_key1

def dataFrame_to_Dict(data):
    #data_dictionary = {}
    data_list = []
    for i,j in data.iteritems():
        dict_j = []
        for z in j:
            dict_j.append(str(z))
        #data_dictionary[str(i)] = dict_j
        data_list.append(dict_j)
    #return data_dictionary
    return data_list

#-----------génération des clés publiques et privés pour crypter les donnés------------ 
def nan1_keys():
    print("")
    print("----------------------------génération des clés pour NAN1-------------------------------")
    print("")
    for i in range(1,11):
        keypair = RSA.generate(2048)
        public_key = keypair.publickey()
        export_private_key(keypair, '../NAN1/SM' + str(i) + '/private_key.pem')
        export_public_key(public_key, '../NAN1/SM' + str(i) + '/public_key.pem')
        grid_connexion.addKeyMeter(accounts[i], public_key, {"from": accounts[0]})

def nan2_keys():
    print("")
    print("----------------------------génération des clés pour NAN2-------------------------------")
    print("")
    for i in range (11,21):
        keypair = RSA.generate(2048)
        public_key = keypair.publickey()
        export_private_key(keypair, '../NAN2/SM' + str(i) + '/private_key.pem')
        export_public_key(public_key, '../NAN2/SM' + str(i) + '/public_key.pem')
        grid_connexion.addKeyMeter(accounts[i], public_key, {"from": accounts[0]})

def wan_keys():
    print("")
    print("----------------------------génération des clés pour WAN-------------------------------")
    print("")
    for i in range(21,31):
        keypair = RSA.generate(2048)
        public_key = keypair.publickey()
        export_private_key(keypair, '../WAN/DC' + str(i-20) + '/private_key.pem')
        export_public_key(public_key, '../WAN/DC' + str(i-20) + '/public_key.pem')
        grid_connexion.addKeyDc(accounts[i], public_key, {"from": accounts[0]})

def encryption(arg_publickey, arg_cleartext):
    encryptor = PKCS1_OAEP.new(arg_publickey)
    ciphertext = encryptor.encrypt(arg_cleartext)
    return base64.b64encode(ciphertext)

def decryption(arg_privatekey, arg_b64text):
    decoded_data = base64.b64decode(arg_b64text)
    decryptor = PKCS1_OAEP.new(arg_privatekey)
    decrypted = decryptor.decrypt(decoded_data)
    return decrypted

def main():
    nan1_keys()
    nan2_keys()
    wan_keys()
    
    

