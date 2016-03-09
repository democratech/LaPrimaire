# graph: confiance = f( N electeurs )

import re
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

electeurs = np.arange(10000,100000,10000)
candidats = np.arange(20,200,10)
Ntests    = 5 
Ne        = len(electeurs)
Nc        = len(candidats)

def readData(Ncandidats, Nelecteurs, essai):
    folder = "data/C_%i.E_%i_%i/" % (Ncandidats, Nelecteurs, essai)
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
    
    
# compute std to zero
res = np.zeros((Nc,Ne))

for j in range(Nc):
    c = candidats[j]
    for i in range(Ne):
        e = electeurs[i]
        acc = 0.0
        for t in range(Ntests):
            acc += float(readData(c,e,t))
            print readData(c,e,t)
        res[j,i] = sqrt(acc/(Ntests))       
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
print threshold
np.savetxt("threshold.txt", res, delimiter = ",")   


#plot
fig = plt.figure()
tes = threshold >= 0
idx = threshold[tes]
plt.plot(candidats[tes], electeurs[idx], "b+")
plt.xlabel("Nombre de candidats")
plt.ylabel("Nombre min d'electeurs")
plt.show()
        
