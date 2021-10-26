ROOT='C:\\Pycharm\\Projects\\polydiavlika\\torus_integrated\\'
TRAFFIC_DATASETS_FOLDER='traffic_datasets\\Dyo_80B_1st\\'
INTER_TRANSMISSION_INFO_FOLDER='transmission_info\\'
TORUS_FILE='torus_matrix.txt'
LOGS_FOLDER='logs\\'
SAVE_LOGS=False
PROPAGATION_TIME=10/(2e8) #PROPAGATION_TIME=0 10/(2e8)
ID_DIFF=1
MAX_PACKET_SIZE=1500 #bytes
MIN_PACKET_SIZE=64 #bytes
CYCLE_SIZE=1500 #bytes
TOTAL_BUFFS_PER_NODE=3
DEFAULT_UNLUCKY_NODE_ID=1
DEFAULT_LUCKY_NUM=10
TOLERANCE = 1e-9
timestep = (0.8)*(1e-9) #timestep = 0.8e-9 -> NEED TOTAL_TIME MOD timestep=0 (sync!)
WAITING=timestep
timeslot=(10)*(1e-9) #timeslot=(51.2)*(1e-9)

# Will be set on startup
CONTROL_MSG_PACKS_PER_BUFF=46
CONTROL_MINIPACK_SIZE=9 #bits
BONUS_MSG_BITSIZE=7 #bits
BREAK_POSITION=3
CUT_1=3
CUT_2=6
CUT_3=8
LUCKY_SLOT_LEN=3
UNLUCKY_SLOT_LEN=2
STR_SOURCE_DEST_ID="{0:03b}"
TOTAL_UNLUCKY_NODES=1
TOTAL_LUCKY_NODES=1
ASSIGN_CHANNEL_POLICY='ALL_BIG'
CYCLE_GUARD_BAND=3 # bytes

####################################################### Architecure Settings
TOTAL_NODES_PER_TOR = 80
TOTAL_TORS=2
# Intra Protocol Settings
INTRA_CHANNEL_BITRATE = 5e9
INTRA_CHANNEL_ID_LIST = [100,200]  # 4 data channel
INTRA_CONTROL_CHANNEL_ID = 500  # 1 control channel
INTRA_NODE_INPUT_HIGH_BUFFER_SIZE = 1e6 # bytes
INTRA_NODE_INPUT_MED_BUFFER_SIZE = 1e6 # bytes
INTRA_NODE_INPUT_LOW_BUFFER_SIZE = 1e6 # bytes
INTRA_GUARD_BAND=True ##
INTRA_REMOVE_INTER=True # True if not proturs experiments
# Inter Protocol Settings
INTER_CHANNEL_BITRATE = 10e9
INTER_CHANNEL_ID_LIST = [1000, 2000, 3000, 4000,5000,6000,7000,8000]  # 8 data channel
INTER_TOR_HIGH_BUFFER_SIZE = 1e6 # bytes
INTER_TOR_MED_BUFFER_SIZE = 1e6 # bytes
INTER_TOR_LOW_BUFFER_SIZE = 1e6 # bytes
# Simulation (traffic dataset) settings
T_BEGIN = 0
T_END = 0.050
##########################################################################################################

# logging
OUTPUT_TABLE_TITLE='packet_id,time,packet_size,packet_qos,source_id,tor_id,destination_id,destination_tor,' \
                    'time_intra_buffer_in,time_intra_buffer_out,time_intra_trx_in,time_intra_trx_out,' \
                   'time_tor_buffer_in,time_tor_buffer_out,time_tor_trx_in,time_tor_trx_out,' \
                   'time_inter_buffer_in,time_inter_buffer_out,time_inter_trx_in,time_inter_trx_out\n'

