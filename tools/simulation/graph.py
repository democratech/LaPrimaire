# graph: confiance = f( N electeurs )

import re
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import argparse
#import mj

Ntests    = 6
Nmentions = 7
root      = "data"

def readData(Ncandidats, Nelecteurs, essai):
    folder = root  + "/C_%i.E_%i_%i/" % (Ncandidats, Nelecteurs, essai)
    fname = folder + "log.txt"
    f = open(fname, "r")
    p = re.compile(ur'5 premiers: ([0-9]+),')
    for l in f.readlines():
        a = re.findall(p, l)
        if a != []:
            break
    return a[0]

def plotStd(res):
    w = np.where(res == 0)[0]
    fig = plt.figure()
    ax = plt.axes()
    if w.size != 0:
        threshold = w[0]
        ax.axvline(threshold, linestyle='--', color='b',label="Nombre minimal d'electeurs")
    plt.plot(electeurs, res, color="b")
    plt.xlabel("Nombre d'electeurs")
    plt.ylabel("Confiance")
    plt.show()  
    
def candidates(Ncandidats, Nelecteurs, essai):
    """ plot distribution of the candidates"""
    folder = root  + "/C_%i.E_%i_%i/" % (Ncandidats, Nelecteurs, essai)
    fname = folder + "terranova." + str(Ncandidats) + ".txt"
    p = np.genfromtxt(fname, delimiter = ",", dtype=float)
    nameMentions = ["Excellent", "Tres bien", "Bien", "Assez bien", "Passable", "Insuffisant", "A rejeter"]
    couleurs = ["DarkRed", "Crimson","Tomato","DarkOrange","Yellow","Khaki","DarkKhaki"]
    abs_res = range(0,Ncandidats)
    width = 0.98
    #plt.bar(abs_res, results[:,0], width, color=couleurs[0], label=nameMentions[0])
    for i in range(Nmentions):
        plt.bar(abs_res, results[:,i], width,color=couleurs[i],  label=nameMentions[i], bottom=np.sum(results[:,:i],axis=1), edgecolor='white')
        plt.bar(abs_prob, probaCandidats[:,i], width,color=couleurs[i], bottom=np.sum(proba[:,:i],axis=1), edgecolor='white')

    plt.ylabel('Mentions')
    plt.xlabel('Candidats')
    plt.title('Jugement majoritaire avec %i candidats et %i electeurs' % (Ncandidats, Nelecteurs))
    #plt.xticks(ind + width/2., ('C1', 'G2', 'G3', 'G4', 'G5'))
    plt.yticks(np.arange(0, 1, 0.1))
    plt.xticks(np.arange(0, Ncandidats))
    plt.legend()

    plt.show()
   
def plotMinElecteurs(threshold, candidats, electeurs):
    fig = plt.figure()
    tes = threshold >= 0
    idx = threshold[tes]
    plt.plot(candidats[tes], electeurs[idx], "b+")
    plt.xlabel("Nombre de candidats")
    plt.ylabel("Nombre min d'electeurs")
    plt.show()

 
def  computeStdToZero(electeurs, candidats):
    Ne        = len(electeurs)
    Nc        = len(candidats)
    res       = np.zeros((Nc,Ne))
    for j in range(Nc):
        c = candidats[j]
        for i in range(Ne):
            e = electeurs[i]
            acc = 0.0
            for t in range(Ntests):
                acc += float(readData(c,e,t))
    #            print readData(c,e,t)
            res[j,i] = sqrt(acc/(Ntests))       
        plotStd(res[j])
    #print res
    np.savetxt("std_err.txt", res, delimiter = ",")   


    # compute min Nelecteurs for each Ncandidats
    threshold = np.zeros(Nc, dtype=int)
    for i in range(Nc):
        c = candidats[i]      
        w = np.where(res[i] == 0)[0]
        if w.size != 0:
            threshold[i] = w[0]
        else:
            threshold[i] = -1
    #print threshold
    np.savetxt("threshold.txt", res, delimiter = ",")   
    
    return threshold

# ------------------------------
# main 
    
if __name__ == '__main__':
        global root, Nmentions
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--nv',  type=int, help='Number of voters', default=110000)
        parser.add_argument('--rv',  type=bool, help='Range for voters', default=True)
        parser.add_argument('--nc',  type=int, help='Number of candidates', default=210)
        parser.add_argument('--rc',  type=bool, help='Range for candidates', default=True)
        parser.add_argument('--ng',  type=int, help='Number of grades', default=Nmentions)
        parser.add_argument('--root',  type=str, help='Root for paths', default=root)
        args = parser.parse_args()
        
        Ncandidats = args.nc
        Nelecteurs = args.nv
        Nmentions = args.ng
        root = args.root
        
        electeurs = np.arange(80000,100000,10000) if args.rv else np.array([Nelecteurs])
        candidats = np.arange(20,200,10) if args.rc else np.array([Ncandidats])
            
        
        threshold = computeStdToZero(electeurs, candidats, Ntests)
        plotMinElecteurs(threshold, candidats, electeurs)
