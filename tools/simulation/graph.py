# graph: confiance = f( N electeurs )

import re
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import argparse
import os,sys
import mj

Nmentions = 7


def getFolderName(c, e, t, root = "data"):
	return "%s/C_%i.E_%i_%i/" % (root, c, e, t)

def readData(Ncandidats, Nelecteurs, test, root = "data"):
    folder = getFolderName(Ncandidats, Nelecteurs, test)
    fname = folder + "log.txt"
    if not os.path.isfile(fname + "log.txt"):
         mj.computeLog(Ncandidats, Nelecteurs, test, root)

    f = open(fname, "r")
    p = re.compile(ur'5 premiers: ([0-9]+),')
    a = []
    for l in f.readlines():
        a = re.findall(p, l)
        if a != []:
            break
    if a == []:
        print "Unreadable data for C_%i.E_%i_%i" % (Ncandidats, Nelecteurs, test)
    return a[0]

# ------------------------------
# graph

def plotBar(Ncandidats,Nelecteurs, Nmentions, results, proba):
    import matplotlib.pyplot as plt
    nameMentions = ["Excellent", "Tres bien", "Bien", "Assez bien", "Passable", "Insuffisant", "A rejeter"]
    couleurs = ["DarkRed", "Crimson","Tomato","DarkOrange","Yellow","Khaki","DarkKhaki"]
    abs_res = range(0,Ncandidats)
    abs_prob = np.arange(0,Ncandidats) + 0.46
    width = 0.45
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

def plotStd(res):
    w = np.where(res == 0)[0]
    fig = plt.figure()
    ax = plt.axes()
    if w.size != 0:
        threshold = w[0]
        ax.axvline(threshold, linestyle='--', color='b',label="Nombre minimal d'electeurs")
    plt.plot(electeurs, res, color="b")
    plt.plot(electeurs, res, color="b-")
    plt.xlabel("Nombre d'electeurs")
    plt.ylabel("Confiance")
    plt.show()  
    
def plotCandidates(Ncandidats, Nelecteurs, test):
    """ plot distribution of the candidates"""
    folder = root  + "/C_%i.E_%i_%i/" % (Ncandidats, Nelecteurs, test)
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
    plt.plot(candidats[tes], electeurs[idx], "b-")
    plt.xlabel("Nombre de candidats")
    plt.ylabel("Nombre min d'electeurs")
    plt.show()



 
def  computeStdToZero(Nc, electeurs,tests):
    Ne        = len(electeurs)
    res       = np.zeros(Ne)
    for i in range(Ne):
        e = electeurs[i]
        acc = 0.0
        for t in tests:
            acc += float(readData(Nc,e,t))
        res[i] = sqrt(acc/(len(tests)))       
    return res
    
def computeAllStd(candidats, electeurs, tests, root = "data"):
    Ne        = len(electeurs)
    Nc        = len(candidats)
    res       = np.zeros((Nc,Ne))
    for j in range(Nc):
        c = candidats[j]
        res[j,:] = computeStdToZero(c, electeurs, tests)
        #plotStd(res[j])
    #print res
    np.savetxt(root + "std_err.txt", res, delimiter = ",")   
    
    # compute min Nelecteurs for each Ncandidats
    threshold = np.zeros(Nc, dtype=int)
    for i in range(Nc):
        c = candidats[i]      
        w = np.where(res[i] < 0.5)[0]
        if w.size != 0:
            threshold[i] = w[0]
        else:
            threshold[i] = -1
    #print threshold
    np.savetxt(root + "threshold.txt", res, delimiter = ",")   
    
    return threshold

# ------------------------------
# main 
    
if __name__ == '__main__':
        #global root, Nmentions
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--nv',  type=int, help='Number of voters', default=105000)
        parser.add_argument('--rv',  action='store_false', help='Range for voters')
        parser.add_argument('--nc',  type=int, help='Number of candidates', default=100)
        parser.add_argument('--nt',  type=int, help='Number of tests', default=5)
        parser.add_argument('--rc',  action='store_false', help='Range for candidates')
        parser.add_argument('--ng',  type=int, help='Number of grades', default=Nmentions)
        parser.add_argument('--root',  type=str, help='Root for paths', default="root")
        parser.add_argument('--priori', action='store_true', help='Plot a priori distribution')
        parser.add_argument('--std', type=int, help='Return std for a certain number of candidate', default=0)
        args = parser.parse_args()
        
        Ncandidats = args.nc
        Nelecteurs = args.nv
        Nmentions = args.ng
        root = args.root
        std = args.std
        tests     = np.arange(args.nt)
	electeurs = np.arange(50000,Nelecteurs,5000) if args.rv else np.array([Nelecteurs])
        candidats = np.arange(60,Ncandidats,10) if args.rc else np.array([Ncandidats])
            
        if args.priori:
            test = 0
            plotCandidates(Ncandidats, Nelecteurs, test)
        elif std:
            print computeStdToZero(std, electeurs)
        else:
            threshold = computeAllStd(candidats, electeurs, tests)
            plotMinElecteurs(threshold, candidats, electeurs)
