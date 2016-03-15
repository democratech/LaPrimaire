# simulation pour le jugement majoritaire

import numpy as np
from scipy.stats import rv_discrete
from math import *
import random
import os,sys
import argparse







def normalize(v, ax=1):
     n = np.sum(v, axis=ax)
     b = np.transpose(v)
     c = np.divide(b,n)
     return np.transpose(c)

def probaCandidates(N, inFile, outFile):
    """Read inFile. If there is not enough candidates, interpolate other. Save in outFile """    
    inCandidates = np.genfromtxt(inFile, delimiter = " ", dtype=float)
    inCandidates = inCandidates[:,:7]
    Nc = len(inCandidates)
    param = np.zeros((7,2))
    param[:,0] = np.mean(inCandidates, axis=0)
    param[:,1] = np.std(inCandidates, axis=0)
    if Nc > N:
        random.shuffle(inCandidates)
        outCandidates = inCandidates[:N,:]
    else:
        outCandidates = np.zeros((N,7))
        outCandidates[:Nc,:] = inCandidates
        for i in range(7):
            coeff = np.random.normal(param[i,0], param[i,1], N-Nc)
            outCandidates[Nc:,i] = coeff
            # neg = outCandidates[Nc:,i]<0
#outCandidates[neg,i] =
    p = normalize(np.absolute(outCandidates)) #, norm='l1',axis=1)
    np.savetxt(outFile, p, delimiter = ",")
    
    
def loadProba(file):
    p = np.genfromtxt(file, delimiter = ",", dtype=float)
    return p
    
    
def subset(Ncandidats, Nlot, occurences):
    proba_candidat = np.array([1/float(j) if j != 0 else 1 for j in occurences])
    proba_candidat = proba_candidat / float(sum(proba_candidat))
    lot = np.random.choice(Ncandidats, size=Nlot, replace=False, p=proba_candidat)
    occurences[lot] += 1
    return lot
    
def vote(lot, proba, Nlot): 
    votes = np.zeros(Nlot)
    for i in range(Nlot):  
    	distrib = rv_discrete(values=(range(7), proba[i,:]))
        votes[i] =  distrib.rvs() 
    return votes
    
def argMedian(A):
    s   = np.array([sum(A[:i+1]) for i in range(7)])
    mid = float(s[7-1])/2
    return np.argwhere(mid < s)[0][0]
    
def tieBreaking(A, B):
    Ac = np.copy(A)
    Bc = np.copy(B)
    medA = argMedian(Ac)
    medB = argMedian(Bc)
    while medA == medB:
        Ac[medA] -= 1
        Bc[medB] -= 1
        medA = argMedian(Ac)
        medB = argMedian(Bc)
    return -1 if (medA < medB) else 1
    
def jugementMajoritaire(results):
    return sorted(range(len(results)), cmp=tieBreaking, key=results.__getitem__)


    
# ------------------------------
#  initialisation :

def simulation(Ncandidats,Nelecteurs, Nlot, Nmentions, root, output,id=0):
    list_results= root  + "terranova.txt"
    resName =  "results.%i.%i.txt"  % (Ncandidats, Nelecteurs) 
    list_interpolated= "terranova." + str(Ncandidats) + ".txt"
    
    if not os.path.isfile(resName) or args.reset:
        #sys.stdout.write('\n'*id)
        np.random.seed()
        probaCandidates(Ncandidats, list_results, root  + list_interpolated)
        probaCandidats  = loadProba(root  + list_interpolated)
        raw             = np.zeros((Ncandidats,Nmentions))
        occurence       = np.zeros(Ncandidats)
        lBin            = round(Nelecteurs/100.0)
        for i in range(Nelecteurs):
            if(i % lBin == 0):
                #sys.stdout.write('\r -- %i candidats, %i electeurs, %i PID -- %d / 10' %  \
                #    (Ncandidats, Nelecteurs, os.getpid(), round(float(i)/float(lBin))))
                sys.stdout.write("\r %i %%" % round(float(i)/float(lBin))) 
                sys.stdout.flush()
            lot     = subset(Ncandidats, Nlot, occurence)
            votes   = vote(lot, probaCandidats[lot,:], Nlot)
            for i in range(Nlot):
                raw[lot[i],votes[i]] += 1
        np.savetxt(root  + "raw."+resName, raw, delimiter = ",")
        results = normalize(raw)
        rk = jugementMajoritaire(raw)
        np.savetxt(root  + "rk."+resName, rk, delimiter = ",")
        rk_proba = jugementMajoritaire(np.trunc(probaCandidats*1000))
        np.savetxt(root  + "rk."+list_interpolated, rk_proba, delimiter = ",")
    
    
    
    probaCandidats  = loadProba(root  + list_interpolated)
    raw = np.genfromtxt(root  + "raw." + resName, delimiter = ",", dtype=float)
    rk = np.genfromtxt(root  + "rk." + resName, dtype=float).astype(int)
    rk_proba = np.genfromtxt(root  + "rk." + list_interpolated,  dtype=float).astype(int)
    results = normalize(raw)
    results = results[rk]
    probaCandidats = probaCandidats[rk]
    err5 = np.sum(rk[:5] != rk_proba[:5])
    errT = np.sum(rk != rk_proba)
    
    output.write("Classement a priori\n")
    output.write(str(rk_proba))
    output.write("\nClassement a posteriori\n")
    output.write(str(rk))
    output.write("\nNombres d'erreurs de classement sur les 5 premiers: %i, sur les %i candidats: %i" 
                % (err5, Ncandidats, errT))

    return [results, probaCandidats]
    
    
# ------------------------------
# graph

def graph(Ncandidats,Nelecteurs, Nmentions):
    import matplotlib.pyplot as plt
    abs_res = range(0,Ncandidats)
    abs_prob = np.arange(0,Ncandidats) + 0.46
    width = 0.45
    #plt.bar(abs_res, results[:,0], width, color=couleurs[0], label=nameMentions[0])
    for i in range(Nmentions):
        plt.bar(abs_res, results[:,i], width,color=couleurs[i],  label=nameMentions[i], bottom=np.sum(results[:,:i],axis=1), edgecolor='white')
        plt.bar(abs_prob, probaCandidats[:,i], width,color=couleurs[i], bottom=np.sum(probaCandidats[:,:i],axis=1), edgecolor='white')

    plt.ylabel('Mentions')
    plt.xlabel('Candidats')
    plt.title('Jugement majoritaire avec %i candidats et %i electeurs' % (Ncandidats, Nelecteurs))
    #plt.xticks(ind + width/2., ('C1', 'G2', 'G3', 'G4', 'G5'))
    plt.yticks(np.arange(0, 1, 0.1))
    plt.xticks(np.arange(0, Ncandidats))
    plt.legend()

    plt.show()
   
   
# ------------------------------
# main 
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset',  action='store_true', help='Reset all simulations')
    parser.add_argument('--nv',  type=int, help='Number of voters', default=100000)
    parser.add_argument('--nc',  type=int, help='Number of candidates', default=100)
    parser.add_argument('--ns',  type=int, help='Number of candidates in a subset', default=10)
    parser.add_argument('--ng',  type=int, help='Number of grades', default=7)
    parser.add_argument('--root',  type=str, help='Root for paths', default="")
    args = parser.parse_args()

    Ncandidats = args.nc
    Nelecteurs = args.nv
    Nlot = args.ns
    Nmentions = args.ng
    root = args.root
    nameMentions = ["Excellent", "Tres bien", "Bien", "Assez bien", "Passable", "Insuffisant", "A rejeter"]
    couleurs = ["DarkRed", "Crimson","Tomato","DarkOrange","Yellow","Khaki","DarkKhaki"]

    [results, probaCandidats] = simulation(Ncandidats,Nelecteurs, Nlot, Nmentions, root, sys.stdout)
    graph(Ncandidats,Nelecteurs, Nmentions)
