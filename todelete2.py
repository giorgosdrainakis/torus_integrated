import csv
import math
import random

from waa import myglobal

file_list=['test1.csv','test5.csv']
packet_list=[]
final_file_name='testA'
class Packet:
    def __init__(self,packet_id,time,packet_size,packet_qos,source_id,destination_id):
        self.packet_id=int(packet_id)
        self.time=float(time)
        self.packet_size=float(packet_size)
        self.packet_qos=packet_qos
        self.source_id=1
        self.destination_id=random.randint(2, 4)
    def show(self):
        outp=str(self.packet_id)+','+\
             str(self.time) + ','+\
            str(self.packet_size) + ',' +\
                str(self.packet_qos) + ',' +\
                str(self.source_id) + ','+ \
                str(self.destination_id)
        return outp

for file in file_list:
    with open(myglobal.ROOT + myglobal.TRAFFIC_DATASETS_FOLDER +'0.2sec_m4\\'+ file) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        packet_id=1
        for row in csv_reader:
            new_packet = Packet(packet_id, row['time'], row['packet_size'], row['packet_qos'], row['source_id'],
                                row['destination_id'])
            packet_id=packet_id+1
            packet_list.append(new_packet)
    print('Len packet list='+str(len(packet_list)))

output_table = 'packet_id,time,packet_size,packet_qos,source_id,destination_id,' \
               'time_buffer_in,time_buffer_out,time_trx_in,time_trx_out,mode\n'
for packet in packet_list:
    output_table = output_table + packet.show() + '\n'

with open(final_file_name, mode='a') as file:
    file.write(output_table)

print('Sorting...')
with open(final_file_name, 'r', newline='') as f_input:
    csv_input = csv.DictReader(f_input)
    data = sorted(csv_input, key=lambda row: (float(row['time']), float(row['packet_id'])))

print('Rewriting...')
with open(final_file_name, 'w', newline='') as f_output:
    csv_output = csv.DictWriter(f_output, fieldnames=csv_input.fieldnames)
    csv_output.writeheader()
    csv_output.writerows(data)