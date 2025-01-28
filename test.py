import numpy as np

arr = np.array([[[0,1,0],[0,0,1]],[[1,1,1],[0,0,0]]])
length = len(arr)
i = 0 

for x in range(length):
    print(arr[i])
    i += 1
