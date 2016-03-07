# lance simulations pour different nombre d'electeurs
import multiprocessing
import mj
import os, sys
import shutil

def worker(Ncandidats,Nelecteurs, Nlot, Nmentions, root, output):
    """worker function"""
    mj.simulation(Ncandidats,Nelecteurs, Nlot, Nmentions, root,output)
    output.close()
    return

if __name__ == '__main__':
    jobs       = []
    Nelecteurs = range(10000,110000,10000)
    Ncandidats = range(20,220,20)
    Nlot       = 10
    Nmentions  = 7
    Ntest      = 5 # chaque Nelecteurs est teste Ntest fois
    data       = "terranova.txt"
    for c in Ncandidats:
        for e in Nelecteurs:
            for t in range(Ntest):
                root = "C_%i.E_%i_%i/" % (c,e,t)
                shutil.rmtree(root, True)
                os.mkdir(root)
                shutil.copy(data, root)
                f = open(root + "log.txt", "w")
                p    = multiprocessing.Process(target=worker, args=(c,e,Nlot,7,root,f,))
                jobs.append(p)
                p.start()
                
        


