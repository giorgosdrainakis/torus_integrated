import datetime
import pandas as pd
from waa.node import *
from waa.traffic import *
from waa.buffer import *
from waa.channel import *

def main():
    if MODE=='WAA':
        BITRATE=5e9
        channel_id_list = [100,200] # 2 data channel
        control_channel_id = 500 # 1 control channel
    else:
        print('Error - WRONG mode!')
        return -1

    # init node and channel list
    nodes=Nodes()

    # create nodes and channels
    for id in range(1,TOTAL_NODES+1):
        new_traffic=Traffic_per_packet(traffic_dataset_folder+'test'+str(id)+'.csv')
        new_node=Node(id,new_traffic)
        new_node.buffer_low=Buffer(LOW_BUFFER_SIZE)
        new_node.buffer_med=Buffer(MED_BUFFER_SIZE)
        new_node.buffer_high=Buffer(HIGH_BUFFER_SIZE)
        nodes.add_new(new_node)

    for id in channel_id_list:
        new_channel=Channel(id,BITRATE)
        nodes.channels.add_new(new_channel)

    if MODE=='WAA':
        control_channel=Channel(control_channel_id,BITRATE)
        nodes.control_channel=control_channel

    # run simulation
    CURRENT_TIME=T_BEGIN
    print('start 0/1000=' + str(datetime.datetime.now()))
    while CURRENT_TIME<=T_END*1.1:# or nodes.have_buffers_packets():
        nodes.add_new_packets_to_buffers(CURRENT_TIME)
        nodes.check_arrival_WAA(CURRENT_TIME)
        nodes.process_new_cycle(CURRENT_TIME)
        nodes.transmit_WAA(CURRENT_TIME)
        CURRENT_TIME=CURRENT_TIME+myglobal.timestep

    # print buffer etc. content
    print('FINISH!')
    mytime = str(datetime.datetime.now())
    mytime = mytime.replace('-', '_')
    mytime = mytime.replace(' ', '_')
    mytime = mytime.replace(':', '_')
    mytime = mytime.replace('.', '_')

    filenames=[]
    for node in nodes.db:
        output_table = 'packet_id,time,packet_size,packet_qos,source_id,destination_id,' \
                       'time_buffer_in,time_buffer_out,time_trx_in,time_trx_out,mode\n'
        print('id='+str(node.id))
        print('rx='+str(len(node.data_sent)))
        print('ovflow='+str(len(node.data_dropped)))
        print('---------')
        for packet in node.data_sent:
            output_table=output_table+packet.show()+'\n'
        for packet in node.data_dropped:
            output_table=output_table+packet.show()+'\n'

        print('Writing node +...'+str(node.id))
        nodename=myglobal.ROOT+'logs//' + 'log'+ mytime +'_for_node_'+  str(node.id) +".csv"
        with open(nodename, mode='a') as file:
            file.write(output_table)
            filenames.append(nodename)

    combined_csv = pd.concat([pd.read_csv(f) for f in filenames])
    combined_name=myglobal.ROOT+'logs//'+'combined'+str(mytime)+'.csv'
    combined_csv.to_csv(combined_name, index=False)

    print('Sorting...')
    with open(combined_name, 'r', newline='') as f_input:
        csv_input = csv.DictReader(f_input)
        data = sorted(csv_input, key=lambda row: (float(row['time']), float(row['packet_id'])))

    print('Rewriting...')
    with open(combined_name, 'w', newline='') as f_output:
        csv_output = csv.DictWriter(f_output, fieldnames=csv_input.fieldnames)
        csv_output.writeheader()
        csv_output.writerows(data)

    print('completeness 1000/1000=' + str(datetime.datetime.now()))


### params and run
MODE='WAA'
T_BEGIN = 0
T_END = 0.1
TOTAL_NODES =  8
HIGH_BUFFER_SIZE = 1e6 # bytes
MED_BUFFER_SIZE = 1e6 # bytes
LOW_BUFFER_SIZE = 1e6 # bytes
traffic_dataset_folder='2021_03_02_18_03_02_702107//'
main() # will create N logfiles for N nodes and a combined csv with all packets in root/logs