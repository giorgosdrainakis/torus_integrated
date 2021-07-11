import math
import random
from torus_integrated import myglobal
from torus_integrated.channel import *
from torus_integrated.traffic import Control_Packet
import datetime

class Tors:
    def __init__(self):
        self.db=[]

    def inter_transmit(self,current_time):
        for tor in self.db:
            tor.inter_transmit(current_time)

    def inter_check_arrival(self,current_time):
        list_of_arrived_packs=[]
        for tor in self.db:
            list_of_arrived_packs.extend(tor.inter_check_arrival(current_time))
        for pack in list_of_arrived_packs:
            self.add_inter_packet_to_local_tor(pack.destination_tor,pack,current_time)

    def add_inter_packet_to_local_tor(self,dest_tor,pack,current_time):
        for tor in self.db:
            if tor.id==dest_tor:
                tor.add_inter_packet_to_local_tor(pack,current_time)

    def have_buffers_packets(self):
        for tor in self.db:
            if tor.have_buffers_packets():
                return True

    def add_new_packets_to_buffers(self,current_time):
        for tor in self.db:
            tor.add_new_packets_to_buffers(current_time)

    def check_arrival_WAA(self,current_time):
        for tor in self.db:
            tor.check_arrival_WAA(current_time)

    def process_new_cycle(self,current_time):
        for tor in self.db:
            tor.process_new_cycle(current_time)

    def transmit_WAA(self, current_time):
        for tor in self.db:
            tor.transmit_WAA(current_time)

    def write_log(self):
        # estimate actual time
        real_time = str(datetime.datetime.now())
        real_time = real_time.replace('-', '_')
        real_time = real_time.replace(' ', '_')
        real_time = real_time.replace(':', '_')
        real_time = real_time.replace('.', '_')
        # log for each tor
        for tor in self.db:
            tor.write_log(real_time)

    def add_new(self,node):
        self.db.append(node)

    def get_node_from_id(self,id):
        for node in self.db:
            if node.id==id:
                return node

class Tor:
    def __init__(self,id):
        self.id=id
        self.nodes=None
        self.outgoing_buffers_low_list=[]
        self.outgoing_buffers_med_list=[]
        self.outgoing_buffers_high_list=[]
        self.data_dropped=[]
        self.meta_buffer=[]

    def add_inter_packet_to_local_tor(self,pack,current_time):
        self.nodes.add_inter_packet_to_local_tor(pack,current_time)

    def get_meta_buffer_size(self):
        size=0
        for pack in self.meta_buffer:
            size=size+pack.packet_size
        return size

    def inter_transmit(self,current_time):
        i=0
        trx_list=list(range(0,len(self.outgoing_buffers_high_list)))
        random.shuffle(trx_list)
        while self.get_meta_buffer_size()<1500 and i<len(trx_list):
            if self.get_meta_buffer_size() < 1500:
                if self.outgoing_buffers_high_list[i].has_packets():
                    self.meta_buffer.append(self.outgoing_buffers_high_list[i].get_next_packet())
            if self.get_meta_buffer_size() < 1500:
                if self.outgoing_buffers_med_list[i].has_packets():
                    self.meta_buffer.append(self.outgoing_buffers_med_list[i].get_next_packet())
            if self.get_meta_buffer_size() < 1500:
                if self.outgoing_buffers_low_list[i].has_packets():
                    self.meta_buffer.append(self.outgoing_buffers_low_list[i].get_next_packet())
            i=i+1
        print('Inter transmit with tor meta buffer size='+str(self.get_meta_buffer_size()))
        for pack in self.meta_buffer:
            pack.self.time_tor_buffer_out=current_time
            pack.time_tor_trx_in=current_time
            pack.time_tor_trx_out=current_time+myglobal.PROPAGATION_TIME*3

    def inter_check_arrival(self,current_time):
        list_of_sent_packs=[]
        for pack in self.meta_buffer:
            has_packet_arrived_inter=pack.time_tor_trx_in<pack.time_tor_trx_out and pack.time_tor_trx_out<=current_time
            if has_packet_arrived_inter:
                list_of_sent_packs.append(pack)
                self.meta_buffer.remove(pack)
        return list_of_sent_packs

    def have_buffers_packets(self):
        return self.nodes.have_buffers_packets()

    def add_new_packets_to_buffers(self,current_time):
        self.nodes.add_new_packets_to_buffers(current_time)

    def check_arrival_WAA(self,current_time):
        total_intra_packet_arrived_list=self.nodes.check_arrival_WAA(current_time)
        for pack in total_intra_packet_arrived_list:
            if pack.destination_tor != self.id:
                self.add_pack_to_outgoing_buffers(pack,current_time)

    def process_new_cycle(self,current_time):
        self.nodes.process_new_cycle(current_time)

    def transmit_WAA(self, current_time):
        self.nodes.transmit_WAA(current_time)

    def write_log(self,real_time):
        self.nodes.write_log(real_time)

    def add_pack_to_outgoing_buffers(self,pack,current_time):
        is_in_buffer = False
        if pack.packet_qos == 'low':
            for outgoing_buffer in self.outgoing_buffers_low_list:
                if pack.destination_tor==outgoing_buffer.destination_tor:
                    is_in_buffer = outgoing_buffer.add(pack, current_time)
        elif pack.packet_qos == 'med':
            for outgoing_buffer in self.outgoing_buffers_med_list:
                if pack.destination_tor==outgoing_buffer.destination_tor:
                    is_in_buffer = outgoing_buffer.add(pack, current_time)
        elif pack.packet_qos == 'high':
            for outgoing_buffer in self.outgoing_buffers_high_list:
                if pack.destination_tor==outgoing_buffer.destination_tor:
                    is_in_buffer = outgoing_buffer.add(pack, current_time)
        if not is_in_buffer:
            print('Dropped packet in TOR=' + str(pack.packet_id) + ' in node=' + str(self.id))
            self.data_dropped.append(pack)







