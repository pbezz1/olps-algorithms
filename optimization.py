import numpy as np
import multiplicative_weigths as mw

#optimizes multiplicative weigths method parameter eta, using a monte carlo algorithm
def optimizeEta(data, steps, avgSteps, mode, isRandom, beta=None):
    best_return=-float("inf")
    opt_eta=None
    current_steps = 0;

    # stores previous results on a dictionary to avoid running multiple times
    runs = {}

    while(current_steps < steps):
        eta=np.random.random()
        eta = round(eta,2)

        if(runs.get(eta) == None):
            #Runs avgSteps times to soften the randomized component
            avg_return=0
            for i in range(avgSteps):
                result = mw.multiplicative_weights(data,eta,mode,isRandom, beta)
                avg_return = avg_return + result['Result'].sum()

            avg_return=avg_return/avgSteps
            runs[eta]=avg_return
            #print("For %.2f value of eta the averageReturn was %f" % (eta, avg_return))
        else:
            avg_return = runs[eta]


        if (avg_return > best_return):
            opt_eta=eta
            best_return=avg_return
            current_steps=0
        else:
            current_steps=current_steps+1

    return opt_eta