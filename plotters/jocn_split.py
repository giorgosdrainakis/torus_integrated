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
from torus_integrated.plotters.jocn_split_data01_1600_16x16_go_8020 import *
from torus_integrated.plotters.jocn_split_data02_800_16x16_go_8020 import *
from torus_integrated.plotters.jocn_split_data03_1600_16x16_stay_8020 import *
from torus_integrated.plotters.jocn_split_data04_800_16x16_stay_8020 import *
from torus_integrated.plotters.jocn_split_data05_2400_16x24_go_8020 import *
from torus_integrated.plotters.jocn_split_data06_2400_16x24_stay_8020 import *
from torus_integrated.plotters.jocn_split_data07_1200_16x24_stay_8020 import *
from torus_integrated.plotters.jocn_split_data07_3200_16x32_go_8020 import *
from torus_integrated.plotters.jocn_split_data08_3200_16x32_stay_8020 import *
from torus_integrated.plotters.jocn_split_data09_1600_16x32_stay_8020 import *
from torus_integrated.plotters.jocn_split_data14_1600_16x16_go_6040 import *
from torus_integrated.plotters.jocn_split_data15_1600_16x16_stay_6040 import *
from torus_integrated.plotters.jocn_split_data16_800_16x16_stay_6040 import *
from torus_integrated.plotters.jocn_split_data17_1600_16x16_go_7030 import *
from torus_integrated.plotters.jocn_split_data18_1600_16x16_stay_7030 import *
from torus_integrated.plotters.jocn_split_data19_800_16x16_stay_7030 import *
from torus_integrated.plotters.jocn_split_data22_400_16x8_go_8020 import *
from torus_integrated.plotters.jocn_split_data23_800_16x8_go_8020 import *

if True:
    del waa_1600_16x16_stay_8020_intra_load_total_bps_avg[12]
    del waa_1600_16x16_stay_8020_intra_thru_total_bps_avg[12]
    del waa_1600_16x16_stay_8020_intra_drop_total_bps_avg[12]
    del waa_1600_16x16_stay_8020_intra_load_total_bps_avg[-1]
    del waa_1600_16x16_stay_8020_intra_thru_total_bps_avg[-1]
    del waa_1600_16x16_stay_8020_intra_drop_total_bps_avg[-1]




def clean_load_thru(load,thru,cleaning_factor):
    selected_i=[]
    for i in range(0,len(load)):
        if load[i]!=0:
            if thru[i] > load[i]:
                thru[i]=load[i]
            selected_i.append(i)

    load = [load[i]/cleaning_factor for i in selected_i]
    load.insert(0,0)
    thru = [thru[i]/cleaning_factor for i in selected_i]
    thru.insert(0,0)
    return load,thru
def clean_load_thru_drop(load,thru,drop,cleaning_factor):
    selected_i=[]
    for i in range(0,len(load)):
        if load[i]!=0:
            if thru[i] > load[i]:
                thru[i]=load[i]
            selected_i.append(i)

    load = [load[i]/cleaning_factor for i in selected_i]
    load.insert(0,0)
    thru = [thru[i]/cleaning_factor for i in selected_i]
    thru.insert(0,0)
    drop = [drop[i]/cleaning_factor for i in selected_i]
    drop.insert(0,0)
    return load,thru,drop
def clean_load_thru_drop_prob(load,thru,drop,drop_prob_avg,drop_prob_high,drop_prob_med,drop_prob_low,cleaning_factor):
    selected_i=[]
    for i in range(0,len(load)):
        if load[i]!=0:
            if thru[i] > load[i]:
                thru[i]=load[i]
            selected_i.append(i)

    load = [load[i]/cleaning_factor for i in selected_i]
    load.insert(0,0)
    thru = [thru[i]/cleaning_factor for i in selected_i]
    thru.insert(0,0)
    drop = [drop[i]/cleaning_factor for i in selected_i]
    drop.insert(0,0)

    drop_prob_avg = [drop_prob_avg[i] for i in selected_i]
    drop_prob_avg.insert(0,0)

    drop_prob_high = [drop_prob_high[i] for i in selected_i]
    drop_prob_high.insert(0,0)

    drop_prob_med= [drop_prob_med[i] for i in selected_i]
    drop_prob_med.insert(0,0)

    drop_prob_low = [drop_prob_low[i] for i in selected_i]
    drop_prob_low.insert(0,0)

    return load,thru,drop,drop_prob_avg,drop_prob_high,drop_prob_med,drop_prob_low
def clean_load_delays(load,avg,high,med,low,cleaning_factor):
    selected_i=[]
    for i in range(0,len(load)):
        if load[i]!=0:
            selected_i.append(i)

    load = [load[i]/cleaning_factor for i in selected_i]
    load.insert(0,0)

    avg = [avg[i]*1e3 for i in selected_i]
    avg.insert(0,0)
    high = [high[i]*1e3 for i in selected_i]
    high.insert(0,0)
    med = [med[i]*1e3 for i in selected_i]
    med.insert(0,0)
    low = [low[i]*1e3 for i in selected_i]
    low.insert(0,0)

    return load,avg,high,med,low

def plot01_16x16_go_8020_intra_thru():
    _cleaning_factor=1e9
    _small_rm_factor=-1
    _big_rm_factor=5
    _max_thru=400
    _x_lim_begin, _x_lim_end=-0.1,450
    _x_label,_y_label='Intra-rack load (Gbps)','Bitrate (Gbps)'

    _LINEWIDTH = 7
    _LEGEND_SIZE = 30
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'center right'


    load_small,thru_small,drop_small=clean_load_thru_drop(waa_800_16x16_go_8020_intra_load_total_bps_avg,
                                                          waa_800_16x16_go_8020_intra_thru_total_bps_avg,
                                                          waa_800_16x16_go_8020_intra_drop_total_bps_avg,
                                                          cleaning_factor=_cleaning_factor)

    load_big, thru_big, drop_big = clean_load_thru_drop(waa_1600_16x16_go_8020_intra_load_total_bps_avg,
                                                        waa_1600_16x16_go_8020_intra_thru_total_bps_avg,
                                                        waa_1600_16x16_go_8020_intra_drop_total_bps_avg,
                                                        cleaning_factor=_cleaning_factor)

    # merge 2 datasets
    load=load_small[:_small_rm_factor]+load_big[_big_rm_factor:]
    thru = thru_small[:_small_rm_factor] + thru_big[_big_rm_factor:]
    drop = drop_small[:_small_rm_factor] + drop_big[_big_rm_factor:]

    # create nominal horizontal line
    nominal_thru=[_max_thru for el in load]

    # dbg
    print('load='+str(load))
    print('thru='+str(thru))
    print('drop=' + str(drop))

    #plot
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.plot(load, thru,'b', label="Throughput",linewidth=_LINEWIDTH)
    ax1.plot(load, drop,'r', label="Drop-rate",linewidth=_LINEWIDTH)
    ax1.plot(load, nominal_thru, 'k--', label="Nominal capacity", linewidth=_LINEWIDTH)

    ax1.set_xlabel(_x_label, fontsize=_LABEL_SIZE)
    ax1.set_ylabel(_y_label, fontsize=_LABEL_SIZE)
    ax1.set_xlim(_x_lim_begin,_x_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()
def plot02_16x16_go_8020_inter_thru():
    _cleaning_factor=1e9
    _small_rm_factor=-2
    _big_rm_factor=4
    _max_thru=16 * 4 * 40
    _x_lim_begin, _x_lim_end=-0.1,1500
    _x_label,_y_label='Inter-rack load (Gbps)','Bitrate (Gbps)'

    _LINEWIDTH = 7
    _LEGEND_SIZE = 30
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'center left'


    load_small,thru_small,drop_small=clean_load_thru_drop(waa_800_16x16_go_8020_inter_load_total_bps_avg,
                                                          waa_800_16x16_go_8020_inter_thru_total_bps_avg,
                                                          waa_800_16x16_go_8020_inter_drop_total_bps_avg,
                                                          cleaning_factor=_cleaning_factor)

    load_big, thru_big, drop_big = clean_load_thru_drop(waa_1600_16x16_go_8020_inter_load_total_bps_avg,
                                                        waa_1600_16x16_go_8020_inter_thru_total_bps_avg,
                                                        waa_1600_16x16_go_8020_inter_drop_total_bps_avg,
                                                        cleaning_factor=_cleaning_factor)

    # merge 2 datasets
    load=load_small[:_small_rm_factor]+load_big[_big_rm_factor:]
    thru = thru_small[:_small_rm_factor] + thru_big[_big_rm_factor:]
    drop = drop_small[:_small_rm_factor] + drop_big[_big_rm_factor:]

    # create nominal horizontal line
    nominal_thru=[_max_thru for el in load]

    # dbg
    print('load_small=' + str(load_small))
    print('load_big=' + str(load_big))
    print('load='+str(load))
    print('thru='+str(thru))
    print('drop=' + str(drop))

    #plot
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.plot(load, thru,'b', label="Throughput",linewidth=_LINEWIDTH)
    ax1.plot(load, drop,'r', label="Drop-rate",linewidth=_LINEWIDTH)
    ax1.plot(load, nominal_thru, 'k--', label="Nominal capacity", linewidth=_LINEWIDTH)

    ax1.set_xlabel(_x_label, fontsize=_LABEL_SIZE)
    ax1.set_ylabel(_y_label, fontsize=_LABEL_SIZE)
    ax1.set_xlim(_x_lim_begin,_x_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()
def plot03_16x16_go_8020_e2e_thru():
    _cleaning_factor=1e12
    _small_rm_factor=-2
    _big_rm_factor=2
    _max_thru=16*0.4+16*0.1
    _x_lim_begin, _x_lim_end=-0.1,10
    _x_label,_y_label='Total load (Tbps)','Bitrate (Tbps)'

    _LINEWIDTH = 7
    _LEGEND_SIZE = 30
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'center right'


    load_small,thru_small,drop_small=clean_load_thru_drop(waa_800_16x16_go_8020_e2e_load_total_bps_avg,
                                                          waa_800_16x16_go_8020_e2e_thru_total_bps_avg,
                                                          waa_800_16x16_go_8020_e2e_drop_total_bps_avg,
                                                          cleaning_factor=_cleaning_factor)

    load_big, thru_big, drop_big = clean_load_thru_drop(waa_1600_16x16_go_8020_e2e_load_total_bps_avg,
                                                        waa_1600_16x16_go_8020_e2e_thru_total_bps_avg,
                                                        waa_1600_16x16_go_8020_e2e_drop_total_bps_avg,
                                                        cleaning_factor=_cleaning_factor)

    # merge 2 datasets
    load=load_small[:_small_rm_factor]+load_big[_big_rm_factor:]
    thru = thru_small[:_small_rm_factor] + thru_big[_big_rm_factor:]
    drop = drop_small[:_small_rm_factor] + drop_big[_big_rm_factor:]

    # create nominal horizontal line
    nominal_thru=[_max_thru for el in load]

    # dbg
    print('load_small=' + str(load_small))
    print('load_big=' + str(load_big))
    print('load='+str(load))
    print('thru='+str(thru))
    print('drop=' + str(drop))

    #plot
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.plot(load, thru,'b', label="Throughput",linewidth=_LINEWIDTH)
    ax1.plot(load, drop,'r', label="Drop-rate",linewidth=_LINEWIDTH)
    ax1.plot(load, nominal_thru, 'k--', label="Nominal capacity", linewidth=_LINEWIDTH)

    ax1.set_xlabel(_x_label, fontsize=_LABEL_SIZE)
    ax1.set_ylabel(_y_label, fontsize=_LABEL_SIZE)
    ax1.set_xlim(_x_lim_begin,_x_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()
def plot04_16x16_go_8020_e2e_delays():
    _cleaning_factor=1e12
    _zero_rm_factor=1
    _small_rm_factor=-2
    _big_rm_factor=2
    _x_lim_begin, _x_lim_end=2,10
    _y_lim_begin,_y_lim_end=1e-3,1e-1
    _x_label,_y_label='Total load (Tbps)','End-to-end delay (ms)'

    _LINEWIDTH = 7
    _LEGEND_SIZE = 30
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'center right'

    load_small, avg_delay_small, high_delay_small, med_delay_small, low_delay_small = clean_load_delays(waa_800_16x16_go_8020_e2e_load_total_bps_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_delay_total_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_delay_high_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_delay_med_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    qload_small, avg_qdelay_small, high_qdelay_small, med_qdelay_small, low_qdelay_small = clean_load_delays(waa_800_16x16_go_8020_e2e_load_total_bps_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_qdelay_total_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_qdelay_high_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_qdelay_med_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_qdelay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    load_big, avg_delay_big, high_delay_big, med_delay_big, low_delay_big = clean_load_delays(
        waa_1600_16x16_go_8020_e2e_load_total_bps_avg,
        waa_1600_16x16_go_8020_e2e_delay_total_avg,
        waa_1600_16x16_go_8020_e2e_delay_high_avg,
        waa_1600_16x16_go_8020_e2e_delay_med_avg,
        waa_1600_16x16_go_8020_e2e_delay_low_avg,
        cleaning_factor=_cleaning_factor)

    qload_big, avg_qdelay_big, high_qdelay_big, med_qdelay_big, low_qdelay_big = clean_load_delays(
        waa_1600_16x16_go_8020_e2e_load_total_bps_avg,
        waa_1600_16x16_go_8020_e2e_qdelay_total_avg,
        waa_1600_16x16_go_8020_e2e_qdelay_high_avg,
        waa_1600_16x16_go_8020_e2e_qdelay_med_avg,
        waa_1600_16x16_go_8020_e2e_qdelay_low_avg,
        cleaning_factor=_cleaning_factor)


    # merge 2 datasets
    load=load_small[_zero_rm_factor:_small_rm_factor]+load_big[_big_rm_factor:]
    avg_delay=avg_delay_small[_zero_rm_factor:_small_rm_factor]+avg_delay_big[_big_rm_factor:]
    high_delay=high_delay_small[_zero_rm_factor:_small_rm_factor]+high_delay_big[_big_rm_factor:]
    med_delay=med_delay_small[_zero_rm_factor:_small_rm_factor]+med_delay_big[_big_rm_factor:]
    low_delay=low_delay_small[_zero_rm_factor:_small_rm_factor]+low_delay_big[_big_rm_factor:]
    qload = qload_small[_zero_rm_factor:_small_rm_factor] + qload_big[_big_rm_factor:]
    avg_qdelay=avg_qdelay_small[_zero_rm_factor:_small_rm_factor]+avg_qdelay_big[_big_rm_factor:]
    high_qdelay=high_qdelay_small[_zero_rm_factor:_small_rm_factor]+high_qdelay_big[_big_rm_factor:]
    med_qdelay=med_qdelay_small[_zero_rm_factor:_small_rm_factor]+med_qdelay_big[_big_rm_factor:]
    low_qdelay=low_qdelay_small[_zero_rm_factor:_small_rm_factor]+low_qdelay_big[_big_rm_factor:]

    # dbg
    print('load_small=' + str(load_small))
    print('load_big=' + str(load_big))
    print('load='+str(load))


    #plot
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.semilogy(load, avg_delay, 'b', label="Total delay", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(qload, avg_qdelay, 'r', label="Queuing delay", linewidth=_LINEWIDTH)

    ax1.set_xlabel(_x_label, fontsize=_LABEL_SIZE)
    ax1.set_ylabel(_y_label, fontsize=_LABEL_SIZE)
    ax1.set_xlim(_x_lim_begin,_x_lim_end)
    ax1.set_ylim(_y_lim_begin, _y_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()


def prep_plot05_16x16_stay_8020_e2e_delays():
    _cleaning_factor=1e12
    _zero_rm_factor=1
    _stay_small_rm_factor=-2
    _stay_big_rm_factor=2
    _go_small_rm_factor=-2
    _go_big_rm_factor=2
    _x_lim_begin, _x_lim_end=2,10
    _y_lim_begin,_y_lim_end=1e-4,1
    _x_label,_y_label='Total load (Tbps)','End-to-end delay (ms)'

    _LINEWIDTH = 7
    _LEGEND_SIZE = 30
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'center right'

    stay_load_small, stay_avg_delay_small, stay_high_delay_small, stay_med_delay_small, stay_low_delay_small = clean_load_delays(waa_800_16x16_stay_8020_e2e_load_total_bps_avg,
                                                                                                        waa_800_16x16_stay_8020_e2e_delay_total_avg,
                                                                                                        waa_800_16x16_stay_8020_e2e_delay_high_avg,
                                                                                                        waa_800_16x16_stay_8020_e2e_delay_med_avg,
                                                                                                        waa_800_16x16_stay_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    stay_load_big, stay_avg_delay_big, stay_high_delay_big, stay_med_delay_big, stay_low_delay_big = clean_load_delays(
        waa_1600_16x16_stay_8020_e2e_load_total_bps_avg,
        waa_1600_16x16_stay_8020_e2e_delay_total_avg,
        waa_1600_16x16_stay_8020_e2e_delay_high_avg,
        waa_1600_16x16_stay_8020_e2e_delay_med_avg,
        waa_1600_16x16_stay_8020_e2e_delay_low_avg,
        cleaning_factor=_cleaning_factor)

    go_load_small, go_avg_delay_small, go_high_delay_small, go_med_delay_small, go_low_delay_small = clean_load_delays(waa_800_16x16_go_8020_e2e_load_total_bps_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_delay_total_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_delay_high_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_delay_med_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    go_load_big, go_avg_delay_big, go_high_delay_big, go_med_delay_big, go_low_delay_big = clean_load_delays(
        waa_1600_16x16_go_8020_e2e_load_total_bps_avg,
        waa_1600_16x16_go_8020_e2e_delay_total_avg,
        waa_1600_16x16_go_8020_e2e_delay_high_avg,
        waa_1600_16x16_go_8020_e2e_delay_med_avg,
        waa_1600_16x16_go_8020_e2e_delay_low_avg,
        cleaning_factor=_cleaning_factor)


    # merge 2 datasets
    stay_load=stay_load_small[_zero_rm_factor:_stay_small_rm_factor]+stay_load_big[_stay_big_rm_factor:]
    stay_avg_delay=stay_avg_delay_small[_zero_rm_factor:_stay_small_rm_factor]+stay_avg_delay_big[_stay_big_rm_factor:]
    stay_high_delay=stay_high_delay_small[_zero_rm_factor:_stay_small_rm_factor]+stay_high_delay_big[_stay_big_rm_factor:]
    stay_med_delay=stay_med_delay_small[_zero_rm_factor:_stay_small_rm_factor]+stay_med_delay_big[_stay_big_rm_factor:]
    stay_low_delay=stay_low_delay_small[_zero_rm_factor:_stay_small_rm_factor]+stay_low_delay_big[_stay_big_rm_factor:]

    go_load=go_load_small[_zero_rm_factor:_go_small_rm_factor]+go_load_big[_go_big_rm_factor:]
    go_avg_delay=go_avg_delay_small[_zero_rm_factor:_go_small_rm_factor]+go_avg_delay_big[_go_big_rm_factor:]
    go_high_delay=go_high_delay_small[_zero_rm_factor:_go_small_rm_factor]+go_high_delay_big[_go_big_rm_factor:]
    go_med_delay=go_med_delay_small[_zero_rm_factor:_go_small_rm_factor]+go_med_delay_big[_go_big_rm_factor:]
    go_low_delay=go_low_delay_small[_zero_rm_factor:_go_small_rm_factor]+go_low_delay_big[_go_big_rm_factor:]

    # dbg
    print('stay_load_small=' + str(stay_load_small))
    print('stay_load_big=' + str(stay_load_big))
    print('stay_load='+str(stay_load))
    print('go_load_small=' + str(go_load_small))
    print('go_load_big=' + str(go_load_big))
    print('go_load='+str(go_load))

    #plot
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.semilogy(stay_load, stay_avg_delay, 'k', label="StayTotal", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(stay_load, stay_high_delay, 'r', label="StayHigh", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(stay_load, stay_med_delay, 'g', label="StayMed", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(stay_load, stay_low_delay, 'b', label="StayLow", linewidth=_LINEWIDTH + 1)

    ax1.semilogy(go_load, go_avg_delay, 'k--', label="goTotal", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(go_load, go_high_delay, 'r--', label="goHigh", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(go_load, go_med_delay, 'g--', label="goMed", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(go_load, go_low_delay, 'b--', label="goLow", linewidth=_LINEWIDTH + 1)

    ax1.set_xlabel(_x_label, fontsize=_LABEL_SIZE)
    ax1.set_ylabel(_y_label, fontsize=_LABEL_SIZE)
    ax1.set_xlim(_x_lim_begin,_x_lim_end)
    ax1.set_ylim(_y_lim_begin, _y_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()
def plot05_16x16_stay_8020_e2e_delays():
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'

    x_lim_begin=-2
    x_lim_end=12
    y_label='End-to-end delay (ms)'
    legend_loc='lower left'

    fig, ax1 = plt.subplots(constrained_layout=False)
    ax1.set_yscale('log')

    load=[2,4,6,8,10]
    high_go=[0.00040,0.00052,0.00078,0.00098,0.0010]
    med_go = [0.00048,0.00058,0.0069,0.027,0.033]
    low_go = [0.0067,0.0098,0.1,0.218,0.223]
    high_stay=[0.00023,0.00025,0.00032,0.00043,0.00048]
    med_stay = [0.00052,0.00067,0.0086,0.033,0.038]
    low_stay = [0.0073,0.016,0.133,0.2586,0.267]

    for i in range(0,len(load)):
        hh=(100*(high_go[i]-high_stay[i]))/high_go[i]
        mm = (100 * (med_go[i] - med_stay[i])) / med_go[i]
        ll = (100 * (low_go[i] - low_stay[i])) / low_go[i]
        print('Load='+str(load[i]))
        print('high change='+str(hh))
        print('med change=' + str(mm))
        print('low change=' + str(ll))
        print('----')

    mini_size = 0.14
    big_size = 0.55
    width = 0.2

    x_med = load
    x_med_2400 = [x - mini_size for x in x_med]
    x_med_3200 = [x + mini_size for x in x_med]

    x_high = [x - big_size for x in x_med]
    x_high_2400 = [x - mini_size for x in x_high]
    x_high_3200  = [x + mini_size for x in x_high]

    x_low = [x + big_size for x in x_med]
    x_low_2400 = [x - mini_size for x in x_low]
    x_low_3200  = [x + mini_size for x in x_low]


    ax1.bar(x_high_2400, high_go, color='white',edgecolor='red', label="Vanilla/High",linewidth=4, width=width,hatch='//')
    ax1.bar(x_med_2400, med_go,  color='white',edgecolor='green', label="Vanilla/Med",linewidth=4, width=width,hatch='//')
    ax1.bar(x_low_2400, low_go,  color='white',edgecolor='blue', label="Vanilla/Low",linewidth=4, width=width,hatch='//')
    ax1.bar(x_high_3200, high_stay, color='white',edgecolor='red',  label="StayIn/High",linewidth=4, width=width, hatch='o')
    ax1.bar(x_med_3200, med_stay, color='white',edgecolor='green', label="StayIn/Med",linewidth=4, width=width, hatch='o')
    ax1.bar(x_low_3200, low_stay, color='white',edgecolor='blue', label="StayIn/Low",linewidth=4, width=width, hatch='o')
    ax1.set_xticks([2,4,6,8,10])

    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=33
    _TICK_PARAMS=45
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
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()

def plot06_16x16_stay_traffic_e2e_delays():
    _cleaning_factor=1e12
    _8020_zero_rm_factor=1
    _8020_small_rm_factor=-3
    _8020_big_rm_factor=3
    _7030_zero_rm_factor=1
    _7030_small_rm_factor=-2
    _7030_big_rm_factor=2
    _6040_zero_rm_factor=1
    _6040_small_rm_factor=-3
    _6040_big_rm_factor=3
    _x_lim_begin, _x_lim_end=2,10
    _y_lim_begin,_y_lim_end=1e-4,1
    _x_label,_y_label='Total load (Tbps)','End-to-end delay (ms)'

    _LINEWIDTH = 7
    _LEGEND_SIZE = 30
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'center right'

    load_8020_small, avgdelay_8020_small, _, _, _ = clean_load_delays(waa_800_16x16_stay_8020_e2e_load_total_bps_avg,
                                                                                                        waa_800_16x16_stay_8020_e2e_delay_total_avg,
                                                                                                        waa_800_16x16_stay_8020_e2e_delay_high_avg,
                                                                                                        waa_800_16x16_stay_8020_e2e_delay_med_avg,
                                                                                                        waa_800_16x16_stay_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    load_8020_big, avgdelay_8020_big, _, _, _ = clean_load_delays(waa_1600_16x16_stay_8020_e2e_load_total_bps_avg,
                                                                                                        waa_1600_16x16_stay_8020_e2e_delay_total_avg,
                                                                                                        waa_1600_16x16_stay_8020_e2e_delay_high_avg,
                                                                                                        waa_1600_16x16_stay_8020_e2e_delay_med_avg,
                                                                                                        waa_1600_16x16_stay_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    load_7030_small, avgdelay_7030_small, _, _, _ = clean_load_delays(waa_800_16x16_stay_7030_e2e_load_total_bps_avg,
                                                                                                        waa_800_16x16_stay_7030_e2e_delay_total_avg,
                                                                                                        waa_800_16x16_stay_7030_e2e_delay_high_avg,
                                                                                                        waa_800_16x16_stay_7030_e2e_delay_med_avg,
                                                                                                        waa_800_16x16_stay_7030_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    load_7030_big, avgdelay_7030_big, _, _, _ = clean_load_delays(waa_1600_16x16_stay_7030_e2e_load_total_bps_avg,
                                                                                                        waa_1600_16x16_stay_7030_e2e_delay_total_avg,
                                                                                                        waa_1600_16x16_stay_7030_e2e_delay_high_avg,
                                                                                                        waa_1600_16x16_stay_7030_e2e_delay_med_avg,
                                                                                                        waa_1600_16x16_stay_7030_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    load_6040_small, avgdelay_6040_small, _, _, _ = clean_load_delays(waa_800_16x16_stay_6040_e2e_load_total_bps_avg,
                                                                                                        waa_800_16x16_stay_6040_e2e_delay_total_avg,
                                                                                                        waa_800_16x16_stay_6040_e2e_delay_high_avg,
                                                                                                        waa_800_16x16_stay_6040_e2e_delay_med_avg,
                                                                                                        waa_800_16x16_stay_6040_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    load_6040_big, avgdelay_6040_big, _, _, _ = clean_load_delays(waa_1600_16x16_stay_6040_e2e_load_total_bps_avg,
                                                                                                        waa_1600_16x16_stay_6040_e2e_delay_total_avg,
                                                                                                        waa_1600_16x16_stay_6040_e2e_delay_high_avg,
                                                                                                        waa_1600_16x16_stay_6040_e2e_delay_med_avg,
                                                                                                        waa_1600_16x16_stay_6040_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)
    # merge 2 datasets
    load_8020=load_8020_small[_8020_zero_rm_factor:_8020_small_rm_factor]+load_8020_big[_8020_big_rm_factor:]
    avgdelay_8020=avgdelay_8020_small[_8020_zero_rm_factor:_8020_small_rm_factor]+avgdelay_8020_big[_8020_big_rm_factor:]
    load_7030=load_7030_small[_7030_zero_rm_factor:_7030_small_rm_factor]+load_7030_big[_7030_big_rm_factor:]
    avgdelay_7030=avgdelay_7030_small[_7030_zero_rm_factor:_7030_small_rm_factor]+avgdelay_7030_big[_7030_big_rm_factor:]
    load_6040=load_6040_small[_6040_zero_rm_factor:_6040_small_rm_factor]+load_6040_big[_6040_big_rm_factor:]
    avgdelay_6040=avgdelay_6040_small[_6040_zero_rm_factor:_6040_small_rm_factor]+avgdelay_6040_big[_6040_big_rm_factor:]


    # dbg
    print('load_8020_small=' + str(load_8020_small))
    print('load_8020_big=' + str(load_8020_big))
    print('load_8020='+str(load_8020))
    print('load_7030_small=' + str(load_7030_small))
    print('load_7030_big=' + str(load_7030_big))
    print('load_7030='+str(load_7030))
    print('load_6040_small=' + str(load_6040_small))
    print('load_6040_big=' + str(load_6040_big))
    print('load_6040='+str(load_6040))


    #plot
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.semilogy(load_6040, avgdelay_6040, 'k', label="intra=60%,inter=40%", linewidth=5,
                 linestyle='dashdot')
    ax1.semilogy(load_7030, avgdelay_7030, 'k', label="intra=70%,inter=30%", linewidth=5,
                 linestyle='dashed')
    ax1.semilogy(load_8020, avgdelay_8020, 'k', label="intra=80%,inter=20%", linewidth=5,
                 linestyle='solid')


    ax1.set_xlabel(_x_label, fontsize=_LABEL_SIZE)
    ax1.set_ylabel(_y_label, fontsize=_LABEL_SIZE)
    ax1.set_xlim(_x_lim_begin,_x_lim_end)
    ax1.set_ylim(_y_lim_begin, _y_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()

def plot07_16xN_stay_8020_server_thru():
    _cleaning_factor=1e9
    _16_small_rm_factor=-1
    _16_big_rm_factor=5
    _24_small_rm_factor=-1
    _24_big_rm_factor=5
    _32_small_rm_factor=-1
    _32_big_rm_factor=5
    _x_lim_begin, _x_lim_end=-0.1,450
    _x_label,_y_label='Intra-rack load (Gbps)','Throughput per server (Gbps)'

    _LINEWIDTH = 7
    _LEGEND_SIZE = 30
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'upper left'


    load_16_small,thru_16_small,_=clean_load_thru_drop(waa_800_16x16_stay_8020_intra_load_total_bps_avg,
                                                          waa_800_16x16_stay_8020_intra_thru_total_bps_avg,
                                                          waa_800_16x16_stay_8020_intra_drop_total_bps_avg,
                                                          cleaning_factor=_cleaning_factor)

    load_16_big, thru_16_big, _ = clean_load_thru_drop(waa_1600_16x16_stay_8020_intra_load_total_bps_avg,
                                                        waa_1600_16x16_stay_8020_intra_thru_total_bps_avg,
                                                        waa_1600_16x16_stay_8020_intra_drop_total_bps_avg,
                                                        cleaning_factor=_cleaning_factor)

    load_24_small,thru_24_small,_=clean_load_thru_drop(waa_1200_16x24_stay_8020_intra_load_total_bps_avg,
                                                          waa_1200_16x24_stay_8020_intra_thru_total_bps_avg,
                                                          waa_1200_16x24_stay_8020_intra_drop_total_bps_avg,
                                                          cleaning_factor=_cleaning_factor)

    load_24_big, thru_24_big, _ = clean_load_thru_drop(waa_2400_16x24_stay_8020_intra_load_total_bps_avg,
                                                        waa_2400_16x24_stay_8020_intra_thru_total_bps_avg,
                                                        waa_2400_16x24_stay_8020_intra_drop_total_bps_avg,
                                                        cleaning_factor=_cleaning_factor)

    load_32_small,thru_32_small,_=clean_load_thru_drop(waa_1600_16x32_stay_8020_intra_load_total_bps_avg,
                                                          waa_1600_16x32_stay_8020_intra_thru_total_bps_avg,
                                                          waa_1600_16x32_stay_8020_intra_drop_total_bps_avg,
                                                          cleaning_factor=_cleaning_factor)

    load_32_big, thru_32_big, _ = clean_load_thru_drop(waa_3200_16x32_stay_8020_intra_load_total_bps_avg,
                                                        waa_3200_16x32_stay_8020_intra_thru_total_bps_avg,
                                                        waa_3200_16x32_stay_8020_intra_drop_total_bps_avg,
                                                        cleaning_factor=_cleaning_factor)
    # merge 2 datasets
    load_16=load_16_small[:_16_small_rm_factor]+load_16_big[_16_big_rm_factor:]
    thru_16 = thru_16_small[:_16_small_rm_factor] + thru_16_big[_16_big_rm_factor:]
    load_24=load_24_small[:_24_small_rm_factor]+load_24_big[_24_big_rm_factor:]
    thru_24 = thru_24_small[:_24_small_rm_factor] + thru_24_big[_24_big_rm_factor:]
    load_32=load_32_small[:_32_small_rm_factor]+load_32_big[_32_big_rm_factor:]
    thru_32 = thru_32_small[:_32_small_rm_factor] + thru_32_big[_32_big_rm_factor:]

    # dbg
    print('load_16_small='+str(load_16_small))
    print('load_16_big=' + str(load_16_big))
    print('load_16=' + str(load_16))
    print('thru_16=' + str(thru_16))
    print('load_24_small='+str(load_24_small))
    print('load_24_big=' + str(load_24_big))
    print('load_24=' + str(load_24))
    print('load_32_small='+str(load_32_small))
    print('load_32_big=' + str(load_32_big))
    print('load_32=' + str(load_32))

    # Activate thru/drop averaging
    thru_16=[x/16 for x in thru_16]
    thru_24=[x/24 for x in thru_24]
    thru_32=[x/32 for x in thru_32]


    #plot
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)
    ax1.plot(load_16, thru_16, 'b', label="N=16", linewidth=_LINEWIDTH)
    ax1.plot(load_24, thru_24, 'b--', label="N=24", linewidth=_LINEWIDTH)
    ax1.plot(load_32, thru_32, 'b-.', label="N=32", linewidth=_LINEWIDTH)


    ax1.set_xlabel(_x_label, fontsize=_LABEL_SIZE)
    ax1.set_ylabel(_y_label, fontsize=_LABEL_SIZE)
    ax1.set_xlim(_x_lim_begin,_x_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()

def plot08_16xN_stay_8020_e2e_delays():
    _cleaning_factor=1e12
    _16_zero_rm_factor=1
    _16_small_rm_factor=-3
    _16_big_rm_factor=3
    _24_zero_rm_factor=1
    _24_small_rm_factor=-3
    _24_big_rm_factor=2
    _32_zero_rm_factor=2
    _32_small_rm_factor=-3
    _32_big_rm_factor=3
    _x_lim_begin, _x_lim_end=2,10
    _y_lim_begin,_y_lim_end=1e-4,1
    _x_label,_y_label='Total load (Tbps)','End-to-end delay (ms)'

    _LINEWIDTH = 7
    _LEGEND_SIZE = 30
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'center right'

    load_16_small, avgdelay_16_small, _, _, _ = clean_load_delays(waa_800_16x16_stay_8020_e2e_load_total_bps_avg,
                                                                                                        waa_800_16x16_stay_8020_e2e_delay_total_avg,
                                                                                                        waa_800_16x16_stay_8020_e2e_delay_high_avg,
                                                                                                        waa_800_16x16_stay_8020_e2e_delay_med_avg,
                                                                                                        waa_800_16x16_stay_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    load_16_big, avgdelay_16_big, _, _, _ = clean_load_delays(waa_1600_16x16_stay_8020_e2e_load_total_bps_avg,
                                                                                                        waa_1600_16x16_stay_8020_e2e_delay_total_avg,
                                                                                                        waa_1600_16x16_stay_8020_e2e_delay_high_avg,
                                                                                                        waa_1600_16x16_stay_8020_e2e_delay_med_avg,
                                                                                                        waa_1600_16x16_stay_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    load_24_small, avgdelay_24_small, _, _, _ = clean_load_delays(waa_1200_16x24_stay_8020_e2e_load_total_bps_avg,
                                                                                                        waa_1200_16x24_stay_8020_e2e_delay_total_avg,
                                                                                                        waa_1200_16x24_stay_8020_e2e_delay_high_avg,
                                                                                                        waa_1200_16x24_stay_8020_e2e_delay_med_avg,
                                                                                                        waa_1200_16x24_stay_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    load_24_big, avgdelay_24_big, _, _, _ = clean_load_delays(waa_2400_16x24_stay_8020_e2e_load_total_bps_avg,
                                                                                                        waa_2400_16x24_stay_8020_e2e_delay_total_avg,
                                                                                                        waa_2400_16x24_stay_8020_e2e_delay_high_avg,
                                                                                                        waa_2400_16x24_stay_8020_e2e_delay_med_avg,
                                                                                                        waa_2400_16x24_stay_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    load_32_small, avgdelay_32_small, _, _, _ = clean_load_delays(waa_1200_16x24_stay_8020_e2e_load_total_bps_avg,
                                                                                                        waa_1600_16x32_stay_8020_e2e_delay_total_avg,
                                                                                                        waa_1600_16x32_stay_8020_e2e_delay_high_avg,
                                                                                                        waa_1600_16x32_stay_8020_e2e_delay_med_avg,
                                                                                                        waa_1600_16x32_stay_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    load_32_big, avgdelay_32_big, _, _, _ = clean_load_delays(waa_3200_16x32_stay_8020_e2e_load_total_bps_avg,
                                                                                                        waa_3200_16x32_stay_8020_e2e_delay_total_avg,
                                                                                                        waa_3200_16x32_stay_8020_e2e_delay_high_avg,
                                                                                                        waa_3200_16x32_stay_8020_e2e_delay_med_avg,
                                                                                                        waa_3200_16x32_stay_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    # merge 2 datasets
    load_16=load_16_small[_16_zero_rm_factor:_16_small_rm_factor]+load_16_big[_16_big_rm_factor:]
    avgdelay_16=avgdelay_16_small[_16_zero_rm_factor:_16_small_rm_factor]+avgdelay_16_big[_16_big_rm_factor:]
    load_24=load_24_small[_24_zero_rm_factor:_24_small_rm_factor]+load_24_big[_24_big_rm_factor:]
    avgdelay_24=avgdelay_24_small[_24_zero_rm_factor:_24_small_rm_factor]+avgdelay_24_big[_24_big_rm_factor:]
    load_32=load_32_small[_32_zero_rm_factor:_32_small_rm_factor]+load_32_big[_32_big_rm_factor:]
    avgdelay_32=avgdelay_32_small[_32_zero_rm_factor:_32_small_rm_factor]+avgdelay_32_big[_32_big_rm_factor:]


    # dbg
    print('load_16_small=' + str(load_16_small))
    print('load_16_big=' + str(load_16_big))
    print('load_16='+str(load_16))
    print('load_24_small=' + str(load_24_small))
    print('load_24_big=' + str(load_24_big))
    print('load_24='+str(load_24))
    print('load_32_small=' + str(load_32_small))
    print('load_32_big=' + str(load_32_big))
    print('load_32='+str(load_32))
    print('avgdelay_32=' + str(avgdelay_32))


    #plot
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.semilogy(load_16, avgdelay_16, 'b', label="N=16", linewidth=_LINEWIDTH)
    ax1.semilogy(load_24, avgdelay_24, 'b--', label="N=24", linewidth=_LINEWIDTH)
    ax1.semilogy(load_32, avgdelay_32, 'b-.', label="N=32", linewidth=_LINEWIDTH)

    ax1.set_xlabel(_x_label, fontsize=_LABEL_SIZE)
    ax1.set_ylabel(_y_label, fontsize=_LABEL_SIZE)
    ax1.set_xlim(_x_lim_begin,_x_lim_end)
    ax1.set_ylim(_y_lim_begin, _y_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()


def plot10_calabr_thru():
    _cleaning_factor=1e12
    _small_rm_factor=-2
    _big_rm_factor=4
    _x_lim_begin, _x_lim_end=-0.1,1.5
    _x_label,_y_label='Normalized load','Normalized throughput'
    _nominal_thru=16*0.4+16*0.1
    _LINEWIDTH = 7
    _LEGEND_SIZE = 30
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'center right'


    load_small,thru_small,_=clean_load_thru_drop(waa_400_16x8_go_8020_e2e_load_total_bps_avg,
                                                          waa_400_16x8_go_8020_e2e_thru_total_bps_avg,
                                                          waa_400_16x8_go_8020_e2e_drop_total_bps_avg,
                                                          cleaning_factor=_cleaning_factor)

    load_big, thru_big, _ = clean_load_thru_drop(waa_800_16x8_go_8020_e2e_load_total_bps_avg,
                                                        waa_800_16x8_go_8020_e2e_thru_total_bps_avg,
                                                        waa_800_16x8_go_8020_e2e_drop_total_bps_avg,
                                                        cleaning_factor=_cleaning_factor)

    # merge 2 datasets
    load=load_small[:_small_rm_factor]+load_big[_big_rm_factor:]
    thru = thru_small[:_small_rm_factor] + thru_big[_big_rm_factor:]
    norm_load=[x/_nominal_thru for x in load]
    norm_thru = [x / _nominal_thru for x in thru]
    # dbg
    print('load_small=' + str(load_small))
    print('load_big=' + str(load_big))
    print('load='+str(load))
    print('thru='+str(thru))
    print('norm_load'+str(norm_load))
    print('norm_thru' + str(norm_thru))

    # calabreta
    cal_load=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    cal_thru=[0.1,0.2,0.3,0.4,0.5,0.6,0.65,0.7,0.7,0.7]

    #plot
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.plot(norm_load, norm_thru,'b', label="Throughput 16x8",linewidth=_LINEWIDTH)
    ax1.plot(cal_load, cal_thru, 'r', label="Calabretta", linewidth=_LINEWIDTH)


    ax1.set_xlabel(_x_label, fontsize=_LABEL_SIZE)
    ax1.set_ylabel(_y_label, fontsize=_LABEL_SIZE)
    ax1.set_xlim(_x_lim_begin,_x_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()

def plot11_calabr_delay():
    _comparison_date=2021
    _cleaning_factor=1e12
    _zero_rm_factor=1
    _small_rm_factor=-2
    _big_rm_factor=4
    _x_lim_begin, _x_lim_end=-0.1,1
    _y_lim_begin,_y_lim_end=1e-4,1
    _x_label,_y_label='Normalized load','Latency (ms)'
    _nominal_thru = 16 * 0.4 + 16 * 0.1

    _LINEWIDTH = 7
    _LEGEND_SIZE = 30
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'center right'

    load_small, avg_delay_small, high_delay_small, med_delay_small, low_delay_small = clean_load_delays(waa_400_16x8_go_8020_e2e_load_total_bps_avg,
                                                                                                        waa_400_16x8_go_8020_e2e_delay_total_avg,
                                                                                                        waa_400_16x8_go_8020_e2e_delay_high_avg,
                                                                                                        waa_400_16x8_go_8020_e2e_delay_med_avg,
                                                                                                        waa_400_16x8_go_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    load_big, avg_delay_big, high_delay_big, med_delay_big, low_delay_big = clean_load_delays(
        waa_800_16x8_go_8020_e2e_load_total_bps_avg,
        waa_800_16x8_go_8020_e2e_delay_total_avg,
        waa_800_16x8_go_8020_e2e_delay_high_avg,
        waa_800_16x8_go_8020_e2e_delay_med_avg,
        waa_800_16x8_go_8020_e2e_delay_low_avg,
        cleaning_factor=_cleaning_factor)

    # merge 2 datasets
    load=load_small[_zero_rm_factor:_small_rm_factor]+load_big[_big_rm_factor:]
    avg_delay=avg_delay_small[_zero_rm_factor:_small_rm_factor]+avg_delay_big[_big_rm_factor:]

    # normalize
    norm_load = [x / _nominal_thru for x in load]

    # calabreta
    cal_load = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    if _comparison_date==2022:
        cal_avg_delay=[4e-3,5e-3,6e-3,7e-3,8e-3,9e-3,10e-3,20e-3,45e-3,53e-3] # ms
        cal_drop_prob=[0,0,7e-5,4e-4,1e-3,1.5e-3,2e-3,3e-3,3e-2,7e-2]
    else:
        cal_avg_delay=[7.5e-3,7.5e-3,7.5e-3,7.5e-3,7.5e-3,8e-3,9e-3,12.5e-3,21e-3,29e-3] # ms
        cal_drop_prob=[0,0,0,0,0.007,0.010,0.012,0.025,0.06,0.105]

    # dbg
    print('load_small=' + str(load_small))
    print('load_big=' + str(load_big))
    print('load='+str(load))


    #plot
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.semilogy(norm_load, avg_delay, 'b', label="Ours 16x8", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(cal_load, cal_avg_delay, 'r', label="Calabretta", linewidth=_LINEWIDTH)

    ax1.set_xlabel(_x_label, fontsize=_LABEL_SIZE)
    ax1.set_ylabel(_y_label, fontsize=_LABEL_SIZE)
    ax1.set_xlim(_x_lim_begin,_x_lim_end)
    ax1.set_ylim(_y_lim_begin, _y_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()

def plot12_calabr_loss():
    _comparison_date=2021
    _cleaning_factor=1e12
    _zero_rm_factor=1
    _small_rm_factor=-2
    _big_rm_factor=4
    _x_lim_begin, _x_lim_end=-0.1,1
    _y_lim_begin,_y_lim_end=1e-4,1
    _x_label,_y_label='Normalized load','Packet loss'
    _nominal_thru = 16 * 0.4 + 16 * 0.1

    _LINEWIDTH = 7
    _LEGEND_SIZE = 30
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'center right'

    load_small, thru_small, drop_small, drop_prob_avg_small, drop_prob_high_small, drop_prob_med_small, drop_prob_low_small = clean_load_thru_drop_prob \
        (waa_400_16x8_go_8020_e2e_load_total_bps_avg, waa_400_16x8_go_8020_e2e_thru_total_bps_avg, waa_400_16x8_go_8020_e2e_drop_total_bps_avg,
         waa_400_16x8_go_8020_e2e_drop_prob_total_avg, waa_400_16x8_go_8020_e2e_drop_prob_high_avg, waa_400_16x8_go_8020_e2e_drop_prob_med_avg,
         waa_400_16x8_go_8020_e2e_drop_prob_low_avg, cleaning_factor=1e12)

    load_big, thru_big, drop_big, drop_prob_avg_big, drop_prob_high_big, drop_prob_med_big, drop_prob_low_big = clean_load_thru_drop_prob \
        (waa_800_16x8_go_8020_e2e_load_total_bps_avg, waa_800_16x8_go_8020_e2e_thru_total_bps_avg, waa_800_16x8_go_8020_e2e_drop_total_bps_avg,
         waa_800_16x8_go_8020_e2e_drop_prob_total_avg, waa_800_16x8_go_8020_e2e_drop_prob_high_avg, waa_800_16x8_go_8020_e2e_drop_prob_med_avg,
         waa_800_16x8_go_8020_e2e_drop_prob_low_avg, cleaning_factor=1e12)

    # merge 2 datasets
    load=load_small[_zero_rm_factor:_small_rm_factor]+load_big[_big_rm_factor:]
    drop_prob_avg=drop_prob_avg_small[_zero_rm_factor:_small_rm_factor]+drop_prob_avg_big[_big_rm_factor:]

    # normalize
    norm_load = [x / _nominal_thru for x in load]

    # calabreta
    cal_load = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    if _comparison_date==2022:
        cal_avg_delay=[4e-3,5e-3,6e-3,7e-3,8e-3,9e-3,10e-3,20e-3,45e-3,53e-3] # ms
        cal_drop_prob=[0,0,7e-5,4e-4,1e-3,1.5e-3,2e-3,3e-3,3e-2,7e-2]
    else:
        cal_avg_delay=[7.5e-3,7.5e-3,7.5e-3,7.5e-3,7.5e-3,8e-3,9e-3,12.5e-3,21e-3,29e-3] # ms
        cal_drop_prob=[0,0,0,0,0.007,0.010,0.012,0.025,0.06,0.105]

    # dbg
    print('load_small=' + str(load_small))
    print('load_big=' + str(load_big))
    print('load='+str(load))

    #plot
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.plot(norm_load, drop_prob_avg, 'b', label="Ours 16x8", linewidth=_LINEWIDTH + 1)
    ax1.plot(cal_load, cal_drop_prob, 'r', label="Calabretta", linewidth=_LINEWIDTH)

    ax1.set_xlabel(_x_label, fontsize=_LABEL_SIZE)
    ax1.set_ylabel(_y_label, fontsize=_LABEL_SIZE)
    ax1.set_xlim(_x_lim_begin,_x_lim_end)
    ax1.set_ylim(_y_lim_begin, _y_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()

#plot01_16x16_go_8020_intra_thru()
#plot02_16x16_go_8020_inter_thru()
#plot03_16x16_go_8020_e2e_thru()
#plot04_16x16_go_8020_e2e_delays()

#prep_plot05_16x16_stay_8020_e2e_delays()
#plot05_16x16_stay_8020_e2e_delays()
#plot06_16x16_stay_traffic_e2e_delays()

#plot07_16xN_stay_8020_server_thru()
#plot08_16xN_stay_8020_e2e_delays()
###plot09_16xN_stay_8020_e2e_delays() todooo

#plot10_calabr_thru()
#plot11_calabr_delay()
plot12_calabr_loss()