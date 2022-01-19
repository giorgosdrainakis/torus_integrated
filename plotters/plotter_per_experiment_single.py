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
filename= 'torus_10ms_300g_3_5_5milli_08intra.csv'
t_end=0.01
t_begin=0
parent_tor=1
run_intra=True

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


record_list=[]
with open(myglobal.ROOT+myglobal.LOGS_FOLDER+filename) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    debug_id=0
    for row in csv_reader:
        new_rec=Record(row['packet_id'],row['time'],row['packet_size'],row['packet_qos'],
                       row['source_id'], row['tor_id'], row['destination_id'], row['destination_tor'],
                       row['time_intra_buffer_in'], row['time_intra_buffer_out'], row['time_intra_trx_in'], row['time_intra_trx_out'],
                       row['time_tor_buffer_in'], row['time_tor_buffer_out'], row['time_tor_trx_in'], row['time_tor_trx_out'],
                       row['time_inter_buffer_in'], row['time_inter_buffer_out'], row['time_inter_trx_in'], row['time_inter_trx_out']
                       )
        record_list.append(new_rec)
        debug_id=debug_id+1
        print(str(debug_id))
load_total=[]
load_high=[]
load_med=[]
load_low=[]
delay_total=[]
delay_high=[]
delay_med=[]
delay_low=[]
qdelay_total=[]
qdelay_high=[]
qdelay_med=[]
qdelay_low=[]
drop_total=[]
drop_high=[]
drop_med=[]
drop_low=[]
thru_total=[]
thru_high=[]
thru_med=[]
thru_low=[]

if run_intra:
    for rec in record_list:
        bypass=False
        if rec.is_intra_for_tor(parent_tor):  # intra
            _time_birth = rec.time
            _source_id = rec.source_id
            _time_buffer_in = rec.time_intra_buffer_in
            _time_trx_in = rec.time_intra_trx_in
            _time_trx_out = rec.time_intra_trx_out
        elif rec.is_outgoing_for_tor(parent_tor):
            _time_birth = rec.time
            _source_id = rec.source_id
            _time_buffer_in = rec.time_intra_buffer_in
            _time_trx_in = rec.time_intra_trx_in
            _time_trx_out = rec.time_intra_trx_out
        elif rec.is_incoming_for_tor(parent_tor):
            _time_birth = rec.time_tor_trx_out
            _source_id = 16
            _time_buffer_in = rec.time_inter_buffer_in
            _time_trx_in = rec.time_inter_trx_in
            _time_trx_out = rec.time_inter_trx_out
        else:
            bypass=True

        if not bypass:
            load_total.append(rec.packet_size)
            if rec.packet_qos=='high':
                load_high.append(rec.packet_size)
            elif rec.packet_qos=='med':
                load_med.append(rec.packet_size)
            elif rec.packet_qos=='low':
                load_low.append(rec.packet_size)

            if _time_buffer_in > -1:
                delay_total.append(_time_trx_out - _time_birth)
                qdelay_total.append(_time_trx_in - _time_birth)
                if rec.packet_qos == 'high':
                    delay_high.append(_time_trx_out - _time_birth)
                    qdelay_high.append(_time_trx_in - _time_birth)
                elif rec.packet_qos == 'med':
                    delay_med.append(_time_trx_out - _time_birth)
                    qdelay_med.append(_time_trx_in - _time_birth)
                elif rec.packet_qos == 'low':
                    delay_low.append(_time_trx_out - _time_birth)
                    qdelay_low.append(_time_trx_in - _time_birth)
            else:
                drop_total.append(rec.packet_size)
                if rec.packet_qos == 'high':
                    drop_high.append(rec.packet_size)
                elif rec.packet_qos == 'med':
                    drop_med.append(rec.packet_size)
                elif rec.packet_qos == 'low':
                    drop_low.append(rec.packet_size)

            if _time_trx_out>_time_trx_in:
                thru_total.append(rec.packet_size)
                if rec.packet_qos == 'high':
                    thru_high.append(rec.packet_size)
                elif rec.packet_qos == 'med':
                    thru_med.append(rec.packet_size)
                elif rec.packet_qos == 'low':
                    thru_low.append(rec.packet_size)
else:
    for rec in record_list:
        bypass=False
        if not rec.is_intra():
            _source_id = rec.tor_id
            _time_load = rec.time_intra_trx_out
            _thru_out = rec.time_inter_trx_out
            _time_buffer1_in = rec.time_intra_buffer_in
            _time_buffer2_in = rec.time_tor_buffer_in
            _time_buffer3_in = rec.time_inter_buffer_in
            _qdelay = (rec.time_intra_buffer_out - rec.time_intra_buffer_in) + (
                        rec.time_tor_buffer_out - rec.time_tor_buffer_in) + (
                                  rec.time_inter_buffer_out - rec.time_inter_buffer_in)
            _delay = rec.time_inter_trx_out - rec.time
        else:
            bypass=True

        if not bypass:
            load_total.append(rec.packet_size)
            if rec.packet_qos=='high':
                load_high.append(rec.packet_size)
            elif rec.packet_qos=='med':
                load_med.append(rec.packet_size)
            elif rec.packet_qos=='low':
                load_low.append(rec.packet_size)
            if _time_buffer1_in > -1 and _time_buffer2_in > -1 and _time_buffer3_in > -1:
                delay_total.append(_delay)
                qdelay_total.append(_qdelay)
                if rec.packet_qos == 'high':
                    delay_high.append(_delay)
                    qdelay_high.append(_qdelay)
                elif rec.packet_qos == 'med':
                    delay_med.append(_delay)
                    qdelay_med.append(_qdelay)
                elif rec.packet_qos == 'low':
                    delay_low.append(_delay)
                    qdelay_low.append(_qdelay)
            else:
                drop_total.append(rec.packet_size)
                if rec.packet_qos == 'high':
                    drop_high.append(rec.packet_size)
                elif rec.packet_qos == 'med':
                    drop_med.append(rec.packet_size)
                elif rec.packet_qos == 'low':
                    drop_low.append(rec.packet_size)
            if t_begin < _thru_out:
                thru_total.append(rec.packet_size)
                if rec.packet_qos == 'high':
                    thru_high.append(rec.packet_size)
                elif rec.packet_qos == 'med':
                    thru_med.append(rec.packet_size)
                elif rec.packet_qos == 'low':
                    thru_low.append(rec.packet_size)


print('load_total='+str(sum(load_total)))
print('load_high='+str(sum(load_high)))
print('load_med='+str(sum(load_med)))
print('load_low='+str(sum(load_low)))
print('delay_total='+str(statistics.mean(delay_total)))
print('delay_high='+str(statistics.mean(delay_high)))
print('delay_med='+str(statistics.mean(delay_med)))
print('delay_low='+str(statistics.mean(delay_low)))
print('qdelay_total='+str(statistics.mean(qdelay_total)))
print('qdelay_high='+str(statistics.mean(qdelay_high)))
print('qdelay_med='+str(statistics.mean(qdelay_med)))
print('qdelay_low='+str(statistics.mean(qdelay_low)))
print('drop_total='+str(sum(drop_total)))
print('drop_high='+str(sum(drop_high)))
print('drop_med='+str(sum(drop_med)))
print('drop_low='+str(sum(drop_low)))
print('thru_total='+str(sum(thru_total)))
print('thru_high='+str(sum(thru_high)))
print('thru_med='+str(sum(thru_med)))
print('thru_low='+str(sum(thru_low)))
print('LOAD Gbps='+str(sum(load_total)*8*1e-9/(t_end-t_begin)))
print('THRU Gbps='+str(sum(thru_total)*8*1e-9/(t_end-t_begin)))
print('DELAY ms='+str(statistics.mean(delay_total)*1000))





















