import tensorflow as tf
tf.test.gpu_device_name() #run to make sure tensorflow is connected to gpu

import numpy as np
import pandas as pd
import csv 
import os  
from random import shuffle
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread, imshow, subplots, show

def skipper(fname):
    with open(fname) as fin:
        no_comments = (line for line in fin if not line.lstrip().startswith('#'))
        next(no_comments, None) # skip header
        for row in no_comments:
            yield row

def main(): 
    
    arr = np.loadtxt(skipper("C:/Users/nmb20/UNiversities/Datasets/Blackjack/train_labels.csv"),
                 delimiter=",", dtype=str)
    
main()