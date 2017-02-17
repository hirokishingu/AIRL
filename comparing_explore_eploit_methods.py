import numpy as np
import matplotlib.pyplot as plt
from compare_epsi import Bandit
from opt_init_values import run_experiment as run_experiment_oiv
from ucb import run_experiment as run_experiment_ucb

class BayesianBandit:
  def __init__(self, m):
    self.m = m
    self.m0 = 0
    self.lambda0 = 1
    self.sum_x = 0
    self.tau = 1

  def pull(self):
    return np.random.randn() + self.m

  def sample(self):
    return np.random.randn() / np.sqrt(self.lambda0) + self.m0

  def update(self, x):
    self.lambda0 += 1
    self.sum_x += x
    self.m0 = self.tau*self.sum_x / self.lambda0

def run_experiment_decaying_epsilon(m1, m2, m3, N):
  bandits = [Bandit(m1), Bandit(m2), Bandit(m3)]

  data = np.empty(N)

  for i in xrange(N):
    p = np.random.random()
    if p < 1.0/(i+1):
      j = np.random.choice(3)
    else:
      j = np.argmax([b.mean for b in bandits])
    x = bandits[j].pull()
    bandits[j].update(x)

    data[i] = x
  cumulative_average = np.cumsum(data) / (np.arange(N) + 1)

  plt.plot(cumulative_average)
  plt.plot(np.ones(N)*m1)
  plt.plot(np.ones(N)*m2)
  plt.plot(np.ones(N)*m3)
  plt.xscale("log")
  plt.show()

  for b in bandits:
    print b.mean

  return cumulative_average

def run_experiment(m1, m2, m3, N):
  bandits = [BayesianBandit(m1), BayesianBandit(m2), BayesianBandit(m3)]

  data = np.empty(N)

  for i in xrange(N):
    j = np.argmax([b.sample() for b in bandits])
    x = bandits[j].pull()
    bandits[j].update(x)

    data[i] = x
  cumulative_average = np.cumsum(data) / (np.arange(N) + 1)

  plt.plot(cumulative_average)
  plt.plot(np.ones(N)*m1)
  plt.plot(np.ones(N)*m2)
  plt.plot(np.ones(N)*m3)
  plt.xscale("log")
  plt.show()

  return cumulative_average

if __name__ == "__main__":
  eps = run_experiment_decaying_epsilon(1.0, 2.0, 3.0, 100000)
  oiv = run_experiment_oiv(1.0, 2.0, 3.0, 100000)
  ucb = run_experiment_ucb(1.0, 2.0, 3.0, 100000)
  bayes = run_experiment(1.0, 2.0, 3.0, 100000)

  plt.plot(eps, label="decaying-epsilon-greedy")
  plt.plot(oiv, label="optimistic")
  plt.plot(ucb, label="ucb1")
  plt.plot(bayes, label="bayesian")
  plt.legend()
  plt.xscale("log")
  plt.show()

  plt.plot(eps, label="decaying-epsilon-greedy")
  plt.plot(oiv, label="optimistic")
  plt.plot(ucb, label="ucb1")
  plt.plot(bayes, label="bayesian")
  plt.legend()
  plt.show()



































