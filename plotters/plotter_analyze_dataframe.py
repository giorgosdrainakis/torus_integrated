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
measurement_type='post' # in [pre,post], pre refers to traffic_generation metrics, post to after_experiments metrics
avgg=True
mode='end2end' # in [intra,inter,end2end]
servers=16 # only for intra
tors=16 # only for inter
parent_tor=1 # only for intra, end2end analysis
# Simulation params
my_tbegin=0
my_tend=0.0010 # intra 0.050
my_samples=100 # intra 100
filename='log2022_05_09_15_28_25_947833_everything.csv'
#filename='torus_logs_globecom\\torus2400_80in.csv'
# Grouping params
start_group_value=0
end_group_value=1e7 #intra/inter/both=8.5e6,9.3e6,1.6e8 (torus1200_6intra_80in)     #Peirama_1_set1  8.5e6       # Peirama2_80_big=5.1e6 #Peirama2_80_small= 1.2e7
grouping_points=25

file=os.path.join(myglobal.LOGS_FOLDER,filename)
df=pd.read_csv(file)
print(str(df.iloc[0]))

df=df.sort_values('packet_id')
print('-----------------')
print(str(df.iloc[0]))
print('-----------------')
print(str(df.iloc[-1]))