import numpy as np
import random


class MAC_network:
    def __init__(self):
        self.T = 0
        self.N = 0
        self.Nsims = 0
        self.Samples = 0
        self.probs = np.linspace(0, 1, self.Samples)

    def computeSimRes(self):
        nodes = np.zeros(self.N)
        slots = np.zeros(self.T)
        simRes = np.zeros((self.Nsims, self.probs.shape[0]))
        for j in range(simRes.shape[0]):
            for i in range(simRes.shape[1]):
                p = self.probs[i]
                for t in range(self.T):
                    for n in range(self.N):
                        r = random.uniform(0, 1)
                        nodes[n] = 1 if r <= p else 0
                    slots[t] = 1 if np.sum(nodes) == 1 else 0
                simRes[j][i] = np.sum(slots)
        meanS = np.mean(simRes, axis=0)
        return meanS

    def computeThrRes(self):
        s = np.zeros(self.probs.shape)
        for i in range(self.Samples):
            p = self.probs[i]
            s[i] = self.N*p*(1-p)**(self.N-1)
        return s
