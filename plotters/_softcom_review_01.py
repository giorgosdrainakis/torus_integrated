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

from torus_integrated.logs.log_20240719_id100_topo1x16_ch1x10_load80g_end100ms_dcTF.result import *
from torus_integrated.logs.log_20240719_id100_topo1x16_ch1x10_load80g_end100ms_dcTF.result_dual import *


def plot_compare_delay_bar():
	plt.rcParams["font.weight"] = "bold"
	plt.rcParams["axes.labelweight"] = "bold"

	x_label='Total load (Gbps)'

	x_lim_begin=3
	x_lim_end=11
	y_label_1='Throughput (Gbps)'
	y_label_2 = 'End-to-end latency (μs)'

	fig, ax1 = plt.subplots(constrained_layout=False)
	ax2 = ax1.twinx()

	ax2.set_yscale('log')

	load=[4,6,8,10]

	waa_thru=[3.95,5.91,7.79,9.28]
	dual_thru=[3.84,5.13,6.68,7.13]
	waa_delay = [13,14,65,222] # us
	dual_delay=[77,296,2004,3529]

	mini_size = 0.16
	big_size = 0.35
	width = 0.25

	x_med = load

	x_high = [x - big_size for x in x_med]
	x_dual_thru = [x - mini_size for x in x_high]
	x_waa_thru  = [x + mini_size for x in x_high]

	x_low = [x + big_size for x in x_med]
	x_dual_delay = [x - mini_size for x in x_low]
	x_waa_delay  = [x + mini_size for x in x_low]


	ax1.bar(x_dual_thru, dual_thru, color='white',edgecolor='blue', label="Dual-MAC throughput",linewidth=4, width=width,hatch='o')
	ax1.bar(x_waa_thru, waa_thru,  color='white',edgecolor='blue', label="WDMA throughput",linewidth=4, width=width,hatch='//')
	ax2.bar(x_dual_delay, dual_delay,  color='white',edgecolor='red', label="Dual-MAC latency",linewidth=4, width=width,hatch='o')
	ax2.bar(x_waa_delay, waa_delay, color='white',edgecolor='red',  label="WDMA latency",linewidth=4, width=width, hatch='//')
	ax1.set_xticks([4,6,8,10])

	_LINEWIDTH=7
	_LABEL_SIZE=30
	_LEGEND_SIZE=18
	_TICK_PARAMS=35
	try:
		ax1.set_xlabel(x_label, fontsize=_LABEL_SIZE)
	except:
		pass
	try:
		ax1.set_ylabel(y_label_1, fontsize=_LABEL_SIZE, color='blue')
		ax2.set_ylabel(y_label_2, fontsize=_LABEL_SIZE, color='red')
	except:
		pass
	try:
		ax1.set_xlim(x_lim_begin,x_lim_end)
		ax2.set_xlim(x_lim_begin, x_lim_end)
	except:
		pass

	ax1.yaxis.label.set_color('blue')
	ax1.tick_params(axis='y', colors='blue')

	ax2.yaxis.label.set_color('red')
	ax2.tick_params(axis='y', colors='red')

	lines, labels = ax1.get_legend_handles_labels()
	lines2, labels2 = ax2.get_legend_handles_labels()
	ax2.legend(lines + lines2, labels + labels2, loc=0,fontsize=_LEGEND_SIZE)

	ax1.grid(True, which='major', axis='both')
	ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
	ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
	ax2.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
	ax2.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

	plt.show()


plot_compare_delay_bar()