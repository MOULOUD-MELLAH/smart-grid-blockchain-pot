#!/usr/bin/env python
# coding: utf-8

# # Chargement du meilleur modèle entrainé

# In[1]:


from keras.models import Sequential, load_model
import tensorflow as tf
import os
import pandas
import sys
import fnmatch
import numpy as np
import glob 
import time

def Energy_Theft_Detection(Path):
    Categories = ["Non Vol","Vol"] 
    Resultat = {} # Dictionnaire contenant "Id Smart Meter : Vol/Pas Vol"
    
    # Changement du répertoire vers le fichiers de mesures 
    try:
        os.chdir(Path)
        print("Changement du repértoire vers l'emplacement du fichier.."+str(os.getcwd()))
        #os.chdir('..')        
    except OSError:
        print("Erreur lors du changement du répértoire vers le fichier de mesures !")  
   
    # Chargement du modèle de détection de vol d'énergie
    try:
        print("Chargement du modèle Energy theft..")
        #os.chdir(Path)
        model = tf.keras.models.load_model('my_best_model.epoch96-loss0.08.hdf5')
        print("------------------Architecture du modèle chargé------------------")
        print(model.summary())
    except OSError:
        print("Erreur lors du chargement du modèle deep learning !")  
    temp = ""
    ID_Smart_Meter = ""
    Total_Time = 0
    print("Traitement des fichiers de mesures..")
    for file in os.listdir('.'): # retourne une liste des fichiers
        if fnmatch.fnmatch(file, 'SM*.csv'):
            a = time.time()
            indice = 0
            temp = str(file)
            print(file)
            # prétraitement du fichier
            file = open(file, "r+")
            lines = file.readlines()
            file.truncate(0)
            file.close()

            var = ""

            for line in lines:
                
                test = line.split(",")    
                if(int(indice)==0):
                    ID_Smart_Meter = test[0]
                    indice = indice +1
                var = var + str(test[1]).strip()+","
            var = ID_Smart_Meter+","+var[:len(var) - 1]
            
            f = open(temp, "w")
            f.write(var)
            f.close()
            file = f
            # Lecture des fichiers contenant les mesures
            try:
                print("Lecture des mesures du fichier "+temp+"..")
                data = pandas.read_csv(temp,header=None)
                ID_Smart_Meter = str(data[0][0])
                print("Traitement des Mesures du Smart Meter "+ID_Smart_Meter)
            except OSError:
                print("Erreur lors de la lecture des mesures !")  
   
            # Prétraitement des mesures
            try:
                print("Prétraitement des mesures..")
                data = data.apply (pandas.to_numeric, errors='coerce') # convert value to float
                data = data.dropna() # drop the nan value
                Valeurs = data.drop(data.columns[0], axis=1)
                
            # Réorganisation des mesures "ID, Mesures"
            
                Valeurs = Valeurs.values
                if(int(Valeurs.shape[0]) == 1 and int(Valeurs.shape[1] == 48)):
                    Valeurs = Valeurs.reshape(Valeurs.shape[0],6,8,1)
                    # Prédiction de vol d'énergie
                    try:
                        print("Prédiction..")
                        prediction = model.predict(Valeurs)   
                        print("Probabilités des deux classes est : "+str(prediction))
                        predicted_class = np.argmax(prediction)
                        pourcentage = "{:.0%}".format(np.max(prediction))
                        print("Probabilité de "+str(Categories[predicted_class]) +" du Smart Meter "+ID_Smart_Meter+" est de : "+ str(np.max(prediction))+" ==> "+pourcentage)
                        Resultat[ID_Smart_Meter]= np.argmax(prediction)
                        print("-------------------------Fin de la prédiction des mesures du Smart Meter "+ID_Smart_Meter+"-------------------------\n")
                        b = time.time()
       
                        print("Le temps d'exécution de la prédiction pour le Smart Meter "+ID_Smart_Meter+" est : "+str(round(b-a, 10))+" secondes\n")
                        Total_Time = Total_Time + round(b-a, 10)
                    except OSError:
                        print("Erreur lors de la prédiction du vol d'énergie  !")
                else : 
                    print("Les mesures fournis ne respectent pas le format : 48 x 2 (48 lignes, 2 colonnes)")
                    print("Probabilité de vol du Smart Meter "+ID_Smart_Meter+" est de : 100%")
                    Resultat[ID_Smart_Meter] = 1 # vol directement de l'énergie dans le cas du non respect du format
                    b = time.time()
                    print("Le temps d'exécution de la prédiction pour le Smart Meter "+ID_Smart_Meter+" est : "+str(round(b-a, 10))+" secondes\n")
                    Total_Time = Total_Time + round(b-a, 10)
            except OSError:
                print("Erreur lors du prétraitement des mesures !")  
        
    if len(Resultat) == 0:
        print("Aucun fichier de mesures n\'a été trouvé")    
    
    print("Le temps d'éxécution total est : "+str(Total_Time)+" secondes")
    print(Resultat)
    return Resultat  # Retourner le dictionnaire de résultats
    
    
#if len(sys.argv) > 1:
    #DataSet_PATH = "C:\\Users\\YANIS\\Downloads\\models-master\\models-master\\IRISH_DataSet"#sys.argv[1]
    #DataSet_PATH = r"C:\Users\YANIS\Downloads\PFE-SMART-GRID-10-20220614T213712Z-001\PFE-SMART-GRID-10\WAN\DC1"
#Resultat = Energy_Theft_Detection(DataSet_PATH)


#else:
#    print("Veuillez Saisir le chemin vers les fichiers de mesures des Smart Meter..!")
    



# In[9]:


"""from keras.layers import Dense, Conv2D
Weights = []
Biases = []
model = tf.keras.models.load_model('my_best_model.epoch96-loss0.08.hdf5')
for idx,i in enumerate(model.layers):
    if(isinstance(i, Conv2D) or isinstance(i, Dense)):
        weights = i.get_weights()[0]
        biases = i.get_weights()[1]
        weights = weights.flatten()
        biases = biases.flatten()
        Weights.append(weights.shape)
        Biases.append(biases.shape)
print("Weights : "+str(Weights))
print("biases : "+str(Biases))"""


# In[ ]:




