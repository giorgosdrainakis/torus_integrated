import csv
import math
from scipy.stats import genpareto
import matplotlib.pyplot as plt
import numpy as numpy
import random
import numpy as np
import statistics
import csv
import matplotlib
from matplotlib.ticker import MaxNLocator
from torus_integrated.myglobal import *

from torus_integrated.logs.log_20240316_id01_topo1x16_ch4x100_load500g.result import *


def plot_thru():
    _load_divide_factor=1e9
    _thru_divide_factor=1e9
    _load = waa_load_total_bps_avg
    _thru = waa_thru_total_bps_avg
    _drop=waa_drop_total_bps_avg

    selected_i = []
    for i in range(0, len(_load)):
        if _load[i] != 0:
            #if _thru[i] > _load[i]:
                #_thru[i] = _load[i]
            if _thru[i] <= _load[i]:
                selected_i.append(i)
            else:
                print('Removing-cleaning i='+str(i))

    _load = [_load[i] / _load_divide_factor for i in selected_i]
    _load.insert(0, 0)
    _thru = [_thru[i] / _thru_divide_factor for i in selected_i]
    _thru.insert(0, 0)
    _drop = [_drop[i] / _thru_divide_factor for i in selected_i]
    _drop.insert(0, 0)

    #calcs
    _util=[]
    for i in range(0,len(_thru)):
        if _load[i]!=0:
            myutil=_thru[i]/_load[i]
            _util.append(myutil)
    print('_util='+str(_util))
    print('Mean util='+str(statistics.mean(_util)))
    print('Load=' + str(_load))
    print('Thru='+str(_thru))

    _color='black'

    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=False)

    _linewidth=6

    ax1.plot(_load, _thru, color='blue', label='Throughput',linewidth=_linewidth, linestyle='solid')
    ax1.plot(_load, _drop, color='red', label='Packet drop rate',linewidth=_linewidth, linestyle='solid')

    try:
        ax1.set_xlim([self.lim_x_start, self.lim_x_end])
    except:
        pass
    try:
        ax1.set_ylim([self.lim_y_start, self.lim_y_end])
    except:
        pass
    try:
        my_ticks = np.arange(self.xtick_min, self.xtick_max + 1, self.xtick_step)
        my_ticks = np.insert(my_ticks, 0, self.xtick_zero, axis=0)
        ax1.set_xticks(my_ticks)
    except:
        pass

    if _load_divide_factor==1e9:
        ax1.set_xlabel('Load (Gbps)', fontsize=21)
    else:
        print('no load divide factor')
        exit()
    if _thru_divide_factor==1e9:
        ax1.set_ylabel('Bitrate (Gbps)', fontsize=21)
    else:
        print('no thru divide factor')
        exit()

    ax1.set_xlabel('Load (Gbps)', fontsize=21)
    ax1.set_ylabel('Throughput (Gbps)', fontsize=21)
    ax1.legend(loc='best', fontsize=21)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=21)
    ax1.tick_params(axis='both', which='minor', labelsize=21)

    plt.show()

def plot_delays():
    _load_divide_factor=1e9
    _delay_divide_factor=1e-9
    _load = waa_load_total_bps_avg
    _thru = waa_thru_total_bps_avg
    _delay_avg = waa_delay_total_avg

    _delay_high = waa_delay_high_avg

    _delay_med = waa_delay_med_avg

    _delay_low = waa_delay_low_avg

    selected_i = []
    for i in range(0, len(_load)):
        if _load[i] != 0:
            #if _thru[i] > _load[i]:
                #_thru[i] = _load[i]
            if _thru[i] <= _load[i]:
                selected_i.append(i)
            else:
                print('Removing-cleaning i='+str(i))

    _load = [_load[i] / _load_divide_factor for i in selected_i]

    _delay_avg=[_delay_avg[i] / _delay_divide_factor for i in selected_i]
    _delay_high=[_delay_high[i] / _delay_divide_factor for i in selected_i]
    _delay_med=[_delay_med[i] / _delay_divide_factor for i in selected_i]
    _delay_low=[_delay_low[i] / _delay_divide_factor for i in selected_i]

    _color='black'

    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=False)

    _linewidth=6

    print('Avg:'+str(_delay_avg))
    print('High:'+str(_delay_high))
    print('Med:'+str(_delay_med))
    print('Low:'+str(_delay_low))

    ax1.semilogy(_load, _delay_avg, color='black', label='Delay Avg',linewidth=_linewidth, linestyle='solid')
    ax1.semilogy(_load, _delay_high, color='red', label='Delay High',linewidth=_linewidth, linestyle='solid')
    ax1.semilogy(_load, _delay_med, color='green', label='Delay Med',linewidth=_linewidth, linestyle='solid')
    ax1.semilogy(_load, _delay_low, color='blue', label='Delay Low',linewidth=_linewidth, linestyle='solid')
    try:
        ax1.set_xlim([self.lim_x_start, self.lim_x_end])
    except:
        pass
    try:
        ax1.set_ylim([self.lim_y_start, self.lim_y_end])
    except:
        pass
    try:
        my_ticks = np.arange(self.xtick_min, self.xtick_max + 1, self.xtick_step)
        my_ticks = np.insert(my_ticks, 0, self.xtick_zero, axis=0)
        ax1.set_xticks(my_ticks)
    except:
        pass

    if _load_divide_factor==1e9:
        ax1.set_xlabel('Load (Gbps)', fontsize=21)
    else:
        print('no load divide factor')
        exit()
    if _delay_divide_factor==1e-9:
        ax1.set_ylabel('Delay (nsec)', fontsize=21)
    elif _delay_divide_factor==1e-6:
        ax1.set_ylabel('Delay (μsec)', fontsize=21)
    else:
        print('no delay divide factor')
        exit()
    ax1.legend(loc='best', fontsize=21)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=21)
    ax1.tick_params(axis='both', which='minor', labelsize=21)

    plt.show()

plot_thru()
plot_delays()