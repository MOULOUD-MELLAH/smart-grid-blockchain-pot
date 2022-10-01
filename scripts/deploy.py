from brownie import accounts, Connexions, config


#déployer le contrat les smart meter de chaqie zone et les DC 
def deploy_grid_connexion():
    print("")
    print("-------------deployemnt des contrats----------------")
    print("")
    print("Le compte Administrateur est " + str(accounts[0]))
    print("")
    
    account = accounts[0]
    grid_connexion = Connexions.deploy({"from":account})
    meterliste1 = []
    meterliste2 = []
    
    print("----------------------------Ajouter Les Smart Meters de NAN1----------------------------")
    print("")
    for i in range(1,11):
        grid_connexion.addMeter(accounts[i],999 + i, 'SM'+str(i), 1, accounts[21],{"from":account})
        meterliste1.append(accounts[i])
    
    print("----------------------------Ajouter Les Smarts Meters de NAN2---------------------------")
    print("")
    for i in range(11,21):
        grid_connexion.addMeter(accounts[i], 999 + i, 'SM'+str(i), 2, accounts[22], {"from":account})
        meterliste2.append(accounts[i])
    
    print("----------------------------Ajouter Les DC de wan---------------------------------------")
    print("")
    
    grid_connexion.addDC(accounts[21],10, "DC1" ,1, meterliste1, {"from":account})
    grid_connexion.addDC(accounts[22],11, "DC2" ,2, meterliste2, {"from":account})

    for i in range(23,31):
        meterliste = [ '0x0000000000000000000000000000000000000000', '0x0000000000000000000000000000000000000000', '0x0000000000000000000000000000000000000000', '0x0000000000000000000000000000000000000000', '0x0000000000000000000000000000000000000000', '0x0000000000000000000000000000000000000000', '0x0000000000000000000000000000000000000000', '0x0000000000000000000000000000000000000000', '0x0000000000000000000000000000000000000000', '0x0000000000000000000000000000000000000000']
        grid_connexion.addDC(accounts[i],i-11, "DC" + str(i-20) ,i-20,meterliste, {"from":account})
    
    return grid_connexion

#initilaiser la liste des reputation NAN1 pour la selection de leader la première fois

def WanInitialise():
    print("-----Initialiser la liste des réputation pour premier cycle de consensus----------------")
    print("") 
    grid_connexion = Connexions[-1]
    grid_connexion.WanInitialise([80,80,80,80,80,80,80,80,85,80], {"from":accounts[0], "gas":1000000, "allow_revert":True})


#initilaiser reputation Rtheft et Ragrégé 
def Rinitilize():
    print("-----Initialiser la liste des réputation (Rtheft et Ragrégé) pour premier cycle de consensus----------------")
    print("") 
    grid_connexion = Connexions[-1]
    grid_connexion.tansactionWanInit([80,80,80,80,80,80,80,80,80,80],[80,80,80,80,80,80,80,80,80,80], {"from":accounts[0], "gas":1000000, "allow_revert":True})
    
#selection de premier leader
 
def SetLeader(address):
    print("----------------------------Selection de Leader-----------------------------------------")
    print("") 
    grid_connexion = Connexions[-1]
    meters = grid_connexion.GetDcAccounts(address)
    rep = grid_connexion.GetRepList()
    Leader = grid_connexion.select_leader(meters, rep, {"from":accounts[0], "gas":1000000, "allow_revert":True})

def initializeVote(_meters):
    print("----------------------------Initialiser Le vote-----------------------------------------")
    print("") 
    grid_connexion = Connexions[-1]
    grid_connexion.VoteInitialize(_meters,{"from":accounts[0]})
    grid_connexion.VoteInitializeB2(_meters,{"from":accounts[0]})

def initializefilesDC1():
    for j in range(1,11):
        open(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\WAN\DC' + str(1) + '\SM' + str(j) + '.csv', 'wb')

def initializefilesDC2():
    for j in range(11,21):
        open(r'C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\WAN\DC' + str(2) + '\SM' + str(j) + '.csv', 'wb')

def getCurrentblock():
    print("----------------------------Dernier block-----------------------------------------------")
    from web3 import Web3
    web3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
    last_block = web3.eth.blockNumber     
    return last_block

def getGas():
    print("")
    print("----------------------------Gas utilisé pour déployement--------------------------------")
    print("")
    from web3 import Web3
    web3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
    trasaction_array = [web3.eth.getTransactionByBlock(i,0)['hash'].hex() for i in range(1, 32)]
    gas = [web3.eth.getTransaction(i)['gas'] for i in trasaction_array]
    print(gas)
    somme_gas = 0
    for i in gas:
        somme_gas = somme_gas + i
    print('Le gas consommé ',somme_gas)

def main ():
    #deploy_grid_connexion()
    WanInitialise()
    SetLeader(accounts[21]) #selecionner le leader parmi les noeuds de dc 1
    initializefilesDC1()
    Rinitilize()
    print(getCurrentblock())
    #getGas()

    