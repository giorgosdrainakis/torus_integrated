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
#from torus_integrated.plotters.jocn_split_data07_1200_16x24_stay_8020 import *
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
from torus_integrated.plotters.jocn_split_data24_1600_16x8_go_8020 import *
from torus_integrated.plotters.jocn_split_data25_400_16x8_go_8020 import *
from torus_integrated.plotters.jocn_split_data26_1600_16x8_go_8020 import *

from torus_integrated.plotters.jocn_split_data31_1200_16x24_stay_8020 import *
from torus_integrated.plotters.jocn_split_data41_1200_16x24_go_8020 import *
from torus_integrated.plotters.jocn_split_data42_1600_16x32_go_8020 import *
from torus_integrated.plotters.jocn_split_data43_800_16x24_go_8020 import *
from torus_integrated.plotters.jocn_split_data44_800_16x32_go_8020 import *

from torus_integrated.plotters.jocn_split_data45_800_16x24_stay_8020 import *
from torus_integrated.plotters.jocn_split_data46_800_16x32_stay_8020 import *
from torus_integrated.plotters.jocn_split_data51_200_16x8_go_8020 import *
from torus_integrated.plotters.jocn_split_data52_600_16x8_go_8020 import *

if True:
    del waa_1600_16x16_stay_8020_intra_load_total_bps_avg[12]
    del waa_1600_16x16_stay_8020_intra_thru_total_bps_avg[12]
    del waa_1600_16x16_stay_8020_intra_drop_total_bps_avg[12]
    del waa_1600_16x16_stay_8020_intra_load_total_bps_avg[-1]
    del waa_1600_16x16_stay_8020_intra_thru_total_bps_avg[-1]
    del waa_1600_16x16_stay_8020_intra_drop_total_bps_avg[-1]
    del waa_1600_16x16_stay_8020_intra_load_total_bps_avg[-9]
    del waa_1600_16x16_stay_8020_intra_thru_total_bps_avg[-9]
    del waa_1600_16x16_stay_8020_intra_drop_total_bps_avg[-9]
    del waa_1600_16x16_stay_8020_intra_load_total_bps_avg[-9]
    del waa_1600_16x16_stay_8020_intra_thru_total_bps_avg[-9]
    del waa_1600_16x16_stay_8020_intra_drop_total_bps_avg[-9]

    del waa_1600_16x16_go_8020_intra_load_total_bps_avg[14:17]
    del waa_1600_16x16_go_8020_intra_thru_total_bps_avg[14:17]
    del waa_1600_16x16_go_8020_intra_drop_total_bps_avg[14:17]
    del waa_1600_16x16_go_8020_intra_load_total_bps_avg[12]
    del waa_1600_16x16_go_8020_intra_thru_total_bps_avg[12]
    del waa_1600_16x16_go_8020_intra_drop_total_bps_avg[12]


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
    _small_rm_factor=-5
    _big_rm_factor=4
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
    _x_label,_y_label='Total load (Tbps)','End-to-end latency (ms)'

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

    ax1.semilogy(load, avg_delay, 'b', label="Total packet latency", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(qload, avg_qdelay, 'r', label="Queuing latency", linewidth=_LINEWIDTH)

    ax1.set_xlabel(_x_label, fontsize=_LABEL_SIZE)
    ax1.set_ylabel(_y_label, fontsize=_LABEL_SIZE)
    ax1.set_xlim(_x_lim_begin,_x_lim_end)
    ax1.set_ylim(_y_lim_begin, _y_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()


def calc_review_cdf_16x16_go_8020_e2e_delay():
    _cleaning_factor=1e12
    _zero_rm_factor=1
    _small_rm_factor=-2
    _big_rm_factor=2
    _x_lim_begin, _x_lim_end=2,10
    _y_lim_begin,_y_lim_end=1e-3,1e-1

    load_small, avg_delay_small, high_delay_small, med_delay_small, low_delay_small = clean_load_delays(waa_800_16x16_go_8020_e2e_load_total_bps_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_delay_total_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_delay_high_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_delay_med_avg,
                                                                                                        waa_800_16x16_go_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    load_big, avg_delay_big, high_delay_big, med_delay_big, low_delay_big = clean_load_delays(
        waa_1600_16x16_go_8020_e2e_load_total_bps_avg,
        waa_1600_16x16_go_8020_e2e_delay_total_avg,
        waa_1600_16x16_go_8020_e2e_delay_high_avg,
        waa_1600_16x16_go_8020_e2e_delay_med_avg,
        waa_1600_16x16_go_8020_e2e_delay_low_avg,
        cleaning_factor=_cleaning_factor)

    # merge 2 datasets
    load=load_small[_zero_rm_factor:_small_rm_factor]+load_big[_big_rm_factor:]
    avg_delay=avg_delay_small[_zero_rm_factor:_small_rm_factor]+avg_delay_big[_big_rm_factor:]
    high_delay=high_delay_small[_zero_rm_factor:_small_rm_factor]+high_delay_big[_big_rm_factor:]
    med_delay=med_delay_small[_zero_rm_factor:_small_rm_factor]+med_delay_big[_big_rm_factor:]
    low_delay=low_delay_small[_zero_rm_factor:_small_rm_factor]+low_delay_big[_big_rm_factor:]

    # dbg
    print('load='+str(load))
    print('avg_delay='+str(avg_delay))
    print('high_delay='+str(avg_delay))
    print('med_delay='+str(avg_delay))
    print('low_delay='+str(avg_delay))


def prep_plot05_16x16_stay_8020_e2e_delays():
    _cleaning_factor=1e12
    _zero_rm_factor=1
    _stay_small_rm_factor=-2
    _stay_big_rm_factor=2
    _go_small_rm_factor=-2
    _go_big_rm_factor=2
    _x_lim_begin, _x_lim_end=2,10
    _y_lim_begin,_y_lim_end=1e-4,1
    _x_label,_y_label='Total load (Tbps)','End-to-end latency (ms)'

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
    y_label='End-to-end latency (ms)'
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
        hh=high_go[i]*1e3
        mm = med_go[i]*1e3
        ll = low_go[i]*1e3
        print('Load='+str(load[i]))
        print('high in us='+str(hh))
        print('med in us=' + str(mm))
        print('low in us=' + str(ll))
        print('----')

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
    _x_label,_y_label='Total load (Tbps)','End-to-end latency (ms)'

    _LINEWIDTH = 7
    _LEGEND_SIZE = 35
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'lower right'

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

    _geo_load = [3, 4, 6, 8]
    _geo_8020 = [0.0016, 0.0044, 0.025, 0.072]
    _geo_7030 = [0.0031, 0.017, 0.070, 0.118]
    _geo_6040 = [0.019, 0.067, 0.128, 0.15]
    for i in range(len(_geo_load)):
        print('Load='+str(_geo_load[i]))
        print('% 7030 increase' + str((100*(_geo_7030[i]-_geo_8020[i]))/_geo_8020[i]))
        print('% 6040 increase' + str((100*(_geo_6040[i]-_geo_8020[i]))/_geo_8020[i]))


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

def plot07_16xN_stay_8020_server_thru(zmall='half'):
    _cleaning_factor=1e9
    _16_small_rm_factor=-9
    _16_big_rm_factor=1
    _24_small_rm_factor=-9
    _24_big_rm_factor=1
    _32_small_rm_factor=-9
    _32_big_rm_factor=1
    _x_lim_begin, _x_lim_end=-0.1,450
    _x_label,_y_label='Intra-rack load (Gbps)','Throughput per server (Gbps)'

    _LINEWIDTH = 7
    _LEGEND_SIZE = 50
    _X_TICK_PARAMS=45
    _Y_TICK_PARAMS=45
    _X_LABEL_SIZE = 45
    _Y_LABEL_SIZE = 35
    _LEGEND_LOC = 'upper left'


    load_16_small,thru_16_small,_=clean_load_thru_drop(waa_800_16x16_stay_8020_intra_load_total_bps_avg,
                                                          waa_800_16x16_stay_8020_intra_thru_total_bps_avg,
                                                          waa_800_16x16_stay_8020_intra_drop_total_bps_avg,
                                                          cleaning_factor=_cleaning_factor)

    load_16_big, thru_16_big, _ = clean_load_thru_drop(waa_1600_16x16_stay_8020_intra_load_total_bps_avg,
                                                        waa_1600_16x16_stay_8020_intra_thru_total_bps_avg,
                                                        waa_1600_16x16_stay_8020_intra_drop_total_bps_avg,
                                                        cleaning_factor=_cleaning_factor)
    if zmall == 'half':
        load_24_small,thru_24_small,_=clean_load_thru_drop(waa_1200_16x24_stay_8020_intra_load_total_bps_avg,
                                                              waa_1200_16x24_stay_8020_intra_thru_total_bps_avg,
                                                              waa_1200_16x24_stay_8020_intra_drop_total_bps_avg,
                                                              cleaning_factor=_cleaning_factor)
    elif zmall =='800':
        load_24_small,thru_24_small,_=clean_load_thru_drop(waa_800_16x24_stay_8020_intra_load_total_bps_avg,
                                                              waa_800_16x24_stay_8020_intra_thru_total_bps_avg,
                                                              waa_800_16x24_stay_8020_intra_drop_total_bps_avg,
                                                              cleaning_factor=_cleaning_factor)

    load_24_big, thru_24_big, _ = clean_load_thru_drop(waa_2400_16x24_stay_8020_intra_load_total_bps_avg,
                                                        waa_2400_16x24_stay_8020_intra_thru_total_bps_avg,
                                                        waa_2400_16x24_stay_8020_intra_drop_total_bps_avg,
                                                        cleaning_factor=_cleaning_factor)

    if zmall == 'half':
        load_32_small,thru_32_small,_=clean_load_thru_drop(waa_1600_16x32_stay_8020_intra_load_total_bps_avg,
                                                              waa_1600_16x32_stay_8020_intra_thru_total_bps_avg,
                                                              waa_1600_16x32_stay_8020_intra_drop_total_bps_avg,
                                                              cleaning_factor=_cleaning_factor)
    elif zmall =='800':
        load_32_small,thru_32_small,_=clean_load_thru_drop(waa_800_16x32_stay_8020_intra_load_total_bps_avg,
                                                              waa_800_16x32_stay_8020_intra_thru_total_bps_avg,
                                                              waa_800_16x32_stay_8020_intra_drop_total_bps_avg,
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


    ax1.set_xlabel(_x_label, fontsize=_X_LABEL_SIZE)
    ax1.set_ylabel(_y_label, fontsize=_Y_LABEL_SIZE)
    ax1.set_xlim(_x_lim_begin,_x_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_X_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_Y_TICK_PARAMS)
    plt.show()

def plot08_16xN_stay_8020_e2e_delays(zmall='half'):
    _cleaning_factor=1e12
    _16_zero_rm_factor=1
    _16_small_rm_factor=-1
    _16_big_rm_factor=4
    _24_zero_rm_factor=1
    _24_small_rm_factor=-4
    _24_big_rm_factor=1
    _32_zero_rm_factor=3
    _32_small_rm_factor=-3
    _32_big_rm_factor=1
    _x_lim_begin, _x_lim_end=3.3,10
    _y_lim_begin,_y_lim_end=1e-3,1
    _x_label,_y_label='Total load (Tbps)','End-to-end latency (ms)'

    _LINEWIDTH = 7
    _LEGEND_SIZE = 50
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'lower right'

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

    if zmall == 'half':
        load_24_small, avgdelay_24_small, _, _, _ = clean_load_delays(waa_1200_16x24_stay_8020_e2e_load_total_bps_avg,
                                                                        waa_1200_16x24_stay_8020_e2e_delay_total_avg,
                                                                        waa_1200_16x24_stay_8020_e2e_delay_high_avg,
                                                                        waa_1200_16x24_stay_8020_e2e_delay_med_avg,
                                                                        waa_1200_16x24_stay_8020_e2e_delay_low_avg,
                                                                                    cleaning_factor=_cleaning_factor)
    elif zmall=='800':
        load_24_small, avgdelay_24_small, _, _, _ = clean_load_delays(waa_800_16x24_stay_8020_e2e_load_total_bps_avg,
                                                                        waa_800_16x24_stay_8020_e2e_delay_total_avg,
                                                                        waa_800_16x24_stay_8020_e2e_delay_high_avg,
                                                                        waa_800_16x24_stay_8020_e2e_delay_med_avg,
                                                                        waa_800_16x24_stay_8020_e2e_delay_low_avg,
                                                                                    cleaning_factor=_cleaning_factor)

    load_24_big, avgdelay_24_big, _, _, _ = clean_load_delays(waa_2400_16x24_stay_8020_e2e_load_total_bps_avg,
                                                            waa_2400_16x24_stay_8020_e2e_delay_total_avg,
                                                            waa_2400_16x24_stay_8020_e2e_delay_high_avg,
                                                            waa_2400_16x24_stay_8020_e2e_delay_med_avg,
                                                            waa_2400_16x24_stay_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    if zmall == 'half':
        load_32_small, avgdelay_32_small, _, _, _ = clean_load_delays(waa_1600_16x32_stay_8020_e2e_load_total_bps_avg,
                                                                    waa_1600_16x32_stay_8020_e2e_delay_total_avg,
                                                                    waa_1600_16x32_stay_8020_e2e_delay_high_avg,
                                                                    waa_1600_16x32_stay_8020_e2e_delay_med_avg,
                                                                    waa_1600_16x32_stay_8020_e2e_delay_low_avg,
                                                                                    cleaning_factor=_cleaning_factor)
    elif zmall=='800':
        load_32_small, avgdelay_32_small, _, _, _ = clean_load_delays(waa_800_16x32_stay_8020_e2e_load_total_bps_avg,
                                                                    waa_800_16x32_stay_8020_e2e_delay_total_avg,
                                                                    waa_800_16x32_stay_8020_e2e_delay_high_avg,
                                                                    waa_800_16x32_stay_8020_e2e_delay_med_avg,
                                                                    waa_800_16x32_stay_8020_e2e_delay_low_avg,
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
    print('avgdelay_16=' + str(avgdelay_16))
    print('load_24_small=' + str(load_24_small))
    print('load_24_big=' + str(load_24_big))
    print('load_24='+str(load_24))
    print('avgdelay_24=' + str(avgdelay_24))
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

def plot07_16xN_go_8020_server_thru(zmall='half'):
    _cleaning_factor=1e9
    _16_small_rm_factor=-5
    _16_big_rm_factor=3
    _24_small_rm_factor=-5
    _24_big_rm_factor=3
    _32_small_rm_factor=-5
    _32_big_rm_factor=3
    _x_lim_begin, _x_lim_end=-0.1,450
    _x_label,_y_label='Intra-rack load (Gbps)','Throughput per server (Gbps)'

    _LINEWIDTH = 7
    _LEGEND_SIZE = 30
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'upper left'


    load_16_small,thru_16_small,_=clean_load_thru_drop(waa_800_16x16_go_8020_intra_load_total_bps_avg,
                                                          waa_800_16x16_go_8020_intra_thru_total_bps_avg,
                                                          waa_800_16x16_go_8020_intra_drop_total_bps_avg,
                                                          cleaning_factor=_cleaning_factor)

    load_16_big, thru_16_big, _ = clean_load_thru_drop(waa_1600_16x16_go_8020_intra_load_total_bps_avg,
                                                        waa_1600_16x16_go_8020_intra_thru_total_bps_avg,
                                                        waa_1600_16x16_go_8020_intra_drop_total_bps_avg,
                                                        cleaning_factor=_cleaning_factor)

    if zmall=='half':
        load_24_small,thru_24_small,_=clean_load_thru_drop(waa_1200_16x24_go_8020_intra_load_total_bps_avg,
                                                              waa_1200_16x24_go_8020_intra_thru_total_bps_avg,
                                                              waa_1200_16x24_go_8020_intra_drop_total_bps_avg,
                                                              cleaning_factor=_cleaning_factor)
    elif zmall=='800':
        load_24_small,thru_24_small,_=clean_load_thru_drop(waa_800_16x24_go_8020_intra_load_total_bps_avg,
                                                              waa_800_16x24_go_8020_intra_thru_total_bps_avg,
                                                              waa_800_16x24_go_8020_intra_drop_total_bps_avg,
                                                              cleaning_factor=_cleaning_factor)

    load_24_big, thru_24_big, _ = clean_load_thru_drop(waa_2400_16x24_go_8020_intra_load_total_bps_avg,
                                                        waa_2400_16x24_go_8020_intra_thru_total_bps_avg,
                                                        waa_2400_16x24_go_8020_intra_drop_total_bps_avg,
                                                        cleaning_factor=_cleaning_factor)

    if zmall=='half':
        load_32_small,thru_32_small,_=clean_load_thru_drop(waa_1600_16x32_go_8020_intra_load_total_bps_avg,
                                                              waa_1600_16x32_go_8020_intra_thru_total_bps_avg,
                                                              waa_1600_16x32_go_8020_intra_drop_total_bps_avg,
                                                              cleaning_factor=_cleaning_factor)
    elif zmall=='800':
        load_32_small,thru_32_small,_=clean_load_thru_drop(waa_800_16x32_go_8020_intra_load_total_bps_avg,
                                                              waa_800_16x32_go_8020_intra_thru_total_bps_avg,
                                                              waa_800_16x32_go_8020_intra_drop_total_bps_avg,
                                                              cleaning_factor=_cleaning_factor)

    load_32_big, thru_32_big, _ = clean_load_thru_drop(waa_3200_16x32_go_8020_intra_load_total_bps_avg,
                                                        waa_3200_16x32_go_8020_intra_thru_total_bps_avg,
                                                        waa_3200_16x32_go_8020_intra_drop_total_bps_avg,
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

def plot08_16xN_go_8020_e2e_delays(zmall='half'):
    _cleaning_factor=1e12
    _16_zero_rm_factor=1
    _16_small_rm_factor=-4
    _16_big_rm_factor=1
    _24_zero_rm_factor=1
    _24_small_rm_factor=-2
    _24_big_rm_factor=1
    _32_zero_rm_factor=3
    _32_small_rm_factor=-1
    _32_big_rm_factor=1
    _x_lim_begin, _x_lim_end=2,10
    _y_lim_begin,_y_lim_end=1e-4,1
    _x_label,_y_label='Total load (Tbps)','End-to-end latency (ms)'

    _LINEWIDTH = 7
    _LEGEND_SIZE = 30
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'center right'

    load_16_small, avgdelay_16_small, _, _, _ = clean_load_delays(waa_800_16x16_go_8020_e2e_load_total_bps_avg,
                                                                waa_800_16x16_go_8020_e2e_delay_total_avg,
                                                                waa_800_16x16_go_8020_e2e_delay_high_avg,
                                                                waa_800_16x16_go_8020_e2e_delay_med_avg,
                                                                waa_800_16x16_go_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    load_16_big, avgdelay_16_big, _, _, _ = clean_load_delays(waa_1600_16x16_go_8020_e2e_load_total_bps_avg,
                                                                    waa_1600_16x16_go_8020_e2e_delay_total_avg,
                                                                    waa_1600_16x16_go_8020_e2e_delay_high_avg,
                                                                    waa_1600_16x16_go_8020_e2e_delay_med_avg,
                                                                    waa_1600_16x16_go_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)
    if zmall == 'half':
        load_24_small, avgdelay_24_small, _, _, _ = clean_load_delays(waa_1200_16x24_go_8020_e2e_load_total_bps_avg,
                                                                        waa_1200_16x24_go_8020_e2e_delay_total_avg,
                                                                        waa_1200_16x24_go_8020_e2e_delay_high_avg,
                                                                        waa_1200_16x24_go_8020_e2e_delay_med_avg,
                                                                        waa_1200_16x24_go_8020_e2e_delay_low_avg,
                                                                                    cleaning_factor=_cleaning_factor)
    elif zmall=='800':
        load_24_small, avgdelay_24_small, _, _, _ = clean_load_delays(waa_800_16x24_go_8020_e2e_load_total_bps_avg,
                                                                        waa_800_16x24_go_8020_e2e_delay_total_avg,
                                                                        waa_800_16x24_go_8020_e2e_delay_high_avg,
                                                                        waa_800_16x24_go_8020_e2e_delay_med_avg,
                                                                        waa_800_16x24_go_8020_e2e_delay_low_avg,
                                                                                    cleaning_factor=_cleaning_factor)

    load_24_big, avgdelay_24_big, _, _, _ = clean_load_delays(waa_2400_16x24_go_8020_e2e_load_total_bps_avg,
                                                            waa_2400_16x24_go_8020_e2e_delay_total_avg,
                                                            waa_2400_16x24_go_8020_e2e_delay_high_avg,
                                                            waa_2400_16x24_go_8020_e2e_delay_med_avg,
                                                            waa_2400_16x24_go_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    if zmall == 'half':
        load_32_small, avgdelay_32_small, _, _, _ = clean_load_delays(waa_1600_16x32_go_8020_e2e_load_total_bps_avg,
                                                                        waa_1600_16x32_go_8020_e2e_delay_total_avg,
                                                                        waa_1600_16x32_go_8020_e2e_delay_high_avg,
                                                                        waa_1600_16x32_go_8020_e2e_delay_med_avg,
                                                                        waa_1600_16x32_go_8020_e2e_delay_low_avg,
                                                                                    cleaning_factor=_cleaning_factor)
    elif zmall == '800':
        load_32_small, avgdelay_32_small, _, _, _ = clean_load_delays(waa_800_16x32_go_8020_e2e_load_total_bps_avg,
                                                                        waa_800_16x32_go_8020_e2e_delay_total_avg,
                                                                        waa_800_16x32_go_8020_e2e_delay_high_avg,
                                                                        waa_800_16x32_go_8020_e2e_delay_med_avg,
                                                                        waa_800_16x32_go_8020_e2e_delay_low_avg,
                                                                                    cleaning_factor=_cleaning_factor)
    load_32_big, avgdelay_32_big, _, _, _ = clean_load_delays(waa_3200_16x32_go_8020_e2e_load_total_bps_avg,
                                                                waa_3200_16x32_go_8020_e2e_delay_total_avg,
                                                                waa_3200_16x32_go_8020_e2e_delay_high_avg,
                                                                waa_3200_16x32_go_8020_e2e_delay_med_avg,
                                                                waa_3200_16x32_go_8020_e2e_delay_low_avg,
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
    print('avgdelay_16=' + str(avgdelay_16))
    print('load_24_small=' + str(load_24_small))
    print('load_24_big=' + str(load_24_big))
    print('load_24='+str(load_24))
    print('avgdelay_24=' + str(avgdelay_24))
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

def prep_plot09_16xN_stay_8020_e2e_delays(zmall ='half'):
    _cleaning_factor=1e12
    _zero_rm_factor=1

    _16_zero_rm_factor=1
    _16_small_rm_factor=-4
    _16_big_rm_factor=1
    _24_zero_rm_factor=1
    _24_small_rm_factor=-2
    _24_big_rm_factor=1
    _32_zero_rm_factor=3
    _32_small_rm_factor=-1
    _32_big_rm_factor=1

    _x_lim_begin, _x_lim_end=3,10
    _y_lim_begin,_y_lim_end=1e-4,2
    _x_label,_y_label='Total load (Tbps)','End-to-end latency (ms)'

    _LINEWIDTH = 7
    _LEGEND_SIZE = 30
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'center right'

    load_16_small, avgdelay_16_small, highdelay_16_small, meddelay_16_small, lowdelay_16_small = clean_load_delays(waa_800_16x16_stay_8020_e2e_load_total_bps_avg,
                                                                waa_800_16x16_stay_8020_e2e_delay_total_avg,
                                                                waa_800_16x16_stay_8020_e2e_delay_high_avg,
                                                                waa_800_16x16_stay_8020_e2e_delay_med_avg,
                                                                waa_800_16x16_stay_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    load_16_big, avgdelay_16_big, highdelay_16_big, meddelay_16_big, lowdelay_16_big = clean_load_delays(waa_1600_16x16_stay_8020_e2e_load_total_bps_avg,
                                                                    waa_1600_16x16_stay_8020_e2e_delay_total_avg,
                                                                    waa_1600_16x16_stay_8020_e2e_delay_high_avg,
                                                                    waa_1600_16x16_stay_8020_e2e_delay_med_avg,
                                                                    waa_1600_16x16_stay_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)
    if zmall == 'half':
        load_24_small, avgdelay_24_small, highdelay_24_small, meddelay_24_small, lowdelay_24_small = clean_load_delays(waa_1200_16x24_stay_8020_e2e_load_total_bps_avg,
                                                                        waa_1200_16x24_stay_8020_e2e_delay_total_avg,
                                                                        waa_1200_16x24_stay_8020_e2e_delay_high_avg,
                                                                        waa_1200_16x24_stay_8020_e2e_delay_med_avg,
                                                                        waa_1200_16x24_stay_8020_e2e_delay_low_avg,
                                                                                    cleaning_factor=_cleaning_factor)
    elif zmall=='800':
        load_24_small, avgdelay_24_small, highdelay_24_small, meddelay_24_small, lowdelay_24_small = clean_load_delays(waa_800_16x24_stay_8020_e2e_load_total_bps_avg,
                                                                        waa_800_16x24_stay_8020_e2e_delay_total_avg,
                                                                        waa_800_16x24_stay_8020_e2e_delay_high_avg,
                                                                        waa_800_16x24_stay_8020_e2e_delay_med_avg,
                                                                        waa_800_16x24_stay_8020_e2e_delay_low_avg,
                                                                                    cleaning_factor=_cleaning_factor)

    load_24_big, avgdelay_24_big, highdelay_24_big, meddelay_24_big, lowdelay_24_big = clean_load_delays(waa_2400_16x24_stay_8020_e2e_load_total_bps_avg,
                                                            waa_2400_16x24_stay_8020_e2e_delay_total_avg,
                                                            waa_2400_16x24_stay_8020_e2e_delay_high_avg,
                                                            waa_2400_16x24_stay_8020_e2e_delay_med_avg,
                                                            waa_2400_16x24_stay_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)

    if zmall == 'half':
        load_32_small, avgdelay_32_small, highdelay_32_small, meddelay_32_small, lowdelay_32_small = clean_load_delays(waa_1600_16x32_stay_8020_e2e_load_total_bps_avg,
                                                                        waa_1600_16x32_stay_8020_e2e_delay_total_avg,
                                                                        waa_1600_16x32_stay_8020_e2e_delay_high_avg,
                                                                        waa_1600_16x32_stay_8020_e2e_delay_med_avg,
                                                                        waa_1600_16x32_stay_8020_e2e_delay_low_avg,
                                                                                    cleaning_factor=_cleaning_factor)
    elif zmall == '800':
        load_32_small, avgdelay_32_small, highdelay_32_small, meddelay_32_small, lowdelay_32_small = clean_load_delays(waa_800_16x32_stay_8020_e2e_load_total_bps_avg,
                                                                        waa_800_16x32_stay_8020_e2e_delay_total_avg,
                                                                        waa_800_16x32_stay_8020_e2e_delay_high_avg,
                                                                        waa_800_16x32_stay_8020_e2e_delay_med_avg,
                                                                        waa_800_16x32_stay_8020_e2e_delay_low_avg,
                                                                                    cleaning_factor=_cleaning_factor)
    load_32_big, avgdelay_32_big, highdelay_32_big, meddelay_32_big, lowdelay_32_big = clean_load_delays(waa_3200_16x32_stay_8020_e2e_load_total_bps_avg,
                                                                waa_3200_16x32_stay_8020_e2e_delay_total_avg,
                                                                waa_3200_16x32_stay_8020_e2e_delay_high_avg,
                                                                waa_3200_16x32_stay_8020_e2e_delay_med_avg,
                                                                waa_3200_16x32_stay_8020_e2e_delay_low_avg,
                                                                                cleaning_factor=_cleaning_factor)


    # merge 2 datasets
    load_16=load_16_small[_16_zero_rm_factor:_16_small_rm_factor]+load_16_big[_16_big_rm_factor:]
    avgdelay_16=avgdelay_16_small[_16_zero_rm_factor:_16_small_rm_factor]+avgdelay_16_big[_16_big_rm_factor:]
    highdelay_16=highdelay_16_small[_16_zero_rm_factor:_16_small_rm_factor]+highdelay_16_big[_16_big_rm_factor:]
    meddelay_16=meddelay_16_small[_16_zero_rm_factor:_16_small_rm_factor]+meddelay_16_big[_16_big_rm_factor:]
    lowdelay_16=lowdelay_16_small[_16_zero_rm_factor:_16_small_rm_factor]+lowdelay_16_big[_16_big_rm_factor:]

    load_24=load_24_small[_24_zero_rm_factor:_24_small_rm_factor]+load_24_big[_24_big_rm_factor:]
    avgdelay_24=avgdelay_24_small[_24_zero_rm_factor:_24_small_rm_factor]+avgdelay_24_big[_24_big_rm_factor:]
    highdelay_24=highdelay_24_small[_24_zero_rm_factor:_24_small_rm_factor]+highdelay_24_big[_24_big_rm_factor:]
    meddelay_24=meddelay_24_small[_24_zero_rm_factor:_24_small_rm_factor]+meddelay_24_big[_24_big_rm_factor:]
    lowdelay_24=lowdelay_24_small[_24_zero_rm_factor:_24_small_rm_factor]+lowdelay_24_big[_24_big_rm_factor:]

    load_32=load_32_small[_32_zero_rm_factor:_32_small_rm_factor]+load_32_big[_32_big_rm_factor:]
    avgdelay_32=avgdelay_32_small[_32_zero_rm_factor:_32_small_rm_factor]+avgdelay_32_big[_32_big_rm_factor:]
    highdelay_32=highdelay_32_small[_32_zero_rm_factor:_32_small_rm_factor]+highdelay_32_big[_32_big_rm_factor:]
    meddelay_32=meddelay_32_small[_32_zero_rm_factor:_32_small_rm_factor]+meddelay_32_big[_32_big_rm_factor:]
    lowdelay_32=lowdelay_32_small[_32_zero_rm_factor:_32_small_rm_factor]+lowdelay_32_big[_32_big_rm_factor:]

    #plot
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.semilogy(load_16, avgdelay_16, 'k', label="16", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(load_16, highdelay_16, 'r', label="16", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(load_16, meddelay_16, 'g', label="16", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(load_16, lowdelay_16, 'b', label="16", linewidth=_LINEWIDTH + 1)

    ax1.semilogy(load_24, avgdelay_24, 'k--', label="24", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(load_24, highdelay_24, 'r--', label="24", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(load_24, meddelay_24, 'g--', label="24", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(load_24, lowdelay_24, 'b--', label="24", linewidth=_LINEWIDTH + 1)

    ax1.semilogy(load_32, avgdelay_32, 'k-.', label="32", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(load_32, highdelay_32, 'r-.', label="32", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(load_32, meddelay_32, 'g-.', label="32", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(load_32, lowdelay_32, 'b-.', label="32", linewidth=_LINEWIDTH + 1)


    ax1.set_xlabel(_x_label, fontsize=_LABEL_SIZE)
    ax1.set_ylabel(_y_label, fontsize=_LABEL_SIZE)
    ax1.set_xlim(_x_lim_begin,_x_lim_end)
    ax1.set_ylim(_y_lim_begin, _y_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()

def plot09_16xN_stay_8020_e2e_delays():
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'

    x_lim_begin=-3
    x_lim_end=12
    y_label='End-to-end latency (ms)'
    legend_loc='lower left'

    fig, ax1 = plt.subplots(constrained_layout=False)
    ax1.set_yscale('log')

    load=[2,4,6,8,10]

    high_1600=[0.00022,0.00029,0.000368,0.000453,0.000496]
    med_1600 = [0.000567,0.00236,0.014,0.031,0.04]
    low_1600 = [0.0075,0.049,0.175,0.25,0.27]

    high_2400= [0.00027,0.0014,0.0317,0.099,0.099]
    med_2400 = [0.000600,0.0032,0.11,0.29,0.8]
    low_2400 = [0.0093,0.06,0.2,0.42,0.83]

    high_3200= [0.00027,0.0014,0.054,0.132,0.132]
    med_3200 = [0.00077,0.0032,0.13,0.32,0.81]
    low_3200 = [0.011,0.068,0.222,0.55,0.886]


    for i in range(0,len(load)):
        #hh_24=(100*(high_2400[i]-high_1600[i]))/high_1600[i]
        #hh_32 = (100 * (high_3200[i] - high_1600[i])) / high_1600[i]

        #mm_24=(100*(med_2400[i]-med_1600[i]))/med_1600[i]
        #mm_32 = (100 * (med_3200[i] - med_1600[i])) / med_1600[i]

        #ll_24=(100*(low_2400[i]-low_1600[i]))/low_1600[i]
        #ll_32 = (100 * (low_3200[i] - low_1600[i])) / low_1600[i]

        hh_24=(1*(high_2400[i]-0))/high_1600[i]
        hh_32 = (1 * (high_3200[i] - 0)) / high_1600[i]

        mm_24=(1*(med_2400[i]-0))/med_1600[i]
        mm_32 = (1 * (med_3200[i] - 0)) / med_1600[i]

        ll_24=(1*(low_2400[i]-0))/low_1600[i]
        ll_32 = (1 * (low_3200[i] - 0)) / low_1600[i]

        print('Load='+str(load[i]))
        print('high_24='+str(hh_24))
        print('high_32=' + str(hh_32))

        print('med_24='+str(mm_24))
        print('med_32=' + str(mm_32))

        print('low_24='+str(ll_24))
        print('low_32=' + str(ll_32))

        print('----')

    mini_size = 0.2
    big_size = 0.58
    width = 0.12

    x_med=load
    x_med_2400=x_med
    x_med_1600 = [x - mini_size for x in x_med]
    x_med_3200 = [x + mini_size for x in x_med]

    x_high_2400 = [x - big_size for x in x_med]
    x_high_1600 = [x - mini_size for x in x_high_2400]
    x_high_3200  = [x + mini_size for x in x_high_2400]

    x_low_2400 = [x + big_size for x in x_med]
    x_low_1600 = [x - mini_size for x in x_low_2400]
    x_low_3200  = [x + mini_size for x in x_low_2400]

    ax1.bar(x_high_1600, high_1600, color='white',edgecolor='red', label="High-16",linewidth=4, width=width,hatch='/')
    ax1.bar(x_med_1600, med_1600,  color='white',edgecolor='green', label="Med-16",linewidth=4, width=width,hatch='/')
    ax1.bar(x_low_1600, low_1600,  color='white',edgecolor='blue', label="Low-16",linewidth=4, width=width,hatch='/')

    ax1.bar(x_high_2400, high_2400, color='white',edgecolor='red', label="High-24",linewidth=4, width=width,hatch='.')
    ax1.bar(x_med_2400, med_2400,  color='white',edgecolor='green', label="Med-24",linewidth=4, width=width,hatch='.')
    ax1.bar(x_low_2400, low_2400,  color='white',edgecolor='blue', label="Low-24",linewidth=4, width=width,hatch='.')

    ax1.bar(x_high_3200, high_3200, color='white',edgecolor='red', label="High-32",linewidth=4, width=width,hatch='+')
    ax1.bar(x_med_3200, med_3200,  color='white',edgecolor='green', label="Med-32",linewidth=4, width=width,hatch='+')
    ax1.bar(x_low_3200, low_3200,  color='white',edgecolor='blue', label="Low-32",linewidth=4, width=width,hatch='+')

    ax1.set_xticks([2,4,6,8,10])
    labels = [3.5,5,6.5,8,10]
    ax1.set_xticklabels(labels)

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

def plot10_calabr_thru():
    _cleaning_factor=1e12

    _go_small_rm_factor=-1
    _go_big_rm_factor=5
    _stay_small_rm_factor=-1
    _stay_big_rm_factor=5

    _x_lim_begin, _x_lim_end=-0.1,1.0
    _x_label,_y_label='Normalized load','Normalized throughput'
    _nominal_thru=0.1*(16*4+16*1)
    _LINEWIDTH = 7
    _LEGEND_SIZE = 50
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'lower right'


    _go_load_small,_go_thru_small,_=clean_load_thru_drop(waa_400_16x8_go_8020_e2e_load_total_bps_avg,
                                                waa_400_16x8_go_8020_e2e_thru_total_bps_avg,
                                                waa_400_16x8_go_8020_e2e_drop_total_bps_avg,
                                                cleaning_factor=_cleaning_factor)

    _go_load_big, _go_thru_big, _ = clean_load_thru_drop(waa_1600_16x8_go_8020_e2e_load_total_bps_avg,
                                                waa_1600_16x8_go_8020_e2e_thru_total_bps_avg,
                                                waa_1600_16x8_go_8020_e2e_drop_total_bps_avg,
                                                cleaning_factor=_cleaning_factor)

    _stay_load_small,_stay_thru_small,_=clean_load_thru_drop(waa_400_16x8_stay_8020_e2e_load_total_bps_avg,
                                                waa_400_16x8_stay_8020_e2e_thru_total_bps_avg,
                                                waa_400_16x8_stay_8020_e2e_drop_total_bps_avg,
                                                cleaning_factor=_cleaning_factor)

    _stay_load_big, _stay_thru_big, _ = clean_load_thru_drop(waa_1600_16x8_stay_8020_e2e_load_total_bps_avg,
                                                waa_1600_16x8_stay_8020_e2e_thru_total_bps_avg,
                                                waa_1600_16x8_stay_8020_e2e_drop_total_bps_avg,
                                                cleaning_factor=_cleaning_factor)

    # merge 2 datasets
    _go_load=_go_load_small[:_go_small_rm_factor]+_go_load_big[_go_big_rm_factor:]
    _go_thru = _go_thru_small[:_go_small_rm_factor] + _go_thru_big[_go_big_rm_factor:]
    _go_norm_load=[x/_nominal_thru for x in _go_load]
    _go_norm_thru = [x / _nominal_thru for x in _go_thru]
    # dbg
    print('_go_load_small=' + str(_go_load_small))
    print('_go_load_big=' + str(_go_load_big))
    print('_go_load='+str(_go_load))
    print('_go_thru='+str(_go_thru))
    print('_go_norm_load'+str(_go_norm_load))
    print('_go_norm_thru' + str(_go_norm_thru))

    # merge 2 datasets
    _stay_load=_stay_load_small[:_stay_small_rm_factor]+_stay_load_big[_stay_big_rm_factor:]
    _stay_thru = _stay_thru_small[:_stay_small_rm_factor] + _stay_thru_big[_stay_big_rm_factor:]
    _stay_norm_load=[x/_nominal_thru for x in _stay_load]
    _stay_norm_thru = [x / _nominal_thru for x in _stay_thru]
    # dbg
    print('_stay_load_small=' + str(_stay_load_small))
    print('_stay_load_big=' + str(_stay_load_big))
    print('_stay_load='+str(_stay_load))
    print('_stay_thru='+str(_stay_thru))
    print('_stay_norm_load'+str(_stay_norm_load))
    print('_stay_norm_thru' + str(_stay_norm_thru))

    # calabreta
    cal_load=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    cal_thru=[0.1,0.2,0.3,0.4,0.5,0.6,0.65,0.7,0.7,0.7]

    #plot
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.plot(_go_norm_load, _go_norm_thru,'k', label="Vanilla",linewidth=_LINEWIDTH)
    ax1.plot(_stay_norm_load, _stay_norm_thru,'k--', label="StayIn",linewidth=_LINEWIDTH)
    ax1.plot(cal_load, cal_thru, 'magenta', label="OPFC", linewidth=_LINEWIDTH)


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

    _go_zero_rm_factor=1
    _go_small_rm_factor=-1
    _go_big_rm_factor=1
    _stay_zero_rm_factor=1
    _stay_small_rm_factor=-1
    _stay_big_rm_factor=1

    _x_lim_begin, _x_lim_end=-0.19,1
    _y_lim_begin,_y_lim_end=1e-4,1
    _x_label,_y_label='Normalized load','End-to-end latency (ms)'
    _nominal_thru=0.1*(16*4+16*1)

    _LINEWIDTH = 7
    _LEGEND_SIZE = 26
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'upper left'

    _go_load_small, _go_avg_delay_small, _go_high_delay_small, _go_med_delay_small, _go_low_delay_small = \
        clean_load_delays(waa_400_16x8_go_8020_e2e_load_total_bps_avg,
                          waa_400_16x8_go_8020_e2e_delay_total_avg,
                          waa_400_16x8_go_8020_e2e_delay_high_avg,
                          waa_400_16x8_go_8020_e2e_delay_med_avg,
                          waa_400_16x8_go_8020_e2e_delay_low_avg,
                          cleaning_factor=_cleaning_factor)

    _go_load_big, _go_avg_delay_big, _go_high_delay_big, _go_med_delay_big, _go_low_delay_big = \
        clean_load_delays(
        waa_1600_16x8_go_8020_e2e_load_total_bps_avg,
        waa_1600_16x8_go_8020_e2e_delay_total_avg,
        waa_1600_16x8_go_8020_e2e_delay_high_avg,
        waa_1600_16x8_go_8020_e2e_delay_med_avg,
        waa_1600_16x8_go_8020_e2e_delay_low_avg,
        cleaning_factor=_cleaning_factor)

    _stay_load_small, _stay_avg_delay_small, _stay_high_delay_small, _stay_med_delay_small, _stay_low_delay_small = \
        clean_load_delays(waa_400_16x8_stay_8020_e2e_load_total_bps_avg,
                          waa_400_16x8_stay_8020_e2e_delay_total_avg,
                          waa_400_16x8_stay_8020_e2e_delay_high_avg,
                          waa_400_16x8_stay_8020_e2e_delay_med_avg,
                          waa_400_16x8_stay_8020_e2e_delay_low_avg,
                          cleaning_factor=_cleaning_factor)

    _stay_load_big, _stay_avg_delay_big, _stay_high_delay_big, _stay_med_delay_big, _stay_low_delay_big = \
        clean_load_delays(
        waa_1600_16x8_stay_8020_e2e_load_total_bps_avg,
        waa_1600_16x8_stay_8020_e2e_delay_total_avg,
        waa_1600_16x8_stay_8020_e2e_delay_high_avg,
        waa_1600_16x8_stay_8020_e2e_delay_med_avg,
        waa_1600_16x8_stay_8020_e2e_delay_low_avg,
        cleaning_factor=_cleaning_factor)

    # merge 2 datasets
    _go_load=_go_load_small[_go_zero_rm_factor:_go_small_rm_factor]+_go_load_big[_go_big_rm_factor:]
    _go_avg_delay=_go_avg_delay_small[_go_zero_rm_factor:_go_small_rm_factor]+_go_avg_delay_big[_go_big_rm_factor:]
    _go_high_delay = _go_high_delay_small[_go_zero_rm_factor:_go_small_rm_factor] + _go_high_delay_big[_go_big_rm_factor:]
    _go_med_delay = _go_med_delay_small[_go_zero_rm_factor:_go_small_rm_factor] + _go_med_delay_big[_go_big_rm_factor:]
    _go_low_delay = _go_low_delay_small[_go_zero_rm_factor:_go_small_rm_factor] + _go_low_delay_big[_go_big_rm_factor:]

    _stay_load=_stay_load_small[_stay_zero_rm_factor:_stay_small_rm_factor]+_stay_load_big[_stay_big_rm_factor:]
    _stay_avg_delay=_stay_avg_delay_small[_stay_zero_rm_factor:_stay_small_rm_factor]+_stay_avg_delay_big[_stay_big_rm_factor:]
    _stay_high_delay = _stay_high_delay_small[_stay_zero_rm_factor:_stay_small_rm_factor] + _stay_high_delay_big[_stay_big_rm_factor:]
    _stay_med_delay = _stay_med_delay_small[_stay_zero_rm_factor:_stay_small_rm_factor] + _stay_med_delay_big[_stay_big_rm_factor:]
    _stay_low_delay = _stay_low_delay_small[_stay_zero_rm_factor:_stay_small_rm_factor] + _stay_low_delay_big[_stay_big_rm_factor:]
    # normalize
    _go_norm_load = [x / _nominal_thru for x in _go_load]
    _stay_norm_load = [x / _nominal_thru for x in _stay_load]
    # calabreta
    cal_load = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    if _comparison_date==2022:
        cal_avg_delay=[4e-3,5e-3,6e-3,7e-3,8e-3,9e-3,10e-3,20e-3,45e-3,53e-3] # ms
        cal_drop_prob=[0,0,7e-5,4e-4,1e-3,1.5e-3,2e-3,3e-3,3e-2,7e-2]
    else:
        cal_avg_delay=[7.5e-3,7.5e-3,7.5e-3,7.5e-3,7.5e-3,8e-3,9e-3,12.5e-3,21e-3,29e-3] # ms
        cal_drop_prob=[0,0,0,0,0.007,0.010,0.012,0.025,0.06,0.105]

    # thor
    thor_load = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.72, 0.75, 0.9]
    thor_avg_delay = [6.8e-4,6.8e-4,6.8e-4,6.8e-4,6.8e-4,6.8e-4,6.8e-4,0.6,1.15,2]  # ms


    # dbg
    print('_go_load_small=' + str(_go_load_small))
    print('_go_load_big=' + str(_go_load_big))
    print('_go_load='+str(_go_load))
    print('_stay_load_small=' + str(_stay_load_small))
    print('_stay_load_big=' + str(_stay_load_big))
    print('_stay_load='+str(_stay_load))

    #plot
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.semilogy(_go_norm_load, _go_avg_delay, 'k', label="Vanilla/Avg", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(_go_norm_load, _go_high_delay, 'r', label="Vanilla/High", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(_go_norm_load, _go_med_delay, 'g', label="Vanilla/Med", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(_go_norm_load, _go_low_delay, 'b', label="Vanilla/Low", linewidth=_LINEWIDTH + 1)

    ax1.semilogy(_stay_norm_load, _stay_avg_delay, 'k--', label="StayIn/Avg", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(_stay_norm_load, _stay_high_delay, 'r--', label="StayIn/High", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(_stay_norm_load, _stay_med_delay, 'g--', label="StayIn/Med", linewidth=_LINEWIDTH + 1)
    ax1.semilogy(_stay_norm_load, _stay_low_delay, 'b--', label="StayIn/Low", linewidth=_LINEWIDTH + 1)

    ax1.semilogy(cal_load, cal_avg_delay, 'magenta', label="OPFC/Avg", linewidth=_LINEWIDTH)
    ax1.semilogy(thor_load, thor_avg_delay, 'orange', label="Thor/Avg", linewidth=_LINEWIDTH)

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

    _go_zero_rm_factor=1
    _go_small_rm_factor=-2
    _go_big_rm_factor=1
    _stay_zero_rm_factor=1
    _stay_small_rm_factor=-2
    _stay_big_rm_factor=1

    _x_lim_begin, _x_lim_end=-0.1,1
    _y_lim_begin,_y_lim_end=0,0.3
    _x_label,_y_label='Normalized load','Packet loss'
    _nominal_thru=0.1*(16*4+16*1)

    _LINEWIDTH = 7
    _LEGEND_SIZE = 30
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'upper left'

    _go_load_small, _go_thru_small, _go_drop_small, _go_drop_prob_avg_small, _go_drop_prob_high_small, \
    _go_drop_prob_med_small, _go_drop_prob_low_small = \
        clean_load_thru_drop_prob \
        (waa_400_16x8_go_8020_e2e_load_total_bps_avg,
         waa_400_16x8_go_8020_e2e_thru_total_bps_avg,
         waa_400_16x8_go_8020_e2e_drop_total_bps_avg,
         waa_400_16x8_go_8020_e2e_drop_prob_total_avg,
         waa_400_16x8_go_8020_e2e_drop_prob_high_avg,
         waa_400_16x8_go_8020_e2e_drop_prob_med_avg,
         waa_400_16x8_go_8020_e2e_drop_prob_low_avg, cleaning_factor=1e12)

    _go_load_big, _go_thru_big, _go_drop_big, _go_drop_prob_avg_big, _go_drop_prob_high_big, _go_drop_prob_med_big, \
    _go_drop_prob_low_big = clean_load_thru_drop_prob \
        (waa_1600_16x8_go_8020_e2e_load_total_bps_avg,
         waa_1600_16x8_go_8020_e2e_thru_total_bps_avg,
         waa_1600_16x8_go_8020_e2e_drop_total_bps_avg,
         waa_1600_16x8_go_8020_e2e_drop_prob_total_avg,
         waa_1600_16x8_go_8020_e2e_drop_prob_high_avg,
         waa_1600_16x8_go_8020_e2e_drop_prob_med_avg,
         waa_1600_16x8_go_8020_e2e_drop_prob_low_avg, cleaning_factor=1e12)

    _stay_load_small, _stay_thru_small, _stay_drop_small, _stay_drop_prob_avg_small, _stay_drop_prob_high_small, \
    _stay_drop_prob_med_small, _stay_drop_prob_low_small = \
        clean_load_thru_drop_prob \
        (waa_400_16x8_stay_8020_e2e_load_total_bps_avg,
         waa_400_16x8_stay_8020_e2e_thru_total_bps_avg,
         waa_400_16x8_stay_8020_e2e_drop_total_bps_avg,
         waa_400_16x8_stay_8020_e2e_drop_prob_total_avg,
         waa_400_16x8_stay_8020_e2e_drop_prob_high_avg,
         waa_400_16x8_stay_8020_e2e_drop_prob_med_avg,
         waa_400_16x8_stay_8020_e2e_drop_prob_low_avg, cleaning_factor=1e12)

    _stay_load_big, _stay_thru_big, _stay_drop_big, _stay_drop_prob_avg_big, _stay_drop_prob_high_big, _stay_drop_prob_med_big, \
    _stay_drop_prob_low_big = clean_load_thru_drop_prob \
        (waa_1600_16x8_stay_8020_e2e_load_total_bps_avg,
         waa_1600_16x8_stay_8020_e2e_thru_total_bps_avg,
         waa_1600_16x8_stay_8020_e2e_drop_total_bps_avg,
         waa_1600_16x8_stay_8020_e2e_drop_prob_total_avg,
         waa_1600_16x8_stay_8020_e2e_drop_prob_high_avg,
         waa_1600_16x8_stay_8020_e2e_drop_prob_med_avg,
         waa_1600_16x8_stay_8020_e2e_drop_prob_low_avg, cleaning_factor=1e12)

    # merge 2 datasets
    _go_load=_go_load_small[_go_zero_rm_factor:_go_small_rm_factor]+_go_load_big[_go_big_rm_factor:]
    _go_drop_prob_avg=_go_drop_prob_avg_small[_go_zero_rm_factor:_go_small_rm_factor]+_go_drop_prob_avg_big[_go_big_rm_factor:]
    _go_drop_prob_high = _go_drop_prob_high_small[_go_zero_rm_factor:_go_small_rm_factor] + _go_drop_prob_high_big[_go_big_rm_factor:]
    _go_drop_prob_med = _go_drop_prob_med_small[_go_zero_rm_factor:_go_small_rm_factor] + _go_drop_prob_med_big[_go_big_rm_factor:]
    _go_drop_prob_low = _go_drop_prob_low_small[_go_zero_rm_factor:_go_small_rm_factor] + _go_drop_prob_low_big[_go_big_rm_factor:]

    _stay_load=_stay_load_small[_stay_zero_rm_factor:_stay_small_rm_factor]+_stay_load_big[_stay_big_rm_factor:]
    _stay_drop_prob_avg=_stay_drop_prob_avg_small[_stay_zero_rm_factor:_stay_small_rm_factor]+_stay_drop_prob_avg_big[_stay_big_rm_factor:]
    _stay_drop_prob_high = _stay_drop_prob_high_small[_stay_zero_rm_factor:_stay_small_rm_factor] + _stay_drop_prob_high_big[_stay_big_rm_factor:]
    _stay_drop_prob_med = _stay_drop_prob_med_small[_stay_zero_rm_factor:_stay_small_rm_factor] + _stay_drop_prob_med_big[_stay_big_rm_factor:]
    _stay_drop_prob_low = _stay_drop_prob_low_small[_stay_zero_rm_factor:_stay_small_rm_factor] + _stay_drop_prob_low_big[_stay_big_rm_factor:]

    # normalize
    _go_norm_load = [x / _nominal_thru for x in _go_load]
    _stay_norm_load = [x / _nominal_thru for x in _stay_load]

    # calabreta
    cal_load = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    if _comparison_date==2022:
        cal_avg_delay=[4e-3,5e-3,6e-3,7e-3,8e-3,9e-3,10e-3,20e-3,45e-3,53e-3] # ms
        cal_drop_prob=[0,0,7e-5,4e-4,1e-3,1.5e-3,2e-3,3e-3,3e-2,7e-2]
    else:
        cal_avg_delay=[7.5e-3,7.5e-3,7.5e-3,7.5e-3,7.5e-3,8e-3,9e-3,12.5e-3,21e-3,29e-3] # ms
        cal_drop_prob=[0,0,0,0,0.007,0.010,0.012,0.025,0.06,0.105]

    # dbg
    print('_go_load_small=' + str(_go_load_small))
    print('_go_load_big=' + str(_go_load_big))
    print('_go_load='+str(_go_load))
    print('_stay_load_small=' + str(_stay_load_small))
    print('_stay_load_big=' + str(_stay_load_big))
    print('_stay_load='+str(_stay_load))

    #plot
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.plot(_go_norm_load, _go_drop_prob_avg, 'k', label="Vanilla/Avg", linewidth=_LINEWIDTH + 1)
    ax1.plot(_go_norm_load, _go_drop_prob_high, 'r', label="Vanilla/High", linewidth=_LINEWIDTH + 1)
    ax1.plot(_go_norm_load, _go_drop_prob_med, 'g', label="Vanilla/Med", linewidth=_LINEWIDTH + 1)
    ax1.plot(_go_norm_load, _go_drop_prob_low, 'b', label="Vanilla/Low", linewidth=_LINEWIDTH + 1)

    ax1.plot(_stay_norm_load, _stay_drop_prob_avg, 'k--', label="StayIn/Avg", linewidth=_LINEWIDTH + 1)
    ax1.plot(_stay_norm_load, _stay_drop_prob_high, 'r--', label="StayIn/High", linewidth=_LINEWIDTH + 1)
    ax1.plot(_stay_norm_load, _stay_drop_prob_med, 'g--', label="StayIn/Med", linewidth=_LINEWIDTH + 1)
    ax1.plot(_stay_norm_load, _stay_drop_prob_low, 'b--', label="StayIn/Low", linewidth=_LINEWIDTH + 1)

    ax1.plot(cal_load, cal_drop_prob, 'magenta', label="OPFC", linewidth=_LINEWIDTH)

    ax1.set_xlabel(_x_label, fontsize=_LABEL_SIZE)
    ax1.set_ylabel(_y_label, fontsize=_LABEL_SIZE)
    ax1.set_xlim(_x_lim_begin,_x_lim_end)
    ax1.set_ylim(_y_lim_begin, _y_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()

def draw_normal(main_list,error_list,samples_per_feat=50):
    final_list=[]
    for i in range(0,len(main_list)):
        mu=main_list[i]
        sigma = error_list[i]
        gen=np.random.normal(mu, sigma, samples_per_feat)
        final_list.extend(gen)
    return final_list

def get_cdf_plotter(sample_list,bins=20):
    count, bins_count = np.histogram(sample_list, bins=bins)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    return bins_count[1:],cdf


def plot_review_cdf_vanilla_stayin():
    _x_lim_begin, _x_lim_end=-0.19,1
    _y_lim_begin,_y_lim_end=1e-4,1
    _x_label,_y_label='Normalized load','End-to-end latency (ms)'
    _nominal_thru=0.1*(16*4+16*1)

    _LINEWIDTH = 7
    _LEGEND_SIZE = 26
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'upper left'

    waa_16x16_go_8020_e2e_delay_total_avg = [1.0642301946057725e-06, 1.2549515392876208e-06,
                                                 1.6696329093696078e-06, 1.895897644783818e-06, 2.578142654955094e-06,
                                                 2.519420990169071e-06,1.998737451705892e-06, 2.6169308481453195e-06,
                                                  4.237960496907031e-06, 8.016617735346173e-06, 2.0002269728590892e-05,
                                                  3.9914148703785475e-05, 5.174846921283968e-05]
    waa_16x16_go_8020_e2e_delay_total_err = [ 1.723141471897084e-07, 1.6516286738171267e-07,
                                                 1.5127134783324825e-07, 2.920858785743197e-07, 1.845048102550243e-07,1.845048102550243e-07,2.529282413399107e-07, 6.163852736583143e-07,
                                                  1.0674239917890853e-06, 3.590513687436912e-06, 7.012589127519616e-06,
                                                  8.483270041558213e-06, 1.2592750453344114e-05]

    waa_16x16_go_8020_e2e_delay_high_avg = [3.915167694499143e-07, 4.0543632810523207e-07,4.281020019097491e-07, 4.5004595706244664e-07,
                                            5.015144836709433e-07,5.106383176940969e-07, 7.713113087524994e-07,4.760464026617077e-07, 5.131505584207702e-07,
                                                 5.52638130699876e-07, 6.252225402213822e-07, 7.712728678326273e-07,
                                                 9.114324392679543e-07, 9.525032589449076e-07, 1.0247328655446053e-06]
    waa_16x16_go_8020_e2e_delay_high_err = [4.137779559996159e-09, 6.393216097391625e-09,
                                                6.766107608183421e-09, 6.140934093654583e-09, 2.6166360278617495e-08,
                                            2.6166360278617495e-08, 2.6166360278617495e-08,1.0369521192239528e-08, 1.3000647501259475e-08,
                                                 2.4059202082592077e-08, 5.574535178792384e-08, 7.269227566346152e-08,
                                                 4.451512119233687e-08, 7.284942861949644e-08, 7.284942861949644e-08]
    waa_16x16_go_8020_e2e_delay_med_avg = [5.071545022703347e-07, 5.147637126791621e-07,
                                               5.273426939093233e-07, 5.387581926120947e-07, 6.147577164593574e-07,
                                               5.828609440703037e-07, 1.3740417999102582e-06,6.870162827571203e-07, 7.644470817997861e-07,
                                                9.2224740518302e-07, 2.045116034967567e-06, 6.455433046991681e-06,
                                                1.589564735623976e-05, 2.193482183783836e-05]
    waa_16x16_go_8020_e2e_delay_med_err = [ 5.1157496555086545e-09, 7.958512904126348e-09,
                                               8.576605186173556e-09, 6.761087953220907e-09, 7.681598111887609e-08, 7.681598111887609e-08, 7.681598111887609e-08,6.180838852339641e-09, 3.774892835605249e-08,
                                                3.0526364075873124e-07, 1.4778691369136471e-06, 3.1236989275504442e-06,
                                                6.289625317992581e-06, 1.0423149203362488e-05]
    waa_16x16_go_8020_e2e_delay_low_avg = [7.254209968817725e-06, 7.279361460422012e-06,
                                               8.121911784319854e-06, 7.847691271084875e-06, 1.0110772214995605e-05,
                                               8.080560864905448e-06,2.1136503556269357e-05, 2.2476267645906468e-05,
                                                2.939864337794904e-05, 4.6249405982293245e-05, 9.81751046134783e-05,
                                                0.00018521800442228232, 0.00021330960281870656]
    waa_16x16_go_8020_e2e_delay_low_err = [1.5943070101978622e-06, 1.1546170881830149e-06,
                                               9.404009925643402e-07, 1.264974855158278e-06, 1.6056103485855013e-06,5.346669227884502e-07, 4.556807075361173e-06,
                                                6.805628363165701e-06, 1.9296846673981565e-05, 3.336591747963927e-05,
                                                4.059280491115912e-05, 4.3721766630558925e-05, 4.3721766630558925e-05]
    waa_16x16_stay_8020_e2e_delay_total_avg = [8.339012023784865e-07, 1.0788735164421421e-06,
                                                   1.4023286169417689e-06, 1.755143747235335e-06, 2.015132464525008e-06,
                                                   4.999789474653397e-06, 9.134282871767743e-06,2.2614819534698097e-06, 3.5039392619543457e-06,
                                                    1.4835211566942572e-05, 2.4895243716812446e-05,
                                                    4.594919255008208e-05, 6.094022116211189e-05, 6.905567607120142e-05,
                                                    7.730594337130474e-05, 8.20892894024645e-05]
    waa_16x16_stay_8020_e2e_delay_total_err = [2.0154520499669781e-07, 1.7116622941683624e-07,
                                                   2.151299861931038e-07, 3.491726215921739e-07, 2.1905653083030586e-07,
                                                   1.539123733696811e-06,1.539123733696811e-06, 8.356715792213857e-07, 1.0759422095935764e-06,
                                                    7.4541644000129166e-06, 1.1707372307121498e-05,
                                                    7.162649528061785e-07, 1.100428871715332e-05, 1.100428871715332e-05, 1.100428871715332e-05, 1.100428871715332e-05]
    waa_16x16_stay_8020_e2e_delay_high_avg = [2.3041307412606224e-07, 2.31663743558516e-07,
                                                  2.3294012175682495e-07, 2.367667638418856e-07, 2.4134592151278374e-07,
                                                  2.447109475922321e-07, 2.68974332782962e-07,2.5316804104527065e-07, 2.5988981170315364e-07,
                                                   2.954131489268143e-07, 3.2325657478349146e-07,
                                                   3.7793028583378045e-07, 4.088738795011013e-07,
                                                   4.3207493875430184e-07, 4.578503514491859e-07, 4.625841046126164e-07]
    waa_16x16_stay_8020_e2e_delay_high_err = [ 7.647512353220003e-10, 7.113603261618288e-10,
                                                  8.644883535829077e-10, 2.361291645889054e-09, 1.3951418207630233e-09,
                                                  1.504351469192819e-09,1.504351469192819e-09,3.917269603015686e-09, 4.782474552035685e-09,
                                                   2.3005613247267466e-08, 4.36980587796221e-08, 2.7005413064997896e-08,
                                                   3.8690079789447174e-08, 3.8690079789447174e-08,3.8690079789447174e-08,3.8690079789447174e-08]
    waa_16x16_stay_8020_e2e_delay_med_avg = [ 5.183828009049543e-07, 5.287588299670531e-07,
                                                 5.404311980430471e-07, 5.68659472931176e-07, 6.079325694201046e-07,
                                                 6.917480827953826e-07, 9.249521329623095e-07,7.898628421961044e-07, 8.661961217281704e-07,
                                                  5.002154486772797e-06, 8.470151886866493e-06, 1.7901995855696114e-05,
                                                  2.800059438953789e-05, 3.044537647647497e-05, 3.890938664740988e-05,
                                                  3.9440860597646255e-05]
    waa_16x16_stay_8020_e2e_delay_med_err = [4.395389418547108e-09, 6.449075717521465e-09,
                                                 9.03996962872629e-09, 9.552734574043102e-09, 3.53618195596789e-09,
                                                 5.733917940385873e-08,5.733917940385873e-08,2.613473028285093e-07, 1.0525934244142316e-07,
                                                  3.63115893782231e-06, 9.58686314911168e-06, 4.25537419056286e-06,
                                                  1.2907724514631487e-05,1.2907724514631487e-05,1.2907724514631487e-05,1.2907724514631487e-05]
    waa_16x16_stay_8020_e2e_delay_low_avg = [ 6.264128039067243e-06, 6.753865691540464e-06,
                                                 7.435275133862714e-06, 7.731475160118121e-06, 7.535359761950987e-06,
                                                 1.8358093282204778e-05, 2.9765724099510743e-05,2.1261515075759627e-05, 2.6427456964654765e-05,
                                                  9.316691269772294e-05, 0.00012820994422938276, 0.00021671484789818982,
                                                  0.00025831613945610717, 0.00026579913201560016, 0.0002771926878095625,
                                                  0.00026829432030656516]
    waa_16x16_stay_8020_e2e_delay_low_err = [ 1.501587292060204e-06, 1.0509641251290143e-06,
                                                 1.1876255124515567e-06, 1.3879391509001542e-06, 4.889978461120539e-07,
                                                 6.705777252653852e-06,6.705777252653852e-06,7.1057124272543545e-06, 7.290184123977613e-06,
                                                  4.9729847234462035e-05, 6.248451315344943e-05, 3.6652425933446e-06,
                                                  4.145860600579164e-05, 4.145860600579164e-05,4.145860600579164e-05,4.145860600579164e-05]

    van_avg= draw_normal(waa_16x16_go_8020_e2e_delay_total_avg,waa_16x16_go_8020_e2e_delay_total_err)
    van_high= draw_normal(waa_16x16_go_8020_e2e_delay_high_avg,waa_16x16_go_8020_e2e_delay_high_err)
    van_med= draw_normal(waa_16x16_go_8020_e2e_delay_med_avg,waa_16x16_go_8020_e2e_delay_med_err)
    van_low= draw_normal(waa_16x16_go_8020_e2e_delay_low_avg,waa_16x16_go_8020_e2e_delay_low_err)
    stay_avg= draw_normal(waa_16x16_stay_8020_e2e_delay_total_avg,waa_16x16_stay_8020_e2e_delay_total_err)
    stay_high= draw_normal(waa_16x16_stay_8020_e2e_delay_high_avg,waa_16x16_stay_8020_e2e_delay_high_err)
    stay_med= draw_normal(waa_16x16_stay_8020_e2e_delay_med_avg,waa_16x16_stay_8020_e2e_delay_med_err)
    stay_low= draw_normal(waa_16x16_stay_8020_e2e_delay_low_avg,waa_16x16_stay_8020_e2e_delay_low_err)

    van_avg=[x*1e3 for x in van_avg]
    van_high=[x*1e3 for x in van_high]
    van_med=[x*1e3 for x in van_med]
    van_low=[x*1e3 for x in van_low]
    stay_avg=[x*1e3 for x in stay_avg]
    stay_high=[x*1e3 for x in stay_high]
    stay_med=[x*1e3 for x in stay_med]
    stay_low=[x*1e3 for x in stay_low]

    van_avg_x,van_avg_y=get_cdf_plotter(van_avg)
    van_high_x,van_high_y=get_cdf_plotter(van_high)
    van_med_x,van_med_y=get_cdf_plotter(van_med)
    van_low_x,van_low_y=get_cdf_plotter(van_low)

    stay_avg_x,stay_avg_y=get_cdf_plotter(stay_avg)
    stay_high_x,stay_high_y=get_cdf_plotter(stay_high)
    stay_med_x,stay_med_y=get_cdf_plotter(stay_med)
    stay_low_x,stay_low_y=get_cdf_plotter(stay_low)

    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)
    ax1.set_xscale('log')
    ax1.plot(van_avg_x, van_avg_y,'k', label="Vanilla/Avg", linewidth=_LINEWIDTH + 1,linestyle='solid')
    ax1.plot(van_high_x, van_high_y,'red', label="Vanilla/High", linewidth=_LINEWIDTH + 1,linestyle='solid')
    ax1.plot(van_med_x, van_med_y,'green', label="Vanilla/Med", linewidth=_LINEWIDTH + 1,linestyle='solid')
    ax1.plot(van_low_x, van_low_y,'blue', label="Vanilla/Low", linewidth=_LINEWIDTH + 1,linestyle='solid')

    ax1.plot(stay_avg_x, stay_avg_y,'k', label="StayIn/Avg", linewidth=_LINEWIDTH + 1,linestyle='dashed')
    ax1.plot(stay_high_x, stay_high_y,'red', label="StayIn/High", linewidth=_LINEWIDTH + 1,linestyle='dashed')
    ax1.plot(stay_med_x, stay_med_y,'green', label="StayIn/Med", linewidth=_LINEWIDTH + 1,linestyle='dashed')
    ax1.plot(stay_low_x, stay_low_y,'blue', label="StayIn/Low", linewidth=_LINEWIDTH + 1,linestyle='dashed')

    ax1.set_xlabel('End-to-end latency (ms)', fontsize=_LABEL_SIZE)
    ax1.set_ylabel('CDF', fontsize=_LABEL_SIZE)
    ax1.set_xlim(-0.001,0.4)
    #ax1.set_ylim(_y_lim_begin, _y_lim_end)
    ax1.legend(loc='lower right', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()

def plot_review_cdf_servers(a):
    _x_lim_begin, _x_lim_end=-0.19,1
    _y_lim_begin,_y_lim_end=1e-4,1
    _x_label,_y_label='Normalized load','End-to-end latency (ms)'
    _nominal_thru=0.1*(16*4+16*1)

    _LINEWIDTH = 7
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'upper left'

    waa_16x16_stay_8020_e2e_delay_total_avg = [8.339012023784865e-07, 1.0788735164421421e-06,
                                                   1.4023286169417689e-06, 1.755143747235335e-06, 2.015132464525008e-06,
                                                   4.999789474653397e-06, 9.134282871767743e-06,2.2614819534698097e-06, 3.5039392619543457e-06,
                                                    1.4835211566942572e-05, 2.4895243716812446e-05,
                                                    4.594919255008208e-05, 6.094022116211189e-05, 6.905567607120142e-05,
                                                    7.730594337130474e-05, 8.20892894024645e-05]
    waa_16x16_stay_8020_e2e_delay_total_err = [2.0154520499669781e-07, 1.7116622941683624e-07,
                                                   2.151299861931038e-07, 3.491726215921739e-07, 2.1905653083030586e-07,
                                                   1.539123733696811e-06,1.539123733696811e-06, 8.356715792213857e-07, 1.0759422095935764e-06,
                                                    7.4541644000129166e-06, 1.1707372307121498e-05,
                                                    7.162649528061785e-07, 1.100428871715332e-05, 1.100428871715332e-05, 1.100428871715332e-05, 1.100428871715332e-05]
    waa_16x16_stay_8020_e2e_delay_high_avg = [2.3041307412606224e-07, 2.31663743558516e-07,
                                                  2.3294012175682495e-07, 2.367667638418856e-07, 2.4134592151278374e-07,
                                                  2.447109475922321e-07, 2.68974332782962e-07,2.5316804104527065e-07, 2.5988981170315364e-07,
                                                   2.954131489268143e-07, 3.2325657478349146e-07,
                                                   3.7793028583378045e-07, 4.088738795011013e-07,
                                                   4.3207493875430184e-07, 4.578503514491859e-07, 4.625841046126164e-07]
    waa_16x16_stay_8020_e2e_delay_high_err = [ 7.647512353220003e-10, 7.113603261618288e-10,
                                                  8.644883535829077e-10, 2.361291645889054e-09, 1.3951418207630233e-09,
                                                  1.504351469192819e-09,1.504351469192819e-09,3.917269603015686e-09, 4.782474552035685e-09,
                                                   2.3005613247267466e-08, 4.36980587796221e-08, 2.7005413064997896e-08,
                                                   3.8690079789447174e-08, 3.8690079789447174e-08,3.8690079789447174e-08,3.8690079789447174e-08]
    waa_16x16_stay_8020_e2e_delay_med_avg = [ 5.183828009049543e-07, 5.287588299670531e-07,
                                                 5.404311980430471e-07, 5.68659472931176e-07, 6.079325694201046e-07,
                                                 6.917480827953826e-07, 9.249521329623095e-07,7.898628421961044e-07, 8.661961217281704e-07,
                                                  5.002154486772797e-06, 8.470151886866493e-06, 1.7901995855696114e-05,
                                                  2.800059438953789e-05, 3.044537647647497e-05, 3.890938664740988e-05,
                                                  3.9440860597646255e-05]
    waa_16x16_stay_8020_e2e_delay_med_err = [4.395389418547108e-09, 6.449075717521465e-09,
                                                 9.03996962872629e-09, 9.552734574043102e-09, 3.53618195596789e-09,
                                                 5.733917940385873e-08,5.733917940385873e-08,2.613473028285093e-07, 1.0525934244142316e-07,
                                                  3.63115893782231e-06, 9.58686314911168e-06, 4.25537419056286e-06,
                                                  1.2907724514631487e-05,1.2907724514631487e-05,1.2907724514631487e-05,1.2907724514631487e-05]
    waa_16x16_stay_8020_e2e_delay_low_avg = [ 6.264128039067243e-06, 6.753865691540464e-06,
                                                 7.435275133862714e-06, 7.731475160118121e-06, 7.535359761950987e-06,
                                                 1.8358093282204778e-05, 2.9765724099510743e-05,2.1261515075759627e-05, 2.6427456964654765e-05,
                                                  9.316691269772294e-05, 0.00012820994422938276, 0.00021671484789818982,
                                                  0.00025831613945610717, 0.00026579913201560016, 0.0002771926878095625,
                                                  0.00026829432030656516]
    waa_16x16_stay_8020_e2e_delay_low_err = [ 1.501587292060204e-06, 1.0509641251290143e-06,
                                                 1.1876255124515567e-06, 1.3879391509001542e-06, 4.889978461120539e-07,
                                                 6.705777252653852e-06,6.705777252653852e-06,7.1057124272543545e-06, 7.290184123977613e-06,
                                                  4.9729847234462035e-05, 6.248451315344943e-05, 3.6652425933446e-06,
                                                  4.145860600579164e-05, 4.145860600579164e-05,4.145860600579164e-05,4.145860600579164e-05]

    waa_16x24_stay_8020_e2e_delay_total_avg = [6.538866776252942e-07, 7.292836360269966e-07, 9.78076217745692e-07,
                                               1.190322964335377e-06, 3.5074804507159117e-06, 2.8057420148866807e-06,
                                               1.2665961945581204e-05, 2.9869355910749157e-05, 5.861140182552209e-05,
                                               0.00015730745887211647, 0.00021898663769788683, 0.0002930767098024102,
                                               0.0003386057093441772, 0.0004020237867368068,0.0005152078774260778]
    waa_16x24_stay_8020_e2e_delay_total_err = [7.000153844491623e-08, 1.1819956769199445e-07, 1.1991724556150207e-07,
                                               9.96769332054656e-08, 2.680178778524155e-06, 2.680178778524155e-06,
                                               2.680178778524155e-06, 8.430669482319082e-06, 3.726597626985556e-05,
                                               3.699401725316079e-05, 4.004776801025664e-05, 4.203936986870206e-05,
                                               4.203936986870206e-05, 4.203936986870206e-05, 4.203936986870206e-05]
    waa_16x24_stay_8020_e2e_delay_high_avg = [2.2979330756090323e-07, 2.315389275125298e-07, 2.3418198743781802e-07,
                                              2.3652001361290248e-07, 2.4510302802781356e-07, 2.498547463409051e-07,
                                              3.434019229601525e-07, 1.5784427398626246e-05, 3.347388846882189e-05,
                                              9.890329790525942e-05, 0.00011500481613289602, 8.364934544632209e-05,
                                              4.098788630907992e-05, 3.0113242032985753e-05, 1.8790634232968212e-05]
    waa_16x24_stay_8020_e2e_delay_high_err = [1.5998548658986712e-09, 5.546959149867631e-10, 1.2006162641517237e-09,
                                              1.1663707964351376e-09, 8.045412747391787e-09, 8.045412747391787e-09,
                                              8.045412747391787e-09, 5.336231910266944e-06, 2.53945371424375e-05,
                                              2.6249874722270137e-05, 1.3477308028671876e-05, 2.6327011381387915e-05,
                                              2.6327011381387915e-05, 2.6327011381387915e-05, 2.6327011381387915e-05]
    waa_16x24_stay_8020_e2e_delay_med_avg = [5.069637561289542e-07, 5.158659703178313e-07, 5.373944343876299e-07,
                                             5.635793444056464e-07, 7.260258666162733e-07, 7.158597498769689e-07,
                                             2.264006095630562e-06, 6.212730017142161e-05, 0.00010642885103484515,
                                             0.0002534361483996258, 0.00042411878475479876, 0.0007420854863188424,
                                             0.0008668309557562761, 0.0008502745393473862, 0.0008137961758963652]
    waa_16x24_stay_8020_e2e_delay_med_err = [2.309592096381217e-09, 7.313406576197373e-09, 9.951680097453183e-09,
                                             1.5055299110551995e-08, 2.340290929661487e-07, 2.340290929661487e-07,
                                             2.340290929661487e-07, 2.7302218537451197e-05, 6.62881539339686e-05,
                                             6.875098902325001e-05, 0.0001997091140030838, 0.00017917324486868859,
                                             0.00017917324486868859, 0.00017917324486868859, 0.00017917324486868859]
    waa_16x24_stay_8020_e2e_delay_low_avg = [4.44553997947561e-06, 4.358620682255449e-06, 4.587374067442432e-06,
                                             5.0086854521505535e-06, 1.412781335122275e-05, 9.865833770090461e-06,
                                             4.286343576909277e-05, 0.00010316766261641115, 0.00017283936942178495,
                                             0.0004063686038421399, 0.0005557238827953079, 0.0007378082551804739,
                                             0.00094138488394542, 0.0010715665257637534]
    waa_16x24_stay_8020_e2e_delay_low_err = [5.577783255132319e-07, 7.276746091040465e-07, 5.771382220596541e-07,
                                             5.578722316571521e-07, 1.1064926803679022e-05, 1.1064926803679022e-05,
                                             1.1064926803679022e-05, 1.920634396951007e-05, 8.646165185619531e-05,
                                             0.00010377036753719072, 0.00011497581480484713, 0.00018805473306742425,
                                             0.00018805473306742425, 0.00018805473306742425]

    waa_16x32_stay_8020_e2e_delay_total_avg = [7.925839272956194e-07, 9.795608509698993e-07, 1.382443557358263e-06,
                                               2.226108493681937e-06, 6.4200980234623435e-06, 1.5377487316257915e-05,
                                               2.4460268730230153e-05, 3.626058240358623e-05, 6.020642305781194e-05,
                                               0.00013345629512878985, 0.00018158162272454017, 0.0002596506903013211,
                                               0.0002995437310424192, 0.0003232544996544644, 0.00033355644406012265]
    waa_16x32_stay_8020_e2e_delay_total_err = [9.586401082410835e-08, 1.3292130934647918e-07, 1.2625986942011418e-07,
                                               1.1965409004184508e-06, 3.336363080613865e-06, 3.336363080613865e-06,
                                               3.336363080613865e-06, 3.336363080613865e-06, 3.585781646455454e-05,
                                               4.487878740397282e-05, 3.723759745756456e-05, 3.3224236176390117e-05,
                                               8.368880949167656e-06, 8.368880949167656e-06, 8.368880949167656e-06]
    waa_16x32_stay_8020_e2e_delay_high_avg = [2.4989560620638395e-07, 2.5159337007920143e-07, 2.558498950413844e-07,
                                              2.6091564918484655e-07, 2.725999071185673e-07, 4.418291142846889e-05,
                                              9.614697616154561e-05, 0.0001238626065644682, 0.00010679408555080735,
                                              5.9219309755883625e-05, 4.383247755117486e-05, 3.2791162224878975e-05]
    waa_16x32_stay_8020_e2e_delay_high_err = [9.5108417645186e-10, 9.062340089279233e-10, 2.0121132706601607e-09,
                                              3.1946242564235964e-09, 6.872079462010108e-09, 2.8281613540136067e-05,
                                              3.327584243134288e-05, 2.07945524563312e-05, 1.975977836069559e-05,
                                              7.579857350378195e-06, 7.579857350378195e-06, 7.579857350378195e-06]
    waa_16x32_stay_8020_e2e_delay_med_avg = [6.044118194658021e-07, 6.147038512469529e-07, 6.431031153065439e-07,
                                             6.719980819137569e-07, 9.088257443041309e-07, 8.728437372714983e-05,
                                             0.0001934023019821313, 0.0002667887706185588, 0.0005722384497185393,
                                             0.000829712487396748, 0.0007162893698308501, 0.0007129503899488196]
    waa_16x32_stay_8020_e2e_delay_med_err = [8.511906046445063e-09, 9.743991796377636e-09, 1.1903426295438578e-08,
                                             2.9749828708469133e-08, 2.3394716667365043e-07, 5.5017059782052605e-05,
                                             6.786813963130007e-05, 8.929276951618635e-05, 0.00019037683181386087,
                                             3.353825801418114e-05, 3.353825801418114e-05, 3.353825801418114e-05]
    waa_16x32_stay_8020_e2e_delay_low_avg = [5.575226974189057e-06, 5.780396849903433e-06, 6.423004624829112e-06,
                                             9.34567714885521e-06, 2.4315317837160972e-05, 0.00014657061859299234,
                                             0.0003051052071425003, 0.0004176720803188001, 0.0006781763038693863,
                                             0.0007653566572346154, 0.0009021912508445281, 0.0009220737796398248]
    waa_16x32_stay_8020_e2e_delay_low_err = [6.039227293654687e-07, 5.993122307872844e-07, 5.442006716292733e-07,
                                             5.210000216488736e-06, 1.2735632285579594e-05, 7.417511312222525e-05,
                                             0.00010984241446976014, 0.00012357430134606257, 9.679149125063208e-05,
                                             2.2197634798670078e-06, 2.2197634798670078e-06, 2.2197634798670078e-06]

    w16_avg= draw_normal(waa_16x16_stay_8020_e2e_delay_total_avg,waa_16x16_stay_8020_e2e_delay_total_err)
    w16_high=draw_normal(waa_16x16_stay_8020_e2e_delay_high_avg,waa_16x16_stay_8020_e2e_delay_high_err)
    w16_med=draw_normal(waa_16x16_stay_8020_e2e_delay_med_avg,waa_16x16_stay_8020_e2e_delay_med_err)
    w16_low=draw_normal(waa_16x16_stay_8020_e2e_delay_low_avg,waa_16x16_stay_8020_e2e_delay_low_err)

    w24_avg= draw_normal(waa_16x24_stay_8020_e2e_delay_total_avg,waa_16x24_stay_8020_e2e_delay_total_err)
    w24_high=draw_normal(waa_16x24_stay_8020_e2e_delay_high_avg,waa_16x24_stay_8020_e2e_delay_high_err)
    w24_med=draw_normal(waa_16x24_stay_8020_e2e_delay_med_avg,waa_16x24_stay_8020_e2e_delay_med_err)
    w24_low=draw_normal(waa_16x24_stay_8020_e2e_delay_low_avg,waa_16x24_stay_8020_e2e_delay_low_err)

    w32_avg= draw_normal(waa_16x32_stay_8020_e2e_delay_total_avg,waa_16x32_stay_8020_e2e_delay_total_err)
    w32_high=draw_normal(waa_16x32_stay_8020_e2e_delay_high_avg,waa_16x32_stay_8020_e2e_delay_high_err)
    w32_med=draw_normal(waa_16x32_stay_8020_e2e_delay_med_avg,waa_16x32_stay_8020_e2e_delay_med_err)
    w32_low=draw_normal(waa_16x32_stay_8020_e2e_delay_low_avg,waa_16x32_stay_8020_e2e_delay_low_err)

    w16_avg=[x*1e3 for x in w16_avg]
    w16_high=[x*1e3 for x in w16_high]
    w16_med=[x*1e3 for x in w16_med]
    w16_low=[x*1e3 for x in w16_low]
    w24_avg=[x*1e3 for x in w24_avg]
    w24_high=[x*1e3 for x in w24_high]
    w24_med=[x*1e3 for x in w24_med]
    w24_low=[x*1e3 for x in w24_low]
    w32_avg=[x*1.2e3 for x in w32_avg]
    w32_high=[x*1.2e3 for x in w32_high]
    w32_med=[x*1.2e3 for x in w32_med]
    w32_low=[x*1.2e3 for x in w32_low]

    w16_avg_x,w16_avg_y=get_cdf_plotter(w16_avg)
    w16_high_x,w16_high_y=get_cdf_plotter(w16_high)
    w16_med_x,w16_med_y=get_cdf_plotter(w16_med)
    w16_low_x,w16_low_y=get_cdf_plotter(w16_low)
    w24_avg_x,w24_avg_y=get_cdf_plotter(w24_avg)
    w24_high_x,w24_high_y=get_cdf_plotter(w24_high)
    w24_med_x,w24_med_y=get_cdf_plotter(w24_med)
    w24_low_x,w24_low_y=get_cdf_plotter(w24_low)
    w32_avg_x,w32_avg_y=get_cdf_plotter(w32_avg)
    w32_high_x,w32_high_y=get_cdf_plotter(w32_high)
    w32_med_x,w32_med_y=get_cdf_plotter(w32_med)
    w32_low_x,w32_low_y=get_cdf_plotter(w32_low)

    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)


    if a==1:
        _LEGEND_LOC = 'lower right'
        _x_lim_end=0.6
        _LEGEND_SIZE = 52
        ax1.plot(w16_avg_x, w16_avg_y,'blue', label="N=16", linewidth=_LINEWIDTH + 1,linestyle='solid')
        ax1.plot(w24_avg_x, w24_avg_y,'blue', label="N=24", linewidth=_LINEWIDTH + 1,linestyle='dashed')
        ax1.plot(w32_avg_x, w32_avg_y,'blue', label="N=32", linewidth=_LINEWIDTH + 1,linestyle='dashdot')
    elif a==2:
        _x_lim_end = 5
        _LEGEND_LOC = 'lower right'
        _LEGEND_SIZE = 41
        #ax1.set_xscale('log')

        ax1.plot(w16_high_x,w16_high_y,'red', label="High(16)", linewidth=_LINEWIDTH + 1,linestyle='solid')
        ax1.plot(w24_high_x,w24_high_y,'red', label="High(24)", linewidth=_LINEWIDTH + 1,linestyle='dashed')
        ax1.plot(w32_high_x,w32_high_y,'red', label="High(32)", linewidth=_LINEWIDTH + 1,linestyle='dashdot')

        ax1.plot(w16_med_x,w16_med_y,'green', label="Med(16)", linewidth=_LINEWIDTH + 1,linestyle='solid')
        ax1.plot(w24_med_x,w24_med_y,'green', label="Med(24)", linewidth=_LINEWIDTH + 1,linestyle='dashed')
        ax1.plot(w32_med_x,w32_med_y,'green', label="Med(32)", linewidth=_LINEWIDTH + 1,linestyle='dashdot')

        ax1.plot( w16_low_x,w16_low_y,'blue', label="Low(16)", linewidth=_LINEWIDTH + 1,linestyle='solid')
        ax1.plot( w24_low_x,w24_low_y,'blue', label="Low(24)", linewidth=_LINEWIDTH + 1,linestyle='dashed')
        ax1.plot(w32_low_x,w32_low_y,'blue', label="Low(32)", linewidth=_LINEWIDTH + 1,linestyle='dashdot')
    elif a==3:
        _LEGEND_LOC = 'lower right'
        _x_lim_end=200
        _LEGEND_SIZE = 32
        ax1.set_xscale('log')
        ax1.plot(w16_avg_x, w16_avg_y,'k', label="Avg(16)", linewidth=_LINEWIDTH + 1,linestyle='solid')
        ax1.plot(w24_avg_x, w24_avg_y,'k', label="Avg(24)", linewidth=_LINEWIDTH + 1,linestyle='dashed')
        ax1.plot(w32_avg_x, w32_avg_y,'k', label="Avg(32)", linewidth=_LINEWIDTH + 1,linestyle='dashdot')

        ax1.plot(w16_high_x,w16_high_y,'red', label="High(16)", linewidth=_LINEWIDTH + 1,linestyle='solid')
        ax1.plot(w24_high_x,w24_high_y,'red', label="High(24)", linewidth=_LINEWIDTH + 1,linestyle='dashed')
        ax1.plot(w32_high_x,w32_high_y,'red', label="High(32)", linewidth=_LINEWIDTH + 1,linestyle='dashdot')

        ax1.plot(w16_med_x,w16_med_y,'green', label="Med(16)", linewidth=_LINEWIDTH + 1,linestyle='solid')
        ax1.plot(w24_med_x,w24_med_y,'green', label="Med(24)", linewidth=_LINEWIDTH + 1,linestyle='dashed')
        ax1.plot(w32_med_x,w32_med_y,'green', label="Med(32)", linewidth=_LINEWIDTH + 1,linestyle='dashdot')

        ax1.plot( w16_low_x,w16_low_y,'blue', label="Low(16)", linewidth=_LINEWIDTH + 1,linestyle='solid')
        ax1.plot( w24_low_x,w24_low_y,'blue', label="Low(24)", linewidth=_LINEWIDTH + 1,linestyle='dashed')
        ax1.plot(w32_low_x,w32_low_y,'blue', label="Low(32)", linewidth=_LINEWIDTH + 1,linestyle='dashdot')


    ax1.set_xlabel('End-to-end latency (ms)', fontsize=_LABEL_SIZE)
    ax1.set_ylabel('CDF', fontsize=_LABEL_SIZE)
    ax1.set_xlim(-0.001,_x_lim_end)
    #ax1.set_ylim(_y_lim_begin, _y_lim_end)
    ax1.legend(loc=_LEGEND_LOC, fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()

def plot_review_cdf_traffic():
    _x_lim_begin, _x_lim_end=-0.19,1
    _y_lim_begin,_y_lim_end=1e-4,1
    _x_label,_y_label='Normalized load','End-to-end latency (ms)'
    _nominal_thru=0.1*(16*4+16*1)

    _LINEWIDTH = 7
    _LEGEND_SIZE = 52
    _TICK_PARAMS = 45
    _LABEL_SIZE = 45
    _LEGEND_LOC = 'upper left'

    waa_16x16_stay_8020_e2e_delay_total_avg = [8.339012023784865e-07, 1.0788735164421421e-06,
                                                   1.4023286169417689e-06, 1.755143747235335e-06, 2.015132464525008e-06,
                                                   4.999789474653397e-06, 9.134282871767743e-06,2.2614819534698097e-06, 3.5039392619543457e-06,
                                                    1.4835211566942572e-05, 2.4895243716812446e-05,
                                                    4.594919255008208e-05, 6.094022116211189e-05, 6.905567607120142e-05,
                                                    7.730594337130474e-05, 8.20892894024645e-05]
    waa_16x16_stay_8020_e2e_delay_total_err = [2.0154520499669781e-07, 1.7116622941683624e-07,
                                                   2.151299861931038e-07, 3.491726215921739e-07, 2.1905653083030586e-07,
                                                   1.539123733696811e-06, 1.539123733696811e-06,8.356715792213857e-07, 1.0759422095935764e-06,
                                                    7.4541644000129166e-06, 1.1707372307121498e-05,
                                                    7.162649528061785e-07, 1.100428871715332e-05, 1.100428871715332e-05, 1.100428871715332e-05, 1.100428871715332e-05]

    waa_16x16_stay_7030_e2e_delay_total_avg = [6.86763110739149e-07, 7.523417005464491e-07,9.442081837299541e-07, 1.281589832609283e-06, 2.624805403614588e-06,
                                                   6.9839322670277535e-06, 1.3988079670189815e-05,1.6788823033535804e-05, 2.40116025644573e-05,7.540293142132962e-06,
                                                    1.664384085157387e-05, 4.04862831214415e-05, 5.8980524508642635e-05,
                                                    6.601094247326225e-05, 7.997857166957745e-05,0.00010179904043358083,
                                                    0.00011613653005708542,
                                                    0.00012241653729203083]

    waa_16x16_stay_7030_e2e_delay_total_err = [ 1.411543109081441e-07, 1.7637477526222403e-07,
                                                   1.624382953022694e-07, 1.655944417031628e-06, 4.306579240659058e-06,
                                                   1.5515890225628785e-06, 3.0419600161087095e-06, 3.0419600161087095e-06, 3.0419600161087095e-06, 8.430873764143533e-06,
                                                    1.402614846609604e-05, 1.6224596922846543e-05,
                                                    6.171779508358921e-06, 1.3076397636981308e-06,
                                                    5.215211468396298e-06, 5.215211468396298e-06,5.215211468396298e-06,5.215211468396298e-06]

    waa_16x16_stay_6040_e2e_delay_total_avg = [1.1861637565820211e-06, 1.5718675887191048e-06,
                                                   3.633625154299062e-06, 1.8655700435962842e-05, 3.412059825579249e-05,
                                                   5.222922178600031e-05, 6.620148395244496e-05,4.1483649812599585e-05, 5.3283099592275946e-05,
                                                    6.335382098129918e-05, 0.00010330243027693087,
                                                    0.00011449901688728686, 0.00012377544517559212,
                                                    0.00013524074251034107, 0.00014742336252030868]
    waa_16x16_stay_6040_e2e_delay_total_err = [ 4.086602157934147e-07, 7.841870494838514e-07,
                                                   3.976197161469704e-06, 1.0773209377101221e-05,
                                                   1.0622649998142639e-05, 1.3868895735957174e-06,
                                                   5.794628581745968e-06,1.204631791239113e-05,
                                                    2.2641773264237986e-05, 2.2984685948412748e-05,
                                                    1.8281184817107344e-05, 1.1089603843859296e-05, 1.856763282026756e-06,  6.7177743693846164e-06, 6.7177743693846164e-06]

    waa_8020= draw_normal(waa_16x16_stay_8020_e2e_delay_total_avg,waa_16x16_stay_8020_e2e_delay_total_err)
    waa_7030= draw_normal(waa_16x16_stay_7030_e2e_delay_total_avg,waa_16x16_stay_7030_e2e_delay_total_err)
    waa_6040= draw_normal(waa_16x16_stay_6040_e2e_delay_total_avg,waa_16x16_stay_6040_e2e_delay_total_err)


    waa_8020=[x*1e3 for x in waa_8020]
    waa_7030=[x*1e3 for x in waa_7030]
    waa_6040=[x*1e3 for x in waa_6040]

    waa_8020_x,waa_8020_y=get_cdf_plotter(waa_8020)
    waa_7030_x,waa_7030_y=get_cdf_plotter(waa_7030)
    waa_6040_x,waa_6040_y=get_cdf_plotter(waa_6040)

    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.plot(waa_8020_x, waa_8020_y,'k', label="Avg (80:20)", linewidth=_LINEWIDTH + 1,linestyle='solid')
    ax1.plot(waa_7030_x, waa_7030_y,'k', label="Avg (70:30)", linewidth=_LINEWIDTH + 1,linestyle='dashed')
    ax1.plot(waa_6040_x, waa_6040_y,'k', label="Avg (60:40)", linewidth=_LINEWIDTH + 1,linestyle='dashdot')


    ax1.set_xlabel('End-to-end latency (ms)', fontsize=_LABEL_SIZE)
    ax1.set_ylabel('CDF', fontsize=_LABEL_SIZE)
    #ax1.set_xlim(-0.001,1000)
    #ax1.set_ylim(_y_lim_begin, _y_lim_end)
    ax1.legend(loc='lower right', fontsize=_LEGEND_SIZE)
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

_16xN='1stay'
if _16xN=='stay':
    plot07_16xN_stay_8020_server_thru(zmall='half')
    plot08_16xN_stay_8020_e2e_delays(zmall='800')
    #prep_plot09_16xN_stay_8020_e2e_delays(zmall='800')
    plot09_16xN_stay_8020_e2e_delays() #todo
elif _16xN=='go':
    plot07_16xN_go_8020_server_thru(zmall='800')#'half'
    #plot08_16xN_go_8020_e2e_delays(zmall='800')
    ###plot09_16xN_go_8020_e2e_delays() todooo


#plot10_calabr_thru()
#plot11_calabr_delay()
#plot12_calabr_loss()

#plot_review_cdf_vanilla_stayin()
#plot_review_cdf_traffic()
#plot_review_cdf_servers(a=1)
#plot_review_cdf_servers(a=2)
plot_review_cdf_servers(a=3)