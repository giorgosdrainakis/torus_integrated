import datetime
import pandas as pd
from torus_integrated.node import *
from torus_integrated.traffic import *
from torus_integrated.buffer import *
from torus_integrated.channel import *
from torus_integrated.tor import *

def main():
    # init tors and torus_list
    tors=Tors()
    torus_list=Torus_Matrix()
    tors.torus_list=torus_list
    tors.channels=Channels()
    # create inter channel list
    for ch_id in myglobal.INTER_CHANNEL_ID_LIST:
        new_channel = Channel(ch_id, myglobal.INTER_CHANNEL_BITRATE)
        tors.channels.add_new(new_channel)
    print('Inter common bitrate=' +str(tors.channels.get_common_bitrate()))
    print('Total channes='+str(len(tors.channels.db)))
    # intra nodes and channes
    for tor_id in range(1,myglobal.TOTAL_TORS+1):
        new_tor=Tor(tor_id)
        new_tor.torus_list=torus_list
        for tor_dest_buff in range(1,myglobal.TOTAL_TORS+1):
            if tor_dest_buff!=tor_id:
                new_tor.outgoing_buffers_low_list.append(Tor_Buffer(myglobal.INTER_TOR_LOW_BUFFER_SIZE,tor_dest_buff))
                new_tor.outgoing_buffers_med_list.append(Tor_Buffer(myglobal.INTER_TOR_MED_BUFFER_SIZE, tor_dest_buff))
                new_tor.outgoing_buffers_high_list.append(Tor_Buffer(myglobal.INTER_TOR_HIGH_BUFFER_SIZE, tor_dest_buff))

        # create Tor's nodes
        nodes = Nodes(tor_id)
        for node_id in range(1, myglobal.TOTAL_NODES_PER_TOR + 1):
            new_traffic = Traffic_per_packet('tor' + str(tor_id) +'node'+str(node_id)+'.csv')
            new_node = Node(node_id,tor_id,new_traffic)
            new_node.intra_buffer_low = Intra_Buffer(myglobal.INTRA_NODE_INPUT_LOW_BUFFER_SIZE,tor_id)
            new_node.intra_buffer_med = Intra_Buffer(myglobal.INTRA_NODE_INPUT_MED_BUFFER_SIZE,tor_id)
            new_node.intra_buffer_high = Intra_Buffer(myglobal.INTRA_NODE_INPUT_HIGH_BUFFER_SIZE,tor_id)
            if node_id==myglobal.TOTAL_NODES_PER_TOR:
                new_node.is_tor=True
            nodes.add_new(new_node)
        # create Tor's intra data channels
        for ch_id in myglobal.INTRA_CHANNEL_ID_LIST:
            new_channel = Channel(ch_id, myglobal.INTRA_CHANNEL_BITRATE)
            nodes.channels.add_new(new_channel)
        print('Intra common bitrate=' + str(nodes.channels.get_common_bitrate()))
        print('Total channes=' + str(len(nodes.channels.db)))
        # create Tor's intra control channels
        control_channel = Channel(myglobal.INTRA_CONTROL_CHANNEL_ID, myglobal.INTRA_CHANNEL_BITRATE)
        nodes.control_channel = control_channel
        # set Tor nodes and add to Tor DB
        new_tor.nodes=nodes
        tors.add_new(new_tor)
        print('Initializing TOR id'+str(tor_id)+',found new nodes=' + str(len(nodes.db)))

    # run simulation
    CURRENT_TIME=myglobal.T_BEGIN
    while CURRENT_TIME<=myglobal.T_END or tors.have_buffers_packets():
        if CURRENT_TIME<=myglobal.T_END:
            tors.add_new_packets_to_buffers(CURRENT_TIME)
        tors.check_arrival_intra(CURRENT_TIME)
        new_cycle=tors.process_new_cycle(CURRENT_TIME)
        tors.transmit_intra(CURRENT_TIME)
        if new_cycle:
            tors.inter_transmit(CURRENT_TIME)
        tors.inter_check_arrival(CURRENT_TIME)
        # guard band
        CURRENT_TIME=CURRENT_TIME+myglobal.CYCLE_GUARD_BAND*8/myglobal.INTRA_CHANNEL_BITRATE
        CURRENT_TIME=CURRENT_TIME+myglobal.timestep

    # print buffer etc. content
    print('FINISH!')
    tors.write_log()

### params and run
if myglobal.TOTAL_NODES_PER_TOR==4:
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
    myglobal.TOTAL_LUCKY_NODES=myglobal.TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
elif myglobal.TOTAL_NODES_PER_TOR==8:
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
    myglobal.TOTAL_LUCKY_NODES=myglobal.TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
elif myglobal.TOTAL_NODES_PER_TOR==12:
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
    myglobal.TOTAL_LUCKY_NODES=myglobal.TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
elif myglobal.TOTAL_NODES_PER_TOR==16:
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
    myglobal.TOTAL_LUCKY_NODES=myglobal.TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
else:
    print('ERROR - Main: Invalid number of nodes per tor')

main() # will create N logfiles for N nodes and a combined csv with all packets in root/logs