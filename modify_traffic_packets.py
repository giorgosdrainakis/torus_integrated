import csv
import math
import random

from waa import myglobal

class Packet:
    def __init__(self,packet_id,time,packet_size,packet_qos,source_id,destination_id):
        self.packet_id=int(packet_id)
        self.time=float(time)
        self.packet_size=float(packet_size)
        self.packet_qos=packet_qos
        self.source_id=source_id
        self.destination_id=destination_id
    def show(self):
        outp=str(self.packet_id)+','+\
             str(self.time) + ','+\
            str(self.packet_size) + ',' +\
                str(self.packet_qos) + ',' +\
                str(self.source_id) + ','+ \
                str(self.destination_id)
        return outp

def modify(file_list,final_file_name,my_source_id,my_dest_list):
    packet_list = []
    packet_id=0
    for file in file_list:
        with open(myglobal.ROOT + myglobal.TRAFFIC_DATASETS_FOLDER +folder_name+ file) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                source_id = my_source_id
                destination_id = random.choice(my_dest_list)
                packet_id=packet_id+1
                new_packet = Packet(packet_id,row['time'],row['packet_size'],row['packet_qos'],source_id,destination_id)
                packet_list.append(new_packet)
        print('Len packet list='+str(len(packet_list)))

    output_table = 'packet_id,time,packet_size,packet_qos,source_id,destination_id\n'
    for packet in packet_list:
        output_table = output_table + packet.show() + '\n'

    with open(myglobal.ROOT + myglobal.TRAFFIC_DATASETS_FOLDER +folder_name+ final_file_name, mode='a') as file:
        file.write(output_table)

    print('Sorting...')
    with open(myglobal.ROOT + myglobal.TRAFFIC_DATASETS_FOLDER +folder_name+ final_file_name, 'r', newline='') as f_input:
        csv_input = csv.DictReader(f_input)
        data = sorted(csv_input, key=lambda row: (float(row['time']), float(row['packet_id'])))

    print('Rewriting...')
    with open(myglobal.ROOT + myglobal.TRAFFIC_DATASETS_FOLDER +folder_name+ final_file_name, 'w', newline='') as f_output:
        csv_output = csv.DictWriter(f_output, fieldnames=csv_input.fieldnames)
        csv_output.writeheader()
        csv_output.writerows(data)

folder_name='0.2sec_test\\'

file_list=['test1.csv','test5.csv']
final_file_name='testA.txt'
my_source_id=1
my_dest_list=[2,3,4]
modify(file_list,final_file_name,my_source_id,my_dest_list)