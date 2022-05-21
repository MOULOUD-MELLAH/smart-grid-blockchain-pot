from brownie import accounts, Connexions, Communications, config

def deploy_grid_connexion():
    account = accounts[0]
    grid_connexion = Connexions.deploy({"from":account})
    
    for i in range(1,4):
        grid_connexion.addMeter(accounts[i],999 + i, 'SM'+str(i), accounts[7],{"from":account})
    
    for i in range(4,7):
        grid_connexion.addMeter(accounts[i], 999 + i, 'SM'+str(i), accounts[8], {"from":account})
    
    grid_connexion.addDC(accounts[7],10, "DC1" ,"zone 1", accounts[1], accounts[2], accounts[3], {"from":account})
    grid_connexion.addDC(accounts[8],11, "DC2" ,"zone 2", accounts[4], accounts[5], accounts[6], {"from":account})
    grid_connexion.addDC(accounts[9],12, "DC3" ,"zone 3", '0x0000000000000000000000000000000000000000', '0x0000000000000000000000000000000000000000', '0x0000000000000000000000000000000000000000', {"from":account})
    return grid_connexion

def deploy_grid_communications():
    account = accounts[0]
    grid_communications = Communications.deploy(account,{"from":account})




def main ():
    deploy_grid_connexion()
    deploy_grid_communications()

