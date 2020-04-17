import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor


# Algorithms
learning_rate = 1
n_estimators = 200
max_depth = 10
regressors = {'Random Forest': (RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth), 'royalblue'),
              'Gradient Boost': (GradientBoostingRegressor(n_estimators=n_estimators, max_depth=max_depth,
                                                           learning_rate=learning_rate), 'darkorange'),
              'AdaBoost': (AdaBoostRegressor(base_estimator=DecisionTreeRegressor(max_depth=max_depth),
                                             n_estimators=n_estimators, learning_rate=learning_rate), 'indigo'),
              'XGBoost': (XGBRegressor(n_estimators=n_estimators, max_depth=max_depth,
                                       learning_rate=learning_rate), 'mediumseagreen')}

# X values
num_cycle = 10  # each cycle is [0pi, 2*pi]
distance = 0.005  # distance between consecutive observations
x = np.arange(0, num_cycle*2*np.pi, distance)
sample_size = 0.005  # as a percentage of x values

# Plot random sample
plt.figure(figsize=(10, 12))
num_obs = int(np.rint(len(x)*sample_size))
x_s = np.random.choice(x, size=num_obs)
y_s = np.sin(x_s)
ax = plt.subplot(611)
ax.scatter(x_s, y_s, c='k', s=2)
plt.ylim(-1.1, 1.1)
plt.xlim(np.min(x), np.max(x))
plt.axhline(0, c='lightgrey', lw=1)
plt.title('Random Sample Size = ' + str(num_obs))

# Plot population
ax = plt.subplot(612)
ax.scatter(x, np.sin(x), c='k', s=2)
plt.ylim(-1.1, 1.1)
plt.xlim(np.min(x), np.max(x))
plt.axhline(0, c='lightgrey', lw=1)
plt.title('Total Population')

counter = 1

for reg in regressors.keys():
    y_s = np.sin(x_s)
    regressors[reg][0].fit(x_s.reshape(-1, 1), y_s)
    y_hat = regressors[reg][0].predict(x.reshape(-1, 1))
    ax = plt.subplot(612+counter)
    ax.scatter(x, y_hat, c=regressors[reg][1], s=2)
    plt.ylim(-1.1, 1.1)
    plt.axhline(0, c='lightgrey', lw=1)
    plt.xlim(np.min(x), np.max(x))
    plt.title(reg)
    counter += 1

plt.show()



