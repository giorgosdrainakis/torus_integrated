import os
import csv
import math
from scipy.stats import genpareto
import matplotlib.pyplot as plt
import numpy as numpy
import random
import numpy as np
import statistics
import csv
from torus_integrated import myglobal
import matplotlib
from matplotlib.ticker import MaxNLocator
from torus_integrated.myglobal import *
# First run with avgg=False to check all samples (where they span)
# According to this plot-> set avgg=True and set grouping parameters to get finalized plots
# Plot label params at the end of the script (thruput-delay-overflow)

# Sampling params
mode='end2end' # in [intra,inter,end2end]
servers=16 # only for intra
tors=16 # only for inter
parent_tor=1 # only for intra, end2end analysis
# Simulation params
my_tbegin=0
my_tend=0.010 # intra 0.050
filename='torus_07_to_10_logs_globecom\\torus3200_highin_intra075_10ms.csv'

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
    def is_intra_for_tor(self,parent_tor_id):
        return (self.is_intra() and self.tor_id==parent_tor_id)
    def is_outgoing_for_tor(self,parent_tor_id):
        return ((not self.is_intra()) and self.tor_id==parent_tor_id)
    def is_incoming_for_tor(self,parent_tor_id):
        return ((not self.is_intra()) and self.destination_tor==parent_tor_id)
    def show_mini(self):
        outp='id='+str(self.packet_id)+',source='+str(self.tor_id)+'-'+str(self.source_id)+',dest='+\
             str(self.destination_tor)+'-'+str(self.destination_id)
        return outp

print('Post-processing log folder=' + str(filename))
my_db=[]
myname=os.path.join(myglobal.ROOT,myglobal.LOGS_FOLDER)
myname = os.path.join(myname, filename)
with open(myname) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        new_rec=Record(row['packet_id'],row['time'],row['packet_size'],row['packet_qos'],
                       row['source_id'], row['tor_id'], row['destination_id'], row['destination_tor'],
                       row['time_intra_buffer_in'], row['time_intra_buffer_out'], row['time_intra_trx_in'], row['time_intra_trx_out'],
                       row['time_tor_buffer_in'], row['time_tor_buffer_out'], row['time_tor_trx_in'], row['time_tor_trx_out'],
                       row['time_inter_buffer_in'], row['time_inter_buffer_out'], row['time_inter_trx_in'], row['time_inter_trx_out']
                       )
        my_db.append(new_rec)

bytes_intra_born=0
bytes_intra_drop=0
bytes_intra_rx=0

bytes_inter_born = 0
bytes_inter_drop_at_intra_buff = 0
bytes_inter_rx_at_source_tor = 0
bytes_inter_drop_at_source_tor = 0
bytes_inter_rx_at_dest_tor = 0
bytes_inter_drop_at_dest_tor = 0
bytes_inter_rx_at_dest_server = 0

print('Entered init with db')
debug_id=0
for rec in my_db:
    print('DBG: B=' + str(debug_id/len(my_db)))
    debug_id = debug_id + 1

    if rec.is_intra():  # intra
        bytes_intra_born = bytes_intra_born+rec.packet_size

        if rec.time_intra_buffer_in>0:
            if rec.time_intra_trx_out:
                bytes_intra_rx=bytes_intra_rx+rec.packet_size
            else:
                print('Error_intra_1')
        else:
            bytes_intra_drop=bytes_intra_drop+rec.packet_size
    else:
        bytes_inter_born = bytes_inter_born+rec.packet_size

        if rec.time_intra_buffer_in>0:
            if rec.time_intra_trx_out:
                bytes_inter_rx_at_source_tor=bytes_inter_rx_at_source_tor+rec.packet_size
            else:
                print('Error_inter_1')
        else:
            bytes_inter_drop_at_intra_buff=bytes_inter_drop_at_intra_buff+rec.packet_size

        if rec.time_tor_buffer_in>0:
            if rec.time_tor_trx_out:
                bytes_inter_rx_at_dest_tor=bytes_inter_rx_at_dest_tor+rec.packet_size
            else:
                print('Error_inter_2')
        else:
            bytes_inter_drop_at_source_tor=bytes_inter_drop_at_source_tor+rec.packet_size

        if rec.time_inter_buffer_in>0:
            if rec.time_inter_trx_out:
                bytes_inter_rx_at_dest_server=bytes_inter_rx_at_dest_server+rec.packet_size
            else:
                print('Error_inter_3')
        else:
            bytes_inter_drop_at_dest_tor=bytes_inter_drop_at_dest_tor+rec.packet_size

        new_rec=Record(row['packet_id'],row['time'],row['packet_size'],row['packet_qos'],
                       row['source_id'], row['tor_id'], row['destination_id'], row['destination_tor'],
                       row['time_intra_buffer_in'], row['time_intra_buffer_out'], row['time_intra_trx_in'], row['time_intra_trx_out'],
                       row['time_tor_buffer_in'], row['time_tor_buffer_out'], row['time_tor_trx_in'], row['time_tor_trx_out'],
                       row['time_inter_buffer_in'], row['time_inter_buffer_out'], row['time_inter_trx_in'], row['time_inter_trx_out']
                       )

print('bytes_intra_born'+'='+str(bytes_intra_born))
print('bytes_intra_drop'+'='+str(bytes_intra_drop))
print('bytes_intra_rx'+'='+str(bytes_intra_rx))
print('bytes_inter_born'+'='+str(bytes_inter_born))
print('bytes_inter_drop_at_intra_buff'+'='+str(bytes_inter_drop_at_intra_buff))
print('bytes_inter_rx_at_source_tor'+'='+str(bytes_inter_rx_at_source_tor))
print('bytes_inter_drop_at_source_tor'+'='+str(bytes_inter_drop_at_source_tor))
print('bytes_inter_rx_at_dest_tor'+'='+str(bytes_inter_rx_at_dest_tor))
print('bytes_inter_drop_at_dest_tor'+'='+str(bytes_inter_drop_at_dest_tor))
print('bytes_inter_rx_at_dest_server'+'='+str(bytes_inter_rx_at_dest_server))
