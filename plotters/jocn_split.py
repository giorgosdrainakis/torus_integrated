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
from torus_integrated.plotters.jocn_split_data import *
from torus_integrated.plotters.jocn_split_data2 import *

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

def plot_thru_intra(data,strategy,distribution='8020'):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Intra-rack load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    if data==1600:
        max_thru = 400
        x_lim_begin = -0.1
        x_lim_end=450
        if strategy=='go':
            if distribution=='8020':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_intra_load_total_bps_avg, waa_1600_go_intra_thru_total_bps_avg,
                                                   waa_1600_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
            elif distribution=='7030':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_intra_7030_load_total_bps_avg, waa_1600_go_intra_7030_thru_total_bps_avg,
                                                   waa_1600_go_intra_7030_drop_total_bps_avg,cleaning_factor=1e9)
            elif distribution=='6040':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_intra_6040_load_total_bps_avg, waa_1600_go_intra_6040_thru_total_bps_avg,
                                                   waa_1600_go_intra_6040_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_1600_stay_intra_load_total_bps_avg, waa_1600_stay_intra_thru_total_bps_avg,
                                               waa_1600_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)
    elif data==2400:
        max_thru = 400
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_2400_go_intra_load_total_bps_avg, waa_2400_go_intra_thru_total_bps_avg,
                                               waa_2400_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_2400_stay_intra_load_total_bps_avg, waa_2400_stay_intra_thru_total_bps_avg,
                                               waa_2400_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)
    elif data==3200:
        max_thru = 400
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_3200_go_intra_load_total_bps_avg, waa_3200_go_intra_thru_total_bps_avg,
                                               waa_3200_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_3200_stay_intra_load_total_bps_avg, waa_3200_stay_intra_thru_total_bps_avg,
                                               waa_3200_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)

    # Activate max throughput line
    nominal_thru=[]
    for el in load:
        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load, thru,'b', label="Throughput",linewidth=_LINEWIDTH)
    ax1.plot(load, drop,'r', label="Drop-rate",linewidth=_LINEWIDTH)
    ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"capacity", linewidth=_LINEWIDTH)
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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def plot_thru_per_server_intra(data,strategy):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Intra-rack load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    if data==1600:
        max_thru = 400
        num_servers = 16
        x_lim_begin = -1
        x_lim_end=450
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_1600_go_intra_load_total_bps_avg, waa_1600_go_intra_thru_total_bps_avg,
                                               waa_1600_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_1600_stay_intra_load_total_bps_avg, waa_1600_stay_intra_thru_total_bps_avg,
                                               waa_1600_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)
    elif data==2400:
        max_thru = 400
        num_servers = 24
        x_lim_begin = -1
        x_lim_end=450
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_2400_go_intra_load_total_bps_avg, waa_2400_go_intra_thru_total_bps_avg,
                                               waa_2400_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_2400_stay_intra_load_total_bps_avg, waa_2400_stay_intra_thru_total_bps_avg,
                                               waa_2400_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)
    elif data==3200:
        max_thru = 400
        num_servers=32
        x_lim_begin = -1
        x_lim_end=450
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_3200_go_intra_load_total_bps_avg, waa_3200_go_intra_thru_total_bps_avg,
                                               waa_3200_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_3200_stay_intra_load_total_bps_avg, waa_3200_stay_intra_thru_total_bps_avg,
                                               waa_3200_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)

    # Activate max throughput line
    nominal_thru=[]
    for el in load:
        nominal_thru.append(max_thru)

    # Activate thru/drop averaging
    thru=[x/num_servers for x in thru]
    drop = [x / num_servers for x in drop]

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load, thru,'b', label="Throughput per server",linewidth=_LINEWIDTH)
    #ax1.plot(load, drop,'r', label="Drop-rate",linewidth=_LINEWIDTH)
    #ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"throughput", linewidth=_LINEWIDTH)
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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def plot_thru_per_server_intra_multiple(data_list,strategy):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Intra-rack load (Gbps)'
    y_label='Throughput per server (Gbps)'
    legend_loc='upper left'

    load_list=[]
    thru_list=[]
    drop_list=[]
    serv_list=[]

    for data in data_list:
        # Clean my loads and assign max thru values and limits
        if data==1600:
            max_thru = 400
            num_servers = 16
            x_lim_begin = -1
            x_lim_end=450
            if strategy=='stay':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_intra_load_total_bps_avg, waa_1600_go_intra_thru_total_bps_avg,
                                                   waa_1600_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
            elif strategy=='go':
                load, thru, drop = clean_load_thru_drop(waa_1600_stay_intra_load_total_bps_avg, waa_1600_stay_intra_thru_total_bps_avg,
                                                   waa_1600_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)
        elif data==2400:
            max_thru = 400
            num_servers = 24
            x_lim_begin = -1
            x_lim_end=450
            if strategy=='go':
                load, thru, drop = clean_load_thru_drop(waa_2400_go_intra_load_total_bps_avg, waa_2400_go_intra_thru_total_bps_avg,
                                                   waa_2400_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
            elif strategy=='stay':
                load, thru, drop = clean_load_thru_drop(waa_2400_stay_intra_load_total_bps_avg, waa_2400_stay_intra_thru_total_bps_avg,
                                                   waa_2400_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)
        elif data==3200:
            max_thru = 400
            num_servers=32
            x_lim_begin = -1
            x_lim_end=450
            if strategy=='go':
                load, thru, drop = clean_load_thru_drop(waa_3200_go_intra_load_total_bps_avg, waa_3200_go_intra_thru_total_bps_avg,
                                                   waa_3200_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
            elif strategy=='stay':
                load, thru, drop = clean_load_thru_drop(waa_3200_stay_intra_load_total_bps_avg, waa_3200_stay_intra_thru_total_bps_avg,
                                                   waa_3200_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)

        load_list.append(load)
        thru_list.append(thru)
        drop_list.append(drop)
        serv_list.append(num_servers)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
    #        nominal_thru.append(max_thru)

    # Activate thru/drop averaging
    for i in range(len(serv_list)):
        thru_list[i]=[x/serv_list[i] for x in thru_list[i]]
        drop_list[i] = [x / serv_list[i] for x in drop_list[i]]

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45
    color=['b','b--','b-.']
    color2 = ['r', 'r--', 'r-.']
    for i in range(len(serv_list)):
        ax1.plot(load_list[i], thru_list[i],color[i], label="N="+str(serv_list[i]),linewidth=_LINEWIDTH)
    #ax1.plot(load, drop,'r', label="Drop-rate",linewidth=_LINEWIDTH)
    #ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"throughput", linewidth=_LINEWIDTH)
    try:
        ax1.set_xlabel(x_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_ylabel(y_label, fontsize=_LABEL_SIZE-9)
    except:
        pass
    try:
        ax1.set_xlim(x_lim_begin,x_lim_end)
    except:
        pass
    try:
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def plot_delay_multiple(data_list,strategy):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'
    y_label='End-to-end delay (ms)'
    legend_loc='lower right'

    load_list=[]
    delay_list=[]
    serv_list=[]

    for data in data_list:
        # Clean my loads and assign max thru values and limits
        # Clean my loads and assign limits
        if data == 1600:
            x_lim_begin = 1.95
            x_lim_end = 10
            num_servers=16
            if strategy == 'go':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_1600_go_e2e_load_total_bps_avg,
                    waa_1600_go_e2e_delay_total_avg,
                    waa_1600_go_e2e_delay_high_avg,
                    waa_1600_go_e2e_delay_med_avg,
                    waa_1600_go_e2e_delay_low_avg,
                    cleaning_factor=1e12)
            elif strategy == 'stay':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_1600_stay_e2e_load_total_bps_avg,
                    waa_1600_stay_e2e_delay_total_avg,
                    waa_1600_stay_e2e_delay_high_avg,
                    waa_1600_stay_e2e_delay_med_avg,
                    waa_1600_stay_e2e_delay_low_avg,
                    cleaning_factor=1e12)
        elif data == 2400:
            x_lim_begin = 1.95
            x_lim_end = 10
            num_servers = 24
            if strategy == 'go':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_2400_go_e2e_load_total_bps_avg,
                    waa_2400_go_e2e_delay_total_avg,
                    waa_2400_go_e2e_delay_high_avg,
                    waa_2400_go_e2e_delay_med_avg,
                    waa_2400_go_e2e_delay_low_avg,
                    cleaning_factor=1e12)
            elif strategy == 'stay':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_2400_stay_e2e_load_total_bps_avg,
                    waa_2400_stay_e2e_delay_total_avg,
                    waa_2400_stay_e2e_delay_high_avg,
                    waa_2400_stay_e2e_delay_med_avg,
                    waa_2400_stay_e2e_delay_low_avg,
                    cleaning_factor=1e12)
        elif data == 3200:
            x_lim_begin = 1.95
            x_lim_end = 10
            num_servers = 32
            if strategy == 'go':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_3200_go_e2e_load_total_bps_avg,
                    waa_3200_go_e2e_delay_total_avg,
                    waa_3200_go_e2e_delay_high_avg,
                    waa_3200_go_e2e_delay_med_avg,
                    waa_3200_go_e2e_delay_low_avg,
                    cleaning_factor=1e12)
            elif strategy == 'stay':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_3200_stay_e2e_load_total_bps_avg,
                    waa_3200_stay_e2e_delay_total_avg,
                    waa_3200_stay_e2e_delay_high_avg,
                    waa_3200_stay_e2e_delay_med_avg,
                    waa_3200_stay_e2e_delay_low_avg,
                    cleaning_factor=1e12)

        load_list.append(load)
        delay_list.append(avg_delay)
        serv_list.append(num_servers)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
    #        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45

    color=['b','b--','b-.']
    for i in range(len(serv_list)):
        ax1.semilogy(load_list[i][limit:], delay_list[i][limit:],color[i], label="N="+str(serv_list[i]), linewidth=_LINEWIDTH)

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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def plot_thru_inter(data,strategy,distribution='8020'):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Inter-rack load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    if data==1600:
        max_thru = 16 * 4 * 40
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':

            if distribution=='8020':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_inter_load_total_bps_avg,
                                                        waa_1600_go_inter_thru_total_bps_avg,
                                                        waa_1600_go_inter_drop_total_bps_avg, cleaning_factor=1e9)
            elif distribution=='7030':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_inter_7030_load_total_bps_avg, waa_1600_go_inter_7030_thru_total_bps_avg,
                                                   waa_1600_go_inter_7030_drop_total_bps_avg,cleaning_factor=1e9)
            elif distribution=='6040':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_inter_6040_load_total_bps_avg, waa_1600_go_inter_6040_thru_total_bps_avg,
                                                   waa_1600_go_inter_6040_drop_total_bps_avg,cleaning_factor=1e9)

        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_1600_stay_inter_load_total_bps_avg, waa_1600_stay_inter_thru_total_bps_avg,
                                               waa_1600_stay_inter_drop_total_bps_avg,cleaning_factor=1e9)
    elif data==2400:
        max_thru = 16 * 4 * 40
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_2400_go_inter_load_total_bps_avg, waa_2400_go_inter_thru_total_bps_avg,
                                               waa_2400_go_inter_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_2400_stay_inter_load_total_bps_avg, waa_2400_stay_inter_thru_total_bps_avg,
                                               waa_2400_stay_inter_drop_total_bps_avg,cleaning_factor=1e9)
    elif data==3200:
        max_thru = 16 * 4 * 40
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_3200_go_inter_load_total_bps_avg, waa_3200_go_inter_thru_total_bps_avg,
                                               waa_3200_go_inter_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_3200_stay_inter_load_total_bps_avg, waa_3200_stay_inter_thru_total_bps_avg,
                                               waa_3200_stay_inter_drop_total_bps_avg,cleaning_factor=1e9)
    nominal_thru=[]
    for el in load:
        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load, thru,'b', label="Throughput",linewidth=_LINEWIDTH)
    ax1.plot(load, drop,'r', label="Drop-rate",linewidth=_LINEWIDTH)
    ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"capacity", linewidth=_LINEWIDTH)
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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def plot_thru_e2e(data,strategy,distribution='8020'):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'
    y_label='Bitrate (Tbps)'
    legend_loc='center right'

    # Clean my loads and assign max thru values and limits
    if data==1600:
        max_thru = 16*0.4+16*0.1
        x_lim_begin = -0.1
        x_lim_end=10
        if strategy=='go':
            if distribution=='8020':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_e2e_load_total_bps_avg, waa_1600_go_e2e_thru_total_bps_avg,
                                               waa_1600_go_e2e_drop_total_bps_avg,cleaning_factor=1e12)
            elif distribution=='7030':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_e2e_7030_load_total_bps_avg, waa_1600_go_e2e_7030_thru_total_bps_avg,
                                                   waa_1600_go_e2e_7030_drop_total_bps_avg,cleaning_factor=1e12)
            elif distribution=='6040':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_e2e_6040_load_total_bps_avg, waa_1600_go_e2e_6040_thru_total_bps_avg,
                                                   waa_1600_go_e2e_6040_drop_total_bps_avg,cleaning_factor=1e12)

        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_1600_stay_e2e_load_total_bps_avg, waa_1600_stay_e2e_thru_total_bps_avg,
                                               waa_1600_stay_e2e_drop_total_bps_avg,cleaning_factor=1e12)
    elif data==2400:
        max_thru = 16*0.4+16*0.1
        x_lim_begin = -0.1
        x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_2400_go_e2e_load_total_bps_avg, waa_2400_go_e2e_thru_total_bps_avg,
                                               waa_2400_go_e2e_drop_total_bps_avg,cleaning_factor=1e12)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_2400_stay_e2e_load_total_bps_avg, waa_2400_stay_e2e_thru_total_bps_avg,
                                               waa_2400_stay_e2e_drop_total_bps_avg,cleaning_factor=1e12)
    elif data==3200:
        max_thru = 16*0.4+16*0.1
        x_lim_begin = -0.1
        x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_3200_go_e2e_load_total_bps_avg, waa_3200_go_e2e_thru_total_bps_avg,
                                               waa_3200_go_e2e_drop_total_bps_avg,cleaning_factor=1e12)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_3200_stay_e2e_load_total_bps_avg, waa_3200_stay_e2e_thru_total_bps_avg,
                                               waa_3200_stay_e2e_drop_total_bps_avg,cleaning_factor=1e12)
    nominal_thru=[]
    for el in load:
        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=30
    _TICK_PARAMS=45
    ax1.plot(load, thru,'b', label="Throughput",linewidth=_LINEWIDTH)
    ax1.plot(load, drop,'r', label="Drop-rate",linewidth=_LINEWIDTH)
    ax1.plot(load, nominal_thru, 'k--', label="Nominal capacity", linewidth=_LINEWIDTH)
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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def plot_delays_e2e(data, strategy,toplot,distribution='8020'):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'
    y_label='End-to-end delay (ms)'
    legend_loc='center right'

    # Clean my loads and assign limits
    if data==1600:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':

            if distribution=='8020':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_1600_go_e2e_load_total_bps_avg,
                    waa_1600_go_e2e_delay_total_avg,
                    waa_1600_go_e2e_delay_high_avg,
                    waa_1600_go_e2e_delay_med_avg,
                    waa_1600_go_e2e_delay_low_avg,
                    cleaning_factor=1e12)
            elif distribution=='7030':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_1600_go_e2e_7030_load_total_bps_avg,
                    waa_1600_go_e2e_7030_delay_total_avg,
                    waa_1600_go_e2e_7030_delay_high_avg,
                    waa_1600_go_e2e_7030_delay_med_avg,
                    waa_1600_go_e2e_7030_delay_low_avg,
                    cleaning_factor=1e12)
            elif distribution=='6040':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_1600_go_e2e_6040_load_total_bps_avg,
                    waa_1600_go_e2e_6040_delay_total_avg,
                    waa_1600_go_e2e_6040_delay_high_avg,
                    waa_1600_go_e2e_6040_delay_med_avg,
                    waa_1600_go_e2e_6040_delay_low_avg,
                    cleaning_factor=1e12)

        elif strategy=='stay':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_1600_stay_e2e_load_total_bps_avg,
                                                                                  waa_1600_stay_e2e_delay_total_avg,
                                                                                  waa_1600_stay_e2e_delay_high_avg,
                                                                                  waa_1600_stay_e2e_delay_med_avg,
                                                                                  waa_1600_stay_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==2400:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_2400_go_e2e_load_total_bps_avg,
                                                                                  waa_2400_go_e2e_delay_total_avg,
                                                                                  waa_2400_go_e2e_delay_high_avg,
                                                                                  waa_2400_go_e2e_delay_med_avg,
                                                                                  waa_2400_go_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_2400_stay_e2e_load_total_bps_avg,
                                                                                  waa_2400_stay_e2e_delay_total_avg,
                                                                                  waa_2400_stay_e2e_delay_high_avg,
                                                                                  waa_2400_stay_e2e_delay_med_avg,
                                                                                  waa_2400_stay_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==3200:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_3200_go_e2e_load_total_bps_avg,
                                                                                  waa_3200_go_e2e_delay_total_avg,
                                                                                  waa_3200_go_e2e_delay_high_avg,
                                                                                  waa_3200_go_e2e_delay_med_avg,
                                                                                  waa_3200_go_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_3200_stay_e2e_load_total_bps_avg,
                                                                                  waa_3200_stay_e2e_delay_total_avg,
                                                                                  waa_3200_stay_e2e_delay_high_avg,
                                                                                  waa_3200_stay_e2e_delay_med_avg,
                                                                                  waa_3200_stay_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)

    print(str(load))
    print(str(high_delay))
    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45

    if toplot in ['only_avg','all']:
        ax1.semilogy(load[limit:], avg_delay[limit:], 'k', label="avg", linewidth=4)
    if toplot in ['only_hml','all']:
        ax1.semilogy(load[limit:], high_delay[limit:],'r', label="High",linewidth=_LINEWIDTH)
        ax1.semilogy(load[limit:], med_delay[limit:],'g', label="Med",linewidth=_LINEWIDTH)
        ax1.semilogy(load[limit:], low_delay[limit:],'b', label="Low",linewidth=_LINEWIDTH)

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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def plot_qdelays_e2e(data, strategy,toplot,distribution='8020'):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'
    y_label='End-to-end qdelay (ms)'
    legend_loc='center right'

    # Clean my loads and assign limits
    if data==1600:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':

            if distribution=='8020':
                load, avg_qdelay, high_qdelay, med_delay, low_qdelay = clean_load_delays(
                    waa_1600_go_e2e_load_total_bps_avg,
                    waa_1600_go_e2e_qdelay_total_avg,
                    waa_1600_go_e2e_qdelay_high_avg,
                    waa_1600_go_e2e_qdelay_med_avg,
                    waa_1600_go_e2e_qdelay_low_avg,
                    cleaning_factor=1e12)
            elif distribution=='7030':
                load, avg_qdelay, high_qdelay, med_qdelay, low_qdelay = clean_load_delays(
                    waa_1600_go_e2e_7030_load_total_bps_avg,
                    waa_1600_go_e2e_7030_qdelay_total_avg,
                    waa_1600_go_e2e_7030_qdelay_high_avg,
                    waa_1600_go_e2e_7030_qdelay_med_avg,
                    waa_1600_go_e2e_7030_qdelay_low_avg,
                    cleaning_factor=1e12)
            elif distribution=='6040':
                load, avg_qdelay, high_qdelay, med_qdelay, low_qdelay = clean_load_delays(
                    waa_1600_go_e2e_6040_load_total_bps_avg,
                    waa_1600_go_e2e_6040_qdelay_total_avg,
                    waa_1600_go_e2e_6040_qdelay_high_avg,
                    waa_1600_go_e2e_6040_qdelay_med_avg,
                    waa_1600_go_e2e_6040_qdelay_low_avg,
                    cleaning_factor=1e12)

        elif strategy=='stay':
            load, avg_qdelay, high_qdelay, med_qdelay, low_qdelay = clean_load_delays(waa_1600_stay_e2e_load_total_bps_avg,
                                                                                  waa_1600_stay_e2e_qdelay_total_avg,
                                                                                  waa_1600_stay_e2e_qdelay_high_avg,
                                                                                  waa_1600_stay_e2e_qdelay_med_avg,
                                                                                  waa_1600_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==2400:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
            load, avg_qdelay, high_qdelay, med_qdelay, low_qdelay = clean_load_delays(waa_2400_go_e2e_load_total_bps_avg,
                                                                                  waa_2400_go_e2e_qdelay_total_avg,
                                                                                  waa_2400_go_e2e_qdelay_high_avg,
                                                                                  waa_2400_go_e2e_qdelay_med_avg,
                                                                                  waa_2400_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load, avg_qdelay, high_qdelay, med_qdelay, low_qdelay = clean_load_delays(waa_2400_stay_e2e_load_total_bps_avg,
                                                                                  waa_2400_stay_e2e_qdelay_total_avg,
                                                                                  waa_2400_stay_e2e_qdelay_high_avg,
                                                                                  waa_2400_stay_e2e_qdelay_med_avg,
                                                                                  waa_2400_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==3200:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
            load, avg_qdelay, high_qdelay, med_qdelay, low_qdelay = clean_load_delays(waa_3200_go_e2e_load_total_bps_avg,
                                                                                  waa_3200_go_e2e_qdelay_total_avg,
                                                                                  waa_3200_go_e2e_qdelay_high_avg,
                                                                                  waa_3200_go_e2e_qdelay_med_avg,
                                                                                  waa_3200_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load, avg_qdelay, high_qdelay, med_qdelay, low_qdelay = clean_load_delays(waa_3200_stay_e2e_load_total_bps_avg,
                                                                                  waa_3200_stay_e2e_qdelay_total_avg,
                                                                                  waa_3200_stay_e2e_qdelay_high_avg,
                                                                                  waa_3200_stay_e2e_qdelay_med_avg,
                                                                                  waa_3200_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)

    print(str(load))
    print(str(high_qdelay))
    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_qdelay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45

    if toplot in ['only_avg','all']:
        ax1.semilogy(load[limit:], avg_qdelay[limit:], 'k', label="avg", linewidth=4)
    if toplot in ['only_hml','all']:
        ax1.semilogy(load[limit:], high_qdelay[limit:],'r', label="High",linewidth=_LINEWIDTH)
        ax1.semilogy(load[limit:], med_qdelay[limit:],'g', label="Med",linewidth=_LINEWIDTH)
        ax1.semilogy(load[limit:], low_qdelay[limit:],'b', label="Low",linewidth=_LINEWIDTH)

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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def plot_qdelays_2e2e(data, strategy,toplot):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'
    y_label='Queuing delay (ms)'
    legend_loc='center right'

    # Clean my loads and assign limits
    if data==1600:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_1600_go_e2e_load_total_bps_avg,
                                                                                  waa_1600_go_e2e_qdelay_total_avg,
                                                                                  waa_1600_go_e2e_qdelay_high_avg,
                                                                                  waa_1600_go_e2e_qdelay_med_avg,
                                                                                  waa_1600_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_1600_stay_e2e_load_total_bps_avg,
                                                                                  waa_1600_stay_e2e_qdelay_total_avg,
                                                                                  waa_1600_stay_e2e_qdelay_high_avg,
                                                                                  waa_1600_stay_e2e_qdelay_med_avg,
                                                                                  waa_1600_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==2400:
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_2400_go_e2e_load_total_bps_avg,
                                                                                  waa_2400_go_e2e_qdelay_total_avg,
                                                                                  waa_2400_go_e2e_qdelay_high_avg,
                                                                                  waa_2400_go_e2e_qdelay_med_avg,
                                                                                  waa_2400_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_2400_stay_e2e_load_total_bps_avg,
                                                                                  waa_2400_stay_e2e_qdelay_total_avg,
                                                                                  waa_2400_stay_e2e_qdelay_high_avg,
                                                                                  waa_2400_stay_e2e_qdelay_med_avg,
                                                                                  waa_2400_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==3200:
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_3200_go_e2e_load_total_bps_avg,
                                                                                  waa_3200_go_e2e_qdelay_total_avg,
                                                                                  waa_3200_go_e2e_qdelay_high_avg,
                                                                                  waa_3200_go_e2e_qdelay_med_avg,
                                                                                  waa_3200_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_3200_stay_e2e_load_total_bps_avg,
                                                                                  waa_3200_stay_e2e_qdelay_total_avg,
                                                                                  waa_3200_stay_e2e_qdelay_high_avg,
                                                                                  waa_3200_stay_e2e_qdelay_med_avg,
                                                                                  waa_3200_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)

    print(str(load))
    print(str(high_delay))
    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45

    if toplot in ['only_avg','all']:
        ax1.semilogy(load[limit:], avg_delay[limit:], 'k', label="avg", linewidth=4)
    if toplot in ['only_hml','all']:
        ax1.semilogy(load[limit:], high_delay[limit:],'r', label="High",linewidth=_LINEWIDTH)
        ax1.semilogy(load[limit:], med_delay[limit:],'g', label="Med",linewidth=_LINEWIDTH)
        ax1.semilogy(load[limit:], low_delay[limit:],'b', label="Low",linewidth=_LINEWIDTH)

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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def plot_delays_n_qdelays_e2e(data, strategy,toplot):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'
    y_label='End-to-end delay (ms)'
    legend_loc='center right'
    y_lim_begin=0
    y_lim_end=1e-1
    # Clean my loads and assign limits
    if data==1600:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
            load_delay, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_1600_go_e2e_load_total_bps_avg,
                                                                                  waa_1600_go_e2e_delay_total_avg,
                                                                                  waa_1600_go_e2e_delay_high_avg,
                                                                                  waa_1600_go_e2e_delay_med_avg,
                                                                                  waa_1600_go_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
            load_q, avg_q, high_q, med_q, low_q = clean_load_delays(waa_1600_go_e2e_load_total_bps_avg,
                                                                                  waa_1600_go_e2e_qdelay_total_avg,
                                                                                  waa_1600_go_e2e_qdelay_high_avg,
                                                                                  waa_1600_go_e2e_qdelay_med_avg,
                                                                                  waa_1600_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load_delay, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_1600_stay_e2e_load_total_bps_avg,
                                                                                  waa_1600_stay_e2e_delay_total_avg,
                                                                                  waa_1600_stay_e2e_delay_high_avg,
                                                                                  waa_1600_stay_e2e_delay_med_avg,
                                                                                  waa_1600_stay_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
            load_q, avg_q, high_q, med_q, low_q = clean_load_delays(waa_1600_stay_e2e_load_total_bps_avg,
                                                                                  waa_1600_stay_e2e_qdelay_total_avg,
                                                                                  waa_1600_stay_e2e_qdelay_high_avg,
                                                                                  waa_1600_stay_e2e_qdelay_med_avg,
                                                                                  waa_1600_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==2400:
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load_delay, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_2400_go_e2e_load_total_bps_avg,
                                                                                  waa_2400_go_e2e_delay_total_avg,
                                                                                  waa_2400_go_e2e_delay_high_avg,
                                                                                  waa_2400_go_e2e_delay_med_avg,
                                                                                  waa_2400_go_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
            load_q, avg_q, high_q, med_q, low_q = clean_load_delays(waa_2400_go_e2e_load_total_bps_avg,
                                                                                  waa_2400_go_e2e_qdelay_total_avg,
                                                                                  waa_2400_go_e2e_qdelay_high_avg,
                                                                                  waa_2400_go_e2e_qdelay_med_avg,
                                                                                  waa_2400_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load_delay, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_2400_stay_e2e_load_total_bps_avg,
                                                                                  waa_2400_stay_e2e_delay_total_avg,
                                                                                  waa_2400_stay_e2e_delay_high_avg,
                                                                                  waa_2400_stay_e2e_delay_med_avg,
                                                                                  waa_2400_stay_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
            load_q, avg_q, high_q, med_q, low_q = clean_load_delays(waa_2400_stay_e2e_load_total_bps_avg,
                                                                                  waa_2400_stay_e2e_qdelay_total_avg,
                                                                                  waa_2400_stay_e2e_qdelay_high_avg,
                                                                                  waa_2400_stay_e2e_qdelay_med_avg,
                                                                                  waa_2400_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==3200:
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load_delay, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_3200_go_e2e_load_total_bps_avg,
                                                                                  waa_3200_go_e2e_delay_total_avg,
                                                                                  waa_3200_go_e2e_delay_high_avg,
                                                                                  waa_3200_go_e2e_delay_med_avg,
                                                                                  waa_3200_go_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
            load_q, avg_q, high_q, med_q, low_q = clean_load_delays(waa_3200_go_e2e_load_total_bps_avg,
                                                                                  waa_3200_go_e2e_qdelay_total_avg,
                                                                                  waa_3200_go_e2e_qdelay_high_avg,
                                                                                  waa_3200_go_e2e_qdelay_med_avg,
                                                                                  waa_3200_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load_delay, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_3200_stay_e2e_load_total_bps_avg,
                                                                                  waa_3200_stay_e2e_delay_total_avg,
                                                                                  waa_3200_stay_e2e_delay_high_avg,
                                                                                  waa_3200_stay_e2e_delay_med_avg,
                                                                                  waa_3200_stay_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
            load_q, avg_q, high_q, med_q, low_q = clean_load_delays(waa_3200_stay_e2e_load_total_bps_avg,
                                                                                  waa_3200_stay_e2e_qdelay_total_avg,
                                                                                  waa_3200_stay_e2e_qdelay_high_avg,
                                                                                  waa_3200_stay_e2e_qdelay_med_avg,
                                                                                  waa_3200_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45

    if toplot in ['only_avg','all']:
        ax1.semilogy(load_delay[limit:], avg_delay[limit:], 'b', label="total delay", linewidth=_LINEWIDTH+1)
        ax1.semilogy(load_q[limit:], avg_q[limit:], 'r', label="queuing delay", linewidth=_LINEWIDTH)
    if toplot in ['only_hml','all']:
        ax1.semilogy(load_delay[limit:], high_delay[limit:],'r', label="High",linewidth=_LINEWIDTH)
        ax1.semilogy(load_delay[limit:], med_delay[limit:],'g', label="Med",linewidth=_LINEWIDTH)
        ax1.semilogy(load_delay[limit:], low_delay[limit:],'b', label="Low",linewidth=_LINEWIDTH)

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
        ax1.set_ylim(y_lim_begin,y_lim_end)
    except:
        pass
    try:
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def plot_compare_delay_bar():
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'

    x_lim_begin=-2
    x_lim_end=12
    y_label='End-to-end delay (ms)'
    legend_loc='lower left'

    fig, ax1 = plt.subplots(constrained_layout=False)
    ax1.set_yscale('log')

    load=[2.5,5,7.5,10]
    high2400=[0.00045,0.00045,0.00050,0.00056]
    med2400=[0.228,0.234,0.517,0.6]
    low2400=[0.353,0.318,0.483,0.574]
    avg2400=[0.046,0.048,0.111,0.17]
    high3200=[0.00034,0.00034,0.00035,0.00041]
    med3200=[0.021,0.021,0.054,0.22]
    low3200=[0.102,0.102,0.145,0.27]
    avg3200=[0.0082,0.0082,0.019,0.06]

    mini_size = 0.16
    big_size = 0.65
    width = 0.25

    x_med = load
    x_med_2400 = [x - mini_size for x in x_med]
    x_med_3200 = [x + mini_size for x in x_med]

    x_high = [x - big_size for x in x_med]
    x_high_2400 = [x - mini_size for x in x_high]
    x_high_3200  = [x + mini_size for x in x_high]

    x_low = [x + big_size for x in x_med]
    x_low_2400 = [x - mini_size for x in x_low]
    x_low_3200  = [x + mini_size for x in x_low]


    ax1.bar(x_high_2400, high2400, color='white',edgecolor='red', label="High-4ch",linewidth=4, width=width,hatch='//')
    ax1.bar(x_med_2400, med2400,  color='white',edgecolor='green', label="Med-4ch",linewidth=4, width=width,hatch='//')
    ax1.bar(x_low_2400, low2400,  color='white',edgecolor='blue', label="Low-4ch",linewidth=4, width=width,hatch='//')
    ax1.bar(x_high_3200, high3200, color='white',edgecolor='red',  label="High-6ch",linewidth=4, width=width, hatch='o')
    ax1.bar(x_med_3200, med3200, color='white',edgecolor='green', label="Med-6ch",linewidth=4, width=width, hatch='o')
    ax1.bar(x_low_3200, low3200, color='white',edgecolor='blue', label="Low-6ch",linewidth=4, width=width, hatch='o')
    ax1.set_xticks([0,2.5,5,7.5,10])
    legend_fontsize = 21
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=37
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
def plot_compare_delay_bar_B():
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
    high_go=[0.000476,0.000506,0.000777,0.000989,0.00103]
    med_go = [0.000685,0.000748,0.0066,0.0272,0.0322]
    low_go = [0.0211,0.0222,0.1,0.225,0.237]
    high_stay=[0.000253,0.000253,0.000321,0.000437,0.000464]
    med_stay = [0.00079,0.00079,0.00814,0.0318,0.0382]
    low_stay = [0.0213,0.024,0.125,0.266,0.277]

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
    ax1.bar(x_high_3200, high_stay, color='white',edgecolor='red',  label="StayIn/Low",linewidth=4, width=width, hatch='o')
    ax1.bar(x_med_3200, med_stay, color='white',edgecolor='green', label="StayIn/Med",linewidth=4, width=width, hatch='o')
    ax1.bar(x_low_3200, low_stay, color='white',edgecolor='blue', label="StayIn/High",linewidth=4, width=width, hatch='o')
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
def plot_compare_delay_bar_C():
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'

    x_lim_begin=-3
    x_lim_end=12
    y_label='End-to-end delay (ms)'
    legend_loc='lower left'

    fig, ax1 = plt.subplots(constrained_layout=False)
    ax1.set_yscale('log')

    load=[2,4,6,8,10]
#    high_1600= [0.000256,0.000256,0.000320,0.000440,0.000460]
#    med_1600 = [0.000800,0.000800,0.000830,0.033700,0.033800]
#    low_1600 = [0.021700,0.021700,0.128000,0.275000,0.288000]

    high_1600=[0.000253,0.000253,0.000321,0.000437,0.000464]
    med_1600 = [0.00079,0.00079,0.00814,0.0318,0.0382]
    low_1600 = [0.0213,0.024,0.125,0.266,0.277]

    high_2400= [0.0160,0.0160,0.0220,0.111,0.117]
    med_2400 = [0.0629,0.0629,0.0784,0.317,0.636]
    low_2400 = [0.1040,0.1040,0.1290,0.459,0.827]

    high_3200= [0.044,0.044,0.048,0.122,0.126]
    med_3200 = [0.089,0.089,0.100,0.362,0.772]
    low_3200 = [0.149,0.149,0.159,0.504,0.844]


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
def plot_delay_comparison(data=1600, strategy='go',toplot='only_avg',dist_list=['8020','7030','6040']):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'
    y_label='End-to-end delay (ms)'
    legend_loc='lower right'

    # Clean my loads and assign limits
    if data==1600:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
                load_6040, avg_delay_6040, high_delay_6040, med_delay_6040, low_delay_6040 = clean_load_delays(
                    waa_1600_go_e2e_6040_load_total_bps_avg,
                    waa_1600_go_e2e_6040_delay_total_avg,
                    waa_1600_go_e2e_6040_delay_high_avg,
                    waa_1600_go_e2e_6040_delay_med_avg,
                    waa_1600_go_e2e_6040_delay_low_avg,
                    cleaning_factor=1e12)
                load_7030, avg_delay_7030, high_delay_7030, med_delay_7030, low_delay_7030 = clean_load_delays(
                    waa_1600_go_e2e_7030_load_total_bps_avg,
                    waa_1600_go_e2e_7030_delay_total_avg,
                    waa_1600_go_e2e_7030_delay_high_avg,
                    waa_1600_go_e2e_7030_delay_med_avg,
                    waa_1600_go_e2e_7030_delay_low_avg,
                    cleaning_factor=1e12)
                load_8020, avg_delay_8020, high_delay_8020, med_delay_8020, low_delay_8020 = clean_load_delays(
                    waa_1600_go_e2e_load_total_bps_avg,
                    waa_1600_go_e2e_delay_total_avg,
                    waa_1600_go_e2e_delay_high_avg,
                    waa_1600_go_e2e_delay_med_avg,
                    waa_1600_go_e2e_delay_low_avg,
                    cleaning_factor=1e12)
        else:
            pass
    else:
        pass

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=40
    _TICK_PARAMS=45

    if toplot in ['only_avg','all']:
        ax1.semilogy(load_6040[limit:], avg_delay_6040[limit:], 'k', label="intra=60%,inter=40%", linewidth=5,linestyle='dashdot')
        ax1.semilogy(load_7030[limit:], avg_delay_7030[limit:], 'k', label="intra=70%,inter=30%", linewidth=5,linestyle='dashed')
        ax1.semilogy(load_8020[limit:], avg_delay_8020[limit:], 'k', label="intra=80%,inter=20%", linewidth=5,linestyle='solid')

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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()


def test_plot_stayin_intra_thru_drop(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Intra-rack load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    # data == 1600:
    max_thru = 400
    x_lim_begin = -0.1
    x_lim_end = 450

    if 8020 in traffic_list:
        load_8020, thru_8020, drop_8020 = clean_load_thru_drop(intra_8020_load_total_bps_avg, intra_8020_thru_total_bps_avg,
                                                   intra_8020_drop_total_bps_avg,cleaning_factor=1e9)
    if 7030 in traffic_list:
        load_7030, thru_7030, drop_7030 = clean_load_thru_drop(intra_7030_load_total_bps_avg, intra_7030_thru_total_bps_avg,
                                                   intra_7030_drop_total_bps_avg,cleaning_factor=1e9)

    if 6040 in traffic_list:
        load_6040, thru_6040, drop_6040 = clean_load_thru_drop(intra_6040_load_total_bps_avg, intra_6040_thru_total_bps_avg,
                                                   intra_6040_drop_total_bps_avg,cleaning_factor=1e9)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
        #nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load_8020, thru_8020,'b', label="Throughput 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_8020, drop_8020,'r', label="Drop 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_7030, thru_7030,'b', label="Throughput 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_7030, drop_7030,'r', label="Drop 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_6040, thru_6040,'b', label="Throughput 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    ax1.plot(load_6040, drop_6040,'r', label="Drop 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    #ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"capacity", linewidth=_LINEWIDTH)
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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def test_plot_stayin_intra_delays(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Intra load (Gbps)'
    y_label='Intra delay (ms)'
    legend_loc='lower right'

    load_list=[]
    delay_list=[]
    label_list=[]

    for tr in traffic_list:
        # Clean my loads and assign max thru values and limits
        # Clean my loads and assign limits
        #if data == 1600:
        x_lim_begin = 0
        x_lim_end = 400
        num_servers=16
        mylabel = str(tr)
        if tr==8020:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    intra_8020_load_total_bps_avg,
                    intra_8020_delay_total_avg,
                    intra_8020_delay_high_avg,
                    intra_8020_delay_med_avg,
                    intra_8020_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==7030:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    intra_7030_load_total_bps_avg,
                    intra_7030_delay_total_avg,
                    intra_7030_delay_high_avg,
                    intra_7030_delay_med_avg,
                    intra_7030_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==6040:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    intra_6040_load_total_bps_avg,
                    intra_6040_delay_total_avg,
                    intra_6040_delay_high_avg,
                    intra_6040_delay_med_avg,
                    intra_6040_delay_low_avg,
                    cleaning_factor=1e9)


        load_list.append(load)
        delay_list.append(avg_delay)
        label_list.append(mylabel)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
    #        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45
    print(str(delay_list))
    color=['b','r','g','k','b--','b-.']
    for i in range(len(label_list)):
        ax1.semilogy(load_list[i][limit:], delay_list[i][limit:],color[i], label="perc="+str(label_list[i]), linewidth=_LINEWIDTH)

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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def test_plot_stayin_inter_thru_drop(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Inter-rack load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    # data == 1600:
    max_thru = 400
    #x_lim_begin = -0.1
    #x_lim_end = 450

    if 8020 in traffic_list:
        load_8020, thru_8020, drop_8020 = clean_load_thru_drop(inter_8020_load_total_bps_avg, inter_8020_thru_total_bps_avg,
                                                   inter_8020_drop_total_bps_avg,cleaning_factor=1e9)
    if 7030 in traffic_list:
        load_7030, thru_7030, drop_7030 = clean_load_thru_drop(inter_7030_load_total_bps_avg, inter_7030_thru_total_bps_avg,
                                                   inter_7030_drop_total_bps_avg,cleaning_factor=1e9)

    if 6040 in traffic_list:
        load_6040, thru_6040, drop_6040 = clean_load_thru_drop(inter_6040_load_total_bps_avg, inter_6040_thru_total_bps_avg,
                                                   inter_6040_drop_total_bps_avg,cleaning_factor=1e9)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
        #nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load_8020, thru_8020,'b', label="Throughput 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_8020, drop_8020,'r', label="Drop 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_7030, thru_7030,'b', label="Throughput 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_7030, drop_7030,'r', label="Drop 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_6040, thru_6040,'b', label="Throughput 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    ax1.plot(load_6040, drop_6040,'r', label="Drop 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    #ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"capacity", linewidth=_LINEWIDTH)
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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def test_plot_stayin_inter_delays(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Inter load (Gbps)'
    y_label='Inter delay (ms)'
    legend_loc='lower right'

    load_list=[]
    delay_list=[]
    label_list=[]

    for tr in traffic_list:
        # Clean my loads and assign max thru values and limits
        # Clean my loads and assign limits
        #if data == 1600:
        #x_lim_begin = 0
        #x_lim_end = 400
        num_servers=16
        mylabel = str(tr)
        if tr==8020:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    inter_8020_load_total_bps_avg,
                    inter_8020_delay_total_avg,
                    inter_8020_delay_high_avg,
                    inter_8020_delay_med_avg,
                    inter_8020_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==7030:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    inter_7030_load_total_bps_avg,
                    inter_7030_delay_total_avg,
                    inter_7030_delay_high_avg,
                    inter_7030_delay_med_avg,
                    inter_7030_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==6040:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    inter_6040_load_total_bps_avg,
                    inter_6040_delay_total_avg,
                    inter_6040_delay_high_avg,
                    inter_6040_delay_med_avg,
                    inter_6040_delay_low_avg,
                    cleaning_factor=1e9)


        load_list.append(load)
        delay_list.append(avg_delay)
        label_list.append(mylabel)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
    #        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45
    print(str(delay_list))
    color=['b','r','g','k','b--','b-.']
    for i in range(len(label_list)):
        ax1.semilogy(load_list[i][limit:], delay_list[i][limit:],color[i], label="perc="+str(label_list[i]), linewidth=_LINEWIDTH)

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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()

def test_plot_stayin_brul_thru_drop(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='PON UL load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    # data == 1600:
    #max_thru = 400
    x_lim_begin = -0.1
    x_lim_end = 2000

    if 8020 in traffic_list:
        load_8020, thru_8020, drop_8020 = clean_load_thru_drop(brul_8020_load_total_bps_avg, brul_8020_thru_total_bps_avg,
                                                   brul_8020_drop_total_bps_avg,cleaning_factor=1e9)
    if 7030 in traffic_list:
        load_7030, thru_7030, drop_7030 = clean_load_thru_drop(brul_7030_load_total_bps_avg, brul_7030_thru_total_bps_avg,
                                                   brul_7030_drop_total_bps_avg,cleaning_factor=1e9)

    if 6040 in traffic_list:
        load_6040, thru_6040, drop_6040 = clean_load_thru_drop(brul_6040_load_total_bps_avg, brul_6040_thru_total_bps_avg,
                                                   brul_6040_drop_total_bps_avg,cleaning_factor=1e9)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
        #nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load_8020, thru_8020,'b', label="Throughput 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_8020, drop_8020,'r', label="Drop 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_7030, thru_7030,'b', label="Throughput 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_7030, drop_7030,'r', label="Drop 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_6040, thru_6040,'b', label="Throughput 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    ax1.plot(load_6040, drop_6040,'r', label="Drop 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    #ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"capacity", linewidth=_LINEWIDTH)
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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def test_plot_stayin_brul_delays(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='PON UL load (Gbps)'
    y_label='PON UL load delay (ms)'
    legend_loc='lower right'

    load_list=[]
    delay_list=[]
    label_list=[]

    for tr in traffic_list:
        # Clean my loads and assign max thru values and limits
        # Clean my loads and assign limits
        #if data == 1600:
        x_lim_begin = 0
        x_lim_end = 2000
        num_servers=16
        mylabel = str(tr)
        if tr==8020:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    brul_8020_load_total_bps_avg,
                    brul_8020_delay_total_avg,
                    brul_8020_delay_high_avg,
                    brul_8020_delay_med_avg,
                    brul_8020_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==7030:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    brul_7030_load_total_bps_avg,
                    brul_7030_delay_total_avg,
                    brul_7030_delay_high_avg,
                    brul_7030_delay_med_avg,
                    brul_7030_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==6040:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    brul_6040_load_total_bps_avg,
                    brul_6040_delay_total_avg,
                    brul_6040_delay_high_avg,
                    brul_6040_delay_med_avg,
                    brul_6040_delay_low_avg,
                    cleaning_factor=1e9)


        load_list.append(load)
        delay_list.append(avg_delay)
        label_list.append(mylabel)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
    #        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45
    print(str(delay_list))
    color=['b','r','g','k','b--','b-.']
    for i in range(len(label_list)):
        ax1.semilogy(load_list[i][limit:], delay_list[i][limit:],color[i], label="perc="+str(label_list[i]), linewidth=_LINEWIDTH)

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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def test_plot_stayin_brdl_thru_drop(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='PON DL load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    # data == 1600:
    max_thru = 400
    #x_lim_begin = -0.1
    #x_lim_end = 450

    if 8020 in traffic_list:
        load_8020, thru_8020, drop_8020 = clean_load_thru_drop(brdl_8020_load_total_bps_avg, brdl_8020_thru_total_bps_avg,
                                                   brdl_8020_drop_total_bps_avg,cleaning_factor=1e9)
    if 7030 in traffic_list:
        load_7030, thru_7030, drop_7030 = clean_load_thru_drop(brdl_7030_load_total_bps_avg, brdl_7030_thru_total_bps_avg,
                                                   brdl_7030_drop_total_bps_avg,cleaning_factor=1e9)

    if 6040 in traffic_list:
        load_6040, thru_6040, drop_6040 = clean_load_thru_drop(brdl_6040_load_total_bps_avg, brdl_6040_thru_total_bps_avg,
                                                   brdl_6040_drop_total_bps_avg,cleaning_factor=1e9)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
        #nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load_8020, thru_8020,'b', label="Throughput 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_8020, drop_8020,'r', label="Drop 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_7030, thru_7030,'b', label="Throughput 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_7030, drop_7030,'r', label="Drop 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_6040, thru_6040,'b', label="Throughput 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    ax1.plot(load_6040, drop_6040,'r', label="Drop 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    #ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"capacity", linewidth=_LINEWIDTH)
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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def test_plot_stayin_brdl_delays(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='PON DL  (Gbps)'
    y_label='PON DL  (ms)'
    legend_loc='lower right'

    load_list=[]
    delay_list=[]
    label_list=[]

    for tr in traffic_list:
        # Clean my loads and assign max thru values and limits
        # Clean my loads and assign limits
        #if data == 1600:
        #x_lim_begin = 0
        #x_lim_end = 400
        num_servers=16
        mylabel = str(tr)
        if tr==8020:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    brdl_8020_load_total_bps_avg,
                    brdl_8020_delay_total_avg,
                    brdl_8020_delay_high_avg,
                    brdl_8020_delay_med_avg,
                    brdl_8020_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==7030:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    brdl_7030_load_total_bps_avg,
                    brdl_7030_delay_total_avg,
                    brdl_7030_delay_high_avg,
                    brdl_7030_delay_med_avg,
                    brdl_7030_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==6040:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    brdl_6040_load_total_bps_avg,
                    brdl_6040_delay_total_avg,
                    brdl_6040_delay_high_avg,
                    brdl_6040_delay_med_avg,
                    brdl_6040_delay_low_avg,
                    cleaning_factor=1e9)


        load_list.append(load)
        delay_list.append(avg_delay)
        label_list.append(mylabel)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
    #        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45
    print(str(delay_list))
    color=['b','r','g','k','b--','b-.']
    for i in range(len(label_list)):
        ax1.semilogy(load_list[i][limit:], delay_list[i][limit:],color[i], label="perc="+str(label_list[i]), linewidth=_LINEWIDTH)

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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()

def test_plot_stayin_e2e_thru_drop(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='end2end load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    # data == 1600:
    max_thru = 400
    x_lim_begin = -0.1
    x_lim_end = 8500

    if 8020 in traffic_list:
        load_8020, thru_8020, drop_8020 = clean_load_thru_drop(e2e_8020_load_total_bps_avg, e2e_8020_thru_total_bps_avg,
                                                   e2e_8020_drop_total_bps_avg,cleaning_factor=1e9)
    if 7030 in traffic_list:
        load_7030, thru_7030, drop_7030 = clean_load_thru_drop(e2e_7030_load_total_bps_avg, e2e_7030_thru_total_bps_avg,
                                                   e2e_7030_drop_total_bps_avg,cleaning_factor=1e9)

    if 6040 in traffic_list:
        load_6040, thru_6040, drop_6040 = clean_load_thru_drop(e2e_6040_load_total_bps_avg, e2e_6040_thru_total_bps_avg,
                                                   e2e_6040_drop_total_bps_avg,cleaning_factor=1e9)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
        #nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load_8020, thru_8020,'b', label="Throughput 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_8020, drop_8020,'r', label="Drop 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_7030, thru_7030,'b', label="Throughput 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_7030, drop_7030,'r', label="Drop 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_6040, thru_6040,'b', label="Throughput 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    ax1.plot(load_6040, drop_6040,'r', label="Drop 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    #ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"capacity", linewidth=_LINEWIDTH)
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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()
def test_plot_stayin_e2e_delays(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='end2end (Gbps)'
    y_label='end2end  (ms)'
    legend_loc='lower right'

    load_list=[]
    delay_list=[]
    label_list=[]

    for tr in traffic_list:
        # Clean my loads and assign max thru values and limits
        # Clean my loads and assign limits
        #if data == 1600:
        x_lim_begin = 0
        x_lim_end = 8500
        num_servers=16
        mylabel = str(tr)
        if tr==8020:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    e2e_8020_load_total_bps_avg,
                    e2e_8020_delay_total_avg,
                    e2e_8020_delay_high_avg,
                    e2e_8020_delay_med_avg,
                    e2e_8020_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==7030:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    e2e_7030_load_total_bps_avg,
                    e2e_7030_delay_total_avg,
                    e2e_7030_delay_high_avg,
                    e2e_7030_delay_med_avg,
                    e2e_7030_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==6040:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    e2e_6040_load_total_bps_avg,
                    e2e_6040_delay_total_avg,
                    e2e_6040_delay_high_avg,
                    e2e_6040_delay_med_avg,
                    e2e_6040_delay_low_avg,
                    cleaning_factor=1e9)


        load_list.append(load)
        delay_list.append(avg_delay)
        label_list.append(mylabel)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
    #        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45
    print(str(delay_list))
    color=['b','r','g','k','b--','b-.']
    for i in range(len(label_list)):
        ax1.semilogy(load_list[i][limit:], delay_list[i][limit:],color[i], label="perc="+str(label_list[i]), linewidth=_LINEWIDTH)

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
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()



# Group A: Plots for basic scenario (1600-go)
#plot_thru_intra(data=1600,strategy='go') # data in [1600,2400,3200], strategy in ['go','stay'] #5a
#plot_thru_inter(data=1600,strategy='go') #5b
#plot_thru_e2e(data=1600, strategy='go') #6a
###plot_delays_e2e(data=1600, strategy='go',toplot='only_avg')
###plot_qdelays_e2e(data=1600, strategy='go',toplot='only_avg')
#plot_delays_n_qdelays_e2e(data=1600, strategy='go',toplot='only_avg') #6b

# Group D: plots for diff data distribution 6040, 7030
#for dist in ['8020','7030','6040']:

    #plot_thru_intra(data=1600,strategy='go',distribution=dist) # data in [1600,2400,3200], strategy in ['go','stay']
    #plot_thru_inter(data=1600,strategy='go',distribution=dist)

    #plot_thru_e2e(data=1600, strategy='go',distribution=dist)
    #plot_delays_e2e(data=1600, strategy='go',toplot='only_avg',distribution=dist)
    #plot_qdelays_e2e(data=1600, strategy='go',toplot='only_avg',distribution=dist)

    #plot_drop_comparison()
#plot_delay_comparison(data=1600, strategy='go',toplot='only_avg',dist_list=['8020','7030','6040']) #7

# Group B: PLot for strategy (1600-go and stay variations)
###plot_delays_e2e(data=1600, strategy='go',toplot='all')
###plot_delays_e2e(data=1600, strategy='stay',toplot='all')
#plot_compare_delay_bar_B() #8

# Group C: PLot for scaling number of servers (1600,2400,3200 stay)
#data_list=[1600,2400,3200]
#plot_thru_per_server_intra_multiple(data_list=data_list,strategy='stay') # data in [1600,2400,3200], strategy in ['go','stay']         #9a
#plot_delay_multiple(data_list=data_list,strategy='stay') # data in [1600,2400,3200], strategy in ['go','stay']                     #9b

#for data in [1600,2400,3200]:
    #plot_delays_e2e(data=data, strategy='stay',toplot='only_hml') # toplot in ['only_avg', 'only_hml', 'all']
#plot_compare_delay_bar_C()                     #10

# test plot
traffic_list=[8020,7030,6040]
test_plot_stayin_intra_thru_drop(traffic_list=traffic_list)
test_plot_stayin_intra_delays(traffic_list=traffic_list)

test_plot_stayin_inter_thru_drop(traffic_list=traffic_list)
test_plot_stayin_inter_delays(traffic_list=traffic_list)

test_plot_stayin_brul_thru_drop(traffic_list=traffic_list)
test_plot_stayin_brul_delays(traffic_list=traffic_list)

test_plot_stayin_brdl_thru_drop(traffic_list=traffic_list)
test_plot_stayin_brdl_delays(traffic_list=traffic_list)

test_plot_stayin_e2e_thru_drop(traffic_list=traffic_list)
test_plot_stayin_e2e_delays(traffic_list=traffic_list)