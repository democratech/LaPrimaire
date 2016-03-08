# graph: confiance = f( N electeurs )

import re
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

Ncandidats = 20
electeurs = [1000]#range(10000,110000,20000)
Ntests = 5 


def readData(Ncandidats, Nelecteurs, essai):
    folder = "C_%i.E_%i_%i/" % (Ncandidats, Nelecteurs, essai)
    fname = folder + "log.txt"
    f = open(fname, "r")
    p = re.compile(ur'5 premiers: ([0-9]+),')
    for l in f.readlines():
        a = re.findall(p, l)
        if a != []:
            break
    return a[0]

res = np.zeros(len(electeurs))
for i in range(len(electeurs)):
    acc = 0.0
    e = electeurs[i]
    for t in range(Ntests):
        acc += float(readData(Ncandidats,e,t))
    res[i] = sqrt(acc/(Ntests))
w = np.where(res == 0)[0]
print res




#plot
fig = plt.figure()
ax = plt.axes()
if w.size != 0:
    threshold = w[0]
    ax.axvline(threshold, linestyle='--', color='b',label="Nombre minimal d'electeurs")
plt.plot(electeurs, res, color="b")
plt.xlabel("Nombre d'electeurs")
plt.ylabel("Confiance")
plt.show()
        
