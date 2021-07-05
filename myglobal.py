ROOT='C:\\Pycharm\\Projects\\polydiavlika\\waa\\'
TRAFFIC_DATASETS_FOLDER='traffic_datasets\\'
PROPAGATION_TIME=10/(2e8) #PROPAGATION_TIME=0 10/(2e8)
ID_DIFF=1
MAX_PACKET_SIZE=1500 #bytes
MIN_PACKET_SIZE=64 #bytes
CYCLE_SIZE=1500 #bytes
CONTROL_MSG_PACKS_PER_BUFF=46
TOTAL_BUFFS_PER_NODE=3
DEFAULT_UNLUCKY_NODE_ID=1
DEFAULT_LUCKY_NUM=10
TOLERANCE = 1e-9
timestep = (0.8)*(1e-9) #timestep = 0.8e-9 -> NEED TOTAL_TIME MOD timestep=0 (sync!)
WAITING=timestep
timeslot=(10)*(1e-9) #timeslot=(51.2)*(1e-9)
# Will be set on startup
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
CYCLE_GUARD_BAND=1 # bytes