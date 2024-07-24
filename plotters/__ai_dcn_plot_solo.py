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
from torus_integrated.logs.log_20240321_id02_topo1x24_ch4x100_load750g.result import *
from torus_integrated.logs.log_20240321_id03_topo1x32_ch4x100_load1000g.result import *
from torus_integrated.logs.log_20240323_id04_topo1x16_ch6x100_load750.result import *
from torus_integrated.logs.log_20240323_id05_topo1x16_ch8x100_load1000g.result import *
from torus_integrated.logs.log_20240625_id06_topo1x16_ch4x100_load500g_end100ms_dcUNI.result import *

#lanman
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

    _linewidth=10

    ax1.plot(_load, _thru, color='blue', label='Throughput',linewidth=_linewidth, linestyle='solid')
    ax1.plot(_load, _drop, color='red', label='Packet drop rate',linewidth=_linewidth, linestyle='solid')
    #new_util=[100*x for x in _util]
    #new_util.insert(0, 0)
    #ax1.plot(_load, new_util, color='black', label='Utilization %',linewidth=_linewidth, linestyle='solid')
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
def plot_delays(load,thru,avg,high,med,low):
    _load_divide_factor=1e9
    _delay_divide_factor=1e-6
    _load = load
    _thru = thru
    _delay_avg = avg
    _delay_high = high
    _delay_med = med
    _delay_low = low

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

    _linewidth=10

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
def plot_01_thru_drop_default():
    _load_divide_factor=1e9
    _thru_divide_factor=1e9
    _load = waa_id01_load_total_bps_avg
    _thru = waa_id01_thru_total_bps_avg
    _drop=waa_id01_drop_total_bps_avg

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

    _nominal=[400 for x in _load]

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

    _linewidth=10

    ax1.plot(_load, _thru, color='blue', label='Throughput',linewidth=_linewidth, linestyle='solid')
    ax1.plot(_load, _drop, color='red', label='Dropping rate',linewidth=_linewidth, linestyle='solid')
    #ax1.plot(_load, _nominal, color='black', label='Nominal rate', linewidth=_linewidth, linestyle='solid')
    #new_util=[100*x for x in _util]
    #new_util.insert(0, 0)
    #ax1.plot(_load, new_util, color='black', label='Utilization %',linewidth=_linewidth, linestyle='solid')
    try:
        ax1.set_xlim([self.lim_x_start, self.lim_x_end])
    except:
        pass
    try:
        ax1.set_ylim([-10, 410])
    except:
        pass
    try:
        my_ticks = np.arange(self.xtick_min, self.xtick_max + 1, self.xtick_step)
        my_ticks = np.insert(my_ticks, 0, self.xtick_zero, axis=0)
        ax1.set_xticks(my_ticks)
    except:
        pass

    if _load_divide_factor==1e9:
        ax1.set_xlabel('Load (Gbps)', fontsize=45)
    else:
        print('no load divide factor')
        exit()
    if _thru_divide_factor==1e9:
        ax1.set_ylabel('Bitrate (Gbps)', fontsize=45)
    else:
        print('no thru divide factor')
        exit()

    ax1.legend(loc='best', fontsize=40)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=45)
    ax1.tick_params(axis='both', which='minor', labelsize=45)

    plt.show()
def plot_02_delays_default():
    _load_divide_factor=1e9
    _delay_divide_factor=1e-6
    _load = waa_id01_load_total_bps_avg
    _thru = waa_id01_thru_total_bps_avg
    _delay_avg = waa_id01_delay_total_avg
    _delay_high = waa_id01_delay_high_avg
    _delay_med = waa_id01_delay_med_avg
    _delay_low = waa_id01_delay_low_avg

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

    _linewidth=10

    print('Avg:'+str(_delay_avg))
    print('High:'+str(_delay_high))
    print('Med:'+str(_delay_med))
    print('Low:'+str(_delay_low))

    ax1.semilogy(_load, _delay_avg, color='black', label='Mean',linewidth=_linewidth, linestyle='solid')
    ax1.semilogy(_load, _delay_high, color='red', label='High',linewidth=_linewidth, linestyle='solid')
    ax1.semilogy(_load, _delay_med, color='green', label='Med',linewidth=_linewidth, linestyle='solid')
    ax1.semilogy(_load, _delay_low, color='blue', label='Low',linewidth=_linewidth, linestyle='solid')
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
        ax1.set_xlabel('Load (Gbps)', fontsize=35)
    else:
        print('no load divide factor')
        exit()
    if _delay_divide_factor==1e-9:
        ax1.set_ylabel('Packet latency (ns)', fontsize=35)
    elif _delay_divide_factor==1e-6:
        ax1.set_ylabel('Packet latency (μs)', fontsize=35)
    else:
        print('no delay divide factor')
        exit()
    ax1.legend(loc='best', fontsize=35)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=35)
    ax1.tick_params(axis='both', which='minor', labelsize=35)

    plt.show()
def plot_03_scale_servers_thru_per_server():
    _load_divide_factor=1e9
    _thru_divide_factor=1e9

    _load16 = waa_id01_load_total_bps_avg
    _thru16 = waa_id01_thru_total_bps_avg

    _load24 = waa_id02_load_total_bps_avg
    _thru24 = waa_id02_thru_total_bps_avg

    _load32 = waa_id03_load_total_bps_avg
    _thru32 = waa_id03_thru_total_bps_avg


    selected_i = []
    for i in range(0, len(_load16)):
        if _load16[i] != 0:
            if _thru16[i] <= _load16[i]:
                selected_i.append(i)
            else:
                print('Removing-cleaning i='+str(i))

    _load16 = [_load16[i] / _load_divide_factor for i in selected_i]
    _load16.insert(0, 0)
    _thru16 = [_thru16[i] / _thru_divide_factor for i in selected_i]
    _thru16.insert(0, 0)
    _thru16 = [x/16 for x in _thru16]

    selected_i = []
    for i in range(0, len(_load24)):
        if _load24[i] != 0:
            if _thru24[i] <= _load24[i]:
                selected_i.append(i)
            else:
                print('Removing-cleaning i='+str(i))

    _load24 = [_load24[i] / _load_divide_factor for i in selected_i]
    _load24.insert(0, 0)
    _thru24 = [_thru24[i] / _thru_divide_factor for i in selected_i]
    _thru24.insert(0, 0)
    _thru24 = [x/24 for x in _thru24]

    selected_i = []
    for i in range(0, len(_load32)):
        if _load32[i] != 0:
            if _thru32[i] <= _load32[i]:
                selected_i.append(i)
            else:
                print('Removing-cleaning i='+str(i))

    _load32 = [_load32[i] / _load_divide_factor for i in selected_i]
    _load32.insert(0, 0)
    _thru32 = [_thru32[i] / _thru_divide_factor for i in selected_i]
    _thru32.insert(0, 0)
    _thru32 = [x/32 for x in _thru32]
    #calcs

    _color='black'

    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=False)

    _linewidth=10

    ax1.plot(_load16, _thru16, color='royalblue', label='$M=16$',linewidth=_linewidth, linestyle='solid')
    ax1.plot(_load24, _thru24, color='forestgreen', label='$M=24$',linewidth=_linewidth, linestyle='solid')
    ax1.plot(_load32, _thru32, color='black', label='$M=32$', linewidth=_linewidth, linestyle='solid')
    #new_util=[100*x for x in _util]
    #new_util.insert(0, 0)
    #ax1.plot(_load, new_util, color='black', label='Utilization %',linewidth=_linewidth, linestyle='solid')
    try:
        ax1.set_xlim([-20, 515])
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
        ax1.set_xlabel('Load (Gbps)', fontsize=35)
    else:
        print('no load divide factor')
        exit()
    if _thru_divide_factor==1e9:
        ax1.set_ylabel('Throughput per server (Gbps)', fontsize=35)
    else:
        print('no thru divide factor')
        exit()

    ax1.legend(loc='best', fontsize=35)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=35)
    ax1.tick_params(axis='both', which='minor', labelsize=35)

    plt.show()
def plot_04_scale_servers_qos_delays():
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    #x_lim_begin=-2
    #x_lim_end=12
    x_label='Load (Gbps)'
    y_label='Packet latency (μs)'

    fig, ax1 = plt.subplots(constrained_layout=False)
    ax1.set_yscale('log')

    load = [100, 200, 300, 400, 500]

    high16 = [0.21, 0.21, 0.21, 0.21, 0.21]
    med16 = [0.25, 0.25, 0.25, 0.25, 0.25]
    low16 = [0.33, 0.35, 0.4, 119.31, 324.88]

    high24 = [0.21, 0.21, 0.21, 0.21, 0.21]
    med24 = [0.25, 0.25, 0.25, 0.25, 0.25]
    low24 = [0.33, 0.36, 0.41, 122.48, 476.57]

    high32 = [0.21, 0.21, 0.21, 0.21, 0.21]
    med32 = [0.25, 0.25, 0.25, 0.25, 0.25]
    low32 = [0.33, 0.36, 0.41, 126.6, 496]

    space_left_mid_bar = 8
    space_between_bars = 25
    width = 6

    x2_middle=load
    x2_left=[x - space_left_mid_bar for x in x2_middle]
    x2_right=[x + space_left_mid_bar for x in x2_middle]

    x1_middle=[x - space_between_bars for x in x2_middle]
    x1_left = [x - space_left_mid_bar for x in x1_middle]
    x1_right  = [x + space_left_mid_bar for x in x1_middle]

    x3_middle=[x + space_between_bars for x in x2_middle]
    x3_left = [x - space_left_mid_bar for x in x3_middle]
    x3_right  = [x + space_left_mid_bar for x in x3_middle]

    ax1.bar(x1_left, high16, color='white',edgecolor='red', label="$M=16$ - High",linewidth=4, width=width,hatch='//')
    ax1.bar(x1_middle, med16,  color='white',edgecolor='green', label="$M=16$ - Med",linewidth=4, width=width,hatch='//')
    ax1.bar(x1_right, low16,  color='white',edgecolor='blue', label="$M=16$ - Low",linewidth=4, width=width,hatch='//')

    ax1.bar(x2_left, high24, color='white',edgecolor='red',  label="$M=24$ - High",linewidth=4, width=width, hatch='.')
    ax1.bar(x2_middle, med24, color='white',edgecolor='green', label="$M=24$ - Med",linewidth=4, width=width, hatch='.')
    ax1.bar(x2_right, low24, color='white',edgecolor='blue', label="$M=24$ - Low",linewidth=4, width=width, hatch='.')

    ax1.bar(x3_left, high32, color='white',edgecolor='red',  label="$M=32$ - High",linewidth=4, width=width, hatch='-')
    ax1.bar(x3_middle, med32, color='white',edgecolor='green', label="$M=32$ - Med",linewidth=4, width=width, hatch='-')
    ax1.bar(x3_right, low32, color='white',edgecolor='blue', label="$M=32$ - Low",linewidth=4, width=width, hatch='-')

    ax1.set_xticks(load)

    _LABEL_SIZE=35
    _LEGEND_SIZE=30
    _TICK_PARAMS=35
    try:
        ax1.set_xlabel(x_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_ylabel(y_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_xlim(x_lim_begin,x_lim_end)
    except:
        pass
    try:
        ax1.legend(loc='best', fontsize=_LEGEND_SIZE)
    except:
        pass
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def plot_05_scale_channels_drop_prob():
    _load_divide_factor=1e9
    _thru_divide_factor=1e9

    _load4 = waa_id01_load_total_bps_avg
    _thru4 = waa_id01_thru_total_bps_avg
    _drop_prob4=waa_id01_drop_prob_total_avg

    _load6 = waa_id04_load_total_bps_avg
    _thru6 = waa_id04_thru_total_bps_avg
    _drop_prob6=waa_id04_drop_prob_total_avg

    _load8 = waa_id05_load_total_bps_avg
    _thru8 = waa_id05_thru_total_bps_avg
    _drop_prob8=waa_id05_drop_prob_total_avg

    selected_i = []
    for i in range(0, len(_load4)):
        if _load4[i] != 0:
            if _thru4[i] <= _load4[i]:
                selected_i.append(i)
            else:
                print('Removing-cleaning i='+str(i))
    _load4 = [_load4[i] / _load_divide_factor for i in selected_i]
    _load4.insert(0, 0)
    _drop_prob4 = [_drop_prob4[i]  for i in selected_i]
    _drop_prob4.insert(0, 0)

    selected_i = []
    for i in range(0, len(_load6)):
        if _load6[i] != 0:
            if _thru6[i] <= _load6[i]:
                selected_i.append(i)
            else:
                print('Removing-cleaning i='+str(i))
    _load6 = [_load6[i] / _load_divide_factor for i in selected_i]
    _load6.insert(0, 0)
    _drop_prob6 = [_drop_prob6[i]  for i in selected_i]
    _drop_prob6.insert(0, 0)

    selected_i = []
    for i in range(0, len(_load8)):
        if _load8[i] != 0:
            if _thru8[i] <= _load8[i]:
                selected_i.append(i)
            else:
                print('Removing-cleaning i='+str(i))
    _load8 = [_load8[i] / _load_divide_factor for i in selected_i]
    _load8.insert(0, 0)
    _drop_prob8 = [_drop_prob8[i]  for i in selected_i]
    _drop_prob8.insert(0, 0)

    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=False)

    _linewidth=10

    ax1.plot(_load4, _drop_prob4, color='royalblue', label='$N=4$',linewidth=_linewidth, linestyle='solid')
    ax1.plot(_load6, _drop_prob6, color='forestgreen', label='$N=6$',linewidth=_linewidth, linestyle='solid')
    ax1.plot(_load8, _drop_prob8, color='black', label='$N=8$', linewidth=_linewidth, linestyle='solid')
    #new_util=[100*x for x in _util]
    #new_util.insert(0, 0)
    #ax1.plot(_load, new_util, color='black', label='Utilization %',linewidth=_linewidth, linestyle='solid')
    try:
        ax1.set_xlim([-10, 680])
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
        ax1.set_xlabel('Load (Gbps)', fontsize=35)
    else:
        print('no load divide factor')
        exit()
    if _thru_divide_factor==1e9:
        ax1.set_ylabel('Dropping Probability', fontsize=35)
    else:
        print('no thru divide factor')
        exit()

    ax1.legend(loc='best', fontsize=35)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=35)
    ax1.tick_params(axis='both', which='minor', labelsize=35)

    plt.show()
def plot_06_scale_ch_qos_delays():
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    #x_lim_begin=-2
    #x_lim_end=12
    x_label='Load (Gbps)'
    y_label='Packet latency (μs)'

    fig, ax1 = plt.subplots(constrained_layout=False)
    ax1.set_yscale('log')

    load = [100, 200, 300, 400, 500]

    high4 = [0.21, 0.21, 0.21, 0.21, 0.21]
    med4 = [0.25, 0.25, 0.25, 0.25, 0.25]
    low4 = [0.33, 0.35, 0.4, 119.31, 324.88]

    high6 = [0.21, 0.21, 0.21, 0.21, 0.21]
    med6 = [0.25, 0.25, 0.25, 0.25, 0.25]
    low6 = [0.33, 0.33, 0.33, 0.37, 0.50]

    high8 = [0.21, 0.21, 0.21, 0.21, 0.21]
    med8 = [0.25, 0.25, 0.25, 0.25, 0.25]
    low8 = [0.33, 0.33, 0.33, 0.37, 0.37]

    space_left_mid_bar = 8
    space_between_bars = 25
    width = 6

    x2_middle=load
    x2_left=[x - space_left_mid_bar for x in x2_middle]
    x2_right=[x + space_left_mid_bar for x in x2_middle]

    x1_middle=[x - space_between_bars for x in x2_middle]
    x1_left = [x - space_left_mid_bar for x in x1_middle]
    x1_right  = [x + space_left_mid_bar for x in x1_middle]

    x3_middle=[x + space_between_bars for x in x2_middle]
    x3_left = [x - space_left_mid_bar for x in x3_middle]
    x3_right  = [x + space_left_mid_bar for x in x3_middle]

    ax1.bar(x1_left, high8, color='white',edgecolor='red', label="$N=8$ - High",linewidth=4, width=width,hatch='//')
    ax1.bar(x1_middle, med8,  color='white',edgecolor='green', label="$N=8$ - Med",linewidth=4, width=width,hatch='//')
    ax1.bar(x1_right, low8,  color='white',edgecolor='blue', label="$N=8$ - Low",linewidth=4, width=width,hatch='//')

    ax1.bar(x2_left, high6, color='white',edgecolor='red',  label="$N=6$ - High",linewidth=4, width=width, hatch='.')
    ax1.bar(x2_middle, med6, color='white',edgecolor='green', label="$N=6$ - Med",linewidth=4, width=width, hatch='.')
    ax1.bar(x2_right, low6, color='white',edgecolor='blue', label="$N=6$ - Low",linewidth=4, width=width, hatch='.')

    ax1.bar(x3_left, high4, color='white',edgecolor='red',  label="$N=4$ - High",linewidth=4, width=width, hatch='-')
    ax1.bar(x3_middle, med4, color='white',edgecolor='green', label="$N=4$ - Med",linewidth=4, width=width, hatch='-')
    ax1.bar(x3_right, low4, color='white',edgecolor='blue', label="$N=4$ - Low",linewidth=4, width=width, hatch='-')

    ax1.set_xticks(load)

    _LABEL_SIZE=35
    _LEGEND_SIZE=30
    _TICK_PARAMS=35
    try:
        ax1.set_xlabel(x_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_ylabel(y_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_xlim(x_lim_begin,x_lim_end)
    except:
        pass
    try:
        ax1.legend(loc='best', fontsize=_LEGEND_SIZE)
    except:
        pass
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()

#lanman
plot_01_thru_drop_default()
plot_02_delays_default()
plot_03_scale_servers_thru_per_server()
plot_04_scale_servers_qos_delays()
plot_05_scale_channels_drop_prob()
plot_06_scale_ch_qos_delays()
