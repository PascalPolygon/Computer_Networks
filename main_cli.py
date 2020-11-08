import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import MAC_module as MAC_module


def plotRes(probs, meanS, s, Nsims):
    plt.close("all")
    print(f"Simulation result for {Nsims} simulations")

    plt.plot(probs, meanS,
             label=f"Result for {Nsims} simulations")
    plt.scatter(probs[np.argmax(meanS)],
                meanS[np.argmax(meanS)], s=100, label=f"Simulation max efficiencty p={probs[np.argmax(meanS)]:.4f}")

    plt.plot(probs, s, label='Theoretical (True) result')
    plt.scatter(probs[np.argmax(s)], s[np.argmax(s)],
                s=100, label=f"Theoretical max efficiency p={probs[np.argmax(s)]:.4f}")

    plt.title('p Vs. Proportion of successful transmission slots')
    plt.xlabel('Success probability for one node (p)')
    plt.ylabel('Proportion of successful transmission slots')
    plt.legend()
    plt.show(block=False)


def main():
    print("############################################################################################")
    print("################### Project 1: Simple MAC protocol efficiency simulation ###################")
    print("############################################################################################")
    MAC = MAC_module.MAC_network()
    cmmd = 'y'
    while(cmmd == 'y'):
        T = int(input("Enter number of time slots: "))
        N = int(input("Enter number of nodes: "))
        Nsims = int(input('Enter number of simulations to run: '))
        Samples = int(input("Enter number of samples to plot: "))

        probs = np.linspace(0, 1, Samples)
        # Theoretical result
        MAC.T = T
        MAC.N = N
        MAC.Nsims = Nsims
        MAC.Samples = Samples
        MAC.probs = np.linspace(0, 1, Samples)

        s = MAC.computeThrRes()

        # Simulation result
        print("Running simulation...")
        start_time = time.time()
        meanS = MAC.computeSimRes()
        print("Simulation done in %.2f seconds." % (time.time()-start_time))

        plotRes(probs, meanS/T, s, Nsims)

        print("Theoretical p for max efficiency: %.4f" % (probs[np.argmax(s)]))
        print("Simulation p for max efficiency: %.4f" %
              (probs[np.argmax(meanS)]))
        cmmd = input("Run another simulation? (y or n): ")


if __name__ == "__main__":
    # execute only if run as a script
    main()
