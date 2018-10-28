import random
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
from statistics import mean
import math
from matplotlib import rc
# rc('text', usetex=True)

true_u1 = 0.4
true_u2 = 0.7
better_arm = 'arm_two'


def get_regret_avgs(method,t):
    total_pulls_arm_1 = total_pulls_arm_2 = 1
    total_ones_arm_1 = total_ones_arm_2 = 0
    regrets = []
    regret = 0
    for i in range(t):
        w_avg1 = total_ones_arm_1/total_pulls_arm_1 + method(total_pulls_arm_1)
        w_avg2 = total_ones_arm_2/total_pulls_arm_2 + method(total_pulls_arm_2)
        arm_true_u = true_u1 if w_avg1 >= w_avg2 else true_u2
        arm = 'arm_one' if w_avg1 >= w_avg2 else 'arm_two'
        pull = random.random()
        res = pull < arm_true_u
        if arm == 'arm_one':
            total_pulls_arm_1 += 1
            if res == 1:
                total_ones_arm_1 +=1
        else:
            total_pulls_arm_2 += 1
            if res == 1:
                total_ones_arm_2 += 1
        regret += max(true_u2,true_u1) - res
        regrets.append(regret)
    return regrets

# optimal = 1000*max(true_u1,true_u2)
# regret = optimal - my_number_of_ones

def get_regrets_dict(t, ax, averaging_constant=1000):
    lines = []
    def one_over_n(n):
        return 1/n
    def none(n):
        return 0
    def one_over_n_squared(n):
        return 1/(n**2)
    def one_over_root_n(n):
        return 1/(math.sqrt(n))
    def one_over_cube_root_n(n):
        return 1/(n**(1./3))
    regrets_matrix_dict = {
    # "1/n" : [one_over_n],
    # "None" : [none],
    # "1/n^2" : [one_over_n_squared],
    "Approach 2" : [one_over_root_n]
    # "1/x^(1/3)" : [one_over_cube_root_n]
    }
    for i in range(averaging_constant):
        for k in regrets_matrix_dict:
            regrets_matrix_dict[k].append(get_regret_avgs((regrets_matrix_dict[k][0]),t))
    for k in regrets_matrix_dict:
        lines.append(ax.plot(list(map(mean, zip(*regrets_matrix_dict[k][1:]))), label=k),)
    return

def explore_exploit(q,t,averaging_constant=1000):
    regret_matrix = []
    for i in range(averaging_constant):
        regrets = []
        explore_pulls_1 = explore_pulls_2 = 0
        regret = 0
                #explore
                    # total successes of q trials with p of success true_u1/true_u2
        for i in range(q):
            pull = random.random()
            res = pull < true_u1
            regret += max(true_u2,true_u1) - res
            if res:
                explore_pulls_1 +=1
            regret += max(true_u2,true_u1) - res
            regrets.append(regret)
        for i in range(q):
            pull = random.random()
            res = pull < true_u2
            if res:
                explore_pulls_2 +=1
            regret += max(true_u2,true_u1) - res
            regrets.append(regret)
        sample_mean_1 = explore_pulls_1/q
        sample_mean_2 = explore_pulls_2/q
        est_better_arm = true_u1 if sample_mean_1 > sample_mean_2 else true_u2
        for i in range(t-2*q):
            pull = random.random()
            res = pull < est_better_arm
            regret += max(true_u2,true_u1) - res
            regrets.append(regret)
        regret_matrix.append(regrets)
    return list(map(mean, zip(*regret_matrix)))


fig,ax = plt.subplots()
lines = get_regrets_dict(1000,ax)
approach_1 = explore_exploit(69,1000)
print("approach_1 regrets: " + str(approach_1))
ax.plot(approach_1, label="Approach 1")
ax.set_title('Average Inflated By Uncertaintly -- Regret vs Time')
ax.set_xlabel('Time')
ax.set_ylabel('Cumulative Regret')
plt.legend()
plt.show()
