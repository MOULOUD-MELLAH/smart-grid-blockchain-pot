from ast import Param
from cgi import print_arguments
from datetime import date
from tempfile import tempdir
from tkinter.tix import Meter
import base64
from numpy import power

from rsa import verify
from brownie import accounts, config, Connexions
import pandas as pd
from tqdm import tqdm
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from scripts.deploy import *
from scripts.generate import *
from scripts.merkleTree import *
from scripts.Energy_Theft_Detection import *

global grid_connexion 
grid_connexion = Connexions[-1]

global counter 
counter = 0

def establish_connection(from_,to_):
    global counter
    counter = counter + 1
    #ajouter une connexion
    try:
        GRID_connections.add(from_ +'-'+ to_)
        #intéraction avec la blockcahin.
        grid_connexion.enableConnections(from_,to_)
        return " Connection Establihed"
    except :
        return " Connection Already Exists"
        

def destablish_connection(from_,to_):
    #supprimer la connexion.
    try:
        GRID_connections.remove(from_ +'-'+ to_)
        grid_connexion.disableConnections(from_,to_)
        return " Connection Destablished"
    except :
        return " No connection exists to disconnect"

#fonction pour récupérer les données sous forme d une liste des listes 
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

#fonction pour enlever les entetes des fichier dans les listes
def dataListe(List):
    data_list = []
    t1 = len(List)
    j=0
    while j < t1:
        dict_j = []
        t2 = len(List[j]) - 1
        z = 1
        while z <= t2:
            dict_j.append(List[j][z])
            z = z+2 
        data_list.append(dict_j)
        j = j+1
    return data_list

#fonction qui permet de  trier les listes selon un ordre décroissant des réputations  
def list_trie(data): 
    i = 1
    l = len(data[2])
    while i < l:
        j = i - 1
        while j >= 0 and int(data[5][j]) < int(data[5][j+1]):
            v = data[2][j]
            v2=data[3][j]
            v3=data[4][j]
            v4 =data[5][j]
            data[2][j] = data[2][j+1]
            data[2][j+1] = v
            data[3][j] = data[3][j+1]
            data[3][j+1] = v2
            data[4][j] = data[4][j+1]
            data[4][j+1] = v3
            data[5][j] = data[5][j+1]
            data[5][j+1] = v4
            j= j-1
        i= i+1
    return data


#fontion qui va retourner le merkle root 
def merkle_root(liste):
    tampered_Tree = MerkleTree()
    tampered_Tree_transaction = liste
    tampered_Tree.listoftransaction = tampered_Tree_transaction
    tampered_Tree.create_tree()
    tampered_Tree_root = tampered_Tree.Get_Root_leaf()
    return tampered_Tree_root


def getLeader(list_account):
    Leader = grid_connexion.get_leader(list_account)
    return Leader 



accounts_list = accounts
GRID_accounts = {}
GRID_connections = set()

for i in range(1,21):
    GRID_accounts[grid_connexion.retrieveMeter(accounts_list[i])] = accounts_list[i]

for i in range(21,31):
    GRID_accounts[grid_connexion.retrieveDC(accounts_list[i])] = accounts_list[i]
    
#print(GRID_accounts)

#affichage 
list_account = []
for k, v in GRID_accounts.items():
    print(k,':',v)
    list_account.append(v)
    
#Adding connections
print("--------------------------------Etablisment de connexions niveau NAN 1----------------------")
for i in range(1,11):
    for j in range (1,11):
        if (i != j):
            print("SM" + str(i) + "-SM" + str(j) + establish_connection(GRID_accounts['SM' + str(i)],GRID_accounts['SM' + str(j) ]))
    print("SM" + str(i) + "-DC1 " + establish_connection(GRID_accounts['SM' + str(i)],GRID_accounts['DC1']))


print("--------------------------------Etablisment de connexions niveau NAN 2----------------------")
for i in range(11,21):
    for j in range (11,21):
        if (i != j):
            print("SM"+str(i) + "-SM" + str(j) + establish_connection(GRID_accounts['SM' + str(i)],GRID_accounts['SM' + str(j) ]))
    print("SM" + str(i) + "-DC2 " + establish_connection(GRID_accounts['SM' + str(i)],GRID_accounts['DC2']))

print("-------------------------------Etablisment de connexions niveau WAN-------------------------")
for i in range(1,11):
    for j in range (1,11):
        if (i != j):
            print("DC" + str(i) + "-DC" + str(j) + establish_connection(GRID_accounts['DC' + str(i)],GRID_accounts['DC' + str(j) ]))

print ("")

global List_rep
global Liste_theft

Leader = getLeader(list_account)
print("le leader est le compte: " + str(grid_connexion.retrieveIDMeter(Leader)) + "   " + str(Leader))
List_rep = grid_connexion.getRepWan()

def transaction_NAN1(leader, date_mesure, time_mesure, repu):
    global counter
    for i in range(1,11):
        open(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv','wb')
   
    mesure = []
    hash_mesure = []
    meter = []
    c = []
    power  = 0
    power2 = []
    for i in range(1,11):
        p = rn.uniform(0, 1.8)
        power = power + p
        mesure.append(str(p))
        hash_mesure.append(sha512(str(mesure[i-1]).encode('utf-8')).hexdigest())
        meter.append(grid_connexion.retrieveIDMeter(accounts[i]))
        data = pd.DataFrame([[date_mesure,time_mesure,meter[i-1] ,mesure[i-1],hash_mesure[i-1],repu[i-1]]])    
        data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')
        public_key_dc = import_public_key(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\WAN\DC' + str(1) + '\public_key.pem')
        
        c.append(encryption(public_key_dc, mesure[i-1].encode('ascii')))
        c[i-1] = c[i-1]
        for j in range(1,11):
            counter = counter + 1
            if(j != i):#envoi des données entre les smart meters 
                print("Envoi des donnees entre SM" + str(i) + " et le SM" + str(j))
                data = pd.DataFrame([[date_mesure, time_mesure, meter[i-1] , c[i-1], hash_mesure[i-1], repu[i-1]]])
                data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(j) + '\SM' + str(j) + '.csv', index=False, mode='a')
    print("")
    print("----------------------------ajoute de l'énergie destribué à la blockchain---------------")
    print("")
    power2.append(str(power))
    grid_connexion.tansactionWanInit2(power2, {'from': accounts[0],  "gas":1000000, "allow_revert":True})
    merkleRoot = merkle_root(hash_mesure)
    print("")
    print("-------------------------------L'ajoute de block B1 ----------------------------------")
    try:
        grid_connexion.tansactionNan1B1(meter, date_mesure, time_mesure, c, merkleRoot,{'from':leader})
        print("Block B1 Ajouté date: " + str(date_mesure) + " l'heure " + str(time_mesure))
        print("")
    except:
        print("erreur dans l'joute de B1 " + str(date_mesure) + "l'heure " + str(time_mesure))
        print("")


#fonction qui va vérifier le block envoyé par le leader 
def Verify_block(leader, date_mesure, time_mesure, rep, a, validateurs, Repmin,  Lagrégé, Ltheft):
    global counter
    print("")
    print("----------------------------Verification de bloc B1-------------------------------------" )
    print("")
    initializeVote(list_account)
    for j in range(1,11):
        open(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(j) + '\VoteSM' + str(j) + '.csv','wb')
    meter3 = []
    rep_m = []
    nouds_valid = []
    nouds_validRep = []

    grid_connexion = Connexions[-1]

    idLeader = grid_connexion.retrieveIDMeter(leader)
    il = idLeader % 1000
    meter= pd.read_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(il) + '\SM' + str(il) + '.csv', header=None)
    meter = dataFrame_to_Dict(meter)
    meter = dataListe(meter)
    meter_validateur = list_trie(meter)
    meter_validateurRep = meter_validateur[5]
    meter_validateurId = meter_validateur[2]
    n = round(len(meter_validateurId)*validateurs) 
    for k in range(1, 1+n):
        nouds_valid.append(meter_validateurId[k])
        nouds_validRep.append(meter_validateurRep[k])
    print("")
    print( "les noeuds validateurs sont : ")
    print(nouds_valid)
    print("")
    for i in range(1,11):
        meter= pd.read_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', header=None)
        meter = dataFrame_to_Dict(meter)
        meter = dataListe(meter)
        date_block = grid_connexion.get_dateUse()
        time_use = grid_connexion.get_TimeUse()
        Send = True 
        if (meter[0][0] != date_block or meter[1][0] != time_use):
            print("SM" + str(i) + " block B1 généré par leader " + str(leader) + " est faut ")
            print("SM" + str(i) + " diminuer la réputation du Leader: " + str(leader))
            print(" ")
            Send = False 
            #leader n'a pas envoyé le block (chaque noeud diminue la réputation de leader)
            meter2= pd.read_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', header = None)
            id = grid_connexion.retrieveIDMeter(leader)
            meter2 = dataFrame_to_Dict(meter2)
            meter2 = dataListe(meter2)
            open(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv','wb')
            l = len(meter2[0])
            #print(l)
            for j in range(0, l):
                if meter2[2][j] == id: 
                    Rc = int(meter2[5][j]) - 10
                    re = a*int(meter2[5][j]) + (1 - a)+Rc
                    re = round(re)
                    if re < Repmin:
                        print("Alert id: " + str(meter2[2][j]))
                    else:
                        Lagrégé[j] = a* Lagrégé[j] + (1-a)/2*Ltheft[j] + (1-a)/2*re
                        if (Lagrégé[j]< Repmin):
                            print("Alert id: " + str(meter2[2][j]))
                    rep_m.append(re)
                    data = pd.DataFrame([[meter2[0][0],meter2[1][0],meter2[2][j] ,meter2[3][j],meter2[4][j],re]])    
                    data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')
                else:
                    data = pd.DataFrame([[meter2[0][0],meter2[1][0],meter2[2][j] ,meter2[3][j],meter2[4][j],meter2[5][j]]])    
                    data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')
                    rep_m.append(meter2[5][j])

        elif(merkle_root(meter[4]) == grid_connexion.get_dataMerkleRoot()):#meter[4] est la liste des hash 
            vote = True
            if (meter[2][i-1] in nouds_valid):
                parm = int(meter[2][i-1]) % 1000
                print("")
                print("noeud valdateur " + str(meter[2][i-1]) + " vote par acceptée" )
                print("")
                grid_connexion.VoteB1(parm, vote,date_mesure,time_mesure, {'from': accounts[i],"gas":1000000, "allow_revert":True})
                meter3.append(grid_connexion.retrieveIDMeter(accounts[i]))
                data2 = pd.DataFrame([[date_mesure,time_mesure,meter3[i-1] ,vote]])    
                data2.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\VoteSM' + str(i) + '.csv', index=False, mode = 'a')
                for j in range(1,11):
                    counter = counter + 1
                    if(j != i):
                        #tu dois crypter le vote avant de l'envoyer
                        data = pd.DataFrame([[date_mesure, time_mesure, meter3[i-1] , vote]])
                        data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(j) + '\VoteSM' + str(j) + '.csv', index=False, mode='a') 
            else:
                meter3.append(grid_connexion.retrieveIDMeter(accounts[i]))
        else:
            vote = False
            if (meter[2][i-1] in nouds_valid):
                parm = int(meter[2][i-1]) % 1000
                print("")
                print("noeud valdateur " + str(meter[2][i-1]) + " vote par refusée" )
                print("")
                grid_connexion.VoteB1(parm, vote,date_mesure,time_mesure, {'from': accounts[i],"gas":1000000, "allow_revert":True})
                meter3.append(grid_connexion.retrieveIDMeter(accounts[i]))
                data2 = pd.DataFrame([[date_mesure,time_mesure,meter3[i-1] ,vote]])    
                data2.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\VoteSM' + str(i) + '.csv', index=False, mode = 'a')
                for j in range(1,4):
                    counter = counter + 1
                    if(j != i):
                        #tu dois crypter le vote avant de l'envoyer
                        data = pd.DataFrame([[date_mesure, time_mesure, meter3[i-1] , vote]])
                        data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(j) + '\VoteSM' + str(j) + '.csv', index=False, mode='a') 
            else:
                meter3.append(grid_connexion.retrieveIDMeter(accounts[i]))
                counter = counter + 1

    if Send == False:# selectionner un autre leader et creer le block 
        print("-------------------------------selection d'un autre leader-------------------------------")
        meters = grid_connexion.GetDcAccounts(accounts[21]) #Dc de NAN 1
        t = len(meters)
        meters_m2 = []
        rep_m2 = []
        for i in range(0, t):
            if meters[i] != leader:
                rep_m2.append(rep[i])
                meters_m2.append(meters[i])
            
        grid_connexion.select_leader(meters_m2, rep_m2, {"from":accounts[0]})
        leader = getLeader(meters_m2)
        Leader = leader 
        print(print("le nouveau leader est le compte: " + str(grid_connexion.retrieveIDMeter(Leader)) + "   " + str(Leader)))
        transaction_NAN1(leader, date_mesure, time_mesure, rep_m)
        Verify_block(leader, date_mesure, time_mesure, rep_m,a, validateurs, Repmin,  Lagrégé, Ltheft)
    List_rep  = Lagrégé
        
        
            

        
        

#fonction qui va mettre à jour la liste des répuations
def ReputationUpdate(leader, a, validateurs, Repmin,  Lagrégé, Ltheft):
    global counter
    nouds_valid = []
    nouds_validRep = []
    Lagrégé = list(Lagrégé)
    print("--------------------Mise à jour de la liste des réputations--------------------------")
    for i in range(1, 11):
        meter = pd.read_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', header=None)
        meter = dataFrame_to_Dict(meter)
        meter = dataListe(meter)
        #mettre à jour la réputation de noueds qui n'ont pas envoyé leurs misures
        open(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv','wb')
        l = len(meter[0])
        print("")
        print("vérifier les noeuds qui n'ont pas envoyé leurs mesure et diminiuer leurs réputation ")
        for j in range(0, l):
            if meter[3][j] == "0":#meter n'a pas envoyé ses musures de consommation 
                id = meter[2][j]
                print("")
                print("Meter " + str(id) + " n'a pas envoyé ses mesures de consommation à " + str(meter[2][i-1])  )
                print("")
                if meter[2][j] == id: 
                    Rc = int(meter[5][j]) - 10
                    re = a*int(meter[5][j]) + (1 - a)*Rc
                    re = round(re)
                    if re < Repmin:
                        print("Alert id: " + str(meter[2][j]))
                    else:
                        Lagrégé[j] = a* Lagrégé[j] + (1-a)/2*Ltheft[j] + (1-a)/2*re
                        if (Lagrégé[j]< Repmin):
                            print("Alert id: " + str(meter[2][j]))
                    data = pd.DataFrame([[meter[0][0],meter[1][0],meter[2][j] ,meter[3][j],meter[4][j],re]])    
                    data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')
            else:
                print("Meter " + str(meter[2][j]) + " a envoyé ses mesures de consommation à " + str(meter[2][i-1]))
                print("")
                data = pd.DataFrame([[meter[0][0],meter[1][0],meter[2][j] ,meter[3][j],meter[4][j],meter[5][j]]])    
                data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')
    print("----------------Vérifier si les données envoyés par le leader sont valides-------------- ")
    if (grid_connexion.DataVa()): #voir si le données envoyées par leader sont valide(si le bloc est valide)
       print(" donnés Validés ")
       print("")
       for i in range(1, 11):
            meter = pd.read_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', header=None)
            meter = dataFrame_to_Dict(meter)
            meter = dataListe(meter)
            open(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv','wb')
            id = grid_connexion.retrieveIDMeter(leader)
            l = len(meter[0])
            for j in range(0, l):
                if meter[2][j] == id:#meter leader 
                    re = meter[5][j]
                    data = pd.DataFrame([[meter[0][0],meter[1][0],meter[2][j] ,meter[3][j],meter[4][j],re]])    
                    data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')
                else:
                    data = pd.DataFrame([[meter[0][0],meter[1][0],meter[2][j] ,meter[3][j],meter[4][j],meter[5][j]]])    
                    data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')       
    else:
        print(" donnés Non Validés ")
        print("diminuer La réputation de Leader")
        print("")

        for i in range(1, 11):
            meter = pd.read_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', header=None)
            meter = dataFrame_to_Dict(meter)
            meter = dataListe(meter)
            open(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv','wb')
            id = grid_connexion.retrieveIDMeter(leader)
            l = len(meter[0])
            for j in range(0, l):
                if meter[2][j] == id:#meter leader 
                    Rc = int(meter[5][j]) - 10
                    re = a*int(meter[5][j]) + (1 - a)*Rc
                    if re < Repmin:
                        print("Alert id: " + str(meter[2][j]))
                    else:
                        Lagrégé[j] = a* Lagrégé[j] + (1-a)/2*Ltheft[j] + (1-a)/2*re
                        if (Lagrégé[j]< Repmin):
                            print("Alert id: " + str(meter[2][j]))
                    re = round(re) #diminuer la réputation de leader 
                    data = pd.DataFrame([[meter[0][0],meter[1][0],meter[2][j] ,meter[3][j],meter[4][j],re]])    
                    data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')
                else:
                    data = pd.DataFrame([[meter[0][0],meter[1][0],meter[2][j] ,meter[3][j],meter[4][j],meter[5][j]]])    
                    data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')

    print('mettre à jour les réputations des noeuds validateurs par rapport au vote')
    for i in range(1, 11):#mettre à jour la réputation des noeuds par rapport vote 
        idLeader = grid_connexion.retrieveIDMeter(leader)
        il = idLeader % 1000
        meter= pd.read_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(il) + '\SM' + str(il) + '.csv', header=None)
        meter = dataFrame_to_Dict(meter)
        meter = dataListe(meter)
        meter_validateur = list_trie(meter)
        meter_validateurRep = meter_validateur[5]
        meter_validateurId = meter_validateur[2]
        n = round(len(meter_validateurId)*validateurs) 
        for k in range(1, 1+n):
            nouds_valid.append(meter_validateurId[k])
            nouds_validRep.append(meter_validateurRep[k])
    for i in range(1, 11):
        meter = pd.read_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', header=None)
        meter = dataFrame_to_Dict(meter)
        meter = dataListe(meter)
        l = len(meter[0])
        open(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv','wb')
        for j in range(0, l):
            if (meter[2][j] in nouds_valid):
                meter2 = pd.read_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\VoteSM' + str(i) + '.csv', header=None)
                meter2 = dataFrame_to_Dict(meter2)
                meter2 = dataListe(meter2)
                l2 = len(meter2[0])
                for k in range(0, l2):
                    if (meter2[3][k] == str(grid_connexion.DataVa()) and meter[2][j] == meter2[2][k] ):#comparer le vote de meter avec vote globale 
                        re = meter[5][j]
                        data = pd.DataFrame([[meter[0][0],meter[1][0],meter[2][j] ,meter[3][j],meter[4][j],re]])    
                        data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')
                    elif (meter2[3][k] != str(grid_connexion.DataVa()) and meter[2][j] == meter2[2][k]):
                        Rc = int(meter[5][j]) - 10
                        re = a*int(meter[5][j]) + (1 - a)*Rc
                        re = round(re) #diminuer la réputation de noeud
                        if re < Repmin:
                            print("Alert id: " + str(meter[2][j]))
                        else:
                            Lagrégé[j] = a* Lagrégé[j] + (1-a)/2*Ltheft[j] + (1-a)/2*re
                            if (Lagrégé[j]< Repmin):
                                print("Alert id: " + str(meter[2][j]))
                        data = pd.DataFrame([[meter[0][0],meter[1][0],meter[2][j] ,meter[3][j],meter[4][j],re]])    
                        data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')
            else:
                data = pd.DataFrame([[meter[0][0],meter[1][0],meter[2][j] ,meter[3][j],meter[4][j],meter[5][j]]])    
                data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')
    List_rep = Lagrégé

def transaction_NAN1_B2(leader, rep):
    global counter
    print("")
    print("----------------------------L'ajoute de block B2----------------------------------------")
    grid_connexion = Connexions[-1]
    if(grid_connexion.DataVa()== False):
        print("")
        print("------------------------Block B1 Non Valide-----------------------------------------")
        print("------------------------Suppresion de Block B1--------------------------------------")
        print("")
        grid_connexion.Delete_B1({"from":accounts[0], "gas":1000000, "allow_revert":True})
        meters = grid_connexion.GetDcAccounts(accounts[7]) #Dc de NAN 1
        t = len(meters)
        meters_m = []
        rep_m = []
        for i in range(0, t):
            if meters[i] != leader:
                rep_m.append(rep[i])
                meters_m.append(meters[i])

        print("------------ Selection d'un nouveau Leader -------------")  
        grid_connexion.select_leader(meters_m, rep_m, {"from":accounts[0]})
        leader = getLeader(meters_m) 
    for i in range(1,11):
        meter= pd.read_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', header=None)
        meter = dataFrame_to_Dict(meter)
        meter = dataListe(meter)
        id = grid_connexion.retrieveIDMeter(leader)
        
        if id == grid_connexion.retrieveIDMeter(accounts[i]):
            print(" Ajoute de B2 par le leader " + str(id) )
            print("")
            rep = meter[5]
            merklerootRep = merkle_root(rep)
            try:
                grid_connexion.tansactionNan1B2(rep, merklerootRep,{'from':leader})
                print("")
                print("Block B2  Ajouté")
                print("")
            except:
                print("")
                print("erreur dans l'joute de B1")
                print("")

#fonction qui va vérifier si le block b2 est valide
def Verify_block_B2(leader, date_mesure, time_mesure, rep, a, validateurs,  Repmin,  Lagrégé, Ltheft):
    global counter
    print("")
    print("----------------------------Verification de bloc B2-------------------------------------" )
    print("")
    initializeVote(list_account)
    for j in range(1,11):
        open(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(j) + '\VoteRepSM' + str(j) + '.csv','wb')
    meter3 = []
    rep_m = []
    nouds_valid = []
    nouds_validRep = []
    grid_connexion = Connexions[-1]
    idLeader = grid_connexion.retrieveIDMeter(leader)
    il = idLeader % 1000
    meter= pd.read_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(il) + '\SM' + str(il) + '.csv', header=None)
    meter = dataFrame_to_Dict(meter)
    meter = dataListe(meter)
    meter_validateur = list_trie(meter)
    meter_validateurRep = meter_validateur[5]
    meter_validateurId = meter_validateur[2]
    n = round(len(meter_validateurId)*validateurs) 
    for k in range(1, 1+n):
        nouds_valid.append(meter_validateurId[k])
        nouds_validRep.append(meter_validateurRep[k])
    print("")
    print( "les noeuds validateurs sont : ")
    print(nouds_valid)
    print("")

    for i in range(1,11):
        meter= pd.read_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', header=None)
        meter = dataFrame_to_Dict(meter)
        meter = dataListe(meter)
        date_block = grid_connexion.get_dateUse()
        time_use = grid_connexion.get_TimeUse()
        Send = True 
        if (meter[0][0] != date_block or meter[1][0] != time_use):
            print("SM" + str(i) + " block B1 généré par leader " + str(leader) + " est faut ")
            print("SM" + str(i) + " diminuer la réputation du Leader: " + str(leader))
            print(" ")
            Send = False 
            #leader n'a pas envoyé le block (chaque noeud diminue la réputation de leader)
            meter2= pd.read_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', header = None)
            id = grid_connexion.retrieveIDMeter(leader)
            meter2 = dataFrame_to_Dict(meter2)
            meter2 = dataListe(meter2)
            open(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv','wb')
            l = len(meter2[0])
            #print(l)
            for j in range(0, l):
                if meter2[2][j] == id: 
                    Rc = int(meter2[5][j]) - 10
                    re = a*int(meter2[5][j]) + (1 - a)*Rc
                    re = round(re)
                    if re < Repmin:
                            print("Alert id: " + str(meter2[2][j]))
                    else:
                        Lagrégé[j] = a* Lagrégé[j] + (1-a)/2*Ltheft[j] + (1-a)/2*re
                        if (Lagrégé[j]< Repmin):
                            print("Alert id: " + str(meter2[2][j]))
                    data = pd.DataFrame([[meter2[0][0],meter2[1][0],meter2[2][j] ,meter2[3][j],meter2[4][j],re]])    
                    data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')
                else:
                    data = pd.DataFrame([[meter2[0][0],meter2[1][0],meter2[2][j] ,meter2[3][j],meter2[4][j],meter2[5][j]]])    
                    data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')

        elif(merkle_root(meter[5]) == grid_connexion.get_dataMerkleRootRep()):  #meter[5] est la liste des réputation
            vote = True
            if (meter[2][i-1] in nouds_valid):
                parm = int(meter[2][i-1]) % 1000
                print("")
                print("noeud valdateur " + str(meter[2][i-1]) + " vote par acceptée" )
                print("")
                grid_connexion.VoteB2(parm, vote,date_mesure,time_mesure, {'from': accounts[i],"gas":1000000, "allow_revert":True})
                meter3.append(grid_connexion.retrieveIDMeter(accounts[i]))
                data2 = pd.DataFrame([[date_mesure,time_mesure,meter3[i-1] ,vote]])    
                data2.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\VoteRepSM' + str(i) + '.csv', index=False, mode = 'a')
                for j in range(1,11):
                    counter = counter + 1
                    if(j != i):
                        #tu dois crypter le vote avant de l'envoyer
                        data = pd.DataFrame([[date_mesure, time_mesure, meter3[i-1] , vote]])
                        data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(j) + '\VoteRepSM' + str(j) + '.csv', index=False, mode='a')
            else: 
                meter3.append(grid_connexion.retrieveIDMeter(accounts[i]))
                counter = counter + 1

        elif (merkle_root(meter[5]) != grid_connexion.get_dataMerkleRootRep()):
            vote = False
            print(merkle_root(meter[5]))
            print(grid_connexion.get_dataMerkleRootRep())
            if (meter[2][i-1] in nouds_valid):
                parm = int(meter[2][i-1]) % 1000
                print("")
                print("noeud valdateur " + str(meter[2][i-1]) + " vote par refusée" )
                print("")
                grid_connexion.VoteB2(parm, vote,date_mesure,time_mesure, {'from': accounts[i],"gas":1000000, "allow_revert":True})
                meter3.append(grid_connexion.retrieveIDMeter(accounts[i]))
                data2 = pd.DataFrame([[date_mesure,time_mesure,meter3[i-1] ,vote]])    
                data2.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\VoteRepSM' + str(i) + '.csv', index=False, mode = 'a')
                for j in range(1,11):
                    counter = counter + 1
                    if(j != i):
                        #tu dois crypter le vote avant de l'envoyer
                        data = pd.DataFrame([[date_mesure, time_mesure, meter3[i-1] , vote]])
                        data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(j) + '\VoteRepSM' + str(j) + '.csv', index=False, mode='a') 
            else: 
                meter3.append(grid_connexion.retrieveIDMeter(accounts[i]))
                counter = counter + 1

    if Send == False:# selectionner un autre leader et creer le block 
        meters = grid_connexion.GetDcAccounts(accounts[21]) #Dc de NAN 1
        t = len(meters)
        meters_m = []
        rep_m = []
        for i in range(0, t):
            if meters[i] != leader:
                rep_m.append(rep[i])
                meters_m.append(meters[i])
        grid_connexion.select_leader(meters_m, rep_m, {"from":accounts[0]})
        leader = getLeader(meters_m) 
        transaction_NAN1_B2(leader,date_mesure,time_mesure, rep_m,  Repmin,  Lagrégé, Ltheft)
        Verify_block_B2(leader, date_mesure, time_mesure, rep_m)
    List_rep = Lagrégé

def RepUpdateB2(leader ,date_mesure, time_mesure,rep, a, validateurs, Repmin,  Lagrégé, Ltheft):
    global counter
    print("")
    print("------------------------Mise à jour dela liste de réputation apres validation de b2---------------")
    print("")
    if (grid_connexion.RepVa() == False):
        print("------------------------B2 non valide selection d'un autre leader-------------------")
        for i in range(1, 11):
            meter = pd.read_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', header=None)
            meter = dataFrame_to_Dict(meter)
            meter = dataListe(meter)
            open(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv','wb')
            id = grid_connexion.retrieveIDMeter(leader)
            l = len(meter[0])
            for j in range(0, l):
                if meter[2][j] == id:#meter leader 
                    Rc = int(meter[5][j]) - 10
                    re = a*int(meter[5][j]) + (1 - a)*Rc
                    if re < Repmin:
                        print("Alert id: " + str(meter[2][j]))
                    else:
                        Lagrégé[j] = a* Lagrégé[j] + (1-a)/2*Ltheft[j] + (1-a)/2*re
                        if (Lagrégé[j]< Repmin):
                            print("Alert id: " + str(meter[2][j]))
                    re = round(re) #diminuer la réputation de leader 
                    data = pd.DataFrame([[meter[0][0],meter[1][0],meter[2][j] ,meter[3][j],meter[4][j],re]])    
                    data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')
                else:
                    data = pd.DataFrame([[meter[0][0],meter[1][0],meter[2][j] ,meter[3][j],meter[4][j],meter[5][j]]])    
                    data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\NAN1\SM' + str(i) + '\SM' + str(i) + '.csv', index=False, mode = 'a')
        meters = grid_connexion.GetDcAccounts(accounts[21]) #Dc de NAN 1
        t = len(meters)
        meters_m = []
        rep_m = []
        for i in range(0, t):
            if meters[i] != leader:
                rep_m.append(rep[i])
                meters_m.append(meters[i])
        grid_connexion.select_leader(meters_m, rep_m, {"from":accounts[0]})
        leader = getLeader(meters_m) 
        transaction_NAN1_B2(leader, rep_m)
        Verify_block_B2(leader, date_mesure, time_mesure, rep_m, a, validateurs,  Repmin,  Lagrégé, Ltheft)
    print("----------------------------Block B2 est valide!----------------------------------------")
    List_rep = Lagrégé
    print("")
    print("----------------------------counter--------------------------------")
    print("Le nombre totale de messages echangés " + str(counter))

def DCGetValuesNan1(date_use, time_use):
    print("")
    print("-----------Récuparation des données par le DC1 seulement si le block est valide----------")
    if (grid_connexion.DataVa()):
        print("")
        print("block daté de " + str(date_use) + " et l'heure " + str(time_use) + " est valide et récupéré par dc " )
        print("")
        ids = grid_connexion.get_IDS(1)
        mesures = grid_connexion.get_Mesures(1)
        grid_connexion.DataVa()
        sommePowers =0
        for id in ids: 
            i = id % 1000
            PRIVKEY= import_private_key(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\WAN\DC' + str(1) + '\private_key.pem')
            mesureCypher = decryption(PRIVKEY, mesures[i])
            data = pd.DataFrame([[id,mesureCypher.decode()]])    
            data.to_csv(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\WAN\DC' + str(1) + '\SM' + str(i+1) + '.csv', header = False, index=False, mode = 'a')
            sommePowers = sommePowers + float(mesureCypher.decode())
        return sommePowers 
    else: 
        print("block daté de " + str(date_use) + " et l'heure " + str(time_use) + " est non valide et ignoré par le dc " )


#l'énergie distribué
def getSommePower():
    po = grid_connexion.getUseZone()
    return po
#La liste des DC wan 
def getWANDc():
    Liste_dc=[]
    for i in range(21, 31):
        id = grid_connexion.getIDDC(accounts[i])
        Liste_dc.append(id)
    return Liste_dc


def RepWanUpdate(k, Ltheft, Lagrégé, Lcons, Repmin, power,power_somme , a, date_use, time_use):
    meters = grid_connexion.get_IDS(1)
    Ltheft = list(Ltheft)
    Lagrégé = list(Lagrégé)
    Lcons = list(Lcons)
    if (power_somme < 1.04*float(power) and k == 1):
        detect_result  = Energy_Theft_Detection(r"C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\WAN\DC1")
        #{'1000':0,'1001':1,'1002':0,'1003':0,'1004':0,'1005':1,'1006':0,'1007':0, '1008':0,'1009':0}
        for i in meters:
            j = i % 1000
            if int(detect_result[str(i)]) == int(1):
                Rtheft = Ltheft[j] - 10
                Ltheft[j] = a*Ltheft[j] + (1-a)*Rtheft 
                print(Ltheft)
                if (Ltheft[j]< Repmin):
                    print("Alert vol d'energie id: " + str(i))
                Lagrégé[j] = a* Lagrégé[j] + (1-a)/2*Ltheft[j] + (1-a)/2*Lcons[j]
                print(Lagrégé)
                if (Lagrégé[j]< Repmin):
                    print("Alert id: " + str(i))
    else:
        for i in meters:
            j = i % 1000 
            Lagrégé[j] = a* Lagrégé[j] + (1-a)/2*Ltheft[j] + (1-a)/2*Lcons[j]
            if (Lagrégé[j]< Repmin):
                print("")
                print("Alert id: " + str(i))
    print("")
    print("----------------------------L'ajoute de block niveau WAN-----------------------")
    print("")
    meters = grid_connexion.get_IDS(1)
    meters2 = getWANDc()
    power = grid_connexion.get_Mesures(1)
    i = round(rn.uniform(0, len(meters2)-1))
    print("")
    print("Le Dc choisi pour ce tour afin d'ajouter le block est " + str(meters2[i]))
    try:
        grid_connexion.transactionWan(date_use, time_use, meters, power, Lagrégé, Ltheft,{"from":accounts[i+21]} )
    except:
        print("")
        print("Erreur de l'ajoute de block WAN ")

def getGas20():
    print("")
    print("----------------------------Gas utilisé pour Transaction avec P = 20%--------------------------------")
    print("")
    from web3 import Web3
    web3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
    trasaction_array = [web3.eth.getTransactionByBlock(i,0)['hash'].hex() for i in range(59, 71)]
    gas = [web3.eth.getTransaction(i)['gas'] for i in trasaction_array]
    print(gas)
    somme_gas = 0
    for i in gas:
        somme_gas = somme_gas + i
    print('Le gas consommé ',somme_gas)
def getGas50():
    print("")
    print("----------------------------Gas utilisé pour Transaction avec P = 50%--------------------------------")
    print("")
    from web3 import Web3
    web3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))    
    trasaction_array = [web3.eth.getTransactionByBlock(i,0)['hash'].hex() for i in range(74, 92)]
    gas = [web3.eth.getTransaction(i)['gas'] for i in trasaction_array]
    print(gas)
    somme_gas = 0
    for i in gas:
        somme_gas = somme_gas + i
    print('Le gas consommé ',somme_gas)

def getCurrentblock():
    print("")
    print("----------------------------Current Block-----------------------------------------------")
    from web3 import Web3
    web3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
    last_block = web3.eth.blockNumber     
    return last_block      

def main():
    date_jour = 9062022
    date_heure = 120000 
    a = 0.4
    threshold = 75
    validateur = 0.2
    for i in range(1, 2):
        grid_connexion = Connexions[-1]
        Liste_theft = grid_connexion.getRepTheftWan() #reputation energy theft dernier block
        List_rep = grid_connexion.getRepWan() #reputation aggrégé dernier block 
        rep = grid_connexion.GetRepList() #rep consensus de dernier block NAN 
        Leader = getLeader(list_account)
        transaction_NAN1(Leader,date_jour,date_heure, rep)
        Verify_block(Leader,date_jour, date_heure, rep, a, validateur, threshold, List_rep, Liste_theft)  
        ReputationUpdate(Leader,a, validateur, threshold, List_rep, Liste_theft)
        transaction_NAN1_B2(Leader, rep)
        grid_connexion = Connexions[-1]
        Verify_block_B2(Leader,date_jour,date_heure, rep, a, validateur, threshold, List_rep, Liste_theft)
        RepUpdateB2(Leader,date_jour,date_heure, rep, a, validateur,threshold, List_rep, Liste_theft)
        Somme_energy = DCGetValuesNan1(date_jour, date_heure) 
        grid_connexion = Connexions[-1]
        power = getSommePower() #somme enrigestré dans la blockchain 
        RepWanUpdate(i, Liste_theft, List_rep, rep,threshold, power[0],Somme_energy , a, date_jour, date_heure)
        grid_connexion = Connexions[-1]
        List_rep = grid_connexion.getRepWan()
        print(List_rep)
        print(getCurrentblock())
        #getGas20()
        #getGas50()
        #date_heure = date_heure + 30 