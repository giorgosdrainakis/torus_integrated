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


def plot_thru():
    _load_divide_factor=1e9
    _thru_divide_factor=1e9
    _load = [0.0, 16594243200.0, 31326648400.0, 42919711200.0, 64141552533.333336, 83489762000.0,
                              99604240000.0, 121667602400.0, 134572714400.0, 148541112000.0, 0, 178315663200.0,
                              201909935200.0, 218157420000.0, 230713750400.0, 0, 266535022400.0, 282980545600.0,
                              300555514200.0, 319599165200.0, 334010304000.0, 349600344333.3333, 366275549295.2381,
                              382328802830.7692, 392835485600.0]
    _thru = [14400000.0, 16593643200.0, 31327848400.0, 42914911200.0, 64140489866.666664,
                              83488562000.0, 99603937200.0, 121671202400.0, 134566451200.0, 148535712000.0, 0,
                              178320463200.0, 201910126400.0, 218162893200.0, 230711241600.0, 0, 266536286800.0,
                              282978852000.0, 300553948000.0, 319600510400.0, 334011427911.1111, 349595511800.0,
                              366272948228.5714, 382330266215.38464, 392823383200.0]

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

    #calcs
    utilization=[]
    for i in range(0,len(_thru)):
        if _load[i]!=0:
            util=_thru[i]/_load[i]
            utilization.append(util)
    print('Utilization='+str(utilization))
    print('Mean util='+str(statistics.mean(utilization)))

    _color='black'

    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=False)

    final_x = np.asarray(_load)
    final_y = np.asarray(_thru)
    _label='4x100 Gbps'
    _linewidth=6

    ax1.plot(final_x, final_y, _color, label=_label,linewidth=_linewidth, linestyle='solid')

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
    ax1.set_xlabel('Load (Gbps)', fontsize=21)
    ax1.set_ylabel('Throughput (Gbps)', fontsize=21)
    ax1.legend(loc='best', fontsize=21)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=21)
    ax1.tick_params(axis='both', which='minor', labelsize=21)

    plt.show()

def plot_delays():
    _load_divide_factor=1e9
    _delay_divide_factor=1e-6
    _load = [0.0, 16594243200.0, 31326648400.0, 42919711200.0, 64141552533.333336, 83489762000.0,
                              99604240000.0, 121667602400.0, 134572714400.0, 148541112000.0, 0, 178315663200.0,
                              201909935200.0, 218157420000.0, 230713750400.0, 0, 266535022400.0, 282980545600.0,
                              300555514200.0, 319599165200.0, 334010304000.0, 349600344333.3333, 366275549295.2381,
                              382328802830.7692, 392835485600.0]
    _thru = [14400000.0, 16593643200.0, 31327848400.0, 42914911200.0, 64140489866.666664,
                              83488562000.0, 99603937200.0, 121671202400.0, 134566451200.0, 148535712000.0, 0,
                              178320463200.0, 201910126400.0, 218162893200.0, 230711241600.0, 0, 266536286800.0,
                              282978852000.0, 300553948000.0, 319600510400.0, 334011427911.1111, 349595511800.0,
                              366272948228.5714, 382330266215.38464, 392823383200.0]
    _delay_avg = [0, 3.150669493020981e-07, 3.1540568444327527e-07, 3.1560476364466594e-07,
                           3.165880393572977e-07, 3.17584770008103e-07, 3.1844968191095143e-07, 3.199331765311336e-07,
                           3.2076229513020033e-07, 3.220306121780506e-07, 0, 3.251985861232954e-07,
                           3.286826572543478e-07, 3.3123640809686736e-07, 3.342603169271484e-07, 0,
                           3.4469771306696634e-07, 3.518050415012516e-07, 3.630320957578146e-07, 3.8128142509051777e-07,
                           4.031189378292053e-07, 4.5296107902520537e-07, 6.334319568439704e-07, 1.5846777204310844e-06,
                           4.070178105961574e-06]

    _delay_high = [0, 2.1455076013803056e-07, 2.1433840884690075e-07, 2.1372352090696936e-07,
                          2.1482929886793575e-07, 2.1558742295761858e-07, 2.159516554338464e-07, 2.1741933635554303e-07,
                          2.2023258332980367e-07, 2.2230983003336246e-07, 0, 2.2874985617078446e-07,
                          2.3623750841913196e-07, 2.438260031630841e-07, 2.5211805275383527e-07, 0,
                          2.869706717009854e-07, 3.104179364517076e-07, 3.5696238722563964e-07, 4.3906857025762134e-07,
                          5.555012646818067e-07, 8.662474726365206e-07, 2.2721593192212496e-06, 1.0523422570918016e-05,
                          3.21331704165311e-05]

    _delay_med = [0, 2.481683328730607e-07, 2.4528216886009717e-07, 2.469205138578771e-07,
                         2.4726556872645636e-07, 2.4871893226769196e-07, 2.4881718441971735e-07, 2.52465666616935e-07,
                         2.5230355630831087e-07, 2.539358862693871e-07, 0, 2.615291720262868e-07, 2.68211796661751e-07,
                         2.767036259512423e-07, 2.8625129939556376e-07, 0, 3.184495471925935e-07,
                         3.4901396111937653e-07, 3.931324133172465e-07, 4.745203740412635e-07, 5.943976452296281e-07,
                         9.337320374697647e-07, 2.4457099329309288e-06, 1.1390504865835674e-05, 3.6442813324691085e-05]

    _delay_low = [0, 3.237096405766777e-07, 3.241523283468476e-07, 3.244780666029507e-07, 3.255422790991915e-07,
                         3.2660429646034763e-07, 3.273894557679278e-07, 3.288279492845693e-07, 3.2963535189614863e-07,
                         3.3077558026053586e-07, 0, 3.334887116716056e-07, 3.366222911982365e-07,
                         3.3875613003563143e-07, 3.412001322056124e-07, 0, 3.493581719575368e-07, 3.546037749138703e-07,
                         3.6244436672933006e-07, 3.744755926564709e-07, 3.8691563962009327e-07, 4.1025434794370376e-07,
                         4.6768077486848836e-07, 6.853299353390079e-07, 1.1600992199229076e-06]

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

    ax1.plot(_load, _delay_avg, color='black', label='Delay Avg',linewidth=_linewidth, linestyle='solid')
    ax1.plot(_load, _delay_high, color='red', label='Delay High',linewidth=_linewidth, linestyle='solid')
    ax1.plot(_load, _delay_med, color='green', label='Delay Med',linewidth=_linewidth, linestyle='solid')
    ax1.plot(_load, _delay_low, color='blue', label='Delay Low',linewidth=_linewidth, linestyle='solid')
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
    ax1.set_xlabel('Load (Gbps)', fontsize=21)
    ax1.set_ylabel('Delay (μsec)', fontsize=21)
    ax1.legend(loc='best', fontsize=21)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=21)
    ax1.tick_params(axis='both', which='minor', labelsize=21)

    plt.show()

plot_thru()
plot_delays()