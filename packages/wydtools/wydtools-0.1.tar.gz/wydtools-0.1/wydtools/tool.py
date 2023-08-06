from numpy import array
import numpy as np
from numpy import load
names = {
    "data_path": "/work/papers/data",
    "paper_path": "/work/papers",
}

DATA = "/work/papers/data"
PAPER = "/work/papers"


def get_vol6_64(nums: int):
    data = load('./vol6_64.npy')
    if nums > data.shape[0]:
        print('Warning: max size is ', data.shape[0])
    return data[0:nums]


# x = np.zeros((100, 100))

# print(x.shape)
# print(x[0:1010].shape)

# get_vol6_64(10221)