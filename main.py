import numpy as np
import random
import matplotlib.pyplot as plt
import sys
import time


def computeSimRes(Nsims, probs, T, N):
    nodes = np.zeros(N)
    slots = np.zeros(T)
    simRes = np.zeros((Nsims, probs.shape[0]))
    for j in range(simRes.shape[0]):
        for i in range(simRes.shape[1]):
            p = probs[i]
            for t in range(T):
                for n in range(N):
                    r = random.uniform(0, 1)
                    nodes[n] = 1 if r <= p else 0
                slots[t] = 1 if np.sum(nodes) == 1 else 0
            simRes[j][i] = np.sum(slots)
    meanS = np.mean(simRes, axis=0)
    return meanS


def computeThrRes(Samples, probs, N):
    s = np.zeros(probs.shape)
    for i in range(Samples):
        p = probs[i]
        s[i] = N*p*(1-p)**(N-1)
    return s


def plotRes(probs, meanS, s, Nsims):
    plt.close("all")
    print(f"Simulation result for {Nsims} simulations")
    plt.plot(probs, meanS,
             label=f"Result for {Nsims} simulations")
    plt.plot(probs, s, label='Theoretical (True) result')
    plt.title('p Vs. Proportion of successful transmission slots')
    plt.xlabel('Success probability for one node (p)')
    plt.ylabel('Proportion of successful transmission slots')
    plt.legend()
    plt.show(block=False)


def main():
    print("#################################################################################")
    print("################### Project 1: Simple MAC protocol simulation ###################")
    print("#################################################################################")
    cmmd = 'y'
    while(cmmd == 'y'):
        T = int(input("Enter number of time slots: "))
        N = int(input("Enter number of nodes: "))
        Nsims = int(input('Enter number of simulations to run: '))
        Samples = int(input("Enter number of samples to plot: "))

        probs = np.linspace(0, 1, Samples)
        # Theoretical result
        s = computeThrRes(Samples, probs, N)
        # Simulation result
        print("Running simulation...")
        start_time = time.time()
        meanS = computeSimRes(Nsims, probs, T, N)
        print("Simulation done in %.2f seconds." % (time.time()-start_time))

        plotRes(probs, meanS/T, s, Nsims)
        cmmd = input("Run another simulation? (y or n): ")


if __name__ == "__main__":
    # execute only if run as a script
    main()
