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
    avg.insert(0,avg[0])
    high = [high[i]*1e3 for i in selected_i]
    high.insert(0,high[0])
    med = [med[i]*1e3 for i in selected_i]
    med.insert(0,med[0])
    low = [low[i]*1e3 for i in selected_i]
    low.insert(0,low[0])

    return load,avg,high,med,low

def plot_thru_intra(data,strategy):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Intra traffic load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    if data==1600:
        max_thru = 400
        x_lim_begin = -0.1
        x_lim_end=450
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_1600_go_intra_load_total_bps_avg, waa_1600_go_intra_thru_total_bps_avg,
                                               waa_1600_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
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
    ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"throughput", linewidth=_LINEWIDTH)
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

    x_label='Intra traffic load (Gbps)'
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
def plot_thru_inter(data,strategy):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Inter traffic load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    if data==1600:
        max_thru = 16 * 4 * 40
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_1600_go_inter_load_total_bps_avg, waa_1600_go_inter_thru_total_bps_avg,
                                               waa_1600_go_inter_drop_total_bps_avg,cleaning_factor=1e9)
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
    ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"throughput", linewidth=_LINEWIDTH)
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
def plot_thru_e2e(data,strategy):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total traffic load (Tbps)'
    y_label='Bitrate (Tbps)'
    legend_loc='lower right'

    # Clean my loads and assign max thru values and limits
    if data==1600:
        max_thru = 16*400+16*100
        x_lim_begin = -1
        x_lim_end=10000
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_1600_go_e2e_load_total_bps_avg, waa_1600_go_e2e_thru_total_bps_avg,
                                               waa_1600_go_e2e_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_1600_stay_e2e_load_total_bps_avg, waa_1600_stay_e2e_thru_total_bps_avg,
                                               waa_1600_stay_e2e_drop_total_bps_avg,cleaning_factor=1e9)
    elif data==2400:
        max_thru = 16*400+16*100
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_2400_go_e2e_load_total_bps_avg, waa_2400_go_e2e_thru_total_bps_avg,
                                               waa_2400_go_e2e_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_2400_stay_e2e_load_total_bps_avg, waa_2400_stay_e2e_thru_total_bps_avg,
                                               waa_2400_stay_e2e_drop_total_bps_avg,cleaning_factor=1e9)
    elif data==3200:
        max_thru = 16*400+16*100
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_3200_go_e2e_load_total_bps_avg, waa_3200_go_e2e_thru_total_bps_avg,
                                               waa_3200_go_e2e_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_3200_stay_e2e_load_total_bps_avg, waa_3200_stay_e2e_thru_total_bps_avg,
                                               waa_3200_stay_e2e_drop_total_bps_avg,cleaning_factor=1e9)
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
    ax1.plot(load, nominal_thru, 'k--', label="Nominal throughput", linewidth=_LINEWIDTH)
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
def plot_delays_e2e(data, strategy,toplot):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total traffic load (Tbps)'
    y_label='End-to-end delay (ms)'
    legend_loc='center right'

    # Clean my loads and assign limits
    if data==1600:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_1600_go_e2e_load_total_bps_avg,
                                                                                  waa_1600_go_e2e_delay_total_avg,
                                                                                  waa_1600_go_e2e_delay_high_avg,
                                                                                  waa_1600_go_e2e_delay_med_avg,
                                                                                  waa_1600_go_e2e_delay_low_avg,
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
def plot_qdelays_e2e(data, strategy,toplot):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total traffic load (Tbps)'
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
def plot_compare_delay_bar():
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total traffic load (Tbps)'

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

# Group A: Plots for basic scenario (1600-go)
#plot_thru_intra(data=1600,strategy='go') # data in [1600,2400,3200], strategy in ['go','stay']
#plot_thru_inter(data=1600,strategy='go')
#plot_thru_e2e(data=1600, strategy='go')
#plot_delays_e2e(data=1600, strategy='go',toplot='only_avg')
#plot_qdelays_e2e(data=1600, strategy='go',toplot='only_avg')

# Group B: PLot for strategy (1600-go and stay variations)
#plot_delays_e2e(data=1600, strategy='go',toplot='all')
#plot_delays_e2e(data=1600, strategy='stay',toplot='all')

# Group C: PLot for scaling number of servers (1600,2400,3200 stay)
#for data in [1600,2400,3200]:
#    plot_thru_per_server_intra(data=data,strategy='stay') # data in [1600,2400,3200], strategy in ['go','stay']

for data in [1600,2400,3200]:
    plot_delays_e2e(data=data, strategy='stay',toplot='only_hml') # toplot in ['only_avg', 'only_hml', 'all']

#plot_compare_delay_bar()