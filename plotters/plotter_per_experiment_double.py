import csv
import math
from scipy.stats import genpareto
import matplotlib.pyplot as plt
import numpy as numpy
import random
import numpy as np
import statistics
import csv
from torus_integrated import myglobal
import matplotlib
from matplotlib.ticker import MaxNLocator
from torus_integrated.myglobal import *
load=[0,118.01370880000002,173.1990048,190.6952448,199.69104320000002,228.9138592,298.0873472]
thru=[0,118.01370880000002,160,160,140.13360640000002,120.9118976,102.7535168]
delay=[0,0.1510571116779896,1.746968029605364,2.885243641777095,3.6538637878109665,4.353948289316993,4.819130471427835]


def test():
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

     #down_x_lim_begin=0
    #down_x_lim_end=1.1
    up_x_label='Intra Traffic Absolute Load (Gbps)'
    y_label='Throughput (Gbps)'
    legend_loc='upper left'

    fig, ax1 = plt.subplots(constrained_layout=True)

    ax2 = ax1.twinx()


    ax1.set_xlabel('Total Inter Load (Gbps)', fontsize=25)
    ax1.set_ylabel('Inter Throughput (Gbps)', color='r', fontsize=25)
    ax1.legend(loc='upper left', fontsize=15)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=20)
    ax1.tick_params(axis='both', which='minor', labelsize=8)
    ax2.set_ylabel('Inter Delay (ms)', color='b', fontsize=25)
    ax2.tick_params(axis='both', which='major', labelsize=20)
    ax2.tick_params(axis='both', which='minor', labelsize=8)

    ax1.plot(load, thru, 'r-',linewidth=4,label='Throughput')
    ax2.plot(load, delay, 'b-',linewidth=4,label='Delay')
    plt.show()


test()















