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
avgg=True
filename= 'test.csv'
my_tbegin=0
my_tend=0.001
my_samples=100 # 500
# Grouping params
start_group_value=0
end_group_value=300000
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
    def get_stats_load_node1_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node1())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node1_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node1())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node1_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node1())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node1(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node1()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node1()/tslot.get_agg_load_node1())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node1(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node1()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node1(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node1()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)
    def get_stats_load_node2_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node2())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node2_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node2())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node2_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node2())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node2(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node2()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node2()/tslot.get_agg_load_node2())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node2(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node2()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node2(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node2()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)
    def get_stats_load_node3_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node3())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node3_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node3())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node3_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node3())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node3(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node3()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node3()/tslot.get_agg_load_node3())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node3(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node3()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node3(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node3()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)
    def get_stats_load_node4_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node4())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node4_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node4())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node4_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node4())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node4(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node4()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node4()/tslot.get_agg_load_node4())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node4(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node4()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node4(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node4()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)
    def get_stats_load_node5_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node5())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node5_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node5())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node5_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node5())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node5(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node5()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node5()/tslot.get_agg_load_node5())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node5(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node5()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node5(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node5()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)
    def get_stats_load_node6_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node6())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node6_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node6())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node6_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node6())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node6(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node6()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node6()/tslot.get_agg_load_node6())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node6(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node6()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node6(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node6()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)
    def get_stats_load_node7_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node7())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node7_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node7())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node7_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node7())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node7(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node7()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node7()/tslot.get_agg_load_node7())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node7(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node7()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node7(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node7()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)
    def get_stats_load_node8_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node8())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node8_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node8())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node8_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node8())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node8(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node8()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node8()/tslot.get_agg_load_node8())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node8(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node8()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node8(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node8()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)
    def get_stats_load_node9_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node9())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node9_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node9())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node9_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node9())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node9(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node9()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node9()/tslot.get_agg_load_node9())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node9(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node9()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node9(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node9()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)
    def get_stats_load_node10_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node10())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node10_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node10())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node10_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node10())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node10(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node10()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node10()/tslot.get_agg_load_node10())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node10(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node10()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node10(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node10()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)
    def get_stats_load_node11_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node11())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node11_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node11())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node11_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node11())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node11(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node11()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node11()/tslot.get_agg_load_node11())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node11(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node11()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node11(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node11()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)

    def get_stats_load_node12_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node12())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node12_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node12())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node12_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node12())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node12(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node12()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node12()/tslot.get_agg_load_node12())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node12(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node12()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node12(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node12()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)

    def get_stats_load_node13_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node13())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node13_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node13())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node13_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node13())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node13(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node13()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node13()/tslot.get_agg_load_node13())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node13(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node13()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node13(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node13()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)

    def get_stats_load_node14_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node14())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node14_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node14())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node14_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node14())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node14(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node14()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node14()/tslot.get_agg_load_node14())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node14(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node14()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node14(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node14()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)

    def get_stats_load_node15_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node15())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node15_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node15())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node15_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node15())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node15(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node15()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node15()/tslot.get_agg_load_node15())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node15(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node15()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node15(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node15()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)

    def get_stats_load_node16_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_node16())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)
    def get_stats_thru_node16_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_node16())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_node16_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_node16())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)
    def get_stats_drop_prob_node16(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_node16()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_node16()/tslot.get_agg_load_node16())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_delay_node16(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_node16()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)
    def get_stats_qdelay_node16(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_node16()
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
        print('(debug): Nominal Rates'+str(self.nominal_rates))
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

    def get_groups_load_node1_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node1_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_node1_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node1_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_node1_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node1_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_node1(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node1()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_node1(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node1()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_node1(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node1()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_load_node2_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node2_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_node2_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node2_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_node2_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node2_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_node2(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node2()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_node2(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node2()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_node2(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node2()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_load_node3_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node3_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_node3_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node3_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_node3_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node3_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_node3(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node3()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_node3(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node3()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_node3(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node3()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_load_node4_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node4_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_node4_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node4_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_node4_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node4_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_node4(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node4()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_node4(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node4()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_node4(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node4()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_load_node5_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node5_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_node5_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node5_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_node5_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node5_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_node5(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node5()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_node5(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node5()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_node5(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node5()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_load_node6_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node6_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_node6_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node6_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_node6_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node6_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_node6(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node6()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_node6(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node6()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_node6(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node6()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_load_node7_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node7_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_node7_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node7_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_node7_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node7_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_node7(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node7()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_node7(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node7()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_node7(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node7()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_load_node8_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node8_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_node8_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node8_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_node8_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node8_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_node8(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node8()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_node8(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node8()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_node8(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node8()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_load_node9_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node9_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_node9_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node9_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_node9_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node9_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_node9(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node9()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_node9(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node9()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_node9(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node9()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_load_node10_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node10_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_node10_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node10_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_node10_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node10_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_node10(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node10()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_node10(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node10()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_node10(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node10()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_load_node11_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node11_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_node11_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node11_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_node11_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node11_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_node11(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node11()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_node11(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node11()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_node11(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node11()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_load_node12_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node12_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_thru_node12_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node12_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_drop_node12_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node12_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_drop_prob_node12(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node12()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_delay_node12(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node12()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_qdelay_node12(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node12()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list


    def get_groups_load_node13_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node13_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_thru_node13_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node13_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_drop_node13_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node13_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_drop_prob_node13(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node13()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_delay_node13(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node13()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_qdelay_node13(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node13()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_load_node14_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node14_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_thru_node14_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node14_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_drop_node14_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node14_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_drop_prob_node14(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node14()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_delay_node14(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node14()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_qdelay_node14(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node14()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_load_node15_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node15_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_thru_node15_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node15_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_drop_node15_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node15_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_drop_prob_node15(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node15()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_delay_node15(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node15()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_qdelay_node15(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node15()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_load_node16_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_load_node16_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_thru_node16_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_node16_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_drop_node16_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_node16_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_drop_prob_node16(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_node16()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_delay_node16(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_node16()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list
    def get_groups_qdelay_node16(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_node16()
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

    def init_with_db(self,record_db):
        print('Entered init with db')
        debug_id=0
        for rec in record_db:
            print('B=' + str(debug_id))
            debug_id = debug_id + 1
            for timeslot in self.db:
                if timeslot.t_begin <= rec.time and rec.time <= timeslot.t_end:
                    timeslot.load_total.append(rec.packet_size)

                    if rec.source_id==1:
                        timeslot.load_node1.append(rec.packet_size)
                    elif rec.source_id==2:
                        timeslot.load_node2.append(rec.packet_size)
                    elif rec.source_id==3:
                        timeslot.load_node3.append(rec.packet_size)
                    elif rec.source_id==4:
                        timeslot.load_node4.append(rec.packet_size)
                    elif rec.source_id==5:
                        timeslot.load_node5.append(rec.packet_size)
                    elif rec.source_id==6:
                        timeslot.load_node6.append(rec.packet_size)
                    elif rec.source_id==7:
                        timeslot.load_node7.append(rec.packet_size)
                    elif rec.source_id==8:
                        timeslot.load_node8.append(rec.packet_size)
                    elif rec.source_id==9:
                        timeslot.load_node9.append(rec.packet_size)
                    elif rec.source_id==10:
                        timeslot.load_node10.append(rec.packet_size)
                    elif rec.source_id==11:
                        timeslot.load_node11.append(rec.packet_size)
                    elif rec.source_id==12:
                        timeslot.load_node12.append(rec.packet_size)
                    elif rec.source_id==13:
                        timeslot.load_node13.append(rec.packet_size)
                    elif rec.source_id==14:
                        timeslot.load_node14.append(rec.packet_size)
                    elif rec.source_id==15:
                        timeslot.load_node15.append(rec.packet_size)
                    elif rec.source_id==16:
                        timeslot.load_node16.append(rec.packet_size)
                    else:
                        print('cannot find source for sourceid='+str(rec.source_id))

                    if rec.packet_qos=='high':
                        timeslot.load_high.append(rec.packet_size)
                    elif rec.packet_qos=='med':
                        timeslot.load_med.append(rec.packet_size)
                    elif rec.packet_qos=='low':
                        timeslot.load_low.append(rec.packet_size)

                    if rec.time_intra_buffer_in > -1:
                        timeslot.delay_total.append(rec.time_intra_trx_out - rec.time)
                        timeslot.qdelay_total.append(rec.time_intra_trx_in - rec.time)
                        if rec.packet_qos == 'high':
                            timeslot.delay_high.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_high.append(rec.time_intra_trx_in - rec.time)
                        elif rec.packet_qos == 'med':
                            timeslot.delay_med.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_med.append(rec.time_intra_trx_in - rec.time)
                        elif rec.packet_qos == 'low':
                            timeslot.delay_low.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_low.append(rec.time_intra_trx_in - rec.time)
                        if rec.source_id == 1:
                            timeslot.delay_node1.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node1.append(rec.time_intra_trx_in - rec.time)
                        elif rec.source_id == 2:
                            timeslot.delay_node2.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node2.append(rec.time_intra_trx_in - rec.time)
                        elif rec.source_id == 3:
                            timeslot.delay_node3.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node3.append(rec.time_intra_trx_in - rec.time)
                        elif rec.source_id == 4:
                            timeslot.delay_node4.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node4.append(rec.time_intra_trx_in - rec.time)
                        elif rec.source_id == 5:
                            timeslot.delay_node5.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node5.append(rec.time_intra_trx_in - rec.time)
                        elif rec.source_id == 6:
                            timeslot.delay_node6.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node6.append(rec.time_intra_trx_in - rec.time)
                        elif rec.source_id == 7:
                            timeslot.delay_node7.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node7.append(rec.time_intra_trx_in - rec.time)
                        elif rec.source_id == 8:
                            timeslot.delay_node8.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node8.append(rec.time_intra_trx_in - rec.time)
                        elif rec.source_id == 9:
                            timeslot.delay_node9.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node9.append(rec.time_intra_trx_in - rec.time)
                        elif rec.source_id == 10:
                            timeslot.delay_node10.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node10.append(rec.time_intra_trx_in - rec.time)
                        elif rec.source_id == 11:
                            timeslot.delay_node11.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node11.append(rec.time_intra_trx_in - rec.time)
                        elif rec.source_id == 12:
                            timeslot.delay_node12.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node12.append(rec.time_intra_trx_in - rec.time)
                        elif rec.source_id == 13:
                            timeslot.delay_node13.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node13.append(rec.time_intra_trx_in - rec.time)
                        elif rec.source_id == 14:
                            timeslot.delay_node14.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node14.append(rec.time_intra_trx_in - rec.time)
                        elif rec.source_id == 15:
                            timeslot.delay_node15.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node15.append(rec.time_intra_trx_in - rec.time)
                        elif rec.source_id == 16:
                            timeslot.delay_node16.append(rec.time_intra_trx_out - rec.time)
                            timeslot.qdelay_node16.append(rec.time_intra_trx_in - rec.time)
                        else:
                            print('cannot find source for sourceid=' + str(rec.source_id))
                    else:
                        timeslot.drop_total.append(rec.packet_size)
                        if rec.packet_qos == 'high':
                            timeslot.drop_high.append(rec.packet_size)
                        elif rec.packet_qos == 'med':
                            timeslot.drop_med.append(rec.packet_size)
                        elif rec.packet_qos == 'low':
                            timeslot.drop_low.append(rec.packet_size)
                        if rec.source_id == 1:
                            timeslot.drop_node1.append(rec.packet_size)
                        elif rec.source_id == 2:
                            timeslot.drop_node2.append(rec.packet_size)
                        elif rec.source_id == 3:
                            timeslot.drop_node3.append(rec.packet_size)
                        elif rec.source_id == 4:
                            timeslot.drop_node4.append(rec.packet_size)
                        elif rec.source_id == 5:
                            timeslot.drop_node5.append(rec.packet_size)
                        elif rec.source_id == 6:
                            timeslot.drop_node6.append(rec.packet_size)
                        elif rec.source_id == 7:
                            timeslot.drop_node7.append(rec.packet_size)
                        elif rec.source_id == 8:
                            timeslot.drop_node8.append(rec.packet_size)
                        elif rec.source_id == 9:
                            timeslot.drop_node9.append(rec.packet_size)
                        elif rec.source_id == 10:
                            timeslot.drop_node10.append(rec.packet_size)
                        elif rec.source_id == 11:
                            timeslot.drop_node11.append(rec.packet_size)
                        elif rec.source_id == 12:
                            timeslot.drop_node12.append(rec.packet_size)
                        elif rec.source_id == 13:
                            timeslot.drop_node13.append(rec.packet_size)
                        elif rec.source_id == 14:
                            timeslot.drop_node14.append(rec.packet_size)
                        elif rec.source_id == 15:
                            timeslot.drop_node15.append(rec.packet_size)
                        elif rec.source_id == 16:
                            timeslot.drop_node16.append(rec.packet_size)
                        else:
                            print('cannot find source for sourceid=' + str(rec.source_id))

            for timeslot in self.db:
                if timeslot.t_begin <= rec.time_intra_trx_out and rec.time_intra_trx_out <= timeslot.t_end:
                    timeslot.thru_total.append(rec.packet_size)
                    if rec.packet_qos == 'high':
                        timeslot.thru_high.append(rec.packet_size)
                    elif rec.packet_qos == 'med':
                        timeslot.thru_med.append(rec.packet_size)
                    elif rec.packet_qos == 'low':
                        timeslot.thru_low.append(rec.packet_size)
                    if rec.source_id==1:
                        timeslot.thru_node1.append(rec.packet_size)
                    elif rec.source_id==2:
                        timeslot.thru_node2.append(rec.packet_size)
                    elif rec.source_id==3:
                        timeslot.thru_node3.append(rec.packet_size)
                    elif rec.source_id==4:
                        timeslot.thru_node4.append(rec.packet_size)
                    elif rec.source_id==5:
                        timeslot.thru_node5.append(rec.packet_size)
                    elif rec.source_id==6:
                        timeslot.thru_node6.append(rec.packet_size)
                    elif rec.source_id==7:
                        timeslot.thru_node7.append(rec.packet_size)
                    elif rec.source_id==8:
                        timeslot.thru_node8.append(rec.packet_size)
                    elif rec.source_id==9:
                        timeslot.thru_node9.append(rec.packet_size)
                    elif rec.source_id==10:
                        timeslot.thru_node10.append(rec.packet_size)
                    elif rec.source_id==11:
                        timeslot.thru_node11.append(rec.packet_size)
                    elif rec.source_id==12:
                        timeslot.thru_node12.append(rec.packet_size)
                    elif rec.source_id==13:
                        timeslot.thru_node13.append(rec.packet_size)
                    elif rec.source_id==14:
                        timeslot.thru_node14.append(rec.packet_size)
                    elif rec.source_id==15:
                        timeslot.thru_node15.append(rec.packet_size)
                    elif rec.source_id==16:
                        timeslot.thru_node16.append(rec.packet_size)
                    else:
                        print('cannot find source for sourceid='+str(rec.source_id))


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
        self.load_total=[]
        self.load_high=[]
        self.load_med= []
        self.load_low = []
        self.load_node1=[]
        self.load_node2=[]
        self.load_node3=[]
        self.load_node4=[]
        self.load_node5=[]
        self.load_node6=[]
        self.load_node7=[]
        self.load_node8=[]
        self.load_node9=[]
        self.load_node10=[]
        self.load_node11=[]
        self.load_node12=[]
        self.load_node13=[]
        self.load_node14=[]
        self.load_node15=[]
        self.load_node16=[]
        self.delay_total=[]
        self.delay_high=[]
        self.delay_med= []
        self.delay_low = []
        self.delay_node1=[]
        self.delay_node2=[]
        self.delay_node3=[]
        self.delay_node4=[]
        self.delay_node5=[]
        self.delay_node6=[]
        self.delay_node7=[]
        self.delay_node8=[]
        self.delay_node9=[]
        self.delay_node10=[]
        self.delay_node11=[]
        self.delay_node12=[]
        self.delay_node13=[]
        self.delay_node14=[]
        self.delay_node15=[]
        self.delay_node16=[]
        self.drop_total=[]
        self.drop_high=[]
        self.drop_med= []
        self.drop_low = []
        self.drop_node1=[]
        self.drop_node2=[]
        self.drop_node3=[]
        self.drop_node4=[]
        self.drop_node5=[]
        self.drop_node6=[]
        self.drop_node7=[]
        self.drop_node8=[]
        self.drop_node9=[]
        self.drop_node10=[]
        self.drop_node11=[]
        self.drop_node12=[]
        self.drop_node13=[]
        self.drop_node14=[]
        self.drop_node15=[]
        self.drop_node16=[]
        self.thru_total=[]
        self.thru_high=[]
        self.thru_med=[]
        self.thru_low=[]
        self.thru_node1=[]
        self.thru_node2=[]
        self.thru_node3=[]
        self.thru_node4=[]
        self.thru_node5=[]
        self.thru_node6=[]
        self.thru_node7=[]
        self.thru_node8=[]
        self.thru_node9=[]
        self.thru_node10=[]
        self.thru_node11=[]
        self.thru_node12=[]
        self.thru_node13=[]
        self.thru_node14=[]
        self.thru_node15=[]
        self.thru_node16=[]
        self.qdelay_total=[]
        self.qdelay_high=[]
        self.qdelay_med=[]
        self.qdelay_low=[]
        self.qdelay_node1=[]
        self.qdelay_node2=[]
        self.qdelay_node3=[]
        self.qdelay_node4=[]
        self.qdelay_node5=[]
        self.qdelay_node6=[]
        self.qdelay_node7=[]
        self.qdelay_node8=[]
        self.qdelay_node9=[]
        self.qdelay_node10=[]
        self.qdelay_node11=[]
        self.qdelay_node12=[]
        self.qdelay_node13=[]
        self.qdelay_node14=[]
        self.qdelay_node15=[]
        self.qdelay_node16=[]

    def get_agg_load_total(self):
        mytotal=0
        for el in self.load_total:
            mytotal=mytotal+el
        return mytotal

    def get_agg_load_high(self):
        mytotal=0
        for el in self.load_high:
            mytotal=mytotal+el
        return mytotal

    def get_agg_load_med(self):
        mytotal=0
        for el in self.load_med:
            mytotal=mytotal+el
        return mytotal

    def get_agg_load_low(self):
        mytotal=0
        for el in self.load_low:
            mytotal=mytotal+el
        return mytotal

    def get_agg_load_node1(self):
        mytotal=0
        for el in self.load_node1:
            mytotal=mytotal+el
        return mytotal

    def get_agg_load_node2(self):
        mytotal=0
        for el in self.load_node2:
            mytotal=mytotal+el
        return mytotal
    def get_agg_load_node3(self):
        mytotal=0
        for el in self.load_node3:
            mytotal=mytotal+el
        return mytotal
    def get_agg_load_node4(self):
        mytotal=0
        for el in self.load_node4:
            mytotal=mytotal+el
        return mytotal
    def get_agg_load_node5(self):
        mytotal=0
        for el in self.load_node5:
            mytotal=mytotal+el
        return mytotal
    def get_agg_load_node6(self):
        mytotal=0
        for el in self.load_node6:
            mytotal=mytotal+el
        return mytotal
    def get_agg_load_node7(self):
        mytotal=0
        for el in self.load_node7:
            mytotal=mytotal+el
        return mytotal
    def get_agg_load_node8(self):
        mytotal=0
        for el in self.load_node8:
            mytotal=mytotal+el
        return mytotal
    def get_agg_load_node9(self):
        mytotal=0
        for el in self.load_node9:
            mytotal=mytotal+el
        return mytotal
    def get_agg_load_node10(self):
        mytotal=0
        for el in self.load_node10:
            mytotal=mytotal+el
        return mytotal
    def get_agg_load_node11(self):
        mytotal=0
        for el in self.load_node11:
            mytotal=mytotal+el
        return mytotal
    def get_agg_load_node12(self):
        mytotal=0
        for el in self.load_node12:
            mytotal=mytotal+el
        return mytotal

    def get_agg_load_node13(self):
        mytotal=0
        for el in self.load_node13:
            mytotal=mytotal+el
        return mytotal
    def get_agg_load_node14(self):
        mytotal=0
        for el in self.load_node14:
            mytotal=mytotal+el
        return mytotal
    def get_agg_load_node15(self):
        mytotal=0
        for el in self.load_node15:
            mytotal=mytotal+el
        return mytotal
    def get_agg_load_node16(self):
        mytotal=0
        for el in self.load_node16:
            mytotal=mytotal+el
        return mytotal

    def get_agg_thru_total(self):
        mytotal=0
        for el in self.thru_total:
            mytotal=mytotal+el
        return mytotal

    def get_agg_thru_high(self):
        mytotal=0
        for el in self.thru_high:
            mytotal=mytotal+el
        return mytotal

    def get_agg_thru_med(self):
        mytotal=0
        for el in self.thru_med:
            mytotal=mytotal+el
        return mytotal

    def get_agg_thru_low(self):
        mytotal=0
        for el in self.thru_low:
            mytotal=mytotal+el
        return mytotal
    def get_agg_thru_node1(self):
        mytotal=0
        for el in self.thru_node1:
            mytotal=mytotal+el
        return mytotal

    def get_agg_thru_node2(self):
        mytotal=0
        for el in self.thru_node2:
            mytotal=mytotal+el
        return mytotal
    def get_agg_thru_node3(self):
        mytotal=0
        for el in self.thru_node3:
            mytotal=mytotal+el
        return mytotal
    def get_agg_thru_node4(self):
        mytotal=0
        for el in self.thru_node4:
            mytotal=mytotal+el
        return mytotal
    def get_agg_thru_node5(self):
        mytotal=0
        for el in self.thru_node5:
            mytotal=mytotal+el
        return mytotal
    def get_agg_thru_node6(self):
        mytotal=0
        for el in self.thru_node6:
            mytotal=mytotal+el
        return mytotal
    def get_agg_thru_node7(self):
        mytotal=0
        for el in self.thru_node7:
            mytotal=mytotal+el
        return mytotal
    def get_agg_thru_node8(self):
        mytotal=0
        for el in self.thru_node8:
            mytotal=mytotal+el
        return mytotal
    def get_agg_thru_node9(self):
        mytotal=0
        for el in self.thru_node9:
            mytotal=mytotal+el
        return mytotal
    def get_agg_thru_node10(self):
        mytotal=0
        for el in self.thru_node10:
            mytotal=mytotal+el
        return mytotal
    def get_agg_thru_node11(self):
        mytotal=0
        for el in self.thru_node11:
            mytotal=mytotal+el
        return mytotal

    def get_agg_thru_node12(self):
        mytotal=0
        for el in self.thru_node12:
            mytotal=mytotal+el
        return mytotal

    def get_agg_thru_node13(self):
        mytotal=0
        for el in self.thru_node13:
            mytotal=mytotal+el
        return mytotal
    def get_agg_thru_node14(self):
        mytotal=0
        for el in self.thru_node14:
            mytotal=mytotal+el
        return mytotal
    def get_agg_thru_node15(self):
        mytotal=0
        for el in self.thru_node15:
            mytotal=mytotal+el
        return mytotal
    def get_agg_thru_node16(self):
        mytotal=0
        for el in self.thru_node16:
            mytotal=mytotal+el
        return mytotal
    def get_agg_drop_total(self):
        mytotal=0
        for el in self.drop_total:
            mytotal=mytotal+el
        return mytotal

    def get_agg_drop_high(self):
        mytotal=0
        for el in self.drop_high:
            mytotal=mytotal+el
        return mytotal

    def get_agg_drop_med(self):
        mytotal=0
        for el in self.drop_med:
            mytotal=mytotal+el
        return mytotal

    def get_agg_drop_low(self):
        mytotal=0
        for el in self.drop_low:
            mytotal=mytotal+el
        return mytotal
    def get_agg_drop_node1(self):
        mytotal=0
        for el in self.drop_node1:
            mytotal=mytotal+el
        return mytotal

    def get_agg_drop_node2(self):
        mytotal=0
        for el in self.drop_node2:
            mytotal=mytotal+el
        return mytotal
    def get_agg_drop_node3(self):
        mytotal=0
        for el in self.drop_node3:
            mytotal=mytotal+el
        return mytotal
    def get_agg_drop_node4(self):
        mytotal=0
        for el in self.drop_node4:
            mytotal=mytotal+el
        return mytotal
    def get_agg_drop_node5(self):
        mytotal=0
        for el in self.drop_node5:
            mytotal=mytotal+el
        return mytotal
    def get_agg_drop_node6(self):
        mytotal=0
        for el in self.drop_node6:
            mytotal=mytotal+el
        return mytotal
    def get_agg_drop_node7(self):
        mytotal=0
        for el in self.drop_node7:
            mytotal=mytotal+el
        return mytotal
    def get_agg_drop_node8(self):
        mytotal=0
        for el in self.drop_node8:
            mytotal=mytotal+el
        return mytotal
    def get_agg_drop_node9(self):
        mytotal=0
        for el in self.drop_node9:
            mytotal=mytotal+el
        return mytotal
    def get_agg_drop_node10(self):
        mytotal=0
        for el in self.drop_node10:
            mytotal=mytotal+el
        return mytotal
    def get_agg_drop_node11(self):
        mytotal=0
        for el in self.drop_node11:
            mytotal=mytotal+el
        return mytotal
    def get_agg_drop_node12(self):
        mytotal=0
        for el in self.drop_node12:
            mytotal=mytotal+el
        return mytotal

    def get_agg_drop_node13(self):
        mytotal=0
        for el in self.drop_node13:
            mytotal=mytotal+el
        return mytotal
    def get_agg_drop_node14(self):
        mytotal=0
        for el in self.drop_node14:
            mytotal=mytotal+el
        return mytotal
    def get_agg_drop_node15(self):
        mytotal=0
        for el in self.drop_node15:
            mytotal=mytotal+el
        return mytotal
    def get_agg_drop_node16(self):
        mytotal=0
        for el in self.drop_node16:
            mytotal=mytotal+el
        return mytotal

    def get_avg_delay_total(self):
        mytotal=0
        N=0
        for el in self.delay_total:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_high(self):
        mytotal=0
        N=0
        for el in self.delay_high:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_med(self):
        mytotal=0
        N=0
        for el in self.delay_med:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_low(self):
        mytotal=0
        N=0
        for el in self.delay_low:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None

    def get_avg_delay_node1(self):
        mytotal=0
        N=0
        for el in self.delay_node1:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_node2(self):
        mytotal=0
        N=0
        for el in self.delay_node2:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_node3(self):
        mytotal=0
        N=0
        for el in self.delay_node3:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_node4(self):
        mytotal=0
        N=0
        for el in self.delay_node4:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_node5(self):
        mytotal=0
        N=0
        for el in self.delay_node5:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_node6(self):
        mytotal=0
        N=0
        for el in self.delay_node6:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_node7(self):
        mytotal=0
        N=0
        for el in self.delay_node7:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_node8(self):
        mytotal=0
        N=0
        for el in self.delay_node8:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_node9(self):
        mytotal=0
        N=0
        for el in self.delay_node9:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_node10(self):
        mytotal=0
        N=0
        for el in self.delay_node10:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_node11(self):
        mytotal=0
        N=0
        for el in self.delay_node11:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_node12(self):
        mytotal=0
        N=0
        for el in self.delay_node12:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None

    def get_avg_delay_node13(self):
        mytotal=0
        N=0
        for el in self.delay_node13:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_node14(self):
        mytotal=0
        N=0
        for el in self.delay_node14:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_node15(self):
        mytotal=0
        N=0
        for el in self.delay_node15:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None
    def get_avg_delay_node16(self):
        mytotal=0
        N=0
        for el in self.delay_node16:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None


    def get_avg_qdelay_total(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_total:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_high(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_high:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_med(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_med:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_low(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_low:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_node1(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node1:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_node2(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node2:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_node3(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node3:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_node4(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node4:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_node5(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node5:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_node6(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node6:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_node7(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node7:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_node8(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node8:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_node9(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node9:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_node10(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node10:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_node11(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node11:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_node12(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node12:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None

    def get_avg_qdelay_node13(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node13:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_node14(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node14:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_node15(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node15:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None
    def get_avg_qdelay_node16(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_node16:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None

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
        print(str(debug_id))
        debug_id=debug_id+1

timeslot_list=My_Timeslot_List(my_tbegin,my_tend,my_samples)
timeslot_list.init_with_db(my_db)


if not avgg:
    LOAD=timeslot_list.get_list_drop_total()
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
    group_list.assign_timeslots_to_groups(timeslot_list)

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

    avg, err = group_list.get_groups_load_node1_bps()
    print('waa_load_node1_bps' + '_avg=' + str(avg))
    print('waa_load_node1_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node1_bps()
    print('waa_thru_node1_bps' + '_avg=' + str(avg))
    print('waa_thru_node1_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node1_bps()
    print('waa_drop_node1_bps' + '_avg=' + str(avg))
    print('waa_drop_node1_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node1()
    print('waa_delay_node1' + '_avg=' + str(avg))
    print('waa_delay_node1' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node1()
    print('waa_qdelay_node1' + '_avg=' + str(avg))
    print('waa_qdelay_node1' + '_err=' + str(err))
    avg, err = group_list.get_groups_load_node2_bps()
    print('waa_load_node2_bps' + '_avg=' + str(avg))
    print('waa_load_node2_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node2_bps()
    print('waa_thru_node2_bps' + '_avg=' + str(avg))
    print('waa_thru_node2_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node2_bps()
    print('waa_drop_node2_bps' + '_avg=' + str(avg))
    print('waa_drop_node2_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node2()
    print('waa_delay_node2' + '_avg=' + str(avg))
    print('waa_delay_node2' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node2()
    print('waa_qdelay_node2' + '_avg=' + str(avg))
    print('waa_qdelay_node2' + '_err=' + str(err))
    avg, err = group_list.get_groups_load_node3_bps()
    print('waa_load_node3_bps' + '_avg=' + str(avg))
    print('waa_load_node3_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node3_bps()
    print('waa_thru_node3_bps' + '_avg=' + str(avg))
    print('waa_thru_node3_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node3_bps()
    print('waa_drop_node3_bps' + '_avg=' + str(avg))
    print('waa_drop_node3_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node3()
    print('waa_delay_node3' + '_avg=' + str(avg))
    print('waa_delay_node3' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node3()
    print('waa_qdelay_node3' + '_avg=' + str(avg))
    print('waa_qdelay_node3' + '_err=' + str(err))
    avg, err = group_list.get_groups_load_node4_bps()
    print('waa_load_node4_bps' + '_avg=' + str(avg))
    print('waa_load_node4_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node4_bps()
    print('waa_thru_node4_bps' + '_avg=' + str(avg))
    print('waa_thru_node4_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node4_bps()
    print('waa_drop_node4_bps' + '_avg=' + str(avg))
    print('waa_drop_node4_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node4()
    print('waa_delay_node4' + '_avg=' + str(avg))
    print('waa_delay_node4' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node4()
    print('waa_qdelay_node4' + '_avg=' + str(avg))
    print('waa_qdelay_node4' + '_err=' + str(err))
    avg, err = group_list.get_groups_load_node5_bps()
    print('waa_load_node5_bps' + '_avg=' + str(avg))
    print('waa_load_node5_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node5_bps()
    print('waa_thru_node5_bps' + '_avg=' + str(avg))
    print('waa_thru_node5_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node5_bps()
    print('waa_drop_node5_bps' + '_avg=' + str(avg))
    print('waa_drop_node5_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node5()
    print('waa_delay_node5' + '_avg=' + str(avg))
    print('waa_delay_node5' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node5()
    print('waa_qdelay_node5' + '_avg=' + str(avg))
    print('waa_qdelay_node5' + '_err=' + str(err))
    avg, err = group_list.get_groups_load_node6_bps()
    print('waa_load_node6_bps' + '_avg=' + str(avg))
    print('waa_load_node6_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node6_bps()
    print('waa_thru_node6_bps' + '_avg=' + str(avg))
    print('waa_thru_node6_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node6_bps()
    print('waa_drop_node6_bps' + '_avg=' + str(avg))
    print('waa_drop_node6_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node6()
    print('waa_delay_node6' + '_avg=' + str(avg))
    print('waa_delay_node6' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node6()
    print('waa_qdelay_node6' + '_avg=' + str(avg))
    print('waa_qdelay_node6' + '_err=' + str(err))
    avg, err = group_list.get_groups_load_node7_bps()
    print('waa_load_node7_bps' + '_avg=' + str(avg))
    print('waa_load_node7_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node7_bps()
    print('waa_thru_node7_bps' + '_avg=' + str(avg))
    print('waa_thru_node7_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node7_bps()
    print('waa_drop_node7_bps' + '_avg=' + str(avg))
    print('waa_drop_node7_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node7()
    print('waa_delay_node7' + '_avg=' + str(avg))
    print('waa_delay_node7' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node7()
    print('waa_qdelay_node7' + '_avg=' + str(avg))
    print('waa_qdelay_node7' + '_err=' + str(err))
    avg, err = group_list.get_groups_load_node8_bps()
    print('waa_load_node8_bps' + '_avg=' + str(avg))
    print('waa_load_node8_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node8_bps()
    print('waa_thru_node8_bps' + '_avg=' + str(avg))
    print('waa_thru_node8_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node8_bps()
    print('waa_drop_node8_bps' + '_avg=' + str(avg))
    print('waa_drop_node8_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node8()
    print('waa_delay_node8' + '_avg=' + str(avg))
    print('waa_delay_node8' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node8()
    print('waa_qdelay_node8' + '_avg=' + str(avg))
    print('waa_qdelay_node8' + '_err=' + str(err))
    avg, err = group_list.get_groups_load_node9_bps()
    print('waa_load_node9_bps' + '_avg=' + str(avg))
    print('waa_load_node9_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node9_bps()
    print('waa_thru_node9_bps' + '_avg=' + str(avg))
    print('waa_thru_node9_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node9_bps()
    print('waa_drop_node9_bps' + '_avg=' + str(avg))
    print('waa_drop_node9_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node9()
    print('waa_delay_node9' + '_avg=' + str(avg))
    print('waa_delay_node9' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node9()
    print('waa_qdelay_node9' + '_avg=' + str(avg))
    print('waa_qdelay_node9' + '_err=' + str(err))
    avg, err = group_list.get_groups_load_node10_bps()
    print('waa_load_node10_bps' + '_avg=' + str(avg))
    print('waa_load_node10_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node10_bps()
    print('waa_thru_node10_bps' + '_avg=' + str(avg))
    print('waa_thru_node10_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node10_bps()
    print('waa_drop_node10_bps' + '_avg=' + str(avg))
    print('waa_drop_node10_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node10()
    print('waa_delay_node10' + '_avg=' + str(avg))
    print('waa_delay_node10' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node10()
    print('waa_qdelay_node10' + '_avg=' + str(avg))
    print('waa_qdelay_node10' + '_err=' + str(err))
    avg, err = group_list.get_groups_load_node11_bps()
    print('waa_load_node11_bps' + '_avg=' + str(avg))
    print('waa_load_node11_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node11_bps()
    print('waa_thru_node11_bps' + '_avg=' + str(avg))
    print('waa_thru_node11_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node11_bps()
    print('waa_drop_node11_bps' + '_avg=' + str(avg))
    print('waa_drop_node11_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node11()
    print('waa_delay_node11' + '_avg=' + str(avg))
    print('waa_delay_node11' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node11()
    print('waa_qdelay_node11' + '_avg=' + str(avg))
    print('waa_qdelay_node11' + '_err=' + str(err))
    avg, err = group_list.get_groups_load_node12_bps()
    print('waa_load_node12_bps' + '_avg=' + str(avg))
    print('waa_load_node12_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node12_bps()
    print('waa_thru_node12_bps' + '_avg=' + str(avg))
    print('waa_thru_node12_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node12_bps()
    print('waa_drop_node12_bps' + '_avg=' + str(avg))
    print('waa_drop_node12_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node12()
    print('waa_delay_node12' + '_avg=' + str(avg))
    print('waa_delay_node12' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node12()
    print('waa_qdelay_node12' + '_avg=' + str(avg))
    print('waa_qdelay_node12' + '_err=' + str(err))

    avg, err = group_list.get_groups_load_node13_bps()
    print('waa_load_node13_bps' + '_avg=' + str(avg))
    print('waa_load_node13_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node13_bps()
    print('waa_thru_node13_bps' + '_avg=' + str(avg))
    print('waa_thru_node13_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node13_bps()
    print('waa_drop_node13_bps' + '_avg=' + str(avg))
    print('waa_drop_node13_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node13()
    print('waa_delay_node13' + '_avg=' + str(avg))
    print('waa_delay_node13' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node13()
    print('waa_qdelay_node13' + '_avg=' + str(avg))
    print('waa_qdelay_node13' + '_err=' + str(err))

    avg, err = group_list.get_groups_load_node14_bps()
    print('waa_load_node14_bps' + '_avg=' + str(avg))
    print('waa_load_node14_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node14_bps()
    print('waa_thru_node14_bps' + '_avg=' + str(avg))
    print('waa_thru_node14_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node14_bps()
    print('waa_drop_node14_bps' + '_avg=' + str(avg))
    print('waa_drop_node14_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node14()
    print('waa_delay_node14' + '_avg=' + str(avg))
    print('waa_delay_node14' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node14()
    print('waa_qdelay_node14' + '_avg=' + str(avg))
    print('waa_qdelay_node14' + '_err=' + str(err))

    avg, err = group_list.get_groups_load_node15_bps()
    print('waa_load_node15_bps' + '_avg=' + str(avg))
    print('waa_load_node15_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node15_bps()
    print('waa_thru_node15_bps' + '_avg=' + str(avg))
    print('waa_thru_node15_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node15_bps()
    print('waa_drop_node15_bps' + '_avg=' + str(avg))
    print('waa_drop_node15_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node15()
    print('waa_delay_node15' + '_avg=' + str(avg))
    print('waa_delay_node15' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node15()
    print('waa_qdelay_node15' + '_avg=' + str(avg))
    print('waa_qdelay_node15' + '_err=' + str(err))

    avg, err = group_list.get_groups_load_node16_bps()
    print('waa_load_node16_bps' + '_avg=' + str(avg))
    print('waa_load_node16_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_thru_node16_bps()
    print('waa_thru_node16_bps' + '_avg=' + str(avg))
    print('waa_thru_node16_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_drop_node16_bps()
    print('waa_drop_node16_bps' + '_avg=' + str(avg))
    print('waa_drop_node16_bps' + '_err=' + str(err))
    avg, err = group_list.get_groups_delay_node16()
    print('waa_delay_node16' + '_avg=' + str(avg))
    print('waa_delay_node16' + '_err=' + str(err))
    avg, err = group_list.get_groups_qdelay_node16()
    print('waa_qdelay_node16' + '_avg=' + str(avg))
    print('waa_qdelay_node16' + '_err=' + str(err))



    plt.plot(prLOAD_BIT, prTHRU_BIT, label="thruput bitrate")
    plt.plot(prLOAD_BIT, prDROP_BIT, label="drop bitrate")
    plt.xlabel('Load (bps)', fontsize=25)
    plt.ylabel('Probability', fontsize=25)
    plt.grid(True, which='major', axis='both')
    plt.title('Both Waiting and Prop Delay', fontsize=25)
    plt.legend()
    plt.show()
