import pandas as pd
import os
from torus_integrated import myglobal

folder='log_20240625_id06_topo1x16_ch4x100_load500g_end100ms_dcUNI'
abs_folder=os.path.join(myglobal.LOGS_FOLDER, folder)

input_csv=os.path.join(abs_folder, 'total_log.csv')

print('Entered break to app, loading total csv')
df=pd.read_csv(input_csv)
list_of_apps = sorted(df['application'].unique())


for app in list_of_apps:
	print('Breaking to app='+str(app))
	df_filtered_by_app = df.loc[df['application'] == app]
	output_csv=os.path.join(abs_folder,'total_log_'+str(app)+'.csv')

	print('Clear prev...')
	try:
		os.remove(output_csv)
		print('Removed prev file=' + str(output_csv))
	except Exception as ex:
		print('Cannot Removed prev file=' + str(ex))

	df_filtered_by_app.to_csv(output_csv,mode='a',index=False)