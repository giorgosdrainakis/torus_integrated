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
    load_60 = [921920000.0, 0, 0, 37785163636.36364, 46538818064.51613, 57879432727.27273, 69084672000.0,
                              80688560000.0, 97652480000.0, 102187120000.0, 111319360000.0, 0, 0, 147297280000.0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 268625280000.0, 0]

    load_70=[681920000.0, 0, 0, 31500053333.333332, 39766598620.68965, 49661440000.0, 59981932307.69231, 68797720000.0, 80427320000.0, 89010080000.0, 100841280000.0, 0, 117040320000.0, 0, 0, 0, 162315520000.0, 0, 0, 0, 0, 0, 0, 0, 239067520000.0]

    load_80=[30720000.0, 0, 23279680000.0, 31144320000.0, 41268252903.22581, 51116617142.85714, 62325920000.0, 73744901818.18182, 80844000000.0, 91678400000.0, 100015040000.0, 0, 127150720000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 248054720000.0]

    thru_60=[1338240000.0, 0, 0, 40223825454.545456, 47697176774.19355, 58892290909.09091, 67469546666.666664, 77411200000.0, 107920960000.0, 98641680000.0, 116533440000.0, 0, 0, 166599360000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 228786240000.0, 0]

    thru_70=[2244800000.0, 0, 0, 32404337777.77778, 42068027586.206894, 49895323076.92308, 58146904615.38461, 68730320000.0, 74586040000.0, 86651840000.0, 110088320000.0, 0, 110888320000.0, 0, 0, 0, 171646720000.0, 0, 0, 0, 0, 0, 0, 0, 219388800000.0]

    thru_80=[107520000.0, 0, 24568426666.666668, 31678621538.46154, 41241816774.19355, 53154133333.333336, 61889051428.57143, 72152669090.90909, 74394880000.0, 117490240000.0, 97678080000.0, 0, 122776640000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 216969600000.0]


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
    load_60 = [921920000.0, 0, 0, 37785163636.36364, 46538818064.51613, 57879432727.27273, 69084672000.0,
                              80688560000.0, 97652480000.0, 102187120000.0, 111319360000.0, 0, 0, 147297280000.0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 268625280000.0, 0]
    load_70=[681920000.0, 0, 0, 31500053333.333332, 39766598620.68965, 49661440000.0, 59981932307.69231, 68797720000.0, 80427320000.0, 89010080000.0, 100841280000.0, 0, 117040320000.0, 0, 0, 0, 162315520000.0, 0, 0, 0, 0, 0, 0, 0, 239067520000.0]
    load_80 = [30720000.0, 0, 23279680000.0, 31144320000.0, 41268252903.22581, 51116617142.85714, 62325920000.0,
               73744901818.18182, 80844000000.0, 91678400000.0, 100015040000.0, 0, 127150720000.0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 248054720000.0]

    avg_delay_60=[7.29791304352244e-07, 0, 0, 7.812631926728026e-07, 8.989376803452106e-07, 1.84633711758062e-06, 2.507995268042738e-06, 3.0210424663882795e-06, 2.8497382980717537e-06, 3.9569547167658025e-06, 2.7283636073825398e-06, 0, 0, 5.529646025811692e-06, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0241816598173807e-05, 0]
    high_delay_60=[5.865000000000731e-07, 0, 0, 5.847135645436079e-07, 5.851522102579949e-07, 5.889988455876842e-07, 5.936782639379598e-07, 5.951464161419753e-07, 6.249864659011913e-07, 6.19340428793593e-07, 6.379644371204624e-07, 0, 0, 7.268958746156322e-07, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.1866081937362092e-06, 0]
    med_delay_60=[1.0510000000001768e-06, 0, 0, 1.0059025903529847e-06, 1.0151216555518196e-06, 1.0660777432363142e-06, 1.0471242505474043e-06, 1.0877305102090472e-06, 9.696674840468596e-07, 1.0714386759398515e-06, 1.1453422365292363e-06, 0, 0, 1.3825803209406465e-06, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6.798845560132707e-06, 0]
    low_delay_60=[8.494666666778203e-07, 0, 0, 3.5891009405539368e-06, 3.1883107766827502e-06, 8.065030222759565e-06, 1.0040151779730945e-05, 1.1412995440321096e-05, 7.963204825378422e-06, 1.1654758807690026e-05, 7.0110577665878815e-06, 0, 0, 1.1329107802578568e-05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.291985623905569e-05, 0]

    avg_delay_70=[6.589619047620506e-07, 0, 0, 6.743984920821077e-07, 9.174811956315184e-07, 1.5266137309504925e-06, 2.326103047983163e-06, 2.1795554070930372e-06, 5.426939832233505e-06, 5.16120195997993e-06, 4.176645470160564e-06, 0, 3.470259210010535e-06, 0, 0, 0, 8.768817619581058e-06, 0, 0, 0, 0, 0, 0, 0, 1.4507333362536728e-05]

    high_delay_70=[5.728500000001888e-07, 0, 0, 5.721295099703293e-07, 5.749317917044338e-07, 5.764704465039149e-07, 5.785172255822523e-07, 5.827490938239682e-07, 5.846086973069966e-07, 5.824037348667035e-07, 6.050906288133289e-07, 0, 6.019088889861555e-07, 0, 0, 0, 6.924023421047035e-07, 0, 0, 0, 0, 0, 0, 0, 9.554655306397798e-07]

    med_delay_70=[7.667500000001735e-07, 0, 0, 1.0059179280813086e-06, 1.0335577416139444e-06, 1.0223727919124644e-06, 1.0387700949136778e-06, 1.0729560010497118e-06, 1.0249626267510684e-06, 9.969858274641104e-07, 1.0631227622522128e-06, 0, 1.0367393353853676e-06, 0, 0, 0, 1.156268275517443e-06, 0, 0, 0, 0, 0, 0, 0, 2.4589390369124468e-06]

    low_delay_70=[6.876000000000953e-07, 0, 0, 1.1009934492185137e-06, 3.688228941780558e-06, 6.54322484776477e-06, 9.654860164497681e-06, 8.267567217922746e-06, 1.8042963051207633e-05, 1.664125364662155e-05, 1.3076262224350088e-05, 0, 7.670065940869535e-06, 0, 0, 0, 1.9886807400434707e-05, 0, 0, 0, 0, 0, 0, 0, 2.4427085598195505e-05]

    avg_delay_80=[5.700333333332844e-07, 0, 6.583944548219758e-07, 7.373377613630286e-07, 1.0163774884614887e-06, 1.856798792973368e-06, 2.361989986258222e-06, 3.532299594763275e-06, 2.5573462801828094e-06, 4.08668186821687e-06, 4.991525816968542e-06, 0, 7.020942147251045e-06, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.4050261325150061e-05]

    high_delay_80=[5.643999999999094e-07, 0, 5.62041507646978e-07, 5.630274733138239e-07, 5.653274471642174e-07, 5.684982483929599e-07, 5.711833853508496e-07, 5.740354191509745e-07, 5.75085104784972e-07, 5.896076398171125e-07, 5.796589439869689e-07, 0, 5.956570286270082e-07, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9.361458964564482e-07]

    med_delay_80=[5.813000000000346e-07, 0, 9.375216925767273e-07, 1.0265189050041474e-06, 1.0498114026916024e-06, 1.083157578739852e-06, 1.0767340365280609e-06, 1.0551558384982171e-06, 1.035049164608357e-06, 9.981023073022375e-07, 1.2131933376832887e-06, 0, 1.1763503460266785e-06, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.6611160565989396e-06]

    low_delay_80=[0, 0, 1.610071229449138e-06, 1.8250378644961724e-06, 3.6278658657837966e-06, 9.030809051082978e-06, 9.049177523795639e-06, 1.2328033559071798e-05, 7.469825079261529e-06, 1.1170554585183747e-05, 1.3648017777904198e-05, 0, 1.483778798603979e-05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.3496302320288964e-05]


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