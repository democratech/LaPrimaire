# simulation pour le jugement majoritaire

import numpy as np
from scipy.stats import rv_discrete
import matplotlib.pyplot as plt
from math import *
import random
import os,sys
import argparse




Ncandidats = 100
Nelecteurs = 100000
Nlot = 10
Nmentions = 7
nameMentions = ["Excellent", "Tres bien", "Bien", "Assez bien", "Passable", "Insuffisant", "A rejeter"]
couleurs = ["DarkRed", "Crimson","Tomato","DarkOrange","Yellow","Khaki","DarkKhaki"]
random.WichmannHill(random.seed())
list_results="terranova.txt"
resName = "results.%i.%i.txt"  % (Ncandidats, Nelecteurs) 
list_interpolated="terranova." + str(Ncandidats) + ".txt"


parser = argparse.ArgumentParser()
parser.add_argument('--reset',  action='store_true', help='Reset all simulations')
args = parser.parse_args()

def normalize(v, ax=1):
     n = np.sum(v, axis=ax)
     b = np.transpose(v)
     c = np.divide(b,n)
     return np.transpose(c)

def probaCandidates(N, inFile, outFile):
    """Read inFile. If there is not enough candidates, interpolate other. Save in outFile """    
    inCandidates = np.genfromtxt(inFile, delimiter = " ", dtype=float)
    inCandidates = inCandidates[:,:Nmentions]
    Nc = len(inCandidates)
    param = np.zeros((Nmentions,2))
    param[:,0] = np.mean(inCandidates, axis=0)
    param[:,1] = np.std(inCandidates, axis=0)
    print param
    if Nc > N:
        random.shuffle(inCandidates)
        outCandidates = inCandidates[:N,:]
    else:
        outCandidates = np.zeros((N,Nmentions))
        outCandidates[:Nc,:] = inCandidates
        for i in range(Nmentions):
            coeff = np.random.normal(param[i,0], param[i,1], N-Nc)
            outCandidates[Nc:,i] = coeff
            # neg = outCandidates[Nc:,i]<0
#outCandidates[neg,i] =
    p = normalize(np.absolute(outCandidates)) #, norm='l1',axis=1)
    np.savetxt(outFile, p, delimiter = ",")
    
    
def loadProba(file):
    p = np.genfromtxt(file, delimiter = ",", dtype=float)
    return p
    
    
def subset(Ncandidat, Nlot, occurences):
    proba_candidat = np.array([1/float(j) if j != 0 else 1 for j in occurences])
    proba_candidat = proba_candidat / float(sum(proba_candidat))
    lot = np.random.choice(Ncandidats, size=Nlot, replace=False, p=proba_candidat)
    occurences[lot] += 1
    return lot
    
def vote(lot, proba): 
    votes = np.zeros(Nlot)
    for i in range(Nlot):  
    	distrib = rv_discrete(values=(range(Nmentions), proba[i,:]))
        votes[i] =  distrib.rvs() 
    return votes
    

    
# ------------------------------
#  initialisation :

results         = np.zeros((Ncandidats,Nmentions))


if not os.path.isfile(resName) or args.reset:
    probaCandidates(Ncandidats,list_results, list_interpolated)
    probaCandidats  = loadProba(list_interpolated)
    occurence       = np.zeros(Ncandidats)
    lBin            = round(Nelecteurs/10.0)
    for i in range(Nelecteurs):
        if(i % lBin == 0):
            print "%d / 10" % round(float(i)/float(lBin))
        lot     = subset(Ncandidats, Nlot, occurence)
        votes   = vote(lot, probaCandidats[lot,:])
        for i in range(Nlot):
            results[lot[i],votes[i]] += 1
    results = normalize(results)
    np.savetxt(resName, results, delimiter = ",")
else:
    probaCandidats  = loadProba(list_interpolated)
    results = np.genfromtxt(resName, delimiter = ",", dtype=float)
    


# print "Probabilites des candidats:"
# print probaCandidats
# print "\n\n"
print "Resultats de l'election"
print results

# ------------------------------
# graph

abs_res = range(0,3*Ncandidats,3)
abs_prob = range(1,3*Ncandidats,3)
width = 0.99
#plt.bar(abs_res, results[:,0], width, color=couleurs[0], label=nameMentions[0])
for i in range(Nmentions):
    plt.bar(abs_res, results[:,i], width,color=couleurs[i],  label=nameMentions[i], bottom=np.sum(results[:,:i],axis=1), edgecolor='white')
    plt.bar(abs_prob, probaCandidats[:,i], width,color=couleurs[i], bottom=np.sum(probaCandidats[:,:i],axis=1), edgecolor='white')

plt.ylabel('Mentions')
plt.title('Jugement majoritaire avec %i candidats et %i electeurs' % (Ncandidats, Nelecteurs))
#plt.xticks(ind + width/2., ('C1', 'G2', 'G3', 'G4', 'G5'))
plt.yticks(np.arange(0, 1, 0.1))
plt.legend()

plt.show()

