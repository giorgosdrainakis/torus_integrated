base_str='tor1node'
list_files=[base_str+str(n) for n in range(1,17)]
import os
import pandas as pd
for filename in list_files:
	_CSV_OUT=os.path.join('C://Pycharm//Projects//polydiavlika//torus_integrated//traffic_datasets//test',filename)
	_CSV_OUT=_CSV_OUT+'.csv'
	print('Going into:'+str(_CSV_OUT))

	def modiff(pack_size):
		if pack_size<=200:
			return 'high'
		else:
			return 'med'

	def mod_time(time):
		import random
		return random.uniform(1e-9, 1e-4)

	df = pd.read_csv(_CSV_OUT)
	df = df.head(100)

	df['modified_packet_qos'] = df.apply(lambda row: modiff(pack_size=row['packet_size']), axis=1)
	df = df.rename(columns={'packet_qos': 'origin', 'modified_packet_qos': 'packet_qos'})
	df = df.drop('origin', axis=1)

	df['time'] = df['time'].apply(pd.to_numeric)
	df['modified_time']= df.apply(lambda row: mod_time(time=row['time']), axis=1)
	df = df.rename(columns={'time': 'origin2', 'modified_time': 'time'})
	df = df.drop('origin2', axis=1)

	df = df.sort_values(by=['time'], ascending=True)

	open(_CSV_OUT, 'w').close()

	df.to_csv(_CSV_OUT, index=False, header=True, mode='a')