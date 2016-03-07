#### test si la distribution des lots permet :
# a. que chaque candidat recoive le meme nombre de votes
# b. que chaque candidat rencontre autant de fois chaque personne

import numpy as np


#### parametres
Ncandidats = 100
Nelecteurs = 100000
Ncpl = 10 # Ncandidats / lots


####
Noccurence = np.zeros(Ncandidats)
meeting = np.zeros((Ncandidats,Ncandidats))
lBin = round(Nelecteurs/10.0)
for i in range(Nelecteurs):
     if(i % lBin == 0):
         print "%d / 10" % round(float(i)/float(lBin))
     proba_candidat = np.array([1/float(j) if j != 0 else 1 for j in Noccurence])
     proba_candidat = proba_candidat / float(sum(proba_candidat))
     lot = np.random.choice(Ncandidats, size=Ncpl, replace=False, p=proba_candidat)
     Noccurence[lot] += 1
     for i in lot:
         meeting[i,lot] += 1
     

stat_meet = []
for i in range(1,Ncandidats):
    for j in range(0, i):
        if j != i:
            stat_meet.append(meeting[i,j])

stat_meet = np.array(stat_meet)

#### resultats

print "Simulation avec %d candidats et %d electeurs." % (Ncandidats, Nelecteurs)
print "Moyenne %e, ecart type %f et std/mean %f (%%) du nombre d'occurences de chaque candidat" % (np.mean(Noccurence), np.std(Noccurence),np.std(Noccurence)/ np.mean(Noccurence)*100) 
print "Moyenne %e, ecart type %f et std/mean %f (%%) du nombre de rencontres entre chaque candidat" % (np.mean(stat_meet), np.std(stat_meet),np.std(stat_meet)/ np.mean(stat_meet)*100)      
# print meeting
# print stat_meet
# print Noccurence