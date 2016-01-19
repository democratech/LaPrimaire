# Pierre-Louis pierre-louis.guhur@laposte.net
# created on 1.12.16
# simulate a vote in which all voters have access only to a certain number of candidates.

import random
import sys
import numpy as np
from math import *
from scipy.stats import rv_discrete
from timeit import default_timer as timer
#import matplotlib.pyplot as plt

start = timer()
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
    sys.stdout.write("[")
    len_bin = round(float(Nvoters)/50.0)
    for i in range(Nvoters):
       #select Ncpv candidates:
       candidates = GetCandidates(k)

       # vote for a candidate
       distrib = rv_discrete(values=(candidates, proba[candidates]))
       candidate = distrib.rvs() # draw a candidate following distribution of ResRegVote
       res[candidate] += 1 
       if i % len_bin == 0:
           sys.stdout.write("=")
    sys.stdout.write("]\n")
    return res
    
def GetError(rk,N):
    idx = np.where(rk[:N] > N)[0]
    err = len(idx)
    return err
    
    
Ncandidates = 100
Nfinal = 10 #number of remaining candidates
Nvoters = 100000   
Ncpv = 10#range(1,50) # Number of candidates per voters
Nsimu = 1000 # Number of simulations

res = np.zeros(Ncpv)
err = np.zeros(Nsimu)
for j in range(Nsimu):
    sys.stdout.write( "\n\nSimulation %d/%d [%d %%]\n" % (j,Nsimu, float(j)/float(Nsimu-1)*100 ))

    proba = ProbaCandidate() 

    # fast vote
    ResFastVote = FastVote(Ncpv)
    RankFastVote = np.argsort(ResFastVote) 
    
    # compute err of this vote
    err[j] = GetError(RankFastVote[-Nfinal:], Nfinal)
    sys.stdout.write("error: %d " % err[j])
    if j > 0:
        sys.stdout.write(" - mean %f - std %f" % (np.mean(err[:j]),np.std(err[:j]) ))
   
sys.stdout.write("\n\n\n\n\nEnd of the simulation :) ")
sys.stdout.write("\nIt took %d s... You should have used GPU instead of me!\n" % (timer()-start)) 
    