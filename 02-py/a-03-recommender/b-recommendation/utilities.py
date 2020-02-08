#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from sklearn import model_selection


def load_data(input_file):  # Load multivar data in the input file
    X = []
    with open(input_file, "r") as f:
        for line in f.readlines():
            data = [float(x) for x in line.split(",")]
            X.append(data)
    return np.array(X)