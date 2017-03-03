from enum import Enum
import numpy as np

class decision_mode(Enum):
    Majority = 1
    Distributed = 2

#Makes decision based on distribution criteria
def make_distributed_decision (weigths_list):
    weigths_sum=0
    for weigth in weigths_list:
        weigths_sum+=weigth

    probabilities_list = []
    for weigth in weigths_list:
        probabilities_list.append(weigth/weigths_sum)

    indexes = np.arange(0, len(weigths_list))
    index = np.random.choice(indexes , p=probabilities_list )
    return index

# Makes the decision based on decision mode
#
def make_decision(weigths_list, mode):
    index = 0
    if(mode == decision_mode.Majority):
        for i in range(1,len(weigths_list)):
            if(weigths_list[index] < weigths_list[i]):
                index=i
    else:
        if(mode == decision_mode.Distributed):
            index=make_distributed_decision(weigths_list)

    return index