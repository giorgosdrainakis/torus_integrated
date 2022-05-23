import datetime
import time
import os
import pandas as pd
from torus_integrated.node import *
from torus_integrated.traffic import *
from torus_integrated.buffer import *
from torus_integrated.channel import *
from torus_integrated.tor import *
import sys

def main_torus_split():
    print('Torus split setup running...')
    tors=Tors()
    tors.create_tors(total_tors=_TOTAL_TORS)
    tors.create_inter_channels(total_inter_channels=_TOTAL_INTER_CHANNELS,inter_bitrate=_INTER_BITRATE,tx_per_tor=_TX_PER_TOR)
    tors.create_tor_outbound_buffers(buffer_size_low=_TOR_OUTBOUND_BUFFER_SIZE_LOW,buffer_size_med=_TOR_OUTBOUND_BUFFER_SIZE_MED,buffer_size_high=_TOR_OUTBOUND_BUFFER_SIZE_HIGH)
    tors.create_nodes()
    tors.init_nodes(total_nodes_per_tor=_TOTAL_NODES_PER_TOR,tor_node_id=_TOR_NODE_ID)
    tors.create_tor_inbound_buffers(buffer_size_low=_TOR_INBOUND_BUFFER_SIZE_LOW,buffer_size_med=_TOR_INBOUND_BUFFER_SIZE_MED,buffer_size_high=_TOR_INBOUND_BUFFER_SIZE_HIGH)
    tors.create_intra_data_channels(total_intra_data_channels=_TOTAL_INTRA_DATA_CHANNELS, intra_bitrate=_INTRA_BITRATE)
    tors.create_intra_control_channel(intra_control_channel_id=_INTRA_CONTROL_CHANNEL_ID)
    tors.create_intra_dedicated_data_channels_dl(total_intra_data_channels_dl=_TOTAL_INTRA_DEDICATED_DATA_CHANNELS_DL, intra_dedicated_bitrate=_INTRA_DEDICATED_BITRATE)
    tors.create_intra_dedicated_data_channels_ul(total_intra_data_channels_ul=_TOTAL_INTRA_DEDICATED_DATA_CHANNELS_UL, intra_dedicated_bitrate=_INTRA_DEDICATED_BITRATE)
    tors.create_intra_dedicated_control_channel(intra_dedicated_control_channel_id=_INTRA_DEDICATED_CONTROL_CHANNEL_ID)
    tors.create_intra_traffic_datasets(remove_inter=_REMOVE_INTER)
    tors.create_node_output_buffers_for_intra_packs(low_size=_NODE_OUTPUT_BUFFERS_FOR_INTRA_PACKS_SIZE_LOW,
                                                    med_size=_NODE_OUTPUT_BUFFERS_FOR_INTRA_PACKS_SIZE_MED,
                                                    high_size=_NODE_OUTPUT_BUFFERS_FOR_INTRA_PACKS_SIZE_HIGH)
    tors.create_node_output_buffers_for_inter_packs(low_size=_NODE_OUTPUT_BUFFERS_FOR_INTER_PACKS_SIZE_LOW,
                                                    med_size=_NODE_OUTPUT_BUFFERS_FOR_INTER_PACKS_SIZE_MED,
                                                    high_size=_NODE_OUTPUT_BUFFERS_FOR_INTER_PACKS_SIZE_HIGH)

    # run simulation
    CURRENT_TIME=_T_BEGIN
    while (CURRENT_TIME<=_T_END or tors.have_buffers_packets()): #and CURRENT_TIME<=myglobal.T_END*1.5:
        # add newly generated packets to intra buffers
        if CURRENT_TIME<=_T_END*1.01:
            tors.check_generated_packets(CURRENT_TIME,split=True)
        # intra network
        tors.check_arrival_intra_and_add_to_outbound_buffers(CURRENT_TIME)
        tors.process_new_cycle(CURRENT_TIME)
        tors.transmit_intra(CURRENT_TIME)
        # dedicated network UL
        tors.check_arrival_dedicated_ul_and_add_to_outbound_buffers(CURRENT_TIME)
        tors.process_new_cycle_dedicated_ul(CURRENT_TIME)
        tors.transmit_dedicated_ul(CURRENT_TIME)

        # dedicated network DL
        tors.check_arrival_dedicated_dl(CURRENT_TIME)
        tors.process_new_cycle_dedicated_dl(CURRENT_TIME)
        tors.transmit_dedicated_dl(CURRENT_TIME)

        # inter network
        tors.inter_check_arrival_and_add_to_inbound_buffers(CURRENT_TIME,split=True)
        tors.inter_transmit(CURRENT_TIME)
        # guard band
        #CURRENT_TIME=CURRENT_TIME+myglobal.INTRA_CYCLE_GUARD_BAND*8/tors.intra_bitrate
        CURRENT_TIME=CURRENT_TIME+_TIMESTEP

    # print buffer etc. content
    print('FINISH! Have buffers in packets?='+str(tors.have_buffers_packets()))
    tors.write_log()

def main_torus_integrated():
    print('Torus integrated setup running...')
    tors=Tors()
    tors.create_tors(total_tors=_TOTAL_TORS)
    tors.create_inter_channels(total_inter_channels=_TOTAL_INTER_CHANNELS,inter_bitrate=_INTER_BITRATE,tx_per_tor=_TX_PER_TOR)
    tors.create_tor_outbound_buffers(buffer_size_low=_TOR_OUTBOUND_BUFFER_SIZE_LOW,buffer_size_med=_TOR_OUTBOUND_BUFFER_SIZE_MED,buffer_size_high=_TOR_OUTBOUND_BUFFER_SIZE_HIGH)

    tors.create_nodes()
    tors.init_nodes(total_nodes_per_tor=_TOTAL_NODES_PER_TOR,tor_node_id=_TOR_NODE_ID)
    tors.create_intra_data_channels(total_intra_data_channels=_TOTAL_INTRA_DATA_CHANNELS, intra_bitrate=_INTRA_BITRATE)
    tors.create_intra_control_channel(intra_control_channel_id=_INTRA_CONTROL_CHANNEL_ID)
    tors.create_intra_traffic_datasets(remove_inter=_REMOVE_INTER)
    tors.create_node_output_buffers_for_intra_packs(low_size=_NODE_OUTPUT_BUFFERS_FOR_INTRA_PACKS_SIZE_LOW,
                                                    med_size=_NODE_OUTPUT_BUFFERS_FOR_INTRA_PACKS_SIZE_MED,
                                                    high_size=_NODE_OUTPUT_BUFFERS_FOR_INTRA_PACKS_SIZE_HIGH)

    # run simulation
    CURRENT_TIME=_T_BEGIN
    while (CURRENT_TIME<=_T_END or tors.have_buffers_packets()): #and CURRENT_TIME<=myglobal.T_END*1.5:
        # add newly generated packets to intra buffers
        if CURRENT_TIME<=_T_END*1.01:
            tors.check_generated_packets(CURRENT_TIME,split=False)
        # intra network
        tors.check_arrival_intra_and_add_to_outbound_buffers(CURRENT_TIME)
        tors.process_new_cycle(CURRENT_TIME)
        tors.transmit_intra(CURRENT_TIME)
        # inter network
        tors.inter_check_arrival_and_add_to_inbound_buffers(CURRENT_TIME,split=False)
        tors.inter_transmit(CURRENT_TIME)
        # guard band
        CURRENT_TIME=CURRENT_TIME+myglobal.INTRA_CYCLE_GUARD_BAND*8/tors.intra_bitrate
        CURRENT_TIME=CURRENT_TIME+_TIMESTEP

    # print buffer etc. content
    print('FINISH! Have buffers in packets?='+str(tors.have_buffers_packets()))
    tors.write_log()

_FRAMEWORK='split' # split
_T_BEGIN = 0
_T_END = 0.010
_TOTAL_TORS=16
_TOTAL_INTER_CHANNELS=8
_INTER_BITRATE=40e9
_TX_PER_TOR=4
_TOR_OUTBOUND_BUFFER_SIZE_LOW=1e6
_TOR_OUTBOUND_BUFFER_SIZE_MED=1e6
_TOR_OUTBOUND_BUFFER_SIZE_HIGH=1e6
_TOR_INBOUND_BUFFER_SIZE_LOW=1e6
_TOR_INBOUND_BUFFER_SIZE_MED=1e6
_TOR_INBOUND_BUFFER_SIZE_HIGH=1e6
_TOTAL_NODES_PER_TOR=16
_TOR_NODE_ID=16
_TOTAL_INTRA_DATA_CHANNELS=4
_INTRA_BITRATE=100e9
_INTRA_CONTROL_CHANNEL_ID=99
_REMOVE_INTER=False
_NODE_OUTPUT_BUFFERS_FOR_INTRA_PACKS_SIZE_LOW=1e6
_NODE_OUTPUT_BUFFERS_FOR_INTRA_PACKS_SIZE_MED=1e6
_NODE_OUTPUT_BUFFERS_FOR_INTRA_PACKS_SIZE_HIGH=1e6
_INTRA_GUARD_BAND=True
_SAVE_LOGS=False
_TIMESTEP = 0.8e-9 #-> NEED TOTAL_TIME MOD timestep=0 (sync!)

_TOTAL_INTRA_DEDICATED_DATA_CHANNELS_DL=1
_INTRA_DEDICATED_BITRATE=100e9
_TOTAL_INTRA_DEDICATED_DATA_CHANNELS_UL=1
_INTRA_DEDICATED_CONTROL_CHANNEL_ID=999
_NODE_OUTPUT_BUFFERS_FOR_INTER_PACKS_SIZE_LOW=1e6
_NODE_OUTPUT_BUFFERS_FOR_INTER_PACKS_SIZE_MED=1e6
_NODE_OUTPUT_BUFFERS_FOR_INTER_PACKS_SIZE_HIGH=1e6

################ params and run
if _SAVE_LOGS:
    real_time = str(datetime.datetime.now())
    real_time = real_time.replace('-', '_')
    real_time = real_time.replace(' ', '_')
    real_time = real_time.replace(':', '_')
    real_time = real_time.replace('.', '_')
    mystr='tmplogger'+str(real_time)+'.log'
    file=os.path.join(myglobal.LOGS_FOLDER,mystr)
    sys.stdout = open(file, "w")

if _TOTAL_NODES_PER_TOR==4:
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
    myglobal.TOTAL_LUCKY_NODES=_TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
elif _TOTAL_NODES_PER_TOR==8:
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
    myglobal.TOTAL_LUCKY_NODES=_TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
elif _TOTAL_NODES_PER_TOR==12:
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
    myglobal.TOTAL_LUCKY_NODES=_TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
elif _TOTAL_NODES_PER_TOR==16 and _INTRA_BITRATE==40e9:
    print('Running with 16 Servers - 16 tors at 40 Gbps')
    time.sleep(3)
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 16
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
    if _INTRA_GUARD_BAND: #
        myglobal.TOTAL_UNLUCKY_NODES=11 # 5*2+11*1
    else:
        myglobal.TOTAL_UNLUCKY_NODES=9 # 7*2+9*1
    myglobal.TOTAL_LUCKY_NODES=_TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
    myglobal.INTRA_CYCLE_GUARD_BAND=9 #byte!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
elif _TOTAL_NODES_PER_TOR==16 and _INTRA_BITRATE==100e9:
    print('Running with 16 Servers at 100 Gbps')
    time.sleep(3)
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 7
    # node description string
    myglobal.STR_SOURCE_DEST_ID = "{0:04b}"
    # define minipack
    myglobal.CONTROL_MINIPACK_SIZE = 11  # bits
    myglobal.CUT_1 = 4
    myglobal.CUT_2 = 8
    myglobal.CUT_3 = 10
    # define bonus msg
    myglobal.BONUS_MSG_BITSIZE = 8  # bits (=cut1+4)
    myglobal.BREAK_POSITION=4 #(cut1)
    # define len of lucky and unlucky slots
    myglobal.LUCKY_SLOT_LEN = 2
    myglobal.UNLUCKY_SLOT_LEN = 1
    # define number of lucky/unlucky nodes per cycle
    if _INTRA_GUARD_BAND: # total packs per cycle=22 (need to calculate)
        myglobal.TOTAL_UNLUCKY_NODES=15
    else:
        myglobal.TOTAL_UNLUCKY_NODES=9 # total packs per cycle=23 (need to calculate)
    myglobal.TOTAL_LUCKY_NODES=_TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
    myglobal.INTRA_CYCLE_GUARD_BAND=23 #byte
    myglobal.MAX_SLOTS_FOR_SMALL_PACKS=17
    myglobal.INTER_CYCLE_GUARD_BAND = 9  # bytes
    myglobal.DEDICATED_UL_CYCLE_GUARD_BAND = 23  # bytes
elif _TOTAL_NODES_PER_TOR==64 and _INTRA_BITRATE==10e9: #
    print('Running with 64 Servers with 10Gbps channel')
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 3
    # node description string
    myglobal.STR_SOURCE_DEST_ID = "{0:06b}"
    # define minipack
    myglobal.CONTROL_MINIPACK_SIZE = 15  # bits
    myglobal.CUT_1 = 6
    myglobal.CUT_2 = 12
    myglobal.CUT_3 = 14
    # define bonus msg
    myglobal.BONUS_MSG_BITSIZE = 10  # bits (=cut1+4)
    myglobal.BREAK_POSITION=6 #(cut1)
    # define len of lucky and unlucky slots
    myglobal.LUCKY_SLOT_LEN = 1
    myglobal.UNLUCKY_SLOT_LEN = 0
    # define number of lucky/unlucky nodes per cycle
    if _INTRA_GUARD_BAND: # total packs per cycle=22 (need to calculate)
        myglobal.TOTAL_UNLUCKY_NODES=42
    else:
        myglobal.TOTAL_UNLUCKY_NODES=41 # total packs per cycle=23 (need to calculate)
    myglobal.TOTAL_LUCKY_NODES=_TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
    myglobal.INTRA_CYCLE_GUARD_BAND=3 #byte
elif _TOTAL_NODES_PER_TOR==80 and _INTRA_BITRATE==5e9:
    print('Running with 80 Servers at 5 Gbps')
    time.sleep(3)
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 2
    # node description string
    myglobal.STR_SOURCE_DEST_ID = "{0:07b}"
    # define minipack
    myglobal.CONTROL_MINIPACK_SIZE = 17  # bits
    myglobal.CUT_1 = 7
    myglobal.CUT_2 = 14
    myglobal.CUT_3 = 16
    # define bonus msg
    myglobal.BONUS_MSG_BITSIZE = 11  # bits (=cut1+4)
    myglobal.BREAK_POSITION=7 #(cut1)
    # define len of lucky and unlucky slots
    myglobal.LUCKY_SLOT_LEN = 1
    myglobal.UNLUCKY_SLOT_LEN = 0
    # define number of lucky/unlucky nodes per cycle
    if _INTRA_GUARD_BAND: # total packs per cycle=22 (need to calculate)
        myglobal.TOTAL_UNLUCKY_NODES=57
    else:
        myglobal.TOTAL_UNLUCKY_NODES=80-23 # total packs per cycle=23 (need to calculate)
    myglobal.TOTAL_LUCKY_NODES=_TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
    myglobal.INTRA_CYCLE_GUARD_BAND=1 #byte
elif _TOTAL_NODES_PER_TOR==80 and _INTRA_BITRATE==10e9:
    print('Running with 80 Servers at 10 Gbps')
    time.sleep(3)
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 2
    # node description string
    myglobal.STR_SOURCE_DEST_ID = "{0:07b}"
    # define minipack
    myglobal.CONTROL_MINIPACK_SIZE = 17  # bits
    myglobal.CUT_1 = 7
    myglobal.CUT_2 = 14
    myglobal.CUT_3 = 16
    # define bonus msg
    myglobal.BONUS_MSG_BITSIZE = 11  # bits (=cut1+4)
    myglobal.BREAK_POSITION=7 #(cut1)
    # define len of lucky and unlucky slots
    myglobal.LUCKY_SLOT_LEN = 1
    myglobal.UNLUCKY_SLOT_LEN = 0
    # define number of lucky/unlucky nodes per cycle
    if _INTRA_GUARD_BAND: # total packs per cycle=22 (need to calculate)
        myglobal.TOTAL_UNLUCKY_NODES=58
    else:
        myglobal.TOTAL_UNLUCKY_NODES=80-23 # total packs per cycle=23 (need to calculate)
    myglobal.TOTAL_LUCKY_NODES=_TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
    myglobal.INTRA_CYCLE_GUARD_BAND=3 #byte
elif _TOTAL_NODES_PER_TOR==80 and _INTRA_BITRATE==20e9:
    print('Running with 80 Servers at 20 Gbps')
    time.sleep(3)
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 2
    # node description string
    myglobal.STR_SOURCE_DEST_ID = "{0:07b}"
    # define minipack
    myglobal.CONTROL_MINIPACK_SIZE = 17  # bits
    myglobal.CUT_1 = 7
    myglobal.CUT_2 = 14
    myglobal.CUT_3 = 16
    # define bonus msg
    myglobal.BONUS_MSG_BITSIZE = 11  # bits (=cut1+4)
    myglobal.BREAK_POSITION=7 #(cut1)
    # define len of lucky and unlucky slots
    myglobal.LUCKY_SLOT_LEN = 1
    myglobal.UNLUCKY_SLOT_LEN = 0
    # define number of lucky/unlucky nodes per cycle
    if _INTRA_GUARD_BAND: # total packs per cycle=22 (need to calculate)
        myglobal.TOTAL_UNLUCKY_NODES=59
    else:
        myglobal.TOTAL_UNLUCKY_NODES=80-23 # total packs per cycle=23 (need to calculate)
    myglobal.TOTAL_LUCKY_NODES=_TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
    myglobal.INTRA_CYCLE_GUARD_BAND=5 #byte!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
elif _TOTAL_NODES_PER_TOR==80 and _INTRA_BITRATE==40e9:
    print('Running with 80 Servers at 40 Gbps')
    time.sleep(3)
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 1
    # node description string
    myglobal.STR_SOURCE_DEST_ID = "{0:07b}"
    # define minipack
    myglobal.CONTROL_MINIPACK_SIZE = 17  # bits
    myglobal.CUT_1 = 7
    myglobal.CUT_2 = 14
    myglobal.CUT_3 = 16
    # define bonus msg
    myglobal.BONUS_MSG_BITSIZE = 11  # bits (=cut1+4)
    myglobal.BREAK_POSITION=7 #(cut1)
    # define len of lucky and unlucky slots
    myglobal.LUCKY_SLOT_LEN = 1
    myglobal.UNLUCKY_SLOT_LEN = 0
    # define number of lucky/unlucky nodes per cycle
    if _INTRA_GUARD_BAND: # total packs per cycle=22 (need to calculate)
        myglobal.TOTAL_UNLUCKY_NODES=60
    else:
        myglobal.TOTAL_UNLUCKY_NODES=80-23 # total packs per cycle=23 (need to calculate)
    myglobal.TOTAL_LUCKY_NODES=_TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
    myglobal.INTRA_CYCLE_GUARD_BAND=9 #byte!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
elif _TOTAL_NODES_PER_TOR==8 and _INTRA_BITRATE==5e9:
    print('Running with 8 Servers at 5 Gbps')
    time.sleep(3)
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 55
    # node description string
    myglobal.STR_SOURCE_DEST_ID = "{0:03b}"
    # define minipack
    myglobal.CONTROL_MINIPACK_SIZE = 9  # bits
    myglobal.CUT_1 = 3
    myglobal.CUT_2 = 6
    myglobal.CUT_3 = 8
    # define bonus msg
    myglobal.BONUS_MSG_BITSIZE = 7  # bits (=cut1+4)
    myglobal.BREAK_POSITION=3 #(cut1)
    # define len of lucky and unlucky slots
    myglobal.LUCKY_SLOT_LEN = 3
    myglobal.UNLUCKY_SLOT_LEN = 2
    # define number of lucky/unlucky nodes per cycle
    if _INTRA_GUARD_BAND: # total packs per cycle=22 (need to calculate)
        myglobal.TOTAL_UNLUCKY_NODES=1
    else:
        myglobal.TOTAL_UNLUCKY_NODES=1 # total packs per cycle=23 (need to calculate)
    myglobal.TOTAL_LUCKY_NODES=_TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
    myglobal.INTRA_CYCLE_GUARD_BAND=1 #byte
elif _TOTAL_NODES_PER_TOR==20 and _INTRA_BITRATE==100e9:
    print('Running with 20 Servers at 100 Gbps')
    time.sleep(3)
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 4
    # node description string
    myglobal.STR_SOURCE_DEST_ID = "{0:05b}"
    # define minipack
    myglobal.CONTROL_MINIPACK_SIZE = 13  # bits
    myglobal.CUT_1 = 5
    myglobal.CUT_2 = 10
    myglobal.CUT_3 = 12
    # define bonus msg
    myglobal.BONUS_MSG_BITSIZE = 9  # bits (=cut1+4)
    myglobal.BREAK_POSITION=5 #(cut1)
    # define len of lucky and unlucky slots
    myglobal.LUCKY_SLOT_LEN = 1
    myglobal.UNLUCKY_SLOT_LEN = 0
    # define number of lucky/unlucky nodes per cycle
    if _INTRA_GUARD_BAND: # total packs per cycle=22 (need to calculate)
        myglobal.TOTAL_UNLUCKY_NODES=4
    else:
        myglobal.TOTAL_UNLUCKY_NODES=1 # total packs per cycle=23 (need to calculate)
    myglobal.TOTAL_LUCKY_NODES=_TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
    myglobal.INTRA_CYCLE_GUARD_BAND=23 #byte
elif _TOTAL_NODES_PER_TOR==20 and _INTRA_BITRATE==40e9:
    print('Running with 20 Servers at 40 Gbps')
    time.sleep(3)
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 10
    # node description string
    myglobal.STR_SOURCE_DEST_ID = "{0:05b}"
    # define minipack
    myglobal.CONTROL_MINIPACK_SIZE = 13  # bits
    myglobal.CUT_1 = 5
    myglobal.CUT_2 = 10
    myglobal.CUT_3 = 12
    # define bonus msg
    myglobal.BONUS_MSG_BITSIZE = 9  # bits (=cut1+4)
    myglobal.BREAK_POSITION=5 #(cut1)
    # define len of lucky and unlucky slots
    myglobal.LUCKY_SLOT_LEN = 1
    myglobal.UNLUCKY_SLOT_LEN = 0
    # define number of lucky/unlucky nodes per cycle
    if _INTRA_GUARD_BAND: # total packs per cycle=22 (need to calculate)
        myglobal.TOTAL_UNLUCKY_NODES=0
    else:
        myglobal.TOTAL_UNLUCKY_NODES=1 # total packs per cycle=23 (need to calculate)
    myglobal.TOTAL_LUCKY_NODES=_TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
    myglobal.INTRA_CYCLE_GUARD_BAND=9 #byte
elif _TOTAL_NODES_PER_TOR==40 and _INTRA_BITRATE==40e9:
    print('Running with 40 Servers at 40 Gbps')
    time.sleep(3)
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 3
    # node description string
    myglobal.STR_SOURCE_DEST_ID = "{0:06b}"
    # define minipack
    myglobal.CONTROL_MINIPACK_SIZE = 15  # bits
    myglobal.CUT_1 = 6
    myglobal.CUT_2 = 12
    myglobal.CUT_3 = 14
    # define bonus msg
    myglobal.BONUS_MSG_BITSIZE = 10  # bits (=cut1+4)
    myglobal.BREAK_POSITION=6 #(cut1)
    # define len of lucky and unlucky slots
    myglobal.LUCKY_SLOT_LEN = 1
    myglobal.UNLUCKY_SLOT_LEN = 0
    # define number of lucky/unlucky nodes per cycle
    if _INTRA_GUARD_BAND: # total packs per cycle=22 (need to calculate)
        myglobal.TOTAL_UNLUCKY_NODES=20
    else:
        myglobal.TOTAL_UNLUCKY_NODES=17 # total packs per cycle=23 (need to calculate)
    myglobal.TOTAL_LUCKY_NODES=_TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
    myglobal.INTRA_CYCLE_GUARD_BAND=9 #byte
elif _TOTAL_NODES_PER_TOR==60 and _INTRA_BITRATE==40e9:
    print('Running with 60 Servers at 40 Gbps')
    time.sleep(3)
    # total packets that will be printed per buff
    myglobal.CONTROL_MSG_PACKS_PER_BUFF = 2
    # node description string
    myglobal.STR_SOURCE_DEST_ID = "{0:06b}"
    # define minipack
    myglobal.CONTROL_MINIPACK_SIZE = 15  # bits
    myglobal.CUT_1 = 6
    myglobal.CUT_2 = 12
    myglobal.CUT_3 = 14
    # define bonus msg
    myglobal.BONUS_MSG_BITSIZE = 10  # bits (=cut1+4)
    myglobal.BREAK_POSITION=6 #(cut1)
    # define len of lucky and unlucky slots
    myglobal.LUCKY_SLOT_LEN = 1
    myglobal.UNLUCKY_SLOT_LEN = 0
    # define number of lucky/unlucky nodes per cycle
    if _INTRA_GUARD_BAND: # total packs per cycle=22 (need to calculate)
        myglobal.TOTAL_UNLUCKY_NODES=40
    else:
        myglobal.TOTAL_UNLUCKY_NODES=37 # total packs per cycle=23 (need to calculate)
    myglobal.TOTAL_LUCKY_NODES=_TOTAL_NODES_PER_TOR-myglobal.TOTAL_UNLUCKY_NODES
    myglobal.INTRA_CYCLE_GUARD_BAND=9 #byte
else:
    print('ERROR - Main: Invalid number of nodes per tor')

if _FRAMEWORK=='integrated':
    main_torus_integrated() # will create N logfiles for N nodes and a combined csv with all packets in root/log
else:
    main_torus_split()