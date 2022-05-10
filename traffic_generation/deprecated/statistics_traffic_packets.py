import csv
import math
import os
import random
from torus_integrated import myglobal

class Packet:
    def __init__(self,packet_id,time,packet_size,packet_qos, source_id, tor_id, destination_id, destination_tor):
        self.packet_id=int(packet_id)
        self.time=float(time)
        self.packet_size=float(packet_size)
        self.packet_qos=packet_qos
        self.source_id=int(source_id)
        self.tor_id=int(tor_id)
        self.destination_id=int(destination_id)
        self.destination_tor=int(destination_tor)

    def is_intra(self):
        return (self.tor_id == self.destination_tor)

    def is_intra_for_tor(self, parent_tor_id):
        return (self.is_intra() and self.tor_id == parent_tor_id)

    def is_outgoing_for_tor(self, parent_tor_id):
        return ((not self.is_intra()) and self.tor_id == parent_tor_id)

    def is_incoming_for_tor(self, parent_tor_id):
        return ((not self.is_intra()) and self.destination_tor == parent_tor_id)
datasets_main_folder='C:\\Pycharm\\Projects\\polydiavlika\\torus_integrated\\traffic_datasets'
#traffic_dataset_folder='torus1200_highin' #84-16
traffic_dataset_folder='torus2400_highin_intra075_10ms'
tors=16
servers=16

traffic_dataset_folder=os.path.join(datasets_main_folder,traffic_dataset_folder)
print('Statistics for dataset folder='+str(traffic_dataset_folder))
my_db=[]
for tor_id in range(1,tors+1):
    for server_id in range(1,servers+1):
        node_csv='tor'+str(tor_id)+'node'+str(server_id)+'.csv'
        filename = os.path.join(traffic_dataset_folder,node_csv)
        with open(filename) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                new_pack=Packet(row['packet_id'],row['time'],row['packet_size'],row['packet_qos'],
                               row['source_id'], row['tor_id'], row['destination_id'], row['destination_tor'])
                my_db.append(new_pack)

per_tor_load=[]
for tor_id in range(1,tors+1):
    per_tor_load.append(0)

intra_high_bytes=0
intra_high_packets=0
intra_med_bytes=0
intra_med_packets=0
intra_low_bytes=0
intra_low_packets=0
inter_high_bytes=0
inter_high_packets=0
inter_med_bytes=0
inter_med_packets=0
inter_low_bytes=0
inter_low_packets=0
total_bytes=0
total_packets=0
intra_bytes=0
intra_packets=0
inter_bytes=0
inter_packets=0
high_bytes=0
high_packets=0
med_bytes=0
med_packets=0
low_bytes=0
low_packets=0

dbg=0
for pack in my_db:
    print(str(100*dbg/len(my_db)))
    total_packets=total_packets+1
    total_bytes=total_bytes+pack.packet_size

    per_tor_load[pack.tor_id]=per_tor_load[pack.tor_id]+pack.packet_size


    if pack.is_intra():
        intra_packets=intra_packets+1
        intra_bytes=intra_bytes+pack.packet_size
        if pack.packet_qos=='high':
            high_packets=high_packets+1
            high_bytes=high_bytes+pack.packet_size
            intra_high_packets=intra_high_packets+1
            intra_high_bytes=intra_high_bytes+pack.packet_size
        elif pack.packet_qos=='med':
            med_packets = med_packets + 1
            med_bytes = med_bytes + pack.packet_size
            intra_med_packets = intra_med_packets + 1
            intra_med_bytes = intra_med_bytes + pack.packet_size
        elif pack.packet_qos=='low':
            low_packets = low_packets + 1
            low_bytes = low_bytes + pack.packet_size
            intra_low_packets = intra_low_packets + 1
            intra_low_bytes = intra_low_bytes + pack.packet_size
    else:
        inter_packets=inter_packets+1
        inter_bytes=inter_bytes+pack.packet_size
        if pack.packet_qos=='high':
            high_packets=high_packets+1
            high_bytes=high_bytes+pack.packet_size
            inter_high_packets=inter_high_packets+1
            inter_high_bytes=inter_high_bytes+pack.packet_size
        elif pack.packet_qos=='med':
            med_packets = med_packets + 1
            med_bytes = med_bytes + pack.packet_size
            inter_med_packets = inter_med_packets + 1
            inter_med_bytes = inter_med_bytes + pack.packet_size
        elif pack.packet_qos=='low':
            low_packets = low_packets + 1
            low_bytes = low_bytes + pack.packet_size
            inter_low_packets = inter_low_packets + 1
            inter_low_bytes = inter_low_bytes + pack.packet_size
    dbg=dbg+1

verification_matrix=[]
verification_matrix.append(total_packets-intra_packets-inter_packets)
verification_matrix.append(total_bytes-intra_bytes-inter_bytes)
verification_matrix.append(total_packets-high_packets-med_packets-low_packets)
verification_matrix.append(total_bytes-high_bytes-med_bytes-low_bytes)
verification_matrix.append(intra_packets-intra_high_packets-intra_med_packets-intra_low_packets)
verification_matrix.append(intra_bytes-intra_high_bytes-intra_med_bytes-intra_low_bytes)
verification_matrix.append(inter_packets-inter_high_packets-inter_med_packets-inter_low_packets)
verification_matrix.append(inter_bytes-inter_high_bytes-inter_med_bytes-inter_low_bytes)

print('Verify measurements')
i=0
for ver in verification_matrix:
    if ver!=0:
        print('Error in position'+str(i))
    else:
        print('OK in position'+str(i))
    i=i+1
print('----')
print('Total packets='+str(total_packets))
print('Total bytes='+str(total_bytes))
print('Total high packets='+str(high_packets)+',perc%='+str(100*high_packets/total_packets))
print('Total high bytes='+str(high_bytes)+',perc%='+str(100*high_bytes/total_bytes))
print('Total med packets='+str(med_packets)+',perc%='+str(100*med_packets/total_packets))
print('Total med bytes='+str(med_bytes)+',perc%='+str(100*med_bytes/total_bytes))
print('Total low packets='+str(med_packets)+',perc%='+str(100*low_packets/total_packets))
print('Total low bytes='+str(med_bytes)+',perc%='+str(100*low_bytes/total_bytes))
print('----')
print('Total intra packets='+str(intra_packets)+',perc%='+str(100*intra_packets/total_packets))
print('Total intra bytes='+str(intra_bytes)+',perc%='+str(100*intra_bytes/total_bytes))
print('Total inter packets='+str(inter_packets)+',perc%='+str(100*inter_packets/total_packets))
print('Total inter bytes='+str(inter_bytes)+',perc%='+str(100*inter_bytes/total_bytes))
print('----')
print('Total high intra packets='+str(intra_high_packets)+',perc%='+str(100*intra_high_packets/intra_packets))
print('Total high intra bytes='+str(intra_high_bytes)+',perc%='+str(100*intra_high_bytes/intra_bytes))
print('Total high inter packets='+str(inter_high_packets)+',perc%='+str(100*inter_high_packets/inter_packets))
print('Total high inter bytes='+str(inter_high_bytes)+',perc%='+str(100*inter_high_bytes/inter_bytes))
print('Total med intra packets='+str(intra_med_packets)+',perc%='+str(100*intra_med_packets/intra_packets))
print('Total med intra bytes='+str(intra_med_bytes)+',perc%='+str(100*intra_med_bytes/intra_bytes))
print('Total med inter packets='+str(inter_med_packets)+',perc%='+str(100*inter_med_packets/inter_packets))
print('Total med inter bytes='+str(inter_med_bytes)+',perc%='+str(100*inter_med_bytes/inter_bytes))
print('Total low intra packets='+str(intra_low_packets)+',perc%='+str(100*intra_low_packets/intra_packets))
print('Total low intra bytes='+str(intra_low_bytes)+',perc%='+str(100*intra_low_bytes/intra_bytes))
print('Total low inter packets='+str(inter_low_packets)+',perc%='+str(100*inter_low_packets/inter_packets))
print('Total low inter bytes='+str(inter_low_bytes)+',perc%='+str(100*inter_low_bytes/inter_bytes))
print('----')
for tor_id in range(1,tors+1):
    print('Tor'+str(tor_id)+',bytes:'+str(per_tor_load[tor_id]))