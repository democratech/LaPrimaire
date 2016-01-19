# Pierre-Louis pierre-louis.guhur@laposte.net
# created on 1.12.16
# simulate a vote in which all voters have access only to a certain number of candidates.

import random
import numpy as np
from math import *
from scipy.stats import rv_discrete
import matplotlib.pyplot as plt


random.seed()

def GetCandidates(n):
    """ return a np.array for n different candidates"""
    cdt = np.arange(Ncandidates)
    random.shuffle(cdt)
    return cdt[:n]
    
def ProbaCandidate():
    """ associate to candidate(i) a proba to receive a vote"""
    #res = [float(Ncandidates-i)/float(Ncandidates) for i in range(Ncandidates)] # triangular
    sigma = 30.0
    res = [exp(-float(i)**2/(2*sigma**2))/(sqrt(2*pi)*sigma) for i in range(Ncandidates)]
    return np.array(res)   
   
def FastVote(k):  
    res = np.zeros(Ncandidates)
    for i in range(Nvoters):
       #select Ncpv candidates:
       candidates = GetCandidates(k)

       # vote for a candidate
       distrib = rv_discrete(values=(candidates, proba[candidates]))
       candidate = distrib.rvs() # draw a candidate following distribution of ResRegVote
       res[candidate] += 1 
    return res
    
def GetError(rk,N):
    idx = np.where(rk[:N] > N)[0]
    err = len(idx)
    return err
    
    
Ncandidates = 100
Nfinal = 10 #number of remaining candidates
Nvoters = 1000
Ncpv = 10#range(1,50) # Number of candidates per voters
Nsimu = 100 # Number of simulations

res = np.zeros(Ncpv)
for k in [Ncpv]:#range(Ncpv):
    print "Ncpv: %d" % k
    err = np.zeros(Nsimu)
    for j in range(Nsimu):
        proba = ProbaCandidate() 

        # fast vote
        ResFastVote = FastVote(k)
        RankFastVote = np.argsort(ResFastVote) 
        
        # compute err of this vote
        err[j] = GetError(RankFastVote[-Nfinal:], Nfinal)
        print "error: " + str(err[j])
    res[k] = sum(err)/Nsimu
    #print "mean error: %d" % res[k]

# display results
plt.plot(range(Ncpv), res)
plt.show()