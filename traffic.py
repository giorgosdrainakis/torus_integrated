import csv
import math

from torus_integrated import myglobal

class Packet:
    def __init__(self,packet_id,time,packet_size,packet_qos,source_id,
                 tor_id,destination_id,destination_tor):
        self.packet_id=int(packet_id)
        self.time=float(time)
        self.packet_size=float(packet_size)
        self.packet_qos=packet_qos
        self.source_id=int(source_id)
        self.destination_id=int(destination_id)
        self.tor_id=int(tor_id)
        self.destination_tor=int(destination_tor)
        self.time_intra_buffer_in=-1
        self.time_intra_buffer_out=-1
        self.time_intra_trx_in=-1
        self.time_intra_trx_out=-1
        self.time_tor_buffer_in=-1
        self.time_tor_buffer_out=-1
        self.time_tor_trx_in=-1
        self.time_tor_trx_out=-1
        self.time_inter_buffer_in=-1
        self.time_inter_buffer_out=-1
        self.time_inter_trx_in=-1
        self.time_inter_trx_out=-1
        self.channel_id=0
        self.annotated=False

    def is_intra(self):
        return (self.tor_id==self.destination_tor)

    def show_mini(self):
        outp='id='+str(self.packet_id)+',source='+str(self.tor_id)+'-'+str(self.source_id)+',dest='+\
             str(self.destination_tor)+'-'+str(self.destination_id)
        return outp

    def show(self):
        outp=str(self.packet_id)+','+\
             str(self.time) + ','+\
            str(self.packet_size) + ',' +\
                str(self.packet_qos) + ',' +\
             str(self.source_id) + ',' + \
             str(self.tor_id) + ',' + \
             str(self.destination_id) + ','+ \
             str(self.destination_tor) + ',' + \
             str(self.time_intra_buffer_in) + ',' + \
             str(self.time_intra_buffer_out) + ',' + \
             str(self.time_intra_trx_in) + ',' + \
             str(self.time_intra_trx_out) + ',' + \
             str(self.time_tor_buffer_in) + ',' + \
             str(self.time_tor_buffer_out) + ',' + \
             str(self.time_tor_trx_in) + ',' + \
             str(self.time_tor_trx_out) + ',' + \
             str(self.time_inter_buffer_in) + ',' + \
             str(self.time_inter_buffer_out) + ',' + \
             str(self.time_inter_trx_in) + ',' + \
             str(self.time_inter_trx_out)
        return outp
class Traffic_per_packet():
    def __init__(self,file):
        self.db=[]
        self.load(file)

    def load(self,file):
        with open(myglobal.ROOT+myglobal.TRAFFIC_DATASETS_FOLDER+file) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                new_packet = Packet(row['packet_id'], row['time'], row['packet_size'],row['packet_qos'],
                                    row['source_id'],row['tor_id'],row['destination_id'],row['destination_tor']
                                    )
                self.add(new_packet)

    def add(self,packet):
        self.db.append(packet)

    def get_next_arrival(self,current_time):
        for packet in self.db:
            if packet.time>=current_time:
                return packet.time

    def get_new_packets(self,current_time):
        packet_list=[]
        for packet in self.db:
            #if math.isclose(current_time,packet.time,abs_tol=myglobal.TOLERANCE): # legacy
            if packet.time<=current_time:
                # if not account for inter traffic and come up with inter packet, remove it
                if myglobal.INTRA_REMOVE_INTER and (not packet.is_intra()):
                    pass
                else:
                    packet_list.append(packet)
                self.db.remove(packet)
            else:
                break
        return packet_list

class Control_Packet:
    def __init__(self,time,source_id):
        self.time=float(time)
        self.source_id=int(source_id)
        self.time_intra_trx_in=-1
        self.time_intra_trx_out=-1
        self.packet_size=0 #bytes
        self.channel_id=0
        self.is_bonus_packet=False
        self.bonus_info=None
        self.annotated=False
        self.minipack_list=[]








