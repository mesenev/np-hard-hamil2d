import numpy as np

with open("input.txt") as f:
    n, *data = f.readlines()
    n = int(n)

adj_matrix = np.zeros((n, n), dtype=int)
for line in data:
    src, target, weight = map(int, line.split())
    adj_matrix[src - 1, target - 1] = weight
    adj_matrix[target - 1, src - 1] = weight
matrix = np.linalg.matrix_power(adj_matrix, 3)
print(matrix)
# [[2 4 2 2 4]
#  [4 2 5 1 6]
#  [2 5 0 4 1]
#  [2 1 4 0 5]
#  [4 6 1 5 2]]