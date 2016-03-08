# lance simulations pour different nombre d'electeurs
import multiprocessing
import mj
import os, sys
import shutil
import time

def worker(Ncandidats,Nelecteurs, Nlot, Nmentions, root, output, id):
    """worker function"""
    mj.simulation(Ncandidats,Nelecteurs, Nlot, Nmentions, root,output,id)
    output.close()
    return

if __name__ == '__main__':
    print "Cette fois, c'est la bonne !"
    print (time.strftime("%H:%M:%S"))
    pool       = multiprocessing.Pool()
    jobs       = []
    Nelecteurs = range(10000,110000,10000)
    Ncandidats = range(20,220,20)
    Nlot       = 10
    Nmentions  = 7
    Ntest      = 5 # chaque Nelecteurs est teste Ntest fois
    data       = "terranova.txt"
    for i in range(len(Ncandidats)):
        for j in range(len( Nelecteurs)):
            for t in range(Ntest):
                c = Ncandidats[i]
                e = Nelecteurs[j]
                root = "C_%i.E_%i_%i/" % (c,e,t)
                shutil.rmtree(root, True)
                os.mkdir(root)
                shutil.copy(data, root)
                f = open(root + "log.txt", "w")
                id = (i+1)*(j+1)*(t+1)
                #p    = pool.apply_async(worker, args=(c,e,Nlot,Nmentions,root,f,))
                p    = multiprocessing.Process(target=worker, args=(c,e,Nlot,Nmentions,root,f,id,))
                jobs.append(p)
                p.start()
    print "Alors, ca marche ? :)"
        


