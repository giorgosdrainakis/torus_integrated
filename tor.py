import itertools
import math
import random
from torus_integrated import myglobal
from torus_integrated.channel import *
from torus_integrated.traffic import Control_Packet
import datetime

class Tors:
    def __init__(self):
        self.db=[]
        self.channels=None
        self.torus_list=None

    def inter_transmit(self,current_time):
        potential_recs=[]
        for tor in self.db:
            potential_rec=tor.check_per_tor_requests()
            print('Tor id-='+str(tor.id)+' potlist='+str(len(potential_rec)))
            potential_recs.extend(potential_rec)

        filtered_recs=[]
        for pot_rec in potential_recs:
            can_enter=True
            for filt_rec in filtered_recs:
                if pot_rec.rx==filt_rec.rx and pot_rec.in_dir==filt_rec.in_dir:
                    can_enter=False
            if can_enter:
                filtered_recs.append(pot_rec)
        # debug
        for el in filtered_recs:
            el.show()

        for tor in self.db:
            tor.inter_transmit(current_time,filtered_recs)

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

    def check_arrival_intra(self,current_time):
        for tor in self.db:
            tor.check_arrival_intra(current_time)

    def process_new_cycle(self,current_time):
        new_cycle=False
        for tor in self.db:
            new_cycle=tor.process_new_cycle(current_time)
        return new_cycle
    
    def transmit_intra(self, current_time):
        for tor in self.db:
            tor.transmit_intra(current_time)

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
        self.meta_buffer_S=[]
        self.meta_buffer_E=[]
        self.meta_buffer_N=[]
        self.meta_buffer_W=[]
        self.torus_list=None

    def add_inter_packet_to_local_tor(self,pack,current_time):
        self.nodes.add_inter_packet_to_local_tor(pack,current_time)

    def check_per_tor_requests(self):
        # Check which outgoing buffers can fill up a 1500 message
        rx_1500_list=self.get_potential_rx_1500_list()
        print('Tor ID='+str(self.id)+'potentialrxlist='+str(len(rx_1500_list)))
        # Build max 4 lamda request
        return self.build_4_lamda_request(rx_1500_list)

    def build_4_lamda_request(self,rx_list):
        mylist=rx_list
        random.shuffle(mylist)
        tx=self.id
        return self.torus_list.get_4_lamda_request_from_rx_list(rx_list,tx)


    def get_potential_rx_1500_list(self):
        # Check which outgoing buffers can fill up a 1500 message
        rx_1500_list=[]
        for rx_id in range(1,myglobal.TOTAL_TORS+1):
            can_fill_with_bigs=False
            for out_buffer in self.outgoing_buffers_med_list:
                # find buffer according to rx id
                if out_buffer.destination_tor==rx_id:
                    if out_buffer.has_packets() and out_buffer.db[0].packet_size==myglobal.MAX_PACKET_SIZE:
                        can_fill_with_bigs=True
            if not can_fill_with_bigs:
                for out_buffer in self.outgoing_buffers_low_list:
                    # find buffer according to rx id
                    if out_buffer.destination_tor == rx_id:
                        if out_buffer.has_packets() and out_buffer.db[0].packet_size == myglobal.MAX_PACKET_SIZE:
                            can_fill_with_bigs = True
            fill_with_smalls_size=0
            for out_buffer in self.outgoing_buffers_high_list:
                # find buffer according to rx id
                if out_buffer.destination_tor==rx_id:
                    i=0
                    while i<len(out_buffer.db) and out_buffer.db[i].packet_size<myglobal.MAX_PACKET_SIZE \
                            and fill_with_smalls_size<(myglobal.MAX_PACKET_SIZE/myglobal.MIN_PACKET_SIZE):
                        i=i+1
                        fill_with_smalls_size=fill_with_smalls_size+1
            for out_buffer in self.outgoing_buffers_med_list:
                # find buffer according to rx id
                if out_buffer.destination_tor==rx_id:
                    i=0
                    while i<len(out_buffer.db) and out_buffer.db[i].packet_size<myglobal.MAX_PACKET_SIZE \
                            and fill_with_smalls_size<(myglobal.MAX_PACKET_SIZE/myglobal.MIN_PACKET_SIZE):
                        i=i+1
                        fill_with_smalls_size=fill_with_smalls_size+1
            for out_buffer in self.outgoing_buffers_low_list:
                # find buffer according to rx id
                if out_buffer.destination_tor==rx_id:
                    i=0
                    while i<len(out_buffer.db) and out_buffer.db[i].packet_size<myglobal.MAX_PACKET_SIZE \
                            and fill_with_smalls_size<(myglobal.MAX_PACKET_SIZE/myglobal.MIN_PACKET_SIZE):
                        i=i+1
                        fill_with_smalls_size=fill_with_smalls_size+1
            if can_fill_with_bigs or fill_with_smalls_size>=int(myglobal.MAX_PACKET_SIZE/myglobal.MIN_PACKET_SIZE):
                rx_1500_list.append(rx_id)
        return rx_1500_list

    def get_meta_buffer_S_size(self):
        size=0
        for pack in self.meta_buffer_S:
            size=size+pack.packet_size
        return size
    def get_meta_buffer_E_size(self):
        size=0
        for pack in self.meta_buffer_E:
            size=size+pack.packet_size
        return size
    def get_meta_buffer_N_size(self):
        size=0
        for pack in self.meta_buffer_N:
            size=size+pack.packet_size
        return size
    def get_meta_buffer_W_size(self):
        size=0
        for pack in self.meta_buffer_W:
            size=size+pack.packet_size
        return size

    def fill_S_meta_buffer(self,current_time,rx_id):
        can_fill_with_bigs = False
        for out_buffer in self.outgoing_buffers_med_list:
            if out_buffer.destination_tor == rx_id:
                if out_buffer.has_packets() and out_buffer.db[0].packet_size == myglobal.MAX_PACKET_SIZE:
                    mypack=out_buffer.db[0]
                    mypack.time_tor_buffer_out=current_time
                    mypack.time_tor_trx_in = current_time
                    trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                    mypack.time_tor_trx_out = mypack.time_tor_trx_in+ trx_time_theor+ myglobal.PROPAGATION_TIME * 1
                    self.meta_buffer_S.append(mypack)
                    out_buffer.db.pop(0)
                    can_fill_with_bigs = True
        if not can_fill_with_bigs:
            for out_buffer in self.outgoing_buffers_low_list:
                if out_buffer.destination_tor == rx_id:
                    if out_buffer.has_packets() and out_buffer.db[0].packet_size == myglobal.MAX_PACKET_SIZE:
                        mypack = out_buffer.db[0]
                        mypack.time_tor_buffer_out = current_time
                        mypack.time_tor_trx_in = current_time
                        trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                        mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                        self.meta_buffer_S.append(mypack)
                        out_buffer.db.pop(0)
                        can_fill_with_bigs = True
        if not can_fill_with_bigs:
            fill_with_smalls_size = 0
            for out_buffer in self.outgoing_buffers_high_list:
                if out_buffer.destination_tor == rx_id:
                    i = 0
                    to_delete_list = []  #
                    while i < len(out_buffer.db) and out_buffer.db[i].packet_size < myglobal.MAX_PACKET_SIZE \
                            and fill_with_smalls_size < (
                            myglobal.MAX_PACKET_SIZE / myglobal.MIN_PACKET_SIZE):
                        mypack = out_buffer.db[i]
                        copy_pack=mypack
                        to_delete_list.append(copy_pack)  #
                        mypack.time_tor_buffer_out = current_time
                        mypack.time_tor_trx_in = current_time
                        trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                        mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                        self.meta_buffer_S.append(mypack)
                        i = i + 1
                        fill_with_smalls_size = fill_with_smalls_size + 1
                    for item in to_delete_list:  #
                        out_buffer.db.remove(item) #
            for out_buffer in self.outgoing_buffers_med_list:
                i = 0
                to_delete_list = []  #
                while i < len(out_buffer.db) and out_buffer.db[i].packet_size < myglobal.MAX_PACKET_SIZE \
                        and fill_with_smalls_size < (
                        myglobal.MAX_PACKET_SIZE / myglobal.MIN_PACKET_SIZE):
                    mypack = out_buffer.db[i]
                    copy_pack = mypack
                    to_delete_list.append(copy_pack)  #
                    mypack.time_tor_buffer_out = current_time
                    mypack.time_tor_trx_in = current_time
                    trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                    mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                    self.meta_buffer_S.append(mypack)
                    #out_buffer.db.pop(i)
                    i = i + 1
                    fill_with_smalls_size = fill_with_smalls_size + 1
                for item in to_delete_list:  #
                    out_buffer.db.remove(item)  #
            for out_buffer in self.outgoing_buffers_low_list:
                i = 0
                to_delete_list = []  #
                while i < len(out_buffer.db) and out_buffer.db[i].packet_size < myglobal.MAX_PACKET_SIZE \
                        and fill_with_smalls_size < (
                        myglobal.MAX_PACKET_SIZE / myglobal.MIN_PACKET_SIZE):
                    mypack = out_buffer.db[i]
                    copy_pack = mypack
                    to_delete_list.append(copy_pack)  #
                    mypack.time_tor_buffer_out = current_time
                    mypack.time_tor_trx_in = current_time
                    trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                    mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                    self.meta_buffer_S.append(mypack)
                    #out_buffer.db.pop(i)
                    i = i + 1
                    fill_with_smalls_size = fill_with_smalls_size + 1
                for item in to_delete_list:  #
                    out_buffer.db.remove(item)  #
        if can_fill_with_bigs:
            print('Will InterTRXing bigs')
        else:
            print('Will InterTRXing smalls='+str(fill_with_smalls_size))
    def fill_N_meta_buffer(self,current_time,rx_id):
        can_fill_with_bigs = False
        for out_buffer in self.outgoing_buffers_med_list:
            if out_buffer.destination_tor == rx_id:
                if out_buffer.has_packets() and out_buffer.db[0].packet_size == myglobal.MAX_PACKET_SIZE:
                    mypack=out_buffer.db[0]
                    mypack.time_tor_buffer_out=current_time
                    mypack.time_tor_trx_in = current_time
                    trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                    mypack.time_tor_trx_out = current_time+ trx_time_theor+ myglobal.PROPAGATION_TIME * 1
                    self.meta_buffer_N.append(mypack)
                    out_buffer.db.pop(0)
                    can_fill_with_bigs = True
        if not can_fill_with_bigs:
            for out_buffer in self.outgoing_buffers_low_list:
                if out_buffer.destination_tor == rx_id:
                    if out_buffer.has_packets() and out_buffer.db[0].packet_size == myglobal.MAX_PACKET_SIZE:
                        mypack = out_buffer.db[0]
                        mypack.time_tor_buffer_out = current_time
                        mypack.time_tor_trx_in = current_time
                        trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                        mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                        self.meta_buffer_N.append(mypack)
                        out_buffer.db.pop(0)
                        can_fill_with_bigs = True
        if not can_fill_with_bigs:
            fill_with_smalls_size = 0
            for out_buffer in self.outgoing_buffers_high_list:
                if out_buffer.destination_tor == rx_id:
                    i = 0
                    to_delete_list=[] #
                    while i < len(out_buffer.db) and out_buffer.db[i].packet_size < myglobal.MAX_PACKET_SIZE \
                            and fill_with_smalls_size < (
                            myglobal.MAX_PACKET_SIZE / myglobal.MIN_PACKET_SIZE):
                        mypack = out_buffer.db[i]
                        copy_pack=mypack
                        to_delete_list.append(copy_pack)  #
                        mypack.time_tor_buffer_out = current_time
                        mypack.time_tor_trx_in = current_time
                        trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                        mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                        self.meta_buffer_N.append(mypack)
                        #out_buffer.db.pop(i)
                        i = i + 1
                        fill_with_smalls_size = fill_with_smalls_size + 1
                    for item in to_delete_list:  #
                        out_buffer.db.remove(item) #
            for out_buffer in self.outgoing_buffers_med_list:
                i = 0
                to_delete_list = []  #
                while i < len(out_buffer.db) and out_buffer.db[i].packet_size < myglobal.MAX_PACKET_SIZE \
                        and fill_with_smalls_size < (
                        myglobal.MAX_PACKET_SIZE / myglobal.MIN_PACKET_SIZE):
                    mypack = out_buffer.db[i]
                    copy_pack = mypack
                    to_delete_list.append(copy_pack)  #
                    mypack.time_tor_buffer_out = current_time
                    mypack.time_tor_trx_in = current_time
                    trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                    mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                    self.meta_buffer_N.append(mypack)
                    #out_buffer.db.pop(i)
                    i = i + 1
                    fill_with_smalls_size = fill_with_smalls_size + 1
                for item in to_delete_list:  #
                    out_buffer.db.remove(item)  #
            for out_buffer in self.outgoing_buffers_low_list:
                i = 0
                to_delete_list = []  #
                while i < len(out_buffer.db) and out_buffer.db[i].packet_size < myglobal.MAX_PACKET_SIZE \
                        and fill_with_smalls_size < (
                        myglobal.MAX_PACKET_SIZE / myglobal.MIN_PACKET_SIZE):
                    mypack = out_buffer.db[i]
                    copy_pack = mypack
                    to_delete_list.append(copy_pack)  #
                    mypack.time_tor_buffer_out = current_time
                    mypack.time_tor_trx_in = current_time
                    trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                    mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                    self.meta_buffer_N.append(mypack)
                    #out_buffer.db.pop(i)
                    i = i + 1
                    fill_with_smalls_size = fill_with_smalls_size + 1
                for item in to_delete_list:  #
                    out_buffer.db.remove(item)  #
        if can_fill_with_bigs:
            print('Will InterTRXing bigs=')
        else:
            print('Will InterTRXing smalls='+str(fill_with_smalls_size))
    def fill_W_meta_buffer(self,current_time,rx_id):
        can_fill_with_bigs = False
        for out_buffer in self.outgoing_buffers_med_list:
            if out_buffer.destination_tor == rx_id:
                if out_buffer.has_packets() and out_buffer.db[0].packet_size == myglobal.MAX_PACKET_SIZE:
                    mypack=out_buffer.db[0]
                    mypack.time_tor_buffer_out=current_time
                    mypack.time_tor_trx_in = current_time
                    trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                    mypack.time_tor_trx_out = current_time+ trx_time_theor+ myglobal.PROPAGATION_TIME * 1
                    self.meta_buffer_W.append(mypack)
                    out_buffer.db.pop(0)
                    can_fill_with_bigs = True
        if not can_fill_with_bigs:
            for out_buffer in self.outgoing_buffers_low_list:
                if out_buffer.destination_tor == rx_id:
                    if out_buffer.has_packets() and out_buffer.db[0].packet_size == myglobal.MAX_PACKET_SIZE:
                        mypack = out_buffer.db[0]
                        mypack.time_tor_buffer_out = current_time
                        mypack.time_tor_trx_in = current_time
                        trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                        mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                        self.meta_buffer_W.append(mypack)
                        out_buffer.db.pop(0)
                        can_fill_with_bigs = True
        if not can_fill_with_bigs:
            fill_with_smalls_size = 0
            for out_buffer in self.outgoing_buffers_high_list:
                if out_buffer.destination_tor == rx_id:
                    i = 0
                    to_delete_list=[] #
                    while i < len(out_buffer.db) and out_buffer.db[i].packet_size < myglobal.MAX_PACKET_SIZE \
                            and fill_with_smalls_size < (
                            myglobal.MAX_PACKET_SIZE / myglobal.MIN_PACKET_SIZE):
                        mypack = out_buffer.db[i]
                        to_delete_list.append(mypack) #
                        mypack.time_tor_buffer_out = current_time
                        mypack.time_tor_trx_in = current_time
                        trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                        mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                        self.meta_buffer_W.append(mypack)
                        #out_buffer.db.pop(i)
                        i = i + 1
                        fill_with_smalls_size = fill_with_smalls_size + 1
                    for item in to_delete_list:  #
                        out_buffer.db.remove(item) #
            for out_buffer in self.outgoing_buffers_med_list:
                i = 0
                to_delete_list = []  #
                while i < len(out_buffer.db) and out_buffer.db[i].packet_size < myglobal.MAX_PACKET_SIZE \
                        and fill_with_smalls_size < (
                        myglobal.MAX_PACKET_SIZE / myglobal.MIN_PACKET_SIZE):
                    mypack = out_buffer.db[i]
                    copy_pack = mypack
                    to_delete_list.append(copy_pack)  #
                    mypack.time_tor_buffer_out = current_time
                    mypack.time_tor_trx_in = current_time
                    trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                    mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                    self.meta_buffer_W.append(mypack)
                    #out_buffer.db.pop(i)
                    i = i + 1
                    fill_with_smalls_size = fill_with_smalls_size + 1
                for item in to_delete_list:  #
                    out_buffer.db.remove(item)  #
            for out_buffer in self.outgoing_buffers_low_list:
                i = 0
                to_delete_list = []  #
                while i < len(out_buffer.db) and out_buffer.db[i].packet_size < myglobal.MAX_PACKET_SIZE \
                        and fill_with_smalls_size < (
                        myglobal.MAX_PACKET_SIZE / myglobal.MIN_PACKET_SIZE):
                    mypack = out_buffer.db[i]
                    copy_pack = mypack
                    to_delete_list.append(copy_pack)  #
                    mypack.time_tor_buffer_out = current_time
                    mypack.time_tor_trx_in = current_time
                    trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                    mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                    self.meta_buffer_W.append(mypack)
                    #out_buffer.db.pop(i)
                    i = i + 1
                    fill_with_smalls_size = fill_with_smalls_size + 1
                for item in to_delete_list:  #
                    out_buffer.db.remove(item)  #
        if can_fill_with_bigs:
            print('Will InterTRXing bigs=')
        else:
            print('Will InterTRXing smalls='+str(fill_with_smalls_size))
    def fill_E_meta_buffer(self,current_time,rx_id):
        can_fill_with_bigs = False
        for out_buffer in self.outgoing_buffers_med_list:
            if out_buffer.destination_tor == rx_id:
                if out_buffer.has_packets() and out_buffer.db[0].packet_size == myglobal.MAX_PACKET_SIZE:
                    mypack=out_buffer.db[0]
                    mypack.time_tor_buffer_out=current_time
                    mypack.time_tor_trx_in = current_time
                    trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                    mypack.time_tor_trx_out = current_time+ trx_time_theor+ myglobal.PROPAGATION_TIME * 1
                    self.meta_buffer_E.append(mypack)
                    out_buffer.db.pop(0)
                    can_fill_with_bigs = True
        if not can_fill_with_bigs:
            for out_buffer in self.outgoing_buffers_low_list:
                if out_buffer.destination_tor == rx_id:
                    if out_buffer.has_packets() and out_buffer.db[0].packet_size == myglobal.MAX_PACKET_SIZE:
                        mypack = out_buffer.db[0]
                        mypack.time_tor_buffer_out = current_time
                        mypack.time_tor_trx_in = current_time
                        trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                        mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                        self.meta_buffer_E.append(mypack)
                        out_buffer.db.pop(0)
                        can_fill_with_bigs = True
        if not can_fill_with_bigs:
            fill_with_smalls_size = 0
            for out_buffer in self.outgoing_buffers_high_list:
                if out_buffer.destination_tor == rx_id:
                    i = 0
                    to_delete_list=[] #
                    while i < len(out_buffer.db) and out_buffer.db[i].packet_size < myglobal.MAX_PACKET_SIZE \
                            and fill_with_smalls_size < (
                            myglobal.MAX_PACKET_SIZE / myglobal.MIN_PACKET_SIZE):
                        mypack = out_buffer.db[i]
                        to_delete_list.append(mypack) #
                        mypack.time_tor_buffer_out = current_time
                        mypack.time_tor_trx_in = current_time
                        trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                        mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                        self.meta_buffer_E.append(mypack)
                        #out_buffer.db.pop(i)
                        i = i + 1
                        fill_with_smalls_size = fill_with_smalls_size + 1
                    for item in to_delete_list:  #
                        out_buffer.db.remove(item) #
            for out_buffer in self.outgoing_buffers_med_list:
                i = 0
                to_delete_list = []  #
                while i < len(out_buffer.db) and out_buffer.db[i].packet_size < myglobal.MAX_PACKET_SIZE \
                        and fill_with_smalls_size < (
                        myglobal.MAX_PACKET_SIZE / myglobal.MIN_PACKET_SIZE):
                    mypack = out_buffer.db[i]
                    copy_pack = mypack
                    to_delete_list.append(copy_pack)  #
                    mypack.time_tor_buffer_out = current_time
                    mypack.time_tor_trx_in = current_time
                    trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                    mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                    self.meta_buffer_E.append(mypack)
                    #out_buffer.db.pop(i)
                    i = i + 1
                    fill_with_smalls_size = fill_with_smalls_size + 1
                for item in to_delete_list:  #
                    out_buffer.db.remove(item)  #
            for out_buffer in self.outgoing_buffers_low_list:
                i = 0
                to_delete_list = []  #
                while i < len(out_buffer.db) and out_buffer.db[i].packet_size < myglobal.MAX_PACKET_SIZE \
                        and fill_with_smalls_size < (
                        myglobal.MAX_PACKET_SIZE / myglobal.MIN_PACKET_SIZE):
                    mypack = out_buffer.db[i]
                    copy_pack = mypack
                    to_delete_list.append(copy_pack)  #
                    mypack.time_tor_buffer_out = current_time
                    mypack.time_tor_trx_in = current_time
                    trx_time_theor=(8*mypack.packet_size)/myglobal.INTER_CHANNEL_BITRATE
                    mypack.time_tor_trx_out = current_time + trx_time_theor + myglobal.PROPAGATION_TIME * 1
                    self.meta_buffer_E.append(mypack)
                    # out_buffer.db.pop(i)
                    i = i + 1
                    fill_with_smalls_size = fill_with_smalls_size + 1
                for item in to_delete_list:  #
                    out_buffer.db.remove(item)  #
        if can_fill_with_bigs:
            print('Will InterTRXing bigs=')
        else:
            print('Will InterTRXing smalls='+str(fill_with_smalls_size))

    def inter_transmit(self,current_time,filtered_recs):
        for rec in filtered_recs:
            if rec.tx==self.id:
                if rec.out_dir=='S':
                    self.fill_S_meta_buffer(current_time,rec.rx)
                elif rec.out_dir=='N':
                    self.fill_N_meta_buffer(current_time,rec.rx)
                elif rec.out_dir=='W':
                    self.fill_W_meta_buffer(current_time,rec.rx)
                elif rec.out_dir=='E':
                    self.fill_E_meta_buffer(current_time,rec.rx)
                else:
                    print('Error, cannot ifnd SNWE metabuffer')

    def inter_check_arrival(self,current_time):
        list_of_sent_packs=[]
        for pack in self.meta_buffer_S:
            has_packet_arrived_inter=pack.time_tor_trx_in<pack.time_tor_trx_out and pack.time_tor_trx_out<=current_time
            if has_packet_arrived_inter:
                print('INTER connection arrived to TOR='+str(self.id)+',pack='+str(pack.show_mini()))
                list_of_sent_packs.append(pack)
                self.meta_buffer_S.remove(pack)
        for pack in self.meta_buffer_N:
            has_packet_arrived_inter=pack.time_tor_trx_in<pack.time_tor_trx_out and pack.time_tor_trx_out<=current_time
            if has_packet_arrived_inter:
                print('INTER connection arrived to TOR='+str(self.id)+',pack='+str(pack.show_mini()))
                list_of_sent_packs.append(pack)
                self.meta_buffer_N.remove(pack)
        for pack in self.meta_buffer_W:
            has_packet_arrived_inter=pack.time_tor_trx_in<pack.time_tor_trx_out and pack.time_tor_trx_out<=current_time
            if has_packet_arrived_inter:
                print('INTER connection arrived to TOR='+str(self.id)+',pack='+str(pack.show_mini()))
                list_of_sent_packs.append(pack)
                self.meta_buffer_W.remove(pack)
        for pack in self.meta_buffer_E:
            has_packet_arrived_inter=pack.time_tor_trx_in<pack.time_tor_trx_out and pack.time_tor_trx_out<=current_time
            if has_packet_arrived_inter:
                print('INTER connection arrived to TOR='+str(self.id)+',pack='+str(pack.show_mini()))
                list_of_sent_packs.append(pack)
                self.meta_buffer_E.remove(pack)
        return list_of_sent_packs

    def have_buffers_packets(self):
        # check inter buffers
        for buffer in self.outgoing_buffers_high_list:
            if buffer.has_packets():
                return True
        for buffer in self.outgoing_buffers_med_list:
            if buffer.has_packets():
                return True
        for buffer in self.outgoing_buffers_low_list:
            if buffer.has_packets():
                return True
        # check intra buffers
        return self.nodes.have_buffers_packets()

    def add_new_packets_to_buffers(self,current_time):
        self.nodes.add_new_packets_to_buffers(current_time)

    def check_arrival_intra(self,current_time):
        outgoing_packets_list=self.nodes.check_arrival_intra(current_time)
        for pack in outgoing_packets_list:
            self.add_pack_to_outgoing_buffers(pack,current_time)

    def process_new_cycle(self,current_time):
        new_cycle=self.nodes.process_new_cycle(current_time)
        return new_cycle
    def transmit_intra(self, current_time):
        self.nodes.transmit_intra(current_time)

    def write_log(self,real_time):
        self.nodes.write_log(real_time)

        output_table = ''
        for packet in self.data_dropped:
            output_table = output_table + packet.show() + '\n'
        combined_name = myglobal.ROOT + myglobal.LOGS_FOLDER + 'log' + str(real_time) + '_tor' + str(self.id) + '_combo.csv'

        with open(combined_name, mode='a') as file:
            file.write(output_table)

        print('Re Sorting TOR='+str(self.id))
        with open(combined_name, 'r', newline='') as f_input:
            csv_input = csv.DictReader(f_input)
            data = sorted(csv_input, key=lambda row: (float(row['time']), float(row['packet_id'])))

        print('Rewriting TOR='+str(self.id))
        with open(combined_name, 'w', newline='') as f_output:
            csv_output = csv.DictWriter(f_output, fieldnames=csv_input.fieldnames)
            csv_output.writeheader()
            csv_output.writerows(data)

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
            print('Dropping to interconnection buffers from TOR=' + str(self.id) + ',pack=' + str(pack.show_mini()))
            self.data_dropped.append(pack)
        else:
            print('Adding to interconnection buffers from TOR=' + str(self.id) + ',pack=' + str(pack.show_mini()))

class Torus_Matrix:
    def __init__(self):
        self.db = []
        self.load()

    def load(self):
        with open(myglobal.ROOT + myglobal.INTER_TRANSMISSION_INFO_FOLDER + myglobal.TORUS_FILE) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                new_rec=Torus_Record(row['rx'],row['tx'],row['out_dir'],row['in_dir'],row['lamda'])
                self.db.append(new_rec)

    def get_4_lamda_request_from_rx_list(self,rx_list,tx):
        ports=4
        while ports>0:
            potentials=[]
            for quatro in itertools.combinations(rx_list, ports):
                # check if 4 different ports with 4 different channels
                out=[]
                for rx in quatro:
                    for rec in self.db:
                        if rec.tx==tx and rec.rx==rx:
                            out.append(rec)
                out_lamdas=[]
                out_ports=[]
                for el in out:
                    out_lamdas.append(el.lamda)
                    out_ports.append(el.out_dir)
                out_lamdas=list(set(out_lamdas))
                out_ports=list(set(out_ports))
                if len(out_lamdas)==ports and len(out_ports)==ports:
                    potentials.append(out)
            if len(potentials)>0:
                random.shuffle(potentials)
                return potentials[0]
            ports=ports-1
        return []

    ############


class Torus_Record:
    def __init__(self, rx,tx,out_dir,in_dir,lamda):
        self.rx=int(rx)
        self.tx=int(tx)
        self.out_dir=str(out_dir)
        self.in_dir=str(in_dir)
        self.lamda=int(lamda)

    def show(self):
        print('rx='+str(self.rx)+',indir='+str(self.in_dir))

