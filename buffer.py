import csv
from torus_integrated import myglobal

class Intra_Buffer():
    def __init__(self,size,parent_tor_id):
        self.size=size
        self.db=[]
        self.parent_tor_id=parent_tor_id

    def has_packets(self):
        if len(self.db)>0:
            return True

    def remove_packet(self,id):
        for pack in self.db:
            if pack.id==id:
                self.db.remove(pack)
                break

    def get_next_packet(self):
        mypacket=self.db[0]
        self.db.pop(0)
        return mypacket

    def add(self,packet,current_time):
        current_buffer_size=self.get_current_size()
        if current_buffer_size+packet.packet_size<=self.size:
            if packet.is_intra():
                packet.time_intra_buffer_in=current_time
            else:
                if self.parent_tor_id == packet.tor_id:  # packet is still in source Tor
                    packet.time_intra_buffer_in=current_time
                else:
                    packet.time_inter_buffer_in = current_time # packet in dest TOR
            self.db.append(packet)
            return True
        else:
            return False #drop

    def delete_by_id(self,id):
        for element in self.db:
            if element.id==id:
                self.db.remove(element)
                break

    def encode_packet_WAA(self,pos):
        mystr = []
        if len(self.db)>pos:
            current_packet=self.db[pos]
            #todo
        else:
            for i in range(0,myglobal.WAA_packet_image_bits):
                mystr.append(-1)
            return mystr

    def get_current_size(self):
        mysize=0
        for element in self.db:
            mysize=mysize+element.packet_size
        return mysize


class Tor_Buffer():
    def __init__(self,size,destination_tor):
        self.size=size
        self.db=[]
        self.destination_tor=int(destination_tor)

    def has_packets(self):
        if len(self.db)>0:
            return True

    def remove_packet(self,id):
        for pack in self.db:
            if pack.id==id:
                self.db.remove(pack)
                break

    def get_next_packet(self):
        mypacket=self.db[0]
        self.db.pop(0)
        return mypacket

    def add(self,packet,current_time):
        current_buffer_size=self.get_current_size()
        if current_buffer_size+packet.packet_size<=self.size:
            packet.time_tor_buffer_in=current_time
            self.db.append(packet)
            return True
        else:
            return False #drop

    def delete_by_id(self,id):
        for element in self.db:
            if element.id==id:
                self.db.remove(element)
                break

    def get_current_size(self):
        mysize=0
        for element in self.db:
            mysize=mysize+element.packet_size
        return mysize
