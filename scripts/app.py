from brownie import accounts, config, Connexions
#import pandas as pd
from tqdm import tqdm

from scripts.deploy import *

global grid_connexion 
grid_connexion = Connexions[-1]

def establish_connection(from_,to_):
    
    #adding connections to GRID_connections set.
    try:
        GRID_connections.add(from_ +'-'+ to_)
        #Interacting with blockchain to transact (enableConnections).
        grid_connexion.enableConnections(from_,to_)
        return "Connection Establihed"
    except :
        return "Connection Already Exists"
        #later try except Exception as error to read from response

def destablish_connection(from_,to_):
    #removing connections from GRID_connections set.

    try:
        GRID_connections.remove(from_ +'-'+ to_)
        #Interacting with blockchain to transact.
        grid_connexion.disableConnections(from_,to_)
        return "Connection Destablished"
    except :
        return "No connection exists to disconnect"

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

def data_transaction(sender,receiver,iteration,amount):
        print(sender,receiver,iteration,amount)
        try:
            contract_passingArbitraryArguments.functions.passingValues(sender,receiver,iteration,amount).transact({'from':sender})
            return "OKo!"
        except:
            return "No connection"


accounts_list = accounts
for i in accounts_list:
    print(i)

#les comptes de 1 à 6 vont représenter les smarts meters des deux regions NAN 1 et NAN 2
#les comptes de 7 à 9 vont représenter les DC de réseau WAN 
GRID_accounts = {}
GRID_connections = set()

for i in range(1,7):
    GRID_accounts[grid_connexion.retrieveMeter(accounts_list[i])] = accounts_list[i]

for i in range(7,10):
    GRID_accounts[grid_connexion.retrieveDC(accounts_list[i])] = accounts_list[i]
    
#print(GRID_accounts)

#affichage 
for k, v in GRID_accounts.items():
    print(k,':',v)
    
#Adding connections
print("-----------Etablisment de connexions niveau NAN 1-----------")
print(establish_connection(GRID_accounts['SM1'],GRID_accounts['SM2']))
print(establish_connection(GRID_accounts['SM1'],GRID_accounts['SM3']))
print(establish_connection(GRID_accounts['SM1'],GRID_accounts['DC1']))
print(establish_connection(GRID_accounts['SM2'],GRID_accounts['SM1']))
print(establish_connection(GRID_accounts['SM2'],GRID_accounts['SM3']))
print(establish_connection(GRID_accounts['SM2'],GRID_accounts['DC1']))
print(establish_connection(GRID_accounts['SM3'],GRID_accounts['SM1']))
print(establish_connection(GRID_accounts['SM3'],GRID_accounts['SM2']))
print(establish_connection(GRID_accounts['SM3'],GRID_accounts['DC1']))

print("-----------Etablisment de connexions niveau NAN 2-----------")
print(establish_connection(GRID_accounts['SM4'],GRID_accounts['SM5']))
print(establish_connection(GRID_accounts['SM4'],GRID_accounts['SM6']))
print(establish_connection(GRID_accounts['SM4'],GRID_accounts['DC2']))
print(establish_connection(GRID_accounts['SM5'],GRID_accounts['SM4']))
print(establish_connection(GRID_accounts['SM5'],GRID_accounts['SM6']))
print(establish_connection(GRID_accounts['SM5'],GRID_accounts['DC2']))
print(establish_connection(GRID_accounts['SM6'],GRID_accounts['SM4']))
print(establish_connection(GRID_accounts['SM6'],GRID_accounts['SM5']))
print(establish_connection(GRID_accounts['SM6'],GRID_accounts['DC2']))

print("-----------Etablisment de connexions niveau WAN-----------")
print(establish_connection(GRID_accounts['DC1'],GRID_accounts['DC2']))
print(establish_connection(GRID_accounts['DC1'],GRID_accounts['DC3']))
print(establish_connection(GRID_accounts['DC2'],GRID_accounts['DC1']))
print(establish_connection(GRID_accounts['DC2'],GRID_accounts['DC3']))
print(establish_connection(GRID_accounts['DC3'],GRID_accounts['DC1']))
print(establish_connection(GRID_accounts['DC3'],GRID_accounts['DC2']))


def main():
    pass