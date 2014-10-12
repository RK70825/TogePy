import time
import random
import heapq

def tls(t_max):
    def tls_alg(cutoff):
        r = 1
        if time.time() > cutoff:
            return r
        else:
            time.sleep(0.001)
            return r + tls_alg(cutoff)
        
    return tls_alg(time.time() + t_max)