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
split=True
measurement_type='post' # in [pre,post], pre refers to traffic_generation metrics, post to after_experiments metrics
avgg=True
mode='bridge_ul' # in [intra,inter,end2end]
servers=8 # only for intra
tors=16 # only for inter
parent_tor=1 # only for intra, end2end analysis
# Simulation params
my_tbegin=0
my_tend=0.010 # intra 0.050
my_samples=100 # intra 100
#filename='log2022_07_12_23_13_52_889801_everything.csv'
filename='log_800_16x8_go_8020.csv'
# Grouping params
start_group_value=0
end_group_value=1e7 #intra/inter/both/bridge_dl/bridge_ul=4e6,2e7,1e8...1.8e7,1e7
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
class My_Group:
    def __init__(self,timestep):
        self.nominal_load=None
        self.timeslots=[]
        self.timestep=timestep

    def get_stats_load_total_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_total())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)

    def get_stats_load_high_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_high())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)

    def get_stats_load_med_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_med())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)

    def get_stats_load_low_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_low())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)

    def get_stats_thru_total_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_total())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_thru_high_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_high())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_thru_med_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_med())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_thru_low_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_low())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_drop_total_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_total())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_drop_high_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_high())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_drop_med_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_med())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_drop_low_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_low())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_drop_prob_total(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_total()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_total()/tslot.get_agg_load_total())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_drop_prob_high(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_high()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_high()/tslot.get_agg_load_high())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_drop_prob_med(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_med()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_med()/tslot.get_agg_load_med())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_drop_prob_low(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_low()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_low()/tslot.get_agg_load_low())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_inter_delay_total(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_inter_delay_total()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_inter_delay_high(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_inter_delay_high()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_inter_delay_med(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_inter_delay_med()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_inter_delay_low(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_inter_delay_low()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_intra_delay_total(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_intra_delay_total()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_intra_delay_high(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_intra_delay_high()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_intra_delay_med(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_intra_delay_med()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_intra_delay_low(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_intra_delay_low()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_delay_total(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_total()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_delay_high(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_high()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_delay_med(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_med()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_delay_low(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_low()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_qdelay_total(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_total()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)

    def get_stats_qdelay_high(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_high()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)

    def get_stats_qdelay_med(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_med()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)

    def get_stats_qdelay_low(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_low()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)
    def get_stats_load_node_bps(self,node):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node(node))
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node_bps(self,node):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node(node))
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node_bps(self,node):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node(node))
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node(self,node):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node(node)==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node(node)/tslot.get_agg_load_node(node))
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node(self,node):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node(node)
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node(self,node):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node(node)
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)
class My_Group_List():
    def __init__(self,tbegin,tend,samples, start_group_value,end_group_value,grouping_points):
        self.db = []
        self.tbegin=tbegin
        self.tend=tend
        self.samples=samples
        self.start_group_value=start_group_value
        self.end_group_value=end_group_value
        self.grouping_point=grouping_points
        self.nominal_rates = np.linspace(self.start_group_value, self.end_group_value, self.grouping_point)
        #print('DBG: Nominal Rates'+str(self.nominal_rates))
        timestep=(self.tend-self.tbegin)/self.samples
        for nomrate in self.nominal_rates:
            mygroup=My_Group(timestep)
            mygroup.nominal_load=nomrate
            self.db.append(mygroup)

    def find_closest(self,old_rate):
        diff = math.inf
        outvalue = None
        for nomrate in self.nominal_rates:
            if abs(old_rate - nomrate) < diff:
                diff = abs(old_rate - nomrate)
                outvalue = nomrate
        return outvalue

    def assign_timeslots_to_groups(self,timeslot_list):
        for timeslot in timeslot_list.db:
            # find closest nominal rate
            current_rate=timeslot.get_agg_load_total()
            new_rate=self.find_closest(current_rate)
            # assign timeslot to group based on previous rate
            found=False
            for group in self.db:
                if group.nominal_load==new_rate:
                    group.timeslots.append(timeslot)
                    found=True
            if not found:
                print('ERROR: Cannot assign timeslot with rate=' + str(new_rate))

    def get_groups_load_total_bps(self):
        avg_list=[]
        err_list=[]
        for gr in self.db:
            avg,err=gr.get_stats_load_total_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list,err_list

    def get_groups_load_high_bps(self):
        avg_list=[]
        err_list=[]
        for gr in self.db:
            avg,err=gr.get_stats_load_high_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list,err_list

    def get_groups_load_med_bps(self):
        avg_list=[]
        err_list=[]
        for gr in self.db:
            avg,err=gr.get_stats_load_med_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list,err_list

    def get_groups_load_low_bps(self):
        avg_list=[]
        err_list=[]
        for gr in self.db:
            avg,err=gr.get_stats_load_low_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list,err_list


    def get_groups_thru_total_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_total_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_high_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_high_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_med_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_med_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_low_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_low_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_total_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_total_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_high_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_high_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_med_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_med_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_low_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_low_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_total(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_total()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_high(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_high()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_med(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_med()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_low(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_low()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_inter_delay_total(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_inter_delay_total()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_inter_delay_high(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_inter_delay_high()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_inter_delay_med(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_inter_delay_med()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_inter_delay_low(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_inter_delay_low()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_intra_delay_total(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_intra_delay_total()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_intra_delay_high(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_intra_delay_high()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_intra_delay_med(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_intra_delay_med()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_intra_delay_low(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_intra_delay_low()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_total(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_total()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_high(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_high()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_med(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_med()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_low(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_low()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_total(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_total()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_high(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_high()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_med(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_med()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_low(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_low()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_load_node_bps(self,node):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node_bps(node)
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_node_bps(self,node):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node_bps(node)
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_node_bps(self,node):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node_bps(node)
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_node(self,node):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node(node)
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_node(self,node):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node(node)
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_node(self,node):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node(node)
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
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

    def init_with_db_inter(self,record_db):
        print('Entered init with db')
        debug_id=0

        total_packets_ids=[]
        record_db_len=len(record_db)
        for rec in record_db:
            #print('DBG: B=' + str(debug_id/len(record_db)))
            debug_id = debug_id + 1

            if not rec.is_intra(): # metraw apo tin wra pou to paketo ftanei (i drop) ston source tor buffer mexri tin wra prin ftasei ston dest buffer
                _source_id=rec.tor_id
                _time_load = rec.time_intra_trx_out
                _thru_out = rec.time_tor_trx_out
                _time_buffer1_in = rec.time_intra_buffer_in
                _time_buffer2_in = rec.time_tor_buffer_in
                _time_buffer3_in = rec.time_inter_buffer_in
                _qdelay=(rec.time_tor_buffer_out-rec.time_tor_buffer_in)
                _delay=rec.time_tor_trx_out-rec.time_intra_trx_out
                for timeslot in self.db:
                    if timeslot.t_begin <= _time_load and _time_load < timeslot.t_end:
                        timeslot.load_total=timeslot.load_total+rec.packet_size
                        timeslot.num_total = timeslot.num_total + 1
                        timeslot.load_node[_source_id]=timeslot.load_node[_source_id]+rec.packet_size
                        timeslot.num_node[_source_id]=timeslot.num_node[_source_id]+1

                        if rec.packet_qos=='high':
                            timeslot.load_high=timeslot.load_high+rec.packet_size
                            timeslot.num_high=timeslot.num_high+1
                        elif rec.packet_qos=='med':
                            timeslot.load_med=timeslot.load_med+rec.packet_size
                            timeslot.num_med = timeslot.num_med + 1
                        elif rec.packet_qos=='low':
                            timeslot.load_low=timeslot.load_low+rec.packet_size
                            timeslot.num_low = timeslot.num_low + 1

                        if _time_buffer1_in > -1 and _time_buffer2_in>-1:
                            timeslot.delay_total=timeslot.delay_total+_delay
                            timeslot.qdelay_total=timeslot.qdelay_total+_qdelay
                            timeslot.succ_total = timeslot.succ_total + 1

                            if rec.packet_qos == 'high':
                                timeslot.delay_high=timeslot.delay_high+ _delay
                                timeslot.qdelay_high=timeslot.qdelay_high+_qdelay
                                timeslot.succ_high=timeslot.succ_high+1
                            elif rec.packet_qos == 'med':
                                timeslot.delay_med=timeslot.delay_med+ _delay
                                timeslot.qdelay_med=timeslot.qdelay_med+_qdelay
                                timeslot.succ_med=timeslot.succ_med+1
                            elif rec.packet_qos == 'low':
                                timeslot.delay_low=timeslot.delay_low+ _delay
                                timeslot.qdelay_low=timeslot.qdelay_low+_qdelay
                                timeslot.succ_low=timeslot.succ_low+1
                            timeslot.delay_node[_source_id]=timeslot.delay_node[_source_id]+_delay
                            timeslot.qdelay_node[_source_id]=timeslot.qdelay_node[_source_id]+_qdelay
                            timeslot.succ_node[_source_id]=timeslot.succ_node[_source_id]+1
                        else:
                            timeslot.drop_total = timeslot.drop_total + (rec.packet_size)
                            if rec.packet_qos == 'high':
                                timeslot.drop_high = timeslot.drop_high + (rec.packet_size)
                            elif rec.packet_qos == 'med':
                                timeslot.drop_med = timeslot.drop_med + (rec.packet_size)
                            elif rec.packet_qos == 'low':
                                timeslot.drop_low = timeslot.drop_low + (rec.packet_size)
                            timeslot.drop_node[_source_id] = timeslot.drop_node[_source_id] + (rec.packet_size)

                for timeslot in self.db:
                    if timeslot.t_begin <= _thru_out and _thru_out < timeslot.t_end:
                        timeslot.thru_total = timeslot.thru_total + (rec.packet_size)

                        if rec.packet_qos == 'high':
                            timeslot.thru_high=timeslot.thru_high+(rec.packet_size)
                        elif rec.packet_qos == 'med':
                            timeslot.thru_med=timeslot.thru_med+(rec.packet_size)
                        elif rec.packet_qos == 'low':
                            timeslot.thru_low=timeslot.thru_low+(rec.packet_size)
                        timeslot.thru_node[_source_id] = timeslot.thru_node[_source_id] + (rec.packet_size)

    def init_with_db_intra(self,record_db,split):
        #print('DBG: Entered init with db')
        debug_id=0

        total_packets_ids=[]
        record_db_len=len(record_db)
        for rec in record_db:
            #print('DBG: B=' + str(debug_id/len(record_db)))
            debug_id = debug_id + 1

            if split:
                go=rec.is_intra_for_tor(parent_tor)
            else:
                go=rec.is_intra_for_tor(parent_tor) or rec.is_outgoing_for_tor(parent_tor) or rec.is_incoming_for_tor(parent_tor)

            if go:
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
                        timeslot.load_total=timeslot.load_total+rec.packet_size
                        timeslot.num_total=timeslot.num_total+1
                        timeslot.load_node[_source_id]=timeslot.load_node[_source_id]+rec.packet_size
                        timeslot.num_node[_source_id]=timeslot.num_node[_source_id]+1

                        if rec.packet_qos=='high':
                            timeslot.load_high=timeslot.load_high+rec.packet_size
                            timeslot.num_high=timeslot.num_high+1
                        elif rec.packet_qos=='med':
                            timeslot.load_med=timeslot.load_med+rec.packet_size
                            timeslot.num_med = timeslot.num_med + 1
                        elif rec.packet_qos=='low':
                            timeslot.load_low=timeslot.load_low+rec.packet_size
                            timeslot.num_low = timeslot.num_low + 1

                        if _time_buffer_in > -1:
                            timeslot.delay_total=timeslot.delay_total+ (_time_trx_out - _time_birth)
                            timeslot.qdelay_total=timeslot.qdelay_total+(_time_trx_in - _time_birth)
                            timeslot.succ_total=timeslot.succ_total+1
                            if rec.packet_qos == 'high':
                                timeslot.delay_high=timeslot.delay_high+ (_time_trx_out - _time_birth)
                                timeslot.qdelay_high=timeslot.qdelay_high+(_time_trx_in - _time_birth)
                                timeslot.succ_high=timeslot.succ_high+1
                            elif rec.packet_qos == 'med':
                                timeslot.delay_med=timeslot.delay_med+ (_time_trx_out - _time_birth)
                                timeslot.qdelay_med=timeslot.qdelay_med+(_time_trx_in - _time_birth)
                                timeslot.succ_med=timeslot.succ_med+1
                            elif rec.packet_qos == 'low':
                                timeslot.delay_low=timeslot.delay_low+ (_time_trx_out - _time_birth)
                                timeslot.qdelay_low=timeslot.qdelay_low+(_time_trx_in - _time_birth)
                                timeslot.succ_low=timeslot.succ_low+1
                            timeslot.delay_node[_source_id]=timeslot.delay_node[_source_id]+(_time_trx_out - _time_birth)
                            timeslot.qdelay_node[_source_id]=timeslot.qdelay_node[_source_id]+(_time_trx_in - _time_birth)
                            timeslot.succ_node[_source_id]=timeslot.succ_node[_source_id]+1
                        else:
                            timeslot.drop_total=timeslot.drop_total+(rec.packet_size)
                            if rec.packet_qos == 'high':
                                timeslot.drop_high = timeslot.drop_high + (rec.packet_size)
                            elif rec.packet_qos == 'med':
                                timeslot.drop_med = timeslot.drop_med + (rec.packet_size)
                            elif rec.packet_qos == 'low':
                                timeslot.drop_low = timeslot.drop_low + (rec.packet_size)
                            timeslot.drop_node[_source_id]=timeslot.drop_node[_source_id]+(rec.packet_size)

                for timeslot in self.db:
                    if timeslot.t_begin <= _time_trx_out and _time_trx_out < timeslot.t_end:
                        timeslot.thru_total=timeslot.thru_total+(rec.packet_size)
                        if rec.packet_qos == 'high':
                            timeslot.thru_high=timeslot.thru_high+(rec.packet_size)
                        elif rec.packet_qos == 'med':
                            timeslot.thru_med=timeslot.thru_med+(rec.packet_size)
                        elif rec.packet_qos == 'low':
                            timeslot.thru_low=timeslot.thru_low+(rec.packet_size)
                        timeslot.thru_node[_source_id] = timeslot.thru_node[_source_id] + (rec.packet_size)

    def init_with_db_end2end(self,record_db):
        print('Entered init with db')
        debug_id=0
        for rec in record_db:
            #print('DBG: B=' + str(debug_id/len(record_db)))
            debug_id = debug_id + 1

            _time_birth = rec.time
            _source_id = rec.tor_id

            if rec.is_intra():  # intra
                _time_buffer1_in = rec.time_intra_buffer_in
                _time_buffer2_in = rec.time_intra_buffer_in
                _time_buffer3_in = rec.time_intra_buffer_in
                _qdelay=rec.time_intra_buffer_out-rec.time_intra_buffer_in
                _delay=rec.time_intra_trx_out-rec.time
                _thru_out=rec.time_intra_trx_out
            else:
                _time_buffer1_in = rec.time_intra_buffer_in
                _time_buffer2_in = rec.time_tor_buffer_in
                _time_buffer3_in = rec.time_inter_buffer_in
                _qdelay=(rec.time_intra_buffer_out-rec.time_intra_buffer_in)+(rec.time_tor_buffer_out-rec.time_tor_buffer_in)+(rec.time_inter_buffer_out-rec.time_inter_buffer_in)
                _delay=rec.time_inter_trx_out-rec.time
                _thru_out = rec.time_inter_trx_out

            for timeslot in self.db:
                if timeslot.t_begin <= _time_birth and _time_birth <= timeslot.t_end:
                    timeslot.load_total = timeslot.load_total + rec.packet_size
                    timeslot.num_total = timeslot.num_total + 1
                    timeslot.load_node[_source_id] = timeslot.load_node[_source_id] + rec.packet_size
                    timeslot.num_node[_source_id] = timeslot.num_node[_source_id] + 1

                    if rec.packet_qos == 'high':
                        timeslot.load_high = timeslot.load_high + rec.packet_size
                        timeslot.num_high = timeslot.num_high + 1
                    elif rec.packet_qos == 'med':
                        timeslot.load_med = timeslot.load_med + rec.packet_size
                        timeslot.num_med = timeslot.num_med + 1
                    elif rec.packet_qos == 'low':
                        timeslot.load_low = timeslot.load_low + rec.packet_size
                        timeslot.num_low = timeslot.num_low + 1

                    if (_time_buffer1_in > -1) and (_time_buffer2_in > -1) and (_time_buffer3_in > -1):
                        timeslot.delay_total=timeslot.delay_total+_delay
                        timeslot.qdelay_total=timeslot.qdelay_total+_qdelay
                        timeslot.succ_total = timeslot.succ_total + 1

                        if rec.packet_qos == 'high':
                            timeslot.delay_high = timeslot.delay_high + _delay
                            timeslot.qdelay_high = timeslot.qdelay_high + _qdelay
                            timeslot.succ_high = timeslot.succ_high + 1
                        elif rec.packet_qos == 'med':
                            timeslot.delay_med = timeslot.delay_med + _delay
                            timeslot.qdelay_med = timeslot.qdelay_med + _qdelay
                            timeslot.succ_med = timeslot.succ_med + 1
                        elif rec.packet_qos == 'low':
                            timeslot.delay_low = timeslot.delay_low + _delay
                            timeslot.qdelay_low = timeslot.qdelay_low + _qdelay
                            timeslot.succ_low = timeslot.succ_low + 1
                        timeslot.delay_node[_source_id] = timeslot.delay_node[_source_id] + _delay
                        timeslot.qdelay_node[_source_id] = timeslot.qdelay_node[_source_id] + _qdelay
                        timeslot.succ_node[_source_id] = timeslot.succ_node[_source_id] + 1

                        if rec.is_intra():
                            timeslot.succ_intra_total=timeslot.succ_intra_total+1
                            timeslot.intra_delay_total=timeslot.intra_delay_total+_delay
                            if rec.packet_qos == 'high':
                                timeslot.succ_intra_high=timeslot.succ_intra_high+1
                                timeslot.intra_delay_high=timeslot.intra_delay_high+_delay
                            elif rec.packet_qos == 'med':
                                timeslot.succ_intra_med=timeslot.succ_intra_med+1
                                timeslot.intra_delay_med = timeslot.intra_delay_med + _delay
                            elif rec.packet_qos == 'low':
                                timeslot.succ_intra_low=timeslot.succ_intra_low+1
                                timeslot.intra_delay_low = timeslot.intra_delay_low + _delay
                        else:
                            timeslot.succ_inter_total=timeslot.succ_inter_total+1
                            timeslot.inter_delay_total = timeslot.inter_delay_total + _delay
                            if rec.packet_qos == 'high':
                                timeslot.succ_inter_high=timeslot.succ_inter_high+1
                                timeslot.inter_delay_high=timeslot.inter_delay_high+_delay
                            elif rec.packet_qos == 'med':
                                timeslot.succ_inter_med=timeslot.succ_inter_med+1
                                timeslot.inter_delay_med = timeslot.inter_delay_med + _delay
                            elif rec.packet_qos == 'low':
                                timeslot.succ_inter_low=timeslot.succ_inter_low+1
                                timeslot.inter_delay_low = timeslot.inter_delay_low + _delay
                    else:
                        timeslot.drop_total = timeslot.drop_total + (rec.packet_size)
                        if rec.packet_qos == 'high':
                            timeslot.drop_high = timeslot.drop_high + (rec.packet_size)
                        elif rec.packet_qos == 'med':
                            timeslot.drop_med = timeslot.drop_med + (rec.packet_size)
                        elif rec.packet_qos == 'low':
                            timeslot.drop_low = timeslot.drop_low + (rec.packet_size)
                        timeslot.drop_node[_source_id] = timeslot.drop_node[_source_id] + (rec.packet_size)

            for timeslot in self.db:
                if timeslot.t_begin <= _thru_out and _thru_out < timeslot.t_end:
                    timeslot.thru_total = timeslot.thru_total + (rec.packet_size)

                    if rec.packet_qos == 'high':
                        timeslot.thru_high = timeslot.thru_high + (rec.packet_size)
                    elif rec.packet_qos == 'med':
                        timeslot.thru_med = timeslot.thru_med + (rec.packet_size)
                    elif rec.packet_qos == 'low':
                        timeslot.thru_low = timeslot.thru_low + (rec.packet_size)
                    timeslot.thru_node[_source_id] = timeslot.thru_node[_source_id] + (rec.packet_size)

    def init_with_db_bridge_ul(self,record_db):
        print('Entered init with db bridge')
        debug_id=0

        for rec in record_db:
            #print('DBG: B=' + str(debug_id/len(record_db)))
            debug_id = debug_id + 1

            if not rec.is_intra(): # metraw apo tin wra pou to inter packet genietai ston server mexri na vgri apo to PON
                _source_id=rec.tor_id
                _time_load = rec.time
                _thru_out = rec.time_intra_trx_out
                _time_buffer1_in = rec.time_intra_buffer_in
                _time_buffer2_in = rec.time_intra_buffer_in
                _time_buffer3_in = rec.time_intra_buffer_in
                _qdelay=(rec.time_intra_buffer_out-rec.time_intra_buffer_in)
                _delay=rec.time_intra_trx_out-rec.time
                for timeslot in self.db:
                    if timeslot.t_begin <= _time_load and _time_load < timeslot.t_end:
                        timeslot.load_total=timeslot.load_total+rec.packet_size
                        timeslot.num_total = timeslot.num_total + 1
                        timeslot.load_node[_source_id]=timeslot.load_node[_source_id]+rec.packet_size
                        timeslot.num_node[_source_id]=timeslot.num_node[_source_id]+1

                        if rec.packet_qos=='high':
                            timeslot.load_high=timeslot.load_high+rec.packet_size
                            timeslot.num_high=timeslot.num_high+1
                        elif rec.packet_qos=='med':
                            timeslot.load_med=timeslot.load_med+rec.packet_size
                            timeslot.num_med = timeslot.num_med + 1
                        elif rec.packet_qos=='low':
                            timeslot.load_low=timeslot.load_low+rec.packet_size
                            timeslot.num_low = timeslot.num_low + 1

                        if _time_buffer1_in > -1 and _time_buffer2_in>-1:
                            timeslot.delay_total=timeslot.delay_total+_delay
                            timeslot.qdelay_total=timeslot.qdelay_total+_qdelay
                            timeslot.succ_total = timeslot.succ_total + 1

                            if rec.packet_qos == 'high':
                                timeslot.delay_high=timeslot.delay_high+ _delay
                                timeslot.qdelay_high=timeslot.qdelay_high+_qdelay
                                timeslot.succ_high=timeslot.succ_high+1
                            elif rec.packet_qos == 'med':
                                timeslot.delay_med=timeslot.delay_med+ _delay
                                timeslot.qdelay_med=timeslot.qdelay_med+_qdelay
                                timeslot.succ_med=timeslot.succ_med+1
                            elif rec.packet_qos == 'low':
                                timeslot.delay_low=timeslot.delay_low+ _delay
                                timeslot.qdelay_low=timeslot.qdelay_low+_qdelay
                                timeslot.succ_low=timeslot.succ_low+1
                            timeslot.delay_node[_source_id]=timeslot.delay_node[_source_id]+_delay
                            timeslot.qdelay_node[_source_id]=timeslot.qdelay_node[_source_id]+_qdelay
                            timeslot.succ_node[_source_id]=timeslot.succ_node[_source_id]+1
                        else:
                            timeslot.drop_total = timeslot.drop_total + (rec.packet_size)
                            if rec.packet_qos == 'high':
                                timeslot.drop_high = timeslot.drop_high + (rec.packet_size)
                            elif rec.packet_qos == 'med':
                                timeslot.drop_med = timeslot.drop_med + (rec.packet_size)
                            elif rec.packet_qos == 'low':
                                timeslot.drop_low = timeslot.drop_low + (rec.packet_size)
                            timeslot.drop_node[_source_id] = timeslot.drop_node[_source_id] + (rec.packet_size)

                for timeslot in self.db:
                    if timeslot.t_begin <= _thru_out and _thru_out < timeslot.t_end:
                        timeslot.thru_total = timeslot.thru_total + (rec.packet_size)

                        if rec.packet_qos == 'high':
                            timeslot.thru_high=timeslot.thru_high+(rec.packet_size)
                        elif rec.packet_qos == 'med':
                            timeslot.thru_med=timeslot.thru_med+(rec.packet_size)
                        elif rec.packet_qos == 'low':
                            timeslot.thru_low=timeslot.thru_low+(rec.packet_size)
                        timeslot.thru_node[_source_id] = timeslot.thru_node[_source_id] + (rec.packet_size)

    def init_with_db_bridge_dl(self,record_db):
        print('Entered init with db bridge')
        debug_id=0

        for rec in record_db:
            #print('DBG: B=' + str(debug_id/len(record_db)))
            debug_id = debug_id + 1

            if not rec.is_intra(): # metraw apo tin wra pou arrive apto source Tor (or drop) mexri pou pianei server
                _source_id=rec.tor_id
                _time_load = rec.time_tor_trx_out
                _thru_out = rec.time_inter_trx_out
                _time_buffer1_in = rec.time_inter_buffer_in
                _time_buffer2_in = rec.time_inter_buffer_in
                _time_buffer3_in = rec.time_inter_buffer_in
                _qdelay=(rec.time_inter_buffer_out-rec.time_inter_buffer_in)
                _delay=rec.time_inter_trx_out-rec.time_tor_trx_out
                for timeslot in self.db:
                    if timeslot.t_begin <= _time_load and _time_load < timeslot.t_end:
                        timeslot.load_total=timeslot.load_total+rec.packet_size
                        timeslot.num_total = timeslot.num_total + 1
                        timeslot.load_node[_source_id]=timeslot.load_node[_source_id]+rec.packet_size
                        timeslot.num_node[_source_id]=timeslot.num_node[_source_id]+1

                        if rec.packet_qos=='high':
                            timeslot.load_high=timeslot.load_high+rec.packet_size
                            timeslot.num_high=timeslot.num_high+1
                        elif rec.packet_qos=='med':
                            timeslot.load_med=timeslot.load_med+rec.packet_size
                            timeslot.num_med = timeslot.num_med + 1
                        elif rec.packet_qos=='low':
                            timeslot.load_low=timeslot.load_low+rec.packet_size
                            timeslot.num_low = timeslot.num_low + 1

                        if _time_buffer1_in > -1 and _time_buffer2_in>-1:
                            timeslot.delay_total=timeslot.delay_total+_delay
                            timeslot.qdelay_total=timeslot.qdelay_total+_qdelay
                            timeslot.succ_total = timeslot.succ_total + 1

                            if rec.packet_qos == 'high':
                                timeslot.delay_high=timeslot.delay_high+ _delay
                                timeslot.qdelay_high=timeslot.qdelay_high+_qdelay
                                timeslot.succ_high=timeslot.succ_high+1
                            elif rec.packet_qos == 'med':
                                timeslot.delay_med=timeslot.delay_med+ _delay
                                timeslot.qdelay_med=timeslot.qdelay_med+_qdelay
                                timeslot.succ_med=timeslot.succ_med+1
                            elif rec.packet_qos == 'low':
                                timeslot.delay_low=timeslot.delay_low+ _delay
                                timeslot.qdelay_low=timeslot.qdelay_low+_qdelay
                                timeslot.succ_low=timeslot.succ_low+1
                            timeslot.delay_node[_source_id]=timeslot.delay_node[_source_id]+_delay
                            timeslot.qdelay_node[_source_id]=timeslot.qdelay_node[_source_id]+_qdelay
                            timeslot.succ_node[_source_id]=timeslot.succ_node[_source_id]+1
                        else:
                            timeslot.drop_total = timeslot.drop_total + (rec.packet_size)
                            if rec.packet_qos == 'high':
                                timeslot.drop_high = timeslot.drop_high + (rec.packet_size)
                            elif rec.packet_qos == 'med':
                                timeslot.drop_med = timeslot.drop_med + (rec.packet_size)
                            elif rec.packet_qos == 'low':
                                timeslot.drop_low = timeslot.drop_low + (rec.packet_size)
                            timeslot.drop_node[_source_id] = timeslot.drop_node[_source_id] + (rec.packet_size)

                for timeslot in self.db:
                    if timeslot.t_begin <= _thru_out and _thru_out < timeslot.t_end:
                        timeslot.thru_total = timeslot.thru_total + (rec.packet_size)

                        if rec.packet_qos == 'high':
                            timeslot.thru_high=timeslot.thru_high+(rec.packet_size)
                        elif rec.packet_qos == 'med':
                            timeslot.thru_med=timeslot.thru_med+(rec.packet_size)
                        elif rec.packet_qos == 'low':
                            timeslot.thru_low=timeslot.thru_low+(rec.packet_size)
                        timeslot.thru_node[_source_id] = timeslot.thru_node[_source_id] + (rec.packet_size)

    def get_list_load_total(self):
        mylist=[]
        for element in self.db:
            mylist.append(element.get_agg_load_total())
        return mylist

    def get_list_thru_total(self):
        mylist=[]
        for element in self.db:
            mylist.append(element.get_agg_thru_total())
        return mylist

    def get_list_drop_total(self):
        mylist=[]
        for element in self.db:
            mylist.append(element.get_agg_drop_total())
        return mylist
class My_Timeslot():
    def __init__(self,tbegin,tend):
        self.t_begin=tbegin
        self.t_end=tend

        self.num_total=0
        self.num_high = 0
        self.num_med = 0
        self.num_low = 0
        self.num_node = []

        self.succ_total=0
        self.succ_high = 0
        self.succ_med = 0
        self.succ_low = 0
        self.succ_intra_total=0
        self.succ_intra_high=0
        self.succ_intra_med=0
        self.succ_intra_low=0
        self.succ_inter_total=0
        self.succ_inter_high = 0
        self.succ_inter_med = 0
        self.succ_inter_low = 0
        self.succ_node = []

        self.load_total=0
        self.load_high=0
        self.load_med= 0
        self.load_low = 0
        self.load_node=[]

        self.delay_total=0
        self.delay_high=0
        self.delay_med= 0
        self.delay_low = 0
        self.delay_node=[]

        self.drop_total=0
        self.drop_high=0
        self.drop_med= 0
        self.drop_low = 0
        self.drop_node=[]

        self.thru_total=0
        self.thru_high=0
        self.thru_med=0
        self.thru_low=0
        self.thru_node=[]

        self.qdelay_total=0
        self.qdelay_high=0
        self.qdelay_med=0
        self.qdelay_low=0
        self.qdelay_node=[]

        self.intra_delay_total=0
        self.intra_delay_high=0
        self.intra_delay_med=0
        self.intra_delay_low=0

        self.inter_delay_total=0
        self.inter_delay_high=0
        self.inter_delay_med=0
        self.inter_delay_low=0

        for i in range(0,100):
            self.num_node.append(0)
            self.succ_node.append(0)
            self.load_node.append(0)
            self.thru_node.append(0)
            self.drop_node.append(0)
            self.delay_node.append(0)
            self.qdelay_node.append(0)


    def get_agg_load_total(self):
        return self.load_total
    def get_agg_load_high(self):
        return self.load_high
    def get_agg_load_med(self):
        return self.load_med
    def get_agg_load_low(self):
        return self.load_low
    def get_agg_load_node(self,node):
        return self.load_node[node]

    def get_agg_thru_total(self):
        return self.thru_total
    def get_agg_thru_high(self):
        return self.thru_high
    def get_agg_thru_med(self):
        return self.thru_med
    def get_agg_thru_low(self):
        return self.thru_low
    def get_agg_thru_node(self,node):
        return self.thru_node[node]

    def get_agg_drop_total(self):
        return self.drop_total
    def get_agg_drop_high(self):
        return self.drop_high
    def get_agg_drop_med(self):
        return self.drop_med
    def get_agg_drop_low(self):
        return self.drop_low
    def get_agg_drop_node(self,node):
        return self.drop_node[node]

    def get_avg_delay_total(self):
        try:
            return self.delay_total/self.succ_total
        except:
            return None
    def get_avg_delay_high(self):
        try:
            return self.delay_high/self.succ_high
        except:
            return None
    def get_avg_delay_med(self):
        try:
            return self.delay_med/self.succ_med
        except:
            return None
    def get_avg_delay_low(self):
        try:
            return self.delay_low/self.succ_low
        except:
            return None
    def get_avg_delay_node(self,node):
        try:
            return self.delay_node[node]/self.succ_node[node]
        except:
            return None

    def get_avg_qdelay_total(self):
        try:
            return self.qdelay_total/self.succ_total
        except:
            return None
    def get_avg_qdelay_high(self):
        try:
            return self.qdelay_high/self.succ_high
        except:
            return None
    def get_avg_qdelay_med(self):
        try:
            return self.qdelay_med/self.succ_med
        except:
            return None
    def get_avg_qdelay_low(self):
        try:
            return self.qdelay_low/self.succ_low
        except:
            return None
    def get_avg_qdelay_node(self,node):
        try:
            return self.qdelay_node[node]/self.succ_node[node]
        except:
            return None

    def get_inter_delay_total(self):
        try:
            return self.inter_delay_total/self.succ_inter_total
        except:
            return None
    def get_inter_delay_high(self):
        try:
            return self.inter_delay_high/self.succ_inter_high
        except:
            return None
    def get_inter_delay_med(self):
        try:
            return self.inter_delay_med/self.succ_inter_med
        except:
            return None
    def get_inter_delay_low(self):
        try:
            return self.inter_delay_low/self.succ_inter_low
        except:
            return None
    def get_intra_delay_total(self):
        try:
            return self.intra_delay_total/self.succ_intra_total
        except:
            return None
    def get_intra_delay_high(self):
        try:
            return self.intra_delay_high/self.succ_intra_high
        except:
            return None
    def get_intra_delay_med(self):
        try:
            return self.intra_delay_med/self.succ_intra_med
        except:
            return None
    def get_intra_delay_low(self):
        try:
            return self.intra_delay_low/self.succ_intra_low
        except:
            return None

if measurement_type=='pre':
    print('Preprocessing dataset folder='+str(myglobal.CURR_TRAFFIC_DATASET_FOLDER))
    my_db=[]
    for tor_id in range(1,tors+1):
        for server_id in range(1,servers+1):
            mystr='tor'+str(tor_id)+'node'+str(server_id)+'.csv'
            filename=os.path.join(myglobal.ROOT,myglobal.CURR_TRAFFIC_DATASET_FOLDER)
            filename = os.path.join(filename,mystr)
            with open(filename) as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                    new_rec=Record(row['packet_id'],row['time'],row['packet_size'],row['packet_qos'],
                                   row['source_id'], row['tor_id'], row['destination_id'], row['destination_tor'],
                                    -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1)
                    my_db.append(new_rec)
elif measurement_type=='post':
    print('Post-processing log folder=' + str(filename))
    my_db=[]
    myname = os.path.join(myglobal.LOGS_FOLDER, filename)
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

timeslot_list=My_Timeslot_List(my_tbegin,my_tend,my_samples)
if mode=='intra':
    timeslot_list.init_with_db_intra(my_db,split=split)
elif mode=='inter':
    timeslot_list.init_with_db_inter(my_db)
elif mode=='end2end':
    timeslot_list.init_with_db_end2end(my_db)
elif mode=='bridge_ul':
    timeslot_list.init_with_db_bridge_ul(my_db)
elif mode=='bridge_dl':
    timeslot_list.init_with_db_bridge_dl(my_db)

if not avgg:
    LOAD=timeslot_list.get_list_load_total()
    THRU=timeslot_list.get_list_thru_total()
    DROP=timeslot_list.get_list_drop_total()
    print(str(LOAD))
    print(str(THRU))
    print(str(DROP))
    plt.plot(LOAD,THRU,'o', label = "thru")
    plt.plot(LOAD, DROP,'o', label = "drop")
    plt.xlabel('Load (bytes per sec)', fontsize=25)
    plt.ylabel('Bits per sec', fontsize=25)
    plt.grid(True, which='major', axis='both')
    plt.title('Here is the title', fontsize=25)
    plt.legend()
    plt.show()
else: #Group stage
    group_list = My_Group_List(my_tbegin, my_tend, my_samples, start_group_value, end_group_value, grouping_points)
    print('Start1')
    group_list.assign_timeslots_to_groups(timeslot_list)
    print('Start2')
    avg, err = group_list.get_groups_load_total_bps()
    prLOAD_BIT = avg
    print('waa_load_total_bps' + '_avg=' + str(avg))
    print('waa_load_total_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_load_high_bps()
    print('waa_load_high_bps' + '_avg=' + str(avg))
    print('waa_load_high_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_load_med_bps()
    print('waa_load_med_bps' + '_avg=' + str(avg))
    print('waa_load_med_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_load_low_bps()
    print('waa_load_low_bps' + '_avg=' + str(avg))
    print('waa_load_low_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_total_bps()
    prTHRU_BIT = avg
    print('waa_thru_total_bps' + '_avg=' + str(avg))
    print('waa_thru_total_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_high_bps()
    print('waa_thru_high_bps' + '_avg=' + str(avg))
    print('waa_thru_high_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_med_bps()
    print('waa_thru_med_bps' + '_avg=' + str(avg))
    print('waa_thru_med_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_low_bps()
    print('waa_thru_low_bps' + '_avg=' + str(avg))
    print('waa_thru_low_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_total_bps()
    prDROP_BIT = avg
    print('waa_drop_total_bps' + '_avg=' + str(avg))
    print('waa_drop_total_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_high_bps()
    print('waa_drop_high_bps' + '_avg=' + str(avg))
    print('waa_drop_high_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_med_bps()
    print('waa_drop_med_bps' + '_avg=' + str(avg))
    print('waa_drop_med_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_low_bps()
    print('waa_drop_low_bps' + '_avg=' + str(avg))
    print('waa_drop_low_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_prob_total()
    print('waa_drop_prob_total' + '_avg=' + str(avg))
    print('waa_drop_prob_total' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_prob_high()
    print('waa_drop_prob_high' + '_avg=' + str(avg))
    print('waa_drop_prob_high' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_prob_med()
    print('waa_drop_prob_med' + '_avg=' + str(avg))
    print('waa_drop_prob_med' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_prob_low()
    print('waa_drop_prob_low' + '_avg=' + str(avg))
    print('waa_drop_prob_low' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_total()
    print('waa_delay_total' + '_avg=' + str(avg))
    print('waa_delay_total' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_high()
    print('waa_delay_high' + '_avg=' + str(avg))
    print('waa_delay_high' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_med()
    print('waa_delay_med' + '_avg=' + str(avg))
    print('waa_delay_med' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_low()
    print('waa_delay_low' + '_avg=' + str(avg))
    print('waa_delay_low' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_total()
    print('waa_qdelay_total' + '_avg=' + str(avg))
    print('waa_qdelay_total' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_high()
    print('waa_qdelay_high' + '_avg=' + str(avg))
    print('waa_qdelay_high' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_med()
    print('waa_qdelay_med' + '_avg=' + str(avg))
    print('waa_qdelay_med' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_low()
    print('waa_qdelay_low' + '_avg=' + str(avg))
    print('waa_qdelay_low' + '_err=' + str(err))
    avg, err = group_list.get_groups_inter_delay_total()
    print('waa_inter_delay_total' + '_avg=' + str(avg))
    print('waa_inter_delay_total' + '_err=' + str(err))
    avg, err = group_list.get_groups_inter_delay_high()
    print('waa_inter_delay_high' + '_avg=' + str(avg))
    print('waa_inter_delay_high' + '_err=' + str(err))
    avg, err = group_list.get_groups_inter_delay_med()
    print('waa_inter_delay_med' + '_avg=' + str(avg))
    print('waa_inter_delay_med' + '_err=' + str(err))
    avg, err = group_list.get_groups_inter_delay_low()
    print('waa_inter_delay_low' + '_avg=' + str(avg))
    print('waa_inter_delay_low' + '_err=' + str(err))
    avg, err = group_list.get_groups_intra_delay_total()
    print('waa_intra_delay_total' + '_avg=' + str(avg))
    print('waa_intra_delay_total' + '_err=' + str(err))
    avg, err = group_list.get_groups_intra_delay_high()
    print('waa_intra_delay_high' + '_avg=' + str(avg))
    print('waa_intra_delay_high' + '_err=' + str(err))
    avg, err = group_list.get_groups_intra_delay_med()
    print('waa_intra_delay_med' + '_avg=' + str(avg))
    print('waa_intra_delay_med' + '_err=' + str(err))
    avg, err = group_list.get_groups_intra_delay_low()
    print('waa_intra_delay_low' + '_avg=' + str(avg))
    print('waa_intra_delay_low' + '_err=' + str(err))

    if mode=='intra':
        main_elements=servers
    else:
        main_elements = tors

    for node in range(1,main_elements+1):
        avg, err = group_list.get_groups_load_node_bps(node)
        print('waa_load_node_bps_'+str(node) + '_avg=' + str(avg))
        print('waa_load_node_bps_'+str(node) + '_err=' + str(err))
        avg, err = group_list.get_groups_thru_node_bps(node)
        print('waa_thru_node_bps_'+str(node) + '_avg=' + str(avg))
        print('waa_thru_node_bps_'+str(node) + '_err=' + str(err))
        avg, err = group_list.get_groups_drop_node_bps(node)
        print('waa_drop_node_bps_'+str(node) + '_avg=' + str(avg))
        print('waa_drop_node_bps_'+str(node) + '_err=' + str(err))
        avg, err = group_list.get_groups_delay_node(node)
        print('waa_delay_node_'+str(node) + '_avg=' + str(avg))
        print('waa_delay_node_'+str(node) + '_err=' + str(err))
        avg, err = group_list.get_groups_qdelay_node(node)
        print('waa_qdelay_node_'+str(node) + '_avg=' + str(avg))
        print('waa_qdelay_node_'+str(node) + '_err=' + str(err))

    plt.plot(prLOAD_BIT, prTHRU_BIT, label="thruput bitrate")
    plt.plot(prLOAD_BIT, prDROP_BIT, label="drop bitrate")
    plt.xlabel('Load (bps)', fontsize=25)
    plt.ylabel('Probability', fontsize=25)
    plt.grid(True, which='major', axis='both')
    plt.title('Both Waiting and Prop Delay', fontsize=25)
    plt.legend()
    plt.show()
