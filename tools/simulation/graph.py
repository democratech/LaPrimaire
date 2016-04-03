# graph: confiance = f( N electeurs )

import re
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import argparse
#import mj

Ntests    = 20
Nmentions = 7
root      = "data"

def readData(Ncandidats, Nelecteurs, essai):
    folder = root  + "/C_%i.E_%i_%i/" % (Ncandidats, Nelecteurs, essai)
    fname = folder + "log.txt"
    f = open(fname, "r")
    p = re.compile(ur'5 premiers: ([0-9]+),')
    a = []
    for l in f.readlines():
        a = re.findall(p, l)
        if a != []:
            break
    if a == []:
        print "Unreadable data for C_%i.E_%i_%i" % (Ncandidats, Nelecteurs, essai)
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
    
def plotCandidates(Ncandidats, Nelecteurs, essai):
    """ plot distribution of the candidates"""
    folder = root  + "/C_%i.E_%i_%i/" % (Ncandidats, Nelecteurs, essai)
    fname = folder + "terranova." + str(Ncandidats) + ".txt"
    p = np.genfromtxt(fname, delimiter = ",", dtype=float)
    nameMentions = ["Excellent", "Tres bien", "Bien", "Assez bien", "Passable", "Insuffisant", "A rejeter"]
    couleurs = ["DarkRed", "Crimson","Tomato","DarkOrange","Yellow","Khaki","DarkKhaki"]
    abs_prob = range(0,Ncandidats)
    width = 0.98
    #plt.bar(abs_res, results[:,0], width, color=couleurs[0], label=nameMentions[0])
    for i in range(Nmentions):
        plt.bar(abs_prob, p[:,i], width,color=couleurs[i], label=nameMentions[i], bottom=np.sum(p[:,:i],axis=1), edgecolor='white')
    plt.ylabel('Mentions')
    plt.xlabel('Candidats')
    plt.title('Jugement majoritaire avec %i candidats et %i electeurs' % (Ncandidats, Nelecteurs))
    plt.yticks(np.arange(0, 1, 0.1))
    plt.xticks(np.arange(0, Ncandidats))
    plt.legend()
    for i in range(Nmentions):
        plt.figure()
        plt.bar(abs_prob, np.sort(p[:,i]), width,color=couleurs[i], edgecolor='white')
        plt.ylabel(nameMentions[i])
        plt.xlabel('Candidats')
        plt.yticks(np.arange(0, 1, 0.1))
        plt.xticks(np.arange(0, Ncandidats))
    plt.show()
   
def plotMinElecteurs(threshold, candidats, electeurs):
    fig = plt.figure()
    tes = threshold >= 0
    idx = threshold[tes]
    plt.plot(candidats[tes], electeurs[idx], "b+")
    plt.xlabel("Nombre de candidats")
    plt.ylabel("Nombre min d'electeurs")
    plt.show()


 
def  computeStdToZero(Nc, electeurs):
    Ne        = len(electeurs)
    res       = np.zeros(Ne)
    for i in range(Ne):
        e = electeurs[i]
        acc = 0.0
        for t in range(Ntests):
            acc += float(readData(Nc,e,t))
        res[i] = sqrt(acc/(Ntests))       
    return res
    
def computeAllStd(candidats, electeurs):
    Ne        = len(electeurs)
    Nc        = len(candidats)
    res       = np.zeros((Nc,Ne))
    for j in range(Nc):
        c = candidats[j]
        res[j,:] = computeStdToZero(c, electeurs)
        #plotStd(res[j])
    #print res
    np.savetxt("std_err.txt", res, delimiter = ",")   
    
    # compute min Nelecteurs for each Ncandidats
    threshold = np.zeros(Nc, dtype=int)
    for i in range(Nc):
        c = candidats[i]      
        w = np.where(res[i] < 1)[0]
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
        #global root, Nmentions
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--nv',  type=int, help='Number of voters', default=120000)
        parser.add_argument('--rv',  action='store_false', help='Range for voters')
        parser.add_argument('--nc',  type=int, help='Number of candidates', default=180)
        parser.add_argument('--rc',  action='store_false', help='Range for candidates')
        parser.add_argument('--ng',  type=int, help='Number of grades', default=Nmentions)
        parser.add_argument('--root',  type=str, help='Root for paths', default=root)
        parser.add_argument('--priori', action='store_true', help='Plot a priori distribution')
        parser.add_argument('--std', type=int, help='Return std for a certain number of candidate', default=0)
        args = parser.parse_args()
        
        Ncandidats = args.nc
        Nelecteurs = args.nv
        Nmentions = args.ng
        root = args.root
        std = args.std
        
        electeurs = np.arange(50000,Nelecteurs,20000) if args.rv else np.array([Nelecteurs])
        candidats = np.arange(20,Ncandidats,20) if args.rc else np.array([Ncandidats])
            
        if args.priori:
            essai = 0
            plotCandidates(Ncandidats, Nelecteurs, essai)
        elif std:
            print computeStdToZero(std, electeurs)
        else:
            threshold = computeAllStd(candidats, electeurs)
            plotMinElecteurs(threshold, candidats, electeurs)
