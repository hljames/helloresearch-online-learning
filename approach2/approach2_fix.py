import random

class Solution():
    def __init__(self, vals, p, counts):
        self.counts = counts
        self.vals = vals
        self.p = p

    def init_vals(self, num_arms):
        self.vals = [0.0] * num_arms
        self.counts = [0] * num_arms

    def best_action(self, vals):
        best = max(vals)
        return vals.index(best)
    
    def choose_arm(self):
        r = random.random(0,1)
        if r < self.p:
            return random.randint(0,1)
        else:
            # return the maximum expected value
            return best_action(self.vals)

    def update(self, arm, actual_reward):
        # update counts
        self.counts[arm] = self.counts[arm] + 1
        n = self.counts[arm]

        # update value
        val = self.vals[arm]
        # calculate new value
        new_val = 1 # TODO: update with actual calculation of new value - prob want to weight it based on n
        self.vals[arm] = new_val
        return

'''
set the real rewards
set the true distributions 

init stuff 
for each trial in trials:
       choose_action
       get_reward 
       update based on arm and reward

record results somewhere
plot results
'''

