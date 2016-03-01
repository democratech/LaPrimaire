# simulation pour le jugement majoritaire

import numpy as np
from scipy.stats import rv_discrete
from math import *
import random
import os,sys

Ncandidats = 100
Nelecteurs = 10000
Nlot = 10
Nmentions = 7
random.WichmannHill(random.seed())
list_results="terranova.txt"
list_interpolated="terranova." + str(Ncandidats) + ".txt"


def probaCandidates(N, inFile, outFile):
    """Read inFile. If there is not enough candidates, interpolate other. Save in outFile """    
    inCandidates = np.genfromtxt(inFile, delimiter = ",", dtype=int)
    Nc = len(inCandidates)
    if Nc > N:
        random.shuffle(inCandidates)
        outCandidates = inCandidates[:N]
    else:
        inc = trunc(float(N-Nc)/Nmentions)
        outCandidates = np.zeros(N)
        outCandidates[:Nc] = inCandidates
        for i in range(Nc, Nc + Nmentions*inc):
            outCandidates[i] = i % Nmentions
        meamMention = round(np.mean(inCandidates))
        for i in range(Nc + Nmentions*inc, N):
            outCandidates[i] = meamMention
    np.savetxt(outFile, outCandidates, delimiter = ",")
    
    
def loadProba(file):
    p = np.genfromtxt(file, delimiter = ",", dtype=float)
    s = sum(p)
    p /= s
    return p
    
    
def subset(Ncandidat, Nlot, occurences):
    proba_candidat = np.array([1/float(j) if j != 0 else 1 for j in occurences])
    proba_candidat = proba_candidat / float(sum(proba_candidat))
    lot = np.random.choice(Ncandidats, size=Nlot, replace=False, p=proba_candidat)
    occurences[lot] += 1
    return lot
    
def vote(lot, proba):    
    distrib = rv_discrete(values=(range(Nmentions), proba))
    votes = distrib.rvs(size=len(lot))
    return votes
    

    
# initialisation :
probaCandidates(Ncandidats,list_results, list_interpolated)
probaCandidats  = loadProba(list_interpolated)
occurence       = np.zeros(Ncandidats)
results         = np.zeros((Ncandidats,6))
lBin            = round(Nelecteurs/10.0)

for i in range(Nelecteurs):
    if(i % lBin == 0):
        print "%d / 10" % round(float(i)/float(lBin))
    lot     = subset(Ncandidats, Nlot, occurence)
    votes   = vote(lot, probaCandidats[lot])
    for i in lot:
        results[i,votes[i]] += 1
        
print "Probabilites des candidats:"
print probaCandidats
print "\n\n"
print "Resultats de l'election"
print results
    
    
