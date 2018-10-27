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
    rewards = np.zeros(num_trials)
    arms = np.zeros((num_trials, num_steps))
    regrets = np.zeros((num_trials, num_steps))
    cumu_regrets = np.zeros((num_trials, num_steps))

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
            rewards[n] = rewards[n] + reward
            regret = max(true_means) - reward
            regrets[n][s] = regret
            if s == 0:
              cumu_regrets[n][s] = regret
            else:
              cumu_regrets[n][s] = cumu_regrets[n][s-1] + regret
            total_rewards[n][s] = reward
    n_steps = np.linspace(0, num_steps, num_steps)
    return [num_trials, n_steps, arms, rewards, regrets, total_rewards,
        cumu_regrets]

def main():
    num_trials = 1000
    num_steps = 10000
    true_means = [0.7, 0.5]
    num_arms = len(true_means) - 1
    p = 1 # fixed value for now - can vary later
    alg = Solution([], p, [])
    alg.init_vals(num_arms)
    results = test(alg, num_arms, num_trials, num_steps, true_means)
    regrets = results[6]
    avg_regret = np.zeros(num_steps)
    for n in range(num_trials):
      for s in range(num_steps):
        avg_regret[s] = avg_regret[s] + regrets[n][s]
    avg_regret = np.divide(avg_regret, num_trials)

    p_1 = 0.1 # fixed value for now - can vary later
    alg_1 = Solution([], p_1, [])
    alg_1.init_vals(num_arms)
    results_1 = test(alg_1, num_arms, num_trials, num_steps, true_means)
    regrets_1 = results_1[6]
    avg_regret_1 = np.zeros(num_steps)
    for n in range(num_trials):
      for s in range(num_steps):
        avg_regret_1[s] = avg_regret_1[s] + regrets_1[n][s]
    avg_regret_1 = np.divide(avg_regret_1, num_trials)
    #regrets = results[6]
    # plot the results -- not sure how to do this
    fig,ax = plt.subplots()
    #regret = regrets[0]
    x = results[1]
    x_1 = results_1[1]
    print(x)
    #print(len(regret))
    ax.scatter(x, avg_regret, color='g')
    ax.set_title("Regret over time")
    ax.scatter(x_1, avg_regret_1, color='k')
    ax.set_xlabel("Number of steps")
    ax.set_ylabel("Regret")
    plt.show()

if __name__ == "__main__":
    main()


