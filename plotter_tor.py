import datetime
import pandas as pd
from waa.node import *
from waa.traffic import *
from waa.buffer import *
from waa.channel import *
class Record():
    def __init__(self,packet_id,time,size,qos,source_id,
                 destination_id,time_buffer_in,time_buffer_out,
                 time_trx_in,time_trx_out,mode,consume_time):
        self.packet_id=int(packet_id)
        self.time=float(time)
        self.packet_size=float(size)
        self.packet_qos=qos
        self.source_id=int(source_id)
        self.destination_id = int(destination_id)
        self.time_buffer_in=float(time_buffer_in)
        self.time_buffer_out =float(time_buffer_out)
        self.time_trx_in =float(time_trx_in)
        self.time_trx_out =float(time_trx_out)
        self.plot_time=0
        self.mode=mode
        self.consume_time=float(consume_time)

combined_name=myglobal.ROOT+'logs//log2021_07_04_23_00_02_639606_for_node_1.csv'

my_db=[]
with open(combined_name) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    debug_id=0
    for row in csv_reader:
        new_rec=Record(row['packet_id'],row['time'],row['packet_size'],
                       row['packet_qos'], row['source_id'], row['destination_id'],
                       row['time_buffer_in'], row['time_buffer_out'],
                       row['time_trx_in'],row['time_trx_out'],row['mode'],row['consume_time'] )
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
        if item.time_trx_out>=myin and item.time_trx_out<myout:
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
        data = sorted(csv_input, key=lambda row: (float(row['time_trx_out']), float(row['packet_id'])))

    print('Rewriting...')
    with open(combined_name, 'w', newline='') as f_output:
        csv_output = csv.DictWriter(f_output, fieldnames=csv_input.fieldnames)
        csv_output.writeheader()
        csv_output.writerows(data)

    print('completeness 1000/1000=' + str(datetime.datetime.now()))

