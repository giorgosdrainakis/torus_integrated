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
    elif MODE=='WAA_single':
        BITRATE=10e9
        channel_id_list = [100] # 1 data channel
        control_channel_id = 500 # 1 control channel
    elif MODE=='WAA_4':
        BITRATE=40e9
        channel_id_list = [100,200,300,400] # 1 data channel
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
    print('Found a total of new nodes='+str(len(nodes.db)))


    for id in channel_id_list:
        new_channel=Channel(id,BITRATE)
        nodes.channels.add_new(new_channel)

    control_channel=Channel(control_channel_id,BITRATE)
    nodes.control_channel=control_channel

    # run simulation
    CURRENT_TIME=T_BEGIN
    print('start 0/1000=' + str(datetime.datetime.now()))
    while CURRENT_TIME<=T_END or nodes.have_buffers_packets():
        if CURRENT_TIME<=T_END:
            nodes.add_new_packets_to_buffers(CURRENT_TIME)
        nodes.check_arrival_WAA(CURRENT_TIME)
        nodes.process_new_cycle(CURRENT_TIME)
        nodes.transmit_WAA(CURRENT_TIME)
        nodes.geodranas_consumption(CURRENT_TIME)
        # guard band
        CURRENT_TIME=CURRENT_TIME+myglobal.CYCLE_GUARD_BAND*8/BITRATE
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
                       'time_buffer_in,time_buffer_out,time_trx_in,time_trx_out,mode,consume_time\n'
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

    for node in nodes.db:
        if node.id==16:
            output_table = 'packet_id,time,packet_size,packet_qos,source_id,destination_id,' \
                           'time_buffer_in,time_buffer_out,time_trx_in,time_trx_out,mode,consume_time\n'

            for packet in node.receiver:
                output_table = output_table + packet.show() + '\n'
            for packet in node.consumed:
                output_table = output_table + packet.show() + '\n'

            print('Writing node +...' + str(node.id))
            nodename = myglobal.ROOT + 'logs//' + 'log' + mytime + '_for_TOR_' + str(node.id) + ".csv"
            with open(nodename, mode='a') as file:
                file.write(output_table)

            print('Sorting...')
            with open(nodename, 'r', newline='') as f_input:
                csv_input = csv.DictReader(f_input)
                data = sorted(csv_input, key=lambda row: (float(row['time']), float(row['packet_id'])))

            print('Rewriting...')
            with open(nodename, 'w', newline='') as f_output:
                csv_output = csv.DictWriter(f_output, fieldnames=csv_input.fieldnames)
                csv_output.writeheader()
                csv_output.writerows(data)

            print('completeness 1000/1000=' + str(datetime.datetime.now()))

### params and run
MODE='WAA_4'
T_BEGIN = 0
T_END = 0.01
TOTAL_NODES =  16
if TOTAL_NODES==4:
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 46
    # node description string
    myglobal.STR_SOURCE_DEST_ID = "{0:02b}"
    # define minipack
    myglobal.CONTROL_MINIPACK_SIZE = 7  # bits
    myglobal.CUT_1 = 2
    myglobal.CUT_2 = 4
    myglobal.CUT_3 = 6
    # define bonus msg
    myglobal.BONUS_MSG_BITSIZE = 6  # bits
    myglobal.BREAK_POSITION=2
    # define len of lucky and unlucky slots
    myglobal.LUCKY_SLOT_LEN = 6
    myglobal.UNLUCKY_SLOT_LEN = 5
    # define number of lucky/unlucky nodes per cycle
    myglobal.TOTAL_UNLUCKY_NODES=1
    myglobal.TOTAL_LUCKY_NODES=TOTAL_NODES-myglobal.TOTAL_UNLUCKY_NODES
elif TOTAL_NODES==8:
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 46
    # node description string
    myglobal.STR_SOURCE_DEST_ID = "{0:03b}"
    # define minipack
    myglobal.CONTROL_MINIPACK_SIZE = 9  # bits
    myglobal.CUT_1 = 3
    myglobal.CUT_2 = 6
    myglobal.CUT_3 = 8
    # define bonus msg
    myglobal.BONUS_MSG_BITSIZE = 7  # bits
    myglobal.BREAK_POSITION=3
    # define len of lucky and unlucky slots
    myglobal.LUCKY_SLOT_LEN = 3
    myglobal.UNLUCKY_SLOT_LEN = 2
    # define number of lucky/unlucky nodes per cycle
    myglobal.TOTAL_UNLUCKY_NODES=1
    myglobal.TOTAL_LUCKY_NODES=TOTAL_NODES-myglobal.TOTAL_UNLUCKY_NODES
elif TOTAL_NODES==12:
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 29
    # node description string
    myglobal.STR_SOURCE_DEST_ID = "{0:04b}"
    # define minipack
    myglobal.CONTROL_MINIPACK_SIZE = 11  # bits
    myglobal.CUT_1 = 4
    myglobal.CUT_2 = 8
    myglobal.CUT_3 = 10
    # define bonus msg
    myglobal.BONUS_MSG_BITSIZE = 8  # bits
    myglobal.BREAK_POSITION=4
    # define len of lucky and unlucky slots
    myglobal.LUCKY_SLOT_LEN = 2
    myglobal.UNLUCKY_SLOT_LEN = 1
    # define number of lucky/unlucky nodes per cycle
    myglobal.TOTAL_UNLUCKY_NODES=1
    myglobal.TOTAL_LUCKY_NODES=TOTAL_NODES-myglobal.TOTAL_UNLUCKY_NODES
elif TOTAL_NODES==16:
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 17
    # node description string
    myglobal.STR_SOURCE_DEST_ID = "{0:04b}"
    # define minipack
    myglobal.CONTROL_MINIPACK_SIZE = 11  # bits
    myglobal.CUT_1 = 4
    myglobal.CUT_2 = 8
    myglobal.CUT_3 = 10
    # define bonus msg
    myglobal.BONUS_MSG_BITSIZE = 8  # bits
    myglobal.BREAK_POSITION=4
    # define len of lucky and unlucky slots
    myglobal.LUCKY_SLOT_LEN = 2
    myglobal.UNLUCKY_SLOT_LEN = 1
    # define number of lucky/unlucky nodes per cycle
    myglobal.TOTAL_UNLUCKY_NODES=9
    myglobal.TOTAL_LUCKY_NODES=TOTAL_NODES-myglobal.TOTAL_UNLUCKY_NODES
else:
    print('Error with number of server')


HIGH_BUFFER_SIZE = 1e6 # bytes
MED_BUFFER_SIZE = 1e6 # bytes
LOW_BUFFER_SIZE = 1e6 # bytes
traffic_dataset_folder='torus//'
main() # will create N logfiles for N nodes and a combined csv with all packets in root/logs