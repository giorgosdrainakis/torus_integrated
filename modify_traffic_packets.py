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
                source_id = random.choice(my_source_id)
                destination_possible=[item for item in my_dest_list if item!= source_id]
                destination_id = random.choice(destination_possible)
                packet_id=packet_id+1
                new_packet = Packet(packet_id,row['time'],row['packet_size'],row['packet_qos'],source_id,destination_id)
                packet_list.append(new_packet)
        print('Len packet list='+str(len(packet_list)))

    for i in range(0,len(my_source_id_list)):
        output_table = 'packet_id,time,packet_size,packet_qos,source_id,destination_id\n'
        for packet in packet_list:
            if packet.source_id==my_source_id[i]:
                output_table = output_table + packet.show() + '\n'

        with open(myglobal.ROOT + myglobal.TRAFFIC_DATASETS_FOLDER +folder_name+ final_file_name[i], mode='a') as file:
            file.write(output_table)

        print('Sorting...')
        with open(myglobal.ROOT + myglobal.TRAFFIC_DATASETS_FOLDER +folder_name+ final_file_name[i], 'r', newline='') as f_input:
            csv_input = csv.DictReader(f_input)
            data = sorted(csv_input, key=lambda row: (float(row['time']), float(row['packet_id'])))

        print('Rewriting...')
        with open(myglobal.ROOT + myglobal.TRAFFIC_DATASETS_FOLDER +folder_name+ final_file_name[i], 'w', newline='') as f_output:
            csv_output = csv.DictWriter(f_output, fieldnames=csv_input.fieldnames)
            csv_output.writeheader()
            csv_output.writerows(data)

folder_name='0.2sec_m12\\'
file_list=['test1.csv','test2.csv']
final_file_name=['testA.csv','testB.csv','testC.csv']
my_source_id_list=[1,2,3]
my_dest_list=[1,2,3,4,5,6,7,8,9,10,11,12]
modify(file_list,final_file_name,my_source_id_list,my_dest_list)
#gia ta 12 i file_list tha einai p.x. test1,test2, final_name tha ine list testA,testB,testC,mysource_list=rand(1,2) kai ant
# antistoixa ta destination. des kai mesa pos tha ta dtixeis me listes kai also na dinei 3 arxeia me swsti taxinomisi
# also change plooter to print per server drop,thru,etc
# ola aytes oi periptwseis pou exw gia ta M isxyoun gia 2 kanalia, sto 1 prepei to reboot
# git push ton edw kodika