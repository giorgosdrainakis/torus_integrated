import os
import csv
import math
from scipy.stats import genpareto
import matplotlib.pyplot as plt
import numpy as numpy
import random
import numpy as np
import statistics
import csv
import pandas as pd
from torus_integrated import myglobal
import matplotlib
from matplotlib.ticker import MaxNLocator
from torus_integrated.myglobal import *
# First run with avgg=False to check all samples (where they span)
# According to this plot-> set avgg=True and set grouping parameters to get finalized plots
# Plot label params at the end of the script (thruput-delay-overflow)

# Sampling params
def geo1():
    my_tbegin=0
    my_tend=0.010 # intra 0.050
    my_samples=100 # intra 100
    filename='torus2400_80in_with_split.csv'


    file=os.path.join(myglobal.LOGS_FOLDER,filename)
    df=pd.read_csv(file)

    boolean = df["packet_id"].is_unique
    print(boolean)

    print(str(df.shape[0]))



def geo2():
    list_of_df=[]
    for node in range(1,17):
        for tor in range(1,17):
            mystr='tor'+str(tor)+'node'+str(node)+'.csv'
            print(mystr)
            file = os.path.join(myglobal.CURR_TRAFFIC_DATASET_FOLDER,mystr)
            df = pd.read_csv(file)
            list_of_df.append(df)

    df = pd.concat(list_of_df)
    print(str(df.shape[0]))

geo1()