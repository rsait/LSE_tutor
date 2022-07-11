import numpy as np

def transform_data(data, flatten=False):
    new_data = data-data[0,:]
    if flatten:
        joints = data.shape[0]
        coords = data.shape[1]
        flattened_data = np.empty(joints*coords)
        flattened_data[0:joints] = new_data[:,0]
        flattened_data[joints:2*joints]=new_data[:,1]
        flattened_data[2*joints:3*joints]
        return flattened_data
    else:
        return new_data
