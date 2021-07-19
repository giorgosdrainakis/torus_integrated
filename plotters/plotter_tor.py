import datetime
import pandas as pd
from torus_integrated.node import *
from torus_integrated.traffic import *
from torus_integrated.buffer import *
from torus_integrated.channel import *
class Record():
    def __init__(self,packet_id,time,packet_size,packet_qos,source_id,tor_id,destination_id,destination_tor,
                 time_intra_buffer_in,time_intra_buffer_out,time_intra_trx_in,time_intra_trx_out,
                 time_tor_buffer_in,time_tor_buffer_out,time_tor_trx_in,time_tor_trx_out,
                 time_inter_buffer_in,time_inter_buffer_out,time_inter_trx_in,time_inter_trx_out):
        self.packet_id = int(packet_id)
        self.time = float(time)
        self.packet_size = float(packet_size)
        self.packet_qos = packet_qos
        self.source_id = int(source_id)
        self.destination_id = int(destination_id)
        self.tor_id = int(tor_id)
        self.destination_tor = int(destination_tor)
        self.time_intra_buffer_in = float(time_intra_buffer_in)
        self.time_intra_buffer_out = float(time_intra_buffer_out)
        self.time_intra_trx_in = float(time_intra_trx_in)
        self.time_intra_trx_out = float(time_intra_trx_out)
        self.time_tor_buffer_in = float(time_tor_buffer_in)
        self.time_tor_buffer_out = float(time_tor_buffer_out)
        self.time_tor_trx_in = float(time_tor_trx_in)
        self.time_tor_trx_out = float(time_tor_trx_out)
        self.time_inter_buffer_in = float(time_inter_buffer_in)
        self.time_inter_buffer_out = float(time_inter_buffer_out)
        self.time_inter_trx_in = float(time_inter_trx_in)
        self.time_inter_trx_out = float(time_inter_trx_out)
    def is_intra(self):
        return (self.tor_id==self.destination_tor)

combined_name=myglobal.ROOT+'logs//log2021_07_04_23_00_02_639606_for_node_1.csv'

my_db=[]
with open(combined_name) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    debug_id=0
    for row in csv_reader:
        new_rec=Record(row['packet_id'],row['time'],row['packet_size'],
                       row['packet_qos'], row['source_id'], row['destination_id'],
                       row['time_intra_buffer_in'], row['time_intra_buffer_out'],
                       row['time_intra_trx_in'],row['time_intra_trx_out'],row['mode'],row['consume_time'] )
        my_db.append(new_rec)
        print(str(debug_id))
        debug_id=debug_id+1

import numpy as np
start=0
stop=0.01
timestep=myglobal.timestep*100000
mytimeslot=[]
mybuffer=[]
myconsumed=[]
added_packs=0
for timeslot in np.arange(start, stop, timestep):
    print('--------- Timeslot='+str(timeslot)+' until'+str(timeslot+timestep))
    mytimeslot.append(timeslot)
    myin=timeslot
    myout=myin+timestep
    mybuffersize=0
    for item in my_db:
        if item.time_intra_trx_out>=myin and item.time_intra_trx_out<myout:
            mybuffersize=mybuffersize+item.packet_size
            added_packs=added_packs+1
    mybuffer.append(mybuffersize)

for timeslot in np.arange(start, stop, timestep):
    myin=timeslot
    myout=myin+timestep
    myconsumedsize=0
    for item in my_db:
        if item.consume_time>=myin and item.consume_time<myout:
            myconsumedsize=myconsumedsize+item.packet_size
    myconsumed.append(myconsumedsize)

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
mybuffer=[x*8/timestep for x in mybuffer]
myconsumed=[x*8/timestep for x in myconsumed]
plt.plot(mytimeslot, mybuffer, 'b--',linewidth=4, label="Load (bps)")
plt.plot(mytimeslot, myconsumed, 'k-o',linewidth=2, label="TOR consumption (bps)")
plt.xlabel('Time (sec)', fontsize=25)
plt.ylabel('Rate', fontsize=25)
plt.grid(True, which='major', axis='both')
plt.legend()
plt.show()


if False:
    print('Sorting...')
    with open(combined_name, 'r', newline='') as f_input:
        csv_input = csv.DictReader(f_input)
        data = sorted(csv_input, key=lambda row: (float(row['time_intra_trx_out']), float(row['packet_id'])))

    print('Rewriting...')
    with open(combined_name, 'w', newline='') as f_output:
        csv_output = csv.DictWriter(f_output, fieldnames=csv_input.fieldnames)
        csv_output.writeheader()
        csv_output.writerows(data)

    print('completeness 1000/1000=' + str(datetime.datetime.now()))

