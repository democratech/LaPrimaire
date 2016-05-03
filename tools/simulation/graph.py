# graph: confiance = f( N electeurs )

import re
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import argparse
import os,sys
import mj

Nmentions = 7



def readData(Ncandidats, Nelecteurs, test, root = "data", relog = False):
    folder = mj.getFolderName(Ncandidats, Nelecteurs, test)
    fname = folder + "log.txt"
    if not os.path.isfile(fname + "log.txt") or relog:
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

def plotBar(Ncandidats,Nelecteurs, test, Nmentions, root="data"):
    import matplotlib.pyplot as plt
    fname = mj.getFolderName(Ncandidats, Nelecteurs, test, root)
    raw_post   = np.genfromtxt(fname + "raw.results.%i.%i.txt" % (Ncandidats, Nelecteurs), dtype=float, delimiter=",").astype(float)
    n_priori = np.genfromtxt(fname + "terranova.%i.txt" % Ncandidats, dtype=float, delimiter=",").astype(float)
    n_post     = mj.normalize(raw_post)
    nameMentions = ["Excellent", "Tres bien", "Bien", "Assez bien", "Passable", "Insuffisant", "A rejeter"]
    couleurs = ["DarkRed", "Crimson","Tomato","DarkOrange","Yellow","Khaki","DarkKhaki"]
    abs_res = range(0,Ncandidats)
    abs_prob = np.arange(0,Ncandidats) + 0.46
    width = 0.45
    #plt.bar(abs_res, results[:,0], width, color=couleurs[0], label=nameMentions[0])
    for i in range(Nmentions):
	plt.bar(abs_res, n_post[:,i], width,color=couleurs[i],  label=nameMentions[i], bottom=np.sum(n_post[:,:i],axis=1), edgecolor='white')
	plt.bar(abs_prob, n_priori[:,i], width,color=couleurs[i], bottom=np.sum(n_priori[:,:i],axis=1), edgecolor='white')

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
    print electeurs[idx]
    print candidats[tes]
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
        w = np.where(res[i] < 0.25)[0]
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
        parser.add_argument('--ng',  type=int, help='Number of grades', default=Nmentions)
        parser.add_argument('--ne',  type=int, help='Number of electors', default=0)
        parser.add_argument('--nc',  type=int, help='Number of candidates', default=0)
        parser.add_argument('--root',  type=str, help='Root for paths', default="root")
        parser.add_argument('--priori', action='store_true', help='Plot a priori distribution')
        parser.add_argument('--bar', action='store_true', help='Plot bars')
        parser.add_argument('--relog', action='store_true')
	parser.add_argument('--std', type=int, help='Return std for a certain number of candidate', default=0)
        args = parser.parse_args()
        
        Nmentions = args.ng
        root = args.root
        std = args.std
	relog = args.relog
	
	electeurs = set()
	candidats = set()
	tests     = set()
	samples = os.listdir("data")
	for s in samples:
	    m = re.findall('C_(\d+).E_(\d+)_(\d+)', s)[0]
	    electeurs |= set([int(m[1])])
	    candidats |= set([int(m[0])])
	    tests     |= set([int(m[2])])
        electeurs = np.sort(list(electeurs))
	candidats = np.sort(list(candidats))
	tests     = np.sort(list(tests))
	print candidats
	print electeurs
       
        Nelecteurs = args.ne if args.ne else max(electeurs)
        Ncandidats = args.nc if args.nc else max(candidats)

	if args.priori:
            test = 0
            plotCandidates(Ncandidats, Nelecteurs, test)
        if args.bar:
            test = 0
            plotBar(Ncandidats, Nelecteurs, test, Nmentions)
        elif std:
            print computeStdToZero(std, electeurs)
        else:
            threshold = computeAllStd(candidats, electeurs, tests)
            print threshold
	    plotMinElecteurs(threshold, candidats, electeurs)
