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

def clean_load_thru(load,thru):
    selected_i=[]
    for i in range(0,len(load)):
        if load[i]!=0:
            if thru[i] > load[i]:
                thru[i]=load[i]
            selected_i.append(i)

    load = [load[i]/1e9 for i in selected_i]
    load.insert(0,0)
    thru = [thru[i]/1e9 for i in selected_i]
    thru.insert(0,0)
    return load,thru

def clean_load_delays(load,avg,high,med,low):
    selected_i=[]
    for i in range(0,len(load)):
        if load[i]!=0:
            selected_i.append(i)

    load = [load[i]/1e9 for i in selected_i]
    load.insert(0,0)

    avg = [avg[i]*1e6 for i in selected_i]
    avg.insert(0,0)
    high = [high[i]*1e6 for i in selected_i]
    high.insert(0,0)
    med = [med[i]*1e6 for i in selected_i]
    med.insert(0,0)
    low = [low[i]*1e6 for i in selected_i]
    low.insert(0,0)

    return load,avg,high,med,low


def plot_thruput():
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    # Mine
    load_60 = [12124800000.0, 0, 0, 0, 209507480000.0, 246094474893.61703, 307066125714.2857, 342045262222.2222, 0, 426044160000.0, 476406080000.0, 0, 581510400000.0, 0, 0, 0, 823682880000.0, 0, 0, 0, 0, 0, 0, 0, 1215992640000.0]
    load_70=[7313920000.0, 0, 0, 0, 149004160000.0, 170093828571.42856, 196314128000.0, 231289835789.4737, 271469040000.0, 295716160000.0, 325599360000.0, 0, 398229120000.0, 0, 0, 508648960000.0, 0, 0, 0, 0, 0, 0, 0, 0, 873175040000.0]
    load_80=[899200000.0, 0, 0, 0, 101833051428.57143, 117968312380.95238, 137338016969.69698, 161942986666.66666, 183424000000.0, 206916480000.0, 228952160000.0, 255178240000.0, 278040000000.0, 0, 325684160000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 565586880000.0]

    thru_60=[15969600000.0, 0, 0, 0, 210104426666.66666, 246393565957.4468, 344580274285.7143, 367461440000.0, 0, 542706560000.0, 548195520000.0, 0, 548145600000.0, 0, 0, 0, 550610240000.0, 0, 0, 0, 0, 0, 0, 0, 540003520000.0]
    thru_70=[11232000000.0, 0, 0, 0, 151845440000.0, 170311897142.85715, 196275144000.0, 230966972631.57895, 279391680000.0, 336355360000.0, 408373120000.0, 0, 493456640000.0, 0, 0, 541843840000.0, 0, 0, 0, 0, 0, 0, 0, 0, 534637120000.0]
    thru_80=[1818880000.0, 0, 0, 0, 101739200000.0, 118090537142.85715, 137253701818.18182, 162332000000.0, 183202720000.0, 209234240000.0, 228972640000.0, 255768000000.0, 280259840000.0, 0, 377407680000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 504104640000.0]

    x_label='Load (Gbps)'
    #x_lim_begin=-0.01
    #x_lim_end=1.01
    y_label='Throughput (Gbps)'
    legend_loc='upper left'

    # Clean my loads
    load_60,thru_60=clean_load_thru(load_60,thru_60)
    load_70, thru_70 = clean_load_thru(load_70, thru_70)
    load_80, thru_80 = clean_load_thru(load_80, thru_80)

    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.plot(load_60, thru_60,'r', label="60% intra",linewidth=4,marker='s',markersize=15,markeredgewidth=3,markeredgecolor='r',markerfacecolor='w')
    ax1.plot(load_70, thru_70,'g', label="70% intra",linewidth=4,marker='D',markersize=15,markeredgewidth=3,markeredgecolor='g',markerfacecolor='w')
    ax1.plot(load_80, thru_80,'b', label="80% intra",linewidth=4,marker='X',markersize=15,markeredgewidth=3,markeredgecolor='b',markerfacecolor='w')

    try:
        ax1.set_xlabel(x_label, fontsize=35)
    except:
        pass
    try:
        ax1.set_ylabel(y_label, fontsize=35)
    except:
        pass
    try:
        ax1.set_xlim(x_lim_begin,x_lim_end)
    except:
        pass
    try:
        ax1.legend(loc=legend_loc, fontsize=35)
    except:
        ax1.legend(loc='upper left', fontsize=35)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=35)
    ax1.tick_params(axis='both', which='minor', labelsize=35)

    plt.show()

def plot_delays():
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    # Mine
    load_60 = [12124800000.0, 0, 0, 0, 209507480000.0, 246094474893.61703, 307066125714.2857, 342045262222.2222, 0, 426044160000.0, 476406080000.0, 0, 581510400000.0, 0, 0, 0, 823682880000.0, 0, 0, 0, 0, 0, 0, 0, 1215992640000.0]
    load_70=[7313920000.0, 0, 0, 0, 149004160000.0, 170093828571.42856, 196314128000.0, 231289835789.4737, 271469040000.0, 295716160000.0, 325599360000.0, 0, 398229120000.0, 0, 0, 508648960000.0, 0, 0, 0, 0, 0, 0, 0, 0, 873175040000.0]
    load_80=[899200000.0, 0, 0, 0, 101833051428.57143, 117968312380.95238, 137338016969.69698, 161942986666.66666, 183424000000.0, 206916480000.0, 228952160000.0, 255178240000.0, 278040000000.0, 0, 325684160000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 565586880000.0]

    avg_delay_60=[1.4350656370699234e-06, 0, 0, 0, 3.422737322780885e-06, 4.295475045573689e-06, 1.4802368636479908e-05, 1.6840689515507412e-05, 0, 8.095661277357953e-05, 9.387929361503521e-05, 0, 0.0001164012654286525, 0, 0, 0, 0.00012545442897281836, 0, 0, 0, 0, 0, 0, 0, 7.420437258947691e-05]

    high_delay_60=[1.961162962962931e-06, 0, 0, 0, 4.242488261569356e-06, 5.400982039874293e-06, 1.3476392454125056e-05, 1.4343981788710673e-05, 0, 2.631249713114129e-05, 2.6524349022751166e-05, 0, 2.611186868978479e-05, 0, 0, 0, 2.7083452848472003e-05, 0, 0, 0, 0, 0, 0, 0, 2.934994259502388e-05]

    med_delay_60=[1.375316666666921e-06, 0, 0, 0, 1.335782045432493e-06, 1.4587582436653592e-06, 2.1856777455451993e-06, 2.4802160649690788e-06, 0, 4.937648026318772e-06, 5.218958460762408e-06, 0, 5.447483613789938e-06, 0, 0, 0, 6.272516673815607e-06, 0, 0, 0, 0, 0, 0, 0, 7.208112617044163e-06]

    low_delay_60=[1.3735673469443973e-06, 0, 0, 0, 1.7587455983126996e-06, 2.8249311014054487e-06, 3.275472409172325e-05, 3.665952947349039e-05, 0, 0.00023525871142948744, 0.0002698843805221359, 0, 0.00028938923668924863, 0, 0, 0, 0.0002513430996188054, 0, 0, 0, 0, 0, 0, 0, 0.00012101101537683804]

    avg_delay_70=[1.387979069769955e-06, 0, 0, 0, 2.717307217993084e-06, 2.9072187538902287e-06, 3.1571761918871054e-06, 3.6713243626887597e-06, 5.460617748132646e-06, 1.2044971545642197e-05, 2.2795684506461567e-05, 0, 3.496207809871063e-05, 0, 0, 5.0540958490093976e-05, 0, 0, 0, 0, 0, 0, 0, 0, 3.920040732734983e-05]

    high_delay_70=[1.921000000000214e-06, 0, 0, 0, 3.2364241849825994e-06, 3.595157575953589e-06, 4.039193533255799e-06, 4.916334551511409e-06, 7.466436062238794e-06, 1.4482493493988942e-05, 1.990651667410034e-05, 0, 2.5397117893691853e-05, 0, 0, 3.0247741715992624e-05, 0, 0, 0, 0, 0, 0, 0, 0, 3.307196622031097e-05]

    med_delay_70=[1.2335600000003277e-06, 0, 0, 0, 1.2194253227252782e-06, 1.2601003353618864e-06, 1.2974285234423823e-06, 1.3824389598665887e-06, 1.6044047500075133e-06, 1.8565671289245232e-06, 2.7791095501904858e-06, 0, 3.5519310913363653e-06, 0, 0, 4.8756394160474095e-06, 0, 0, 0, 0, 0, 0, 0, 0, 4.966137460249461e-06]

    low_delay_70=[1.3650776119434425e-06, 0, 0, 0, 1.5450407006841818e-06, 1.6326146344790617e-06, 1.6690471463219925e-06, 1.943587013494969e-06, 3.5246515890532148e-06, 1.6263720944321853e-05, 4.51899364108096e-05, 0, 6.902542862525443e-05, 0, 0, 9.712715524519821e-05, 0, 0, 0, 0, 0, 0, 0, 0, 5.518263294429213e-05]

    avg_delay_80=[1.1084195121951836e-06, 0, 0, 0, 2.1349694240070972e-06, 2.223587810455525e-06, 2.345743529302538e-06, 2.5743544667181248e-06, 2.7104950483188016e-06, 2.893148423780739e-06, 3.071550897413997e-06, 3.210378332649722e-06, 3.693733568291909e-06, 0, 7.341203031383518e-06, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.6317187400393763e-05]

    high_delay_80=[1.3530133333332825e-06, 0, 0, 0, 2.4929152504464625e-06, 2.676494272082685e-06, 2.917169863128172e-06, 3.3509328084042058e-06, 3.6830693719168686e-06, 4.065780861933986e-06, 4.550846136371737e-06, 4.970537880508054e-06, 5.990099088035671e-06, 0, 1.1559983639084752e-05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.250865300841989e-05]

    med_delay_80=[1.0502833333334825e-06, 0, 0, 0, 1.1642634599957212e-06, 1.1870225905133712e-06, 1.2043694151751151e-06, 1.2453908227303818e-06, 1.2631110861816255e-06, 1.3056900055553903e-06, 1.3123616050214836e-06, 1.3721058884362096e-06, 1.4380314341875265e-06, 0, 1.9269917857127737e-06, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.2070058668422708e-06]

    low_delay_80=[8.961857142858217e-07, 0, 0, 0, 1.3278193705090052e-06, 1.3747357713085807e-06, 1.4055624893903836e-06, 1.4932299270564422e-06, 1.5375318452869147e-06, 1.693759464413627e-06, 1.701559689839514e-06, 1.763087230522787e-06, 1.8938623556606212e-06, 0, 5.579679078598485e-06, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.2046254028554435e-05]


    x_label='Load (Gbps)'
    #x_lim_begin=-0.01
    #x_lim_end=1.01
    y_label='Delay (ms)'
    legend_loc='upper left'

    # Clean my loads
    load_60,avg_delay_60,high_delay_60,med_delay_60,low_delay_60=clean_load_delays(load_60,avg_delay_60,high_delay_60,med_delay_60,low_delay_60)
    load_70,avg_delay_70,high_delay_70,med_delay_70,low_delay_70=clean_load_delays(load_70,avg_delay_70,high_delay_70,med_delay_70,low_delay_70)
    load_80, avg_delay_80, high_delay_80, med_delay_80, low_delay_80 = clean_load_delays(load_80, avg_delay_80,
                                                                                         high_delay_80, med_delay_80,
                                                                                         low_delay_80)

    fig, ax1 = plt.subplots(constrained_layout=True)

    ax1.plot(load_60, avg_delay_60,'k-.', label="Avg(60% intra)",linewidth=4)
    ax1.plot(load_70, avg_delay_70,'k--', label="Avg(70% intra)",linewidth=4)
    ax1.plot(load_80, avg_delay_80,'k', label="Avg(80% intra)",linewidth=4)

    ax1.plot(load_60, high_delay_60,'r-.', label="High(60% intra)",linewidth=4)
    ax1.plot(load_70, high_delay_70,'r--', label="High(70% intra)",linewidth=4)
    ax1.plot(load_80, high_delay_80,'r', label="High(80% intra)",linewidth=4)

    ax1.plot(load_60, med_delay_60,'g-.', label="Med(60% intra)",linewidth=4)
    ax1.plot(load_70, med_delay_70,'g--', label="Med(70% intra)",linewidth=4)
    ax1.plot(load_80, med_delay_80,'g', label="Med(80% intra)",linewidth=4)

    ax1.plot(load_60, low_delay_60,'b-.', label="Low(60% intra)",linewidth=4)
    ax1.plot(load_70, low_delay_70,'b--', label="Low(70% intra)",linewidth=4)
    ax1.plot(load_80, low_delay_80,'b', label="Low(80% intra)",linewidth=4)

    try:
        ax1.set_xlabel(x_label, fontsize=35)
    except:
        pass
    try:
        ax1.set_ylabel(y_label, fontsize=35)
    except:
        pass
    try:
        ax1.set_xlim(x_lim_begin,x_lim_end)
    except:
        pass
    try:
        ax1.legend(loc=legend_loc, fontsize=35)
    except:
        ax1.legend(loc='upper left', fontsize=35)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=35)
    ax1.tick_params(axis='both', which='minor', labelsize=35)

    plt.show()

plot_thruput()
plot_delays()