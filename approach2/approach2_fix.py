import random
import matplotlib.pyplot as plt
import numpy as np

class Solution():
    def __init__(self, vals, p, counts):
        self.counts = counts
        self.vals = vals
        self.p = p

    def init_vals(self, num_arms):
        n = num_arms + 1
        self.vals = np.zeros(n)
        self.counts = np.zeros(n) # could just make this an int array

    def best_action(self, vals):
        return vals.argmax()
    
    def choose_arm(self, num_arms):
        r = random.random()
        if r < self.p:
            return random.randint(0, num_arms)
        else:
            # return the maximum expected value
            return self.best_action(self.vals)

    def update(self, arm, actual_reward):
        # update counts
        self.counts[arm] = self.counts[arm] + 1
        n = self.counts[arm]

        # update value
        val = self.vals[arm]
        # calculate new value
        new_val = ((n - 1) / float(n)) * val + (1 / float(n)) * actual_reward
        self.vals[arm] = new_val
        return

def test(alg, num_arms, num_trials, num_steps, true_means):
    total_rewards = np.zeros((num_trials, num_steps))
    n = num_arms + 1
    rewards = np.zeros(n)
    arms = np.zeros((num_trials, num_steps))
    regrets = np.zeros((num_trials, num_steps))

    for n in range(num_trials):
        alg.init_vals(num_arms)
        for s in range(num_steps):
            chosen_arm = alg.choose_arm(num_arms)
            arms[n][s] = chosen_arm
            i = random.random()
            if i < true_means[chosen_arm]:
                reward = 1.0
            else:
                reward = 0.0
            alg.update(chosen_arm, reward)
            rewards[chosen_arm] = reward
            regret = rewards.sum() / s
            regrets[n][s] = regret
            total_rewards[n][s] = reward
            s = s + 1
        n = n + 1
    return [num_trials, num_steps, arms, rewards, regrets, total_rewards]

def main():
    num_trials = 10
    num_steps = 1000
    true_means = [0.9, 0.5]
    num_arms = len(true_means) - 1
    print('num arms is', num_arms)
    p = 0.2 # fixed value for now - can vary later
    alg = Solution([], p, [])
    alg.init_vals(num_arms)
    results = test(alg, num_arms, num_trials, num_steps, true_means)
    # plot the results -- not sure how to do this
    fig,ax = plt.subplots()
    regret = regrets[0]
    ax.scatter(results[1], regret)
    ax.set_title("Regret over time")
    ax.set_xlabel("Number of steps")
    ax.set_ylabel("Regret")
    plt.show()

if __name__ == "__main__":
    main()

    
