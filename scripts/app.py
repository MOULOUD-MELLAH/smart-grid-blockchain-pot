from brownie import accounts, config, Connexions, Communications
import pandas as pd
from tqdm import tqdm

from scripts.deploy import *

global grid_connexion 
global grid_connexion2
grid_connexion = Connexions[-1]
grid_connexion2 = Communications[-1]

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
            data_list.append(str(z))
        #data_dictionary[str(i)] = dict_j
        
    #return data_dictionary
    return data_list

def data_transaction(sender,receiver,iteration,amount):
        print(sender,receiver,iteration,amount)
        #try:
        grid_connexion2.passingValues(sender,receiver,iteration,amount, {'from':sender, "gas":3000000, "allow_revert": True})
        #return "OKo!"
        #except:
        #return "No connection"

def Nan1B1(ID1, ID2, ID3, dateUse, Power1, Power2, Power3, Rep1, Rep2, Rep3, merkleRoot):
    account = accounts[0]
    transaction = grid_connexion.tansactionNan1B1(ID1, ID2, ID3, dateUse, Power1, Power2, Power3, Rep1, Rep2, Rep3, merkleRoot, {"from": account}) 
    transaction.wait(1)
    



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

SM1_SM2 = pd.read_csv('../NAN1/SM1_SM2.csv', header=None)
SM1_SM3 = pd.read_csv('../NAN1/SM1_SM3.csv', header=None)
SM2_SM1 = pd.read_csv('../NAN1/SM2_SM1.csv', header=None)
SM2_SM3 = pd.read_csv('../NAN1/SM2_SM3.csv', header=None)
SM3_SM1 = pd.read_csv('../NAN1/SM3_SM1.csv', header=None)
SM3_SM2 = pd.read_csv('../NAN1/SM3_SM2.csv', header=None)

data_SM1_SM2 = dataFrame_to_Dict(SM1_SM2)
data_SM1_SM3 = dataFrame_to_Dict(SM1_SM3)
data_SM2_SM1 = dataFrame_to_Dict(SM2_SM1)
data_SM2_SM3 = dataFrame_to_Dict(SM2_SM3)
data_SM3_SM1 = dataFrame_to_Dict(SM3_SM1)
data_SM3_SM2 = dataFrame_to_Dict(SM3_SM2)

GRID_Connections = {'SM1_SM2' : data_SM1_SM2,
                    'SM1_SM3' : data_SM1_SM3,
                    'SM2_SM1' : data_SM2_SM1,
                    'SM2_SM3' : data_SM2_SM3,
                    'SM3_SM1' : data_SM3_SM1,
                    'SM3_SM1' : data_SM3_SM2
                   }

counter = 0
processing = True
while processing:
    for key in GRID_Connections.keys():
        try:
            sender, receiver = key.split("_")
            payload = GRID_Connections[key][counter]

            print(data_transaction(GRID_accounts[sender],GRID_accounts[receiver],counter,payload))

        except IndexError:
            processing = False
            break
    counter += 1


print(SM1_SM2)

data_A1_A2 = dataFrame_to_Dict(SM1_SM2)
print(data_A1_A2[1][0:5])
print(data_A1_A2[1][6:11])


#Nan1B1(1000, 1002, 1003, "00:00:00", 200, 200, 200, 80, 80, 80, "dddsd")

def main():
    pass