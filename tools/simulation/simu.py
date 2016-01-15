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
    
def RegVote():
    """ vector dim Ncandidates with int random values between 0 and Nvoters"""
    res = np.zeros(Ncandidates)
    
    for i in range(Nvoters):
        vote = random.randint(0,Ncandidates-1)
        res[vote] += 1
    return res
   
def FastVote(k):  
    res = np.zeros(Ncandidates)
    for i in range(Nvoters):
       #select Ncpv candidates:
       candidates = GetCandidates(k)

       # vote for a candidate
       distrib = rv_discrete(values=(candidates, ResRegVote[candidates]/Nvoters))
       candidate = distrib.rvs() # draw a candidate following distribution of ResRegVote
       res[candidate] += 1 
    return res
    
def GetError(rk1,rk2,N):
    err = 0
    for i in range(N):
        idx = np.where(rk2 == rk1[i])[0][0]
        err += 1 if idx > N else 0
    return err
    
    
Ncandidates = 100
Nfinal = 10 #number of kept candidates
Nvoters = 100000
Ncpv = 10#range(1,50) # Number of candidates per voters
Nsimu = 10 # Number of simulations

res = np.zeros(Ncpv)
for k in [Ncpv]:#range(Ncpv):
    print "Ncpv: %d" % k
    err = np.zeros(Nsimu)
    for j in range(Nsimu):
        # regular vote
        #print "regular vote"
        ResRegVote = RegVote() 
        RankRegVote = np.argsort(ResRegVote)#sort Ncandidates by decreasing number of votes
        print RankRegVote[:Nfinal]
        
        # fast vote
        #print "fast vote"
        ResFastVote = FastVote(k)
        RankFastVote = np.argsort(ResFastVote)
        print RankFastVote[:Nfinal]
        
        # compare votes
        err[j] = GetError(RankRegVote, RankFastVote, Nfinal)
        print err[j]
    res[k] = sum(err)/Nsimu
    #print "mean error: %d" % res[k]

# display results
plt.plot(range(Ncpv), res)
plt.show()