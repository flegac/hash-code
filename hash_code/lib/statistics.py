import numpy as np
from scipy.stats import describe, find_repeats, entropy, iqr, pearsonr

data = np.random.random((100)) * 100
data = np.round(data)
print( describe(data))
print( find_repeats(data))
print('entropy', entropy(data))
print('iqr', iqr(data))

data = np.round(np.random.random((2,2)) * 100).astype(np.int)

x, y = data[0], data[1]
print('x', x)
print('y', y)

print('pearsonr', pearsonr(x, y))
