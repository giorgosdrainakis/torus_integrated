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
avgg=False
filename= '4a3_needs_processing_dataset_in_iccs_pc.csv'
parent_tor=1
my_tbegin=0
my_tend=0.050
my_samples=100 # 500
# Grouping params
start_group_value=0
end_group_value=2.2e6#Peirama_1_set1  8.5e6       # Peirama2_80_big=5.1e6 #Peirama2_80_small= 1.2e7
grouping_points=25

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


class My_Timeslot_List():
    def __init__(self,tbegin,tend,samples):
        self.db=[]
        self.tbegin=tbegin
        self.tend=tend
        self.samples=samples
        self.total_time = my_tend - my_tbegin
        self.timestep = self.total_time / samples
        tt_range = np.linspace(self.tbegin, self.tend, self.samples)
        for tt in tt_range:
            new_timeslot=My_Timeslot(tt,tt+self.timestep)
            self.db.append(new_timeslot)

    def init_with_db(self,record_db):
        print('DBG: Entered init with db')
        debug_id=0
        #total_packets_ids=[]
        for rec in record_db:
            print('DBG: B=' + str(debug_id/len(record_db)))
            debug_id = debug_id + 1

            if rec.is_intra_for_tor(parent_tor) or rec.is_outgoing_for_tor(parent_tor) or rec.is_incoming_for_tor(parent_tor):
                #if rec.packet_id in total_packets_ids:
                #    print('ERROR: This is a dublicate packet' + str(rec.packet_id))
                #total_packets_ids.append(rec.packet_id)

                if rec.is_intra_for_tor(parent_tor):  # intra
                    _time_birth=rec.time
                    _source_id=rec.source_id
                    _time_buffer_in = rec.time_intra_buffer_in
                    _time_trx_in=rec.time_intra_trx_in
                    _time_trx_out = rec.time_intra_trx_out
                elif rec.is_outgoing_for_tor(parent_tor):
                    _time_birth=rec.time
                    _source_id = rec.source_id
                    _time_buffer_in=rec.time_intra_buffer_in
                    _time_trx_in = rec.time_intra_trx_in
                    _time_trx_out = rec.time_intra_trx_out
                elif rec.is_incoming_for_tor(parent_tor):
                    _time_birth=rec.time_tor_trx_out
                    _source_id = 16
                    _time_buffer_in = rec.time_inter_buffer_in
                    _time_trx_in = rec.time_inter_trx_in
                    _time_trx_out = rec.time_inter_trx_out
                else:
                    print('ERROR: Unknown packet, =' + str(rec.show_mini()))

                for timeslot in self.db:
                    if timeslot.t_begin <= _time_birth and _time_birth < timeslot.t_end:
                        timeslot.load_total_num=timeslot.load_total_num+rec.packet_size

    def get_list_load_total(self):
        mylist=[]
        for element in self.db:
            mylist.append(element.get_agg_load_total_num())
        return mylist

class My_Timeslot():
    def __init__(self,tbegin,tend):
        self.load_total_num=0
        self.t_begin=tbegin
        self.t_end=tend
        self.load_total=[]

    def get_agg_load_total(self):
        mytotal=0
        for el in self.load_total:
            mytotal=mytotal+el
        return mytotal
    def get_agg_load_total_num(self):
        return self.load_total_num


my_db=[]
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
        my_db.append(new_rec)
        #print(str(debug_id/len(csv_reader)))
        debug_id=debug_id+1

timeslot_list=My_Timeslot_List(my_tbegin,my_tend,my_samples)
timeslot_list.init_with_db(my_db)

if not avgg:
    LOAD=timeslot_list.get_list_load_total()
    LOAD=[54477372.0, 33075744.0, 29087392.0, 26730276.0, 25011432.0, 22693228.0, 22045596.0, 23830844.0, 22656452.0, 17776888.0, 17512000.0, 21722004.0, 21744556.0, 25959660.0, 21905676.0, 19637688.0, 18418104.0, 20239976.0, 17829396.0, 17057184.0, 18951188.0, 20537324.0, 16820188.0, 19848188.0, 19956996.0, 21572352.0, 19486100.0, 25102564.0, 20730876.0, 23468640.0, 17790096.0, 20433336.0, 19896468.0, 20239348.0, 24736856.0, 19981048.0, 21700968.0, 18066572.0, 19730920.0, 20881852.0, 18982024.0, 17514452.0, 20987664.0, 22184052.0, 20671264.0, 19033816.0, 22740780.0, 22083688.0, 21571536.0, 17132012.0, 16316748.0, 16103272.0, 17663576.0, 17593544.0, 16164644.0, 14981344.0, 17201624.0, 15676052.0, 16211496.0, 15286192.0, 16623548.0, 17010692.0, 16451596.0, 15755356.0, 15648556.0, 15232400.0, 17484684.0, 15256744.0, 16194932.0, 15205572.0, 14744668.0, 20345756.0, 15835168.0, 19112532.0, 21139004.0, 15879240.0, 15407668.0, 14790912.0, 17582800.0, 13766388.0, 16177012.0, 15491748.0, 21676152.0, 19363440.0, 16977216.0, 19229372.0, 17543260.0, 16524288.0, 17938380.0, 18770912.0, 19256228.0, 18800292.0, 21032292.0, 16353928.0, 15453720.0, 16630180.0, 17513408.0, 17673624.0, 20917060.0, 0]
    LOAD_bit=[x*1 for x in LOAD]
    LOAD_bit.sort()
    print(LOAD_bit)

