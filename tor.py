import itertools
import math
import random
from torus_integrated import myglobal
from torus_integrated.channel import *
from torus_integrated.traffic import Control_Packet
from torus_integrated.transmission_info.torus_matrix import *
import datetime
import pandas as pd

class Tors:
    def __init__(self):
        self.db=[]
        self.channels=None
        self.torus_list=None
        self.current_cycle = 0

    def get_per_cycle_time(self):
        return (myglobal.MAX_PACKET_SIZE*8)/self.channels.get_common_bitrate()

    def is_new_cycle(self,current_time):
        cycle_time = self.get_per_cycle_time()
        entered_new_cycle = (current_time >= cycle_time * self.current_cycle)
        if entered_new_cycle:
            self.current_cycle = self.current_cycle + 1
        return entered_new_cycle

    def inter_transmit(self,current_time):
        if self.is_new_cycle(current_time):
            print('Entered new inter cycle=' + str(self.current_cycle) + ' at=' + str(current_time))

            # Get list of all per tor requests
            all_tors_actual_requests=[]
            all_tors_backup_requests=[]
            for tor in self.db:
                actual,backup=tor.check_per_tor_requests()
                all_tors_actual_requests.extend(actual)
                all_tors_backup_requests.extend(backup)
            all_tors_backup_requests.sort(key=lambda x: x.size, reverse=True)
            chosen_reqs = []

            # First try to fit it all actual (big) requests from each TOR (maximize size policy)
            for actual_req in all_tors_actual_requests:
                can_enter=True
                need_swap=False
                old_rec_to_swap=None

                for chosen_req in chosen_reqs:
                    if actual_req.rx==chosen_req.rx and actual_req.in_dir==chosen_req.in_dir:#*-+ and actual_req.lamda==chosen_req.lamda:
                        # check if swap
                        if actual_req.size>chosen_req.size:
                            need_swap=True
                            old_rec_to_swap=chosen_req
                        else:
                            can_enter = False
                if can_enter:
                    chosen_reqs.append(actual_req)
                    if need_swap:
                        chosen_reqs.remove(old_rec_to_swap)

            # If empty space in the tx train, add backup reqs
            max_allowed_reqs=myglobal.INTER_TX_PER_TOR*myglobal.TOTAL_TORS
            i=0
            while ((len(chosen_reqs)<max_allowed_reqs) and (i<len(all_tors_backup_requests))):
                backup_req=all_tors_backup_requests[i]
                current_txs = 0
                is_conflict=False
                # check if conflict at receiver or backup req will exceed number of max_allowed_transmissions per TOR
                for chosen_req in chosen_reqs:
                    if chosen_req.tx == backup_req.tx:
                        current_txs=current_txs+1
                    if backup_req.rx == chosen_req.rx and backup_req.in_dir == chosen_req.in_dir:
                        is_conflict=True
                # if ok, add to chosen requests
                if ((not is_conflict) and (current_txs<myglobal.INTER_TX_PER_TOR)):
                    chosen_reqs.append(backup_req)
                i=i+1

            # debug
            print('INTER will transmit a total of recs='+str(len(chosen_reqs)))
            for el in chosen_reqs:
                el.show()

            for tor in self.db:
                tor.inter_transmit(current_time,chosen_reqs)

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
        tor_names=[]
        # log for each tor
        for tor in self.db:
            tor_names.append(tor.write_log(real_time))

        combined_csv = pd.concat([pd.read_csv(f) for f in tor_names])
        combined_name = myglobal.ROOT + myglobal.LOGS_FOLDER + 'log' + str(real_time) + '_everything.csv'
        combined_csv.to_csv(combined_name, index=False)

        #print('Sorting ALL:')
        #with open(combined_name, 'r', newline='') as f_input:
        #    csv_input = csv.DictReader(f_input)
        #    data = sorted(csv_input, key=lambda row: (float(row['time']), float(row['packet_id'])))

        #print('Rewriting ALL:')
        #with open(combined_name, 'w', newline='') as f_output:
        #    csv_output = csv.DictWriter(f_output, fieldnames=csv_input.fieldnames)
        #    csv_output.writeheader()
        #    csv_output.writerows(data)

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
        self.torus_matrix = Torus_Matrix()

    def add_inter_packet_to_local_tor(self,pack,current_time):
        self.nodes.add_inter_packet_to_local_tor(pack,current_time)

    def check_per_tor_requests(self):
        # 1) Each TOR makes a total request to transmit (sub-requests) to all trx_directions.
        # 2) Each sub-request (1500-message) must be targeted to one destination (rx). Cannot couple multiple.
        # 3) Each sub-request has a maximum size of trx window (1500)
        rx_torus_rec_list=[]
        for rx_id in range(1, myglobal.TOTAL_TORS + 1):
            if rx_id!=self.id:
                can_fill_with_bigs = False
                for out_buffer in self.outgoing_buffers_med_list:
                    # find buffer according to rx id
                    if out_buffer.destination_tor == rx_id:
                        if out_buffer.has_packets() and out_buffer.db[0].packet_size == myglobal.MAX_PACKET_SIZE:
                            can_fill_with_bigs = True
                if not can_fill_with_bigs:
                    for out_buffer in self.outgoing_buffers_low_list:
                        # find buffer according to rx id
                        if out_buffer.destination_tor == rx_id:
                            if out_buffer.has_packets() and out_buffer.db[0].packet_size == myglobal.MAX_PACKET_SIZE:
                                can_fill_with_bigs = True
                if not can_fill_with_bigs:
                    fill_with_smalls_size = 0
                    for out_buffer in self.outgoing_buffers_high_list:
                        # find buffer according to rx id
                        if out_buffer.destination_tor == rx_id:
                            i = 0
                            while i < len(out_buffer.db) and out_buffer.db[i].packet_size < myglobal.MAX_PACKET_SIZE \
                                    and fill_with_smalls_size < (myglobal.MAX_PACKET_SIZE / myglobal.MIN_PACKET_SIZE):
                                i = i + 1
                                fill_with_smalls_size = fill_with_smalls_size + 1
                    for out_buffer in self.outgoing_buffers_med_list:
                        # find buffer according to rx id
                        if out_buffer.destination_tor == rx_id:
                            i = 0
                            while i < len(out_buffer.db) and out_buffer.db[i].packet_size < myglobal.MAX_PACKET_SIZE \
                                    and fill_with_smalls_size < (myglobal.MAX_PACKET_SIZE / myglobal.MIN_PACKET_SIZE):
                                i = i + 1
                                fill_with_smalls_size = fill_with_smalls_size + 1
                    for out_buffer in self.outgoing_buffers_low_list:
                        # find buffer according to rx id
                        if out_buffer.destination_tor == rx_id:
                            i = 0
                            while i < len(out_buffer.db) and out_buffer.db[i].packet_size < myglobal.MAX_PACKET_SIZE \
                                    and fill_with_smalls_size < (myglobal.MAX_PACKET_SIZE / myglobal.MIN_PACKET_SIZE):
                                i = i + 1
                                fill_with_smalls_size = fill_with_smalls_size + 1

                out_dir,in_dir,lamda=self.torus_matrix.get_trx_info_from_tx_rx_id(self.id,rx_id)
                new_torus_rec=Torus_Record(rx_id,self.id,out_dir,in_dir,lamda)
                if can_fill_with_bigs:
                    new_torus_rec.size=myglobal.MAX_PACKET_SIZE
                else:
                    new_torus_rec.size=fill_with_smalls_size*myglobal.MIN_PACKET_SIZE
                rx_torus_rec_list.append(new_torus_rec)

        # Split list into actual requests/backup requests according to max TRX for all directions
        rx_torus_rec_list.sort(key=lambda x: x.size, reverse=True)
        actual_list=rx_torus_rec_list[:myglobal.INTER_TX_PER_TOR]
        backup_list=rx_torus_rec_list[myglobal.INTER_TX_PER_TOR:]

        return actual_list,backup_list


    def build_15_lamda_request(self,rx_list):
        mylist=rx_list
        random.shuffle(mylist)
        tx=self.id
        return self.torus_list.get_15_lamda_request_from_rx_list(rx_list,tx)

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
            print('Tor'+str(self.id)+'(S)'+':Will InterTRXing bigs')
        else:
            print('Tor'+str(self.id)+'(S)'+':Will InterTRXing smalls='+str(fill_with_smalls_size))

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
            print('Tor'+str(self.id)+'(N)'+':Will InterTRXing bigs')
        else:
            print('Tor'+str(self.id)+'(N)'+':Will InterTRXing smalls='+str(fill_with_smalls_size))
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
            print('Tor'+str(self.id)+'(W)'+':Will InterTRXing bigs')
        else:
            print('Tor'+str(self.id)+'(W)'+':Will InterTRXing smalls='+str(fill_with_smalls_size))
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
            print('Tor'+str(self.id)+'(E)'+':Will InterTRXing bigs')
        else:
            print('Tor'+str(self.id)+'(E)'+':Will InterTRXing smalls='+str(fill_with_smalls_size))

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
        return combined_name

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





