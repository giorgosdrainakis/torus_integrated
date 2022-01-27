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
    load_60 = [0.0, 0, 0, 487066697142.8571, 592102357333.3334, 754790656000.0, 875849554285.7142, 1047345920000.0, 1179021120000.0, 1358563520000.0, 0, 0, 0, 1884026560000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3401480960000.0, 0]
    load_70=[0.0, 0, 0, 459817600000.0, 558386316800.0, 652921801739.1305, 784129903157.8948, 920563520000.0, 1027025120000.0, 0, 1365442240000.0, 1451960640000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3239842240000.0]
    load_80=[0.0, 0, 0, 0, 553885520000.0, 656807200000.0, 776922496000.0, 935143744000.0, 0, 1201727253333.3333, 1398157760000.0, 1459603840000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3196537920000.0]

    thru_60=[35820160000.0, 0, 0, 493866560000.0, 592352325333.3334, 774621184000.0, 928126857142.8572, 1183299200000.0, 1275616960000.0, 1415959680000.0, 0, 0, 0, 1859107520000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2249467520000.0, 0]
    thru_70=[35129600000.0, 0, 0, 485584000000.0, 563630451200.0, 651762093913.0435, 786180614736.8422, 930737493333.3334, 1107078560000.0, 0, 1453556480000.0, 1752612480000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2500252800000.0]
    thru_80=[9347840000.0, 0, 0, 0, 560376150000.0, 654966309565.2174, 777380384000.0, 938625792000.0, 0, 1195146453333.3333, 1408772800000.0, 1768233920000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2759130560000.0]

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
    load_60 = [0.0, 0, 0, 487066697142.8571, 592102357333.3334, 754790656000.0, 875849554285.7142, 1047345920000.0, 1179021120000.0, 1358563520000.0, 0, 0, 0, 1884026560000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3401480960000.0, 0]
    load_70=[0.0, 0, 0, 459817600000.0, 558386316800.0, 652921801739.1305, 784129903157.8948, 920563520000.0, 1027025120000.0, 0, 1365442240000.0, 1451960640000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3239842240000.0]
    load_80=[0.0, 0, 0, 0, 553885520000.0, 656807200000.0, 776922496000.0, 935143744000.0, 0, 1201727253333.3333, 1398157760000.0, 1459603840000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3196537920000.0]

    avg_delay_60=[0, 0, 0, 2.8786587387474343e-06, 3.953037112672614e-06, 7.461249539484479e-06, 1.3075767780246552e-05, 3.464913481572528e-05, 4.2064515368973154e-05, 5.02777905933029e-05, 0, 0, 0, 5.7478359163974306e-05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.311201755527175e-05, 0]

    high_delay_60=[0, 0, 0, 2.3692109530096506e-06, 2.8361020152769243e-06, 5.254605349395426e-06, 7.794509819990373e-06, 1.1406528204731055e-05, 1.1527785865617422e-05, 1.138772720618235e-05, 0, 0, 0, 1.1957790852092326e-05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.3077310966897296e-05, 0]

    med_delay_60=[0, 0, 0, 1.994881635138726e-06, 2.030821657483891e-06, 2.2354047781955058e-06, 2.602880961082981e-06, 3.4541596444561442e-06, 3.6006209720693137e-06, 3.593543366222987e-06, 0, 0, 0, 4.333340906515114e-06, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0405190850717104e-05, 0]

    low_delay_60=[0, 0, 0, 1.0733589006049093e-05, 1.415212305622367e-05, 2.1040204294089304e-05, 3.788405356663518e-05, 0.00010098111990963547, 0.0001216036091746237, 0.00013286634063843357, 0, 0, 0, 0.00012223111754271462, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8.409770648244698e-05, 0]

    avg_delay_70=[0, 0, 0, 2.5997107866855963e-06, 2.78322738964322e-06, 3.5608496936358016e-06, 4.4653671587596845e-06, 5.732521119717377e-06, 8.569525342705006e-06, 0, 1.5985111832534173e-05, 1.9880944789141286e-05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.9739269035726742e-05]

    high_delay_70=[0, 0, 0, 1.7033448606323833e-06, 1.8062952237024964e-06, 1.9702837217892913e-06, 2.3301906060385025e-06, 3.696422943488903e-06, 5.778046938866e-06, 0, 8.442340916537677e-06, 9.96860851732808e-06, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.101969706863482e-05]

    med_delay_70=[0, 0, 0, 1.689609251097961e-06, 1.7276629166415495e-06, 1.74749034932549e-06, 1.7944394171456906e-06, 1.9429391153171717e-06, 2.073056298749414e-06, 0, 2.503373675929928e-06, 3.021184235902545e-06, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0800138080413155e-06]

    low_delay_70=[0, 0, 0, 1.37866262217104e-05, 1.1792711774780513e-05, 1.3809722163876929e-05, 1.422058647639307e-05, 1.4466475688144777e-05, 2.0904829431060508e-05, 0, 3.527388446325978e-05, 4.4712230430531076e-05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4.686283286733422e-05]

    avg_delay_80=[0, 0, 0, 0, 2.2845700775070995e-06, 3.030328016271685e-06, 3.822940364583933e-06, 4.364535660752312e-06, 0, 5.606407023443225e-06, 6.125761110600151e-06, 7.443542479052807e-06, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.8175229782067442e-05]

    high_delay_80=[0, 0, 0, 0, 1.1993924407688927e-06, 1.2497616864125311e-06, 1.3274062082448491e-06, 1.4343509036673557e-06, 0, 1.623567287738931e-06, 1.9226262029287894e-06, 3.012246506340721e-06, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7.552501611493741e-06]

    med_delay_80=[0, 0, 0, 0, 1.4968797128732002e-06, 1.5024433561399118e-06, 1.5201064377301627e-06, 1.5323856268277726e-06, 0, 1.5398316147649042e-06, 1.6082827089788057e-06, 1.7312231860757636e-06, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.6010905020971604e-06]

    low_delay_80=[0, 0, 0, 0, 1.1193691325534279e-05, 1.3626090588193647e-05, 1.468739965093906e-05, 1.3929809143520075e-05, 0, 1.5211275673317992e-05, 1.4444127646851423e-05, 1.689330459233939e-05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.8038864433854265e-05]


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