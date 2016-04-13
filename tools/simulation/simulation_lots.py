import numpy as np
import mj
import matplotlib.pyplot as plt
from matplotlib import cm
import sys, os

# ---------------------------------------------------------------------------------------------------
# montrer que l'algorithme de construction des lots est fiable
# 
Ncandidats  = 100
electeurs   = np.arange(10000,100000,10000)
Nlot        = 10
root        = "simulation/lots/"


def simulation(Nelecteurs, Nlot):
    occurence       = np.zeros(Ncandidats)
    corr            = np.zeros((Ncandidats,Ncandidats))
    log_occr        = root + "occr/Nc_%i-Ne_%i-Nl_%i.txt" % (Ncandidats, Nelecteurs, Nlot)
    log_corr        = root + "corr/Nc_%i-Ne_%i-Nl_%i.txt" % (Ncandidats, Nelecteurs, Nlot)
    try:
        os.makedirs(root + "occr")
        os.makedirs(root + "corr")
    except OSError:
        pass
    if os.path.isfile(log_occr) and os.path.isfile(log_corr):
        occurence = np.genfromtxt(log_occr, delimiter=",")
        corr      = np.genfromtxt(log_corr, delimiter=",")
        return [occurence,corr]
        
    for i in range(Nelecteurs):
        lot     = mj.subset(Ncandidats, Nlot, occurence)
        for j in lot:
            corr[j,lot] += 1
    np.savetxt(log_corr, corr, delimiter = ",", fmt="%i")
    np.savetxt(log_occr, occurence, delimiter = ",", fmt="%i")
    return [occurence, corr]
    
def plotOccurences(occurence):
    width = 0.95
    m     = np.mean(occurence)
    plt.bar(range(Ncandidats), occurence, width,color="#3a6d99", edgecolor='white')
    plt.ylabel('Nombre d\'occurence')
    plt.xlabel('Candidats')
    plt.xlim([0,Ncandidats])
    plt.plot([0, Ncandidats], [m,m], color="#d91d1c")
    plt.show()
    
def plotRSMvsCandidats(occurences, electeurs):
    RSM = []
    for occr in occurences:
        m    = np.mean(occr)
        std  = np.std(occr)
        RSM.append(std/m)
    print RSM
    plt.ylabel('Ratio deviation/moyenne')
    plt.xlabel('Nombre d\'electeurs')
    plt.xlim([0,max(electeurs)])
    plt.plot(electeurs, RSM, color="#d91d1c")
    plt.show()
    
def plotCorrelations(corr):
    # mask =  np.tri(corr.shape[0], k=-1)
    # A    =  np.ma.array(corr, mask=mask)
    plt.pcolor(corr)
    plt.colorbar()
    plt.ylabel('Candidats')
    plt.xlabel('Candidats')
    # plt.yticks(np.arange(0.5,10.5),range(0,10))
    # plt.xticks(np.arange(0.5,10.5),range(0,10))
    plt.show()


# ------
# plot 1
#[occr,corr] = simulation(100000, Nlot)
#plotOccurences(occr)

# ------
# plot 2
# occrs = []
# for e in electeurs:
#     [occr,corr] = simulation(e, Nlot)
#     occrs.append(occr)
# plotRSMvsCandidats(occrs, electeurs)
    
# ------
# plot 3
# 
[occr,corr] = simulation(100000, Nlot)
plotCorrelations(corr)