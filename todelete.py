import pandas as pd

logfile='C:\\Pycharm\\Projects\\polydiavlika\\torus_integrated\\logs\\log_20240321_id03_topo1x32_ch4x100_load1000g\\log2024_03_23_02_54_32_950410_tor1_combo.csv'
output='C:\\Pycharm\\Projects\\polydiavlika\\torus_integrated\\logs\\log_20240321_id03_topo1x32_ch4x100_load1000g\\total_log.csv'
# sort ToR
print('Re Sorting TOR=')
s_df=pd.read_csv(logfile)
s_df.sort_values(['time', 'packet_id'], ascending=[True, True], inplace=True)
print('Rewriting TOR=')
s_df.to_csv(output, mode='a',index=False, header=True)

