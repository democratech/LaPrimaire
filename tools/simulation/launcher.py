# lance simulations pour different nombre d'electeurs
import multiprocessing
import mj
import os, sys
import shutil
import time
import numpy as np

def worker((Ncandidats,Nelecteurs, Nlot, Nmentions, root, output, id)):
    """worker function"""
    sys.stdout.write('\nSTART -- %i candidats, %i electeurs, %i ID, %i PID -- \n' %  \
                    (Ncandidats, Nelecteurs, id, os.getpid()))
    sys.stdout.flush()
    time.sleep(0.01) # being sure that simulation are differently initialized
    o = open(output, "w")
    mj.simulation(Ncandidats,Nelecteurs, Nlot, Nmentions, root,o,id)
    o.close()
    sys.stdout.write('\nDONE -- %i candidats, %i electeurs, %i PID -- \n' %  \
                    (Ncandidats, Nelecteurs, os.getpid()))
    sys.stdout.flush()
    return

if __name__ == '__main__':
    print "Cette fois, c'est la bonne !"
    print (time.strftime("%H:%M:%S"))
    
    #jobs       = []
    Nelecteurs = range(10000,100000,10000)
    Ncandidats = range(20,200,10)
    Nlot       = 10
    Nmentions  = 7
    Ntest      = 5 # chaque Nelecteurs est teste Ntest fois
    Nworkers   = Ntest*len(Nelecteurs)*len(Ncandidats)
    data       = "terranova.txt"
    args       = []
    for i in range(len(Ncandidats)):
        for j in range(len( Nelecteurs)):
            for t in range(Ntest):
                
                c = Ncandidats[i]
                e = Nelecteurs[j]
                root = "C_%i.E_%i_%i/" % (c,e,t)
                shutil.rmtree(root, True)
                os.mkdir(root)
                shutil.copy(data, root)
                f = root + "log.txt"
                id = (i+1)*(j+1)*(t+1)
                arg = [c,e,Nlot,Nmentions,root,f,id]
                args.append(arg)

                #p    = pool.apply_async(worker, args=(c,e,Nlot,Nmentions,root,f,))
                # p    = multiprocessing.Process(target=worker, args=)
                # jobs.append(p)
                # p.start()
    
    pool       = multiprocessing.Pool()
    pool.map(worker, args)
                
    print "Alors, ca marche ? :)"
        


