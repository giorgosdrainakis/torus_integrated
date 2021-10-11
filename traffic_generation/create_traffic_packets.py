import csv
import datetime
import math
import random
from torus_integrated import myglobal
from scipy.stats import genpareto
import numpy as numpy
from scipy.stats import weibull_min
from pathlib import Path

def get_variable_packet_size(small_size,big_size,small_prob):
    myrand=random.random()
    if (myrand<=small_prob):
        ret=small_size
    else:
        ret=big_size
    return ret
def get_interval_times_exponential(t_begin,t_end,packet_num):
    mean_interval_time=(t_end-t_begin)/packet_num
    interval_times_abs = numpy.random.exponential(scale=mean_interval_time, size=packet_num)
    interval_times_actual=[]
    new_sample_time=t_begin
    for abs_time in interval_times_abs:
        new_sample_time=new_sample_time+abs_time
        if new_sample_time>t_end:
            break
        else:
            interval_times_actual.append(new_sample_time)
    return interval_times_actual
def get_interval_times_lognormal(t_begin,t_end,packet_num,sigma):
    mean_interval_time=(t_end-t_begin)/packet_num
    interval_times_abs = numpy.random.lognormal(mean=math.log(mean_interval_time,3), sigma=sigma, size=packet_num)
    interval_times_actual=[]
    new_sample_time=t_begin
    for abs_time in interval_times_abs:
        new_sample_time=new_sample_time+abs_time
        if new_sample_time>t_end:
            break
        else:
            interval_times_actual.append(new_sample_time)
    return interval_times_actual
def get_interval_times_weibull(t_begin,t_end,packet_num,alpha):
    mean_interval_time=(t_end-t_begin)/packet_num
    #interval_times_abs = mean_interval_time*numpy.random.weibull(a=alpha,size=packet_num)
    interval_times_abs = weibull_min.rvs(alpha, loc=0, scale=mean_interval_time, size=packet_num)
    interval_times_actual=[]
    new_sample_time=t_begin
    for abs_time in interval_times_abs:
        new_sample_time=new_sample_time+abs_time
        if new_sample_time>t_end:
            break
        else:
            interval_times_actual.append(new_sample_time)
    return interval_times_actual
def get_on_off_times(t_begin,t_end,packet_num,c_pareto,sigma):
    mean_interval_time=(t_end-t_begin)/packet_num
    #on_times_abs=gprnd(c_pareto,mean_interval_time,0,1,packet_num) todo
    on_times_abs = genpareto.rvs(c_pareto,scale=mean_interval_time, size=packet_num)
    #off_times_abs=lognrnd(log(mean_interval_time),sigma,1,packet_num) todo
    off_times_abs = numpy.random.lognormal(mean=math.log(mean_interval_time,2), sigma=sigma, size=packet_num)
    on_periods=[]
    counter=1
    current_time=t_begin

    while current_time<=t_end:
        # off phase
        current_time=current_time+off_times_abs[counter]
        new_on_start=current_time
        # on phase
        current_time=current_time+on_times_abs[counter]
        new_off_start=current_time
        if current_time<=t_end:
            on_periods.append([new_on_start,new_off_start])
        counter=counter+1
    return on_periods
def generate_packets_low_qos(packet_id,t_begin,t_end,avg_throughput,source_id,destination_ids,c_pareto,
                             sigma_lognormal,alpha,
                             torid,inter_dest_list,intra_traffic_perc):
    csv_reader=''
    first_packet_id=packet_id
    avg_packet_size=64*0.6+1500*0.4 #bytes
    avg_traffic=avg_throughput*(t_end-t_begin) #bytes
    avg_packet_num=round(avg_traffic/avg_packet_size)
    on_times=get_on_off_times(t_begin,t_end,avg_packet_num,c_pareto,sigma_lognormal)
    total_len=len(on_times)
    for on_time in on_times:
        avg_traffic=avg_throughput*(on_time[1]-on_time[0])
        avg_packet_num = max(round(avg_traffic / avg_packet_size),1)
        interval_times=get_interval_times_weibull(on_time[0],on_time[1],avg_packet_num,alpha)
        for inttime in interval_times:
            new_time=inttime
            packet_size = get_variable_packet_size(64, 1500, 0.6)
            qos = 'low'
            luckynum=random.uniform(0,1)
            if luckynum<=intra_traffic_perc:
                destination_id = random.sample(destination_ids, 1)[0]
                destination_tor=torid
            else:
                destination_id = 0
                destination_tor=random.sample(inter_dest_list, 1)[0]

            # 'packet_id,time,packet_size,packet_qos,source_id,source_tor,destination_id,destination_tor\
            csv_reader=csv_reader+str(packet_id)+','+str(new_time)+','\
                       +str(packet_size)+','+str(qos)+','+str(source_id)+','\
                       +str(torid)+','+str(destination_id)+','+str(destination_tor)+'\n'
            packet_id = packet_id + 1
            print('node '+str(source_id)+',low progress %='+str((packet_id-first_packet_id)*100/total_len))
    return csv_reader,packet_id
def generate_packets_med_qos(packet_id,t_begin,t_end,avg_throughput,source_id,destination_ids,sigma_lognormal,
                             torid,inter_dest_list,intra_traffic_perc):
    csv_reader=''
    first_packet_id=packet_id
    avg_packet_size=64*0.7+1500*0.3#bytes
    avg_traffic=avg_throughput*(t_end-t_begin) #bytes
    avg_packet_num=round(avg_traffic/avg_packet_size)
    interval_times=get_interval_times_lognormal(t_begin,t_end,avg_packet_num,sigma_lognormal)
    total_len=len(interval_times)
    for inttime in interval_times:
        packet_size=get_variable_packet_size(64,1500,0.7)
        qos='med'
        new_time=inttime

        luckynum = random.uniform(0, 1)
        if luckynum <= intra_traffic_perc:
            destination_id = random.sample(destination_ids, 1)[0]
            destination_tor = torid
        else:
            destination_id = 0
            destination_tor = random.sample(inter_dest_list, 1)[0]

        # 'packet_id,time,packet_size,packet_qos,source_id,source_tor,destination_id,destination_tor\
        csv_reader = csv_reader + str(packet_id) + ',' + str(new_time) + ',' \
                     + str(packet_size) + ',' + str(qos) + ',' + str(source_id) + ',' \
                     + str(torid) + ',' + str(destination_id) + ',' + str(destination_tor) + '\n'
        packet_id = packet_id + 1
        print('node ' + str(source_id) + ',med progress %=' + str((packet_id - first_packet_id) * 100 / total_len))
    return csv_reader,packet_id
def generate_packets_high_qos(packet_id,t_begin,t_end,avg_throughput,source_id,destination_ids,
                              torid,inter_dest_list,intra_traffic_perc):
    csv_reader=''
    packet_id=packet_id
    first_packet_id=packet_id
    avg_packet_size=64#bytes
    avg_traffic=avg_throughput*(t_end-t_begin)#bytes
    avg_packet_num=round(avg_traffic/avg_packet_size)
    interval_times=get_interval_times_exponential(t_begin,t_end,avg_packet_num)
    total_len=len(interval_times)
    for inttime in interval_times:
        packet_size=avg_packet_size
        qos='high'
        new_time=inttime

        luckynum = random.uniform(0, 1)
        if luckynum <= intra_traffic_perc:
            destination_id = random.sample(destination_ids, 1)[0]
            destination_tor = torid
        else:
            destination_id = 0
            destination_tor = random.sample(inter_dest_list, 1)[0]

        # 'packet_id,time,packet_size,packet_qos,source_id,source_tor,destination_id,destination_tor\
        csv_reader = csv_reader + str(packet_id) + ',' + str(new_time) + ',' \
                     + str(packet_size) + ',' + str(qos) + ',' + str(source_id) + ',' \
                     + str(torid) + ',' + str(destination_id) + ',' + str(destination_tor) + '\n'
        packet_id=packet_id+1
        print('node ' + str(source_id) + ',high progress %=' + str((packet_id - first_packet_id) * 100 / total_len))
    return csv_reader,packet_id
def export_traffic_dataset_single(nodeid,intralist,torid,interlist,t_begin,t_end,avg_throughput,qos,hasHeader,
                                  low_thru_param,med_thru_param,high_thru_param,intra_traffic_perc,init_packet_id):
    packet_id=init_packet_id
    sigma_lognormal_low = 6
    sigma_lognormal_med = 3
    alpha_weibull = 0.1
    c_pareto = 0.5
    csv_content = ''
    thru_low=avg_throughput*low_thru_param #3
    thru_med=avg_throughput*med_thru_param #2.5
    thru_high=avg_throughput*high_thru_param #0.1

    intra_dest_list=intralist
    inter_dest_list=interlist
    # Generate low qos traffic
    if qos=='all' or qos=='low':
        low_packets,packet_id=generate_packets_low_qos(packet_id,t_begin,t_end,thru_low,nodeid,
                                                       intra_dest_list,c_pareto,sigma_lognormal_low,alpha_weibull,
                                                       torid,inter_dest_list,intra_traffic_perc)
        if low_packets is None:
            print('Warning: No low packets generated - check distribution params')
            return 0
        else:
            print(len(low_packets))
            csv_content = csv_content+low_packets

    # Generate medium qos traffic
    if qos=='all' or qos=='med':
        med_packets,packet_id=generate_packets_med_qos(packet_id,t_begin,t_end,thru_med,nodeid,
                                                       intra_dest_list,sigma_lognormal_med,
                                                       torid,inter_dest_list,intra_traffic_perc)
        if med_packets is None:
            print('Warning: No med packets generated - check distribution params')
            return 0
        else:
            print(len(med_packets))
            csv_content = csv_content+med_packets

    # Generate high qos traffic
    if qos=='all' or qos=='high':
        high_packets,packet_id=generate_packets_high_qos(packet_id,t_begin,t_end,
                                                         thru_high,nodeid,intra_dest_list,
                                                         torid,inter_dest_list,intra_traffic_perc)
        if high_packets is None:
            print('Warning: No high packets generated - check distribution params')
            return 0
        else:
            print(len(high_packets))
            csv_content = csv_content+high_packets

    csv_names='packet_id,time,packet_size,packet_qos,source_id,tor_id,' \
              'destination_id,destination_tor\n'
    if hasHeader:
        output_table= csv_names+csv_content
    else:
        output_table=csv_content

    mytime = str(datetime.datetime.now())
    mytime = mytime.replace('-', '_')
    mytime = mytime.replace(' ', '_')
    mytime = mytime.replace(':', '_')
    mytime = mytime.replace('.', '_')

    print('Writing...')
    current_file=myglobal.ROOT + myglobal.TRAFFIC_DATASETS_FOLDER+mynewfolder+'tor'+str(torid)+'node'+str(nodeid)+".csv"

    with open(current_file, mode='a') as file:
        file.write(output_table + '\n')
    print('Sorting...')
    with open(current_file, 'r', newline='') as f_input:
        csv_input = csv.DictReader(f_input)
        data = sorted(csv_input, key=lambda row: (float(row['time']), float(row['packet_id'])))
        print(len(data))
    print('Rewriting...')
    with open(current_file, 'w', newline='') as f_output:
        csv_output = csv.DictWriter(f_output, fieldnames=csv_input.fieldnames)
        csv_output.writeheader()
        csv_output.writerows(data)
    return packet_id
def get_timestamp_to_string():
    mytime = str(datetime.datetime.now())
    mytime = mytime.replace('-', '_')
    mytime = mytime.replace(' ', '_')
    mytime = mytime.replace(':', '_')
    mytime = mytime.replace('.', '_')
    return mytime
def run_with_params(): # main
    new_packet_id=0
    for tor in inter_tor_list:
        for node in intra_nodes_list:
            my_tor=[tor]
            my_node=[node]
            intra_dest_list=[item for item in intra_nodes_list if item not in my_node]
            inter_dest_list=[item for item in inter_tor_list if item not in my_tor]
            hasHeader=True
            intra_traffic_perc = intra_perc
            new_packet_id=export_traffic_dataset_single(node,intra_dest_list,tor,inter_dest_list,t_begin,t_end,avg_throughput_per_node,
                                qos,hasHeader,low_thru_shape_param,med_thru_shape_param,
                                          high_thru_shape_param,intra_traffic_perc,new_packet_id)

#############  params  ###############
t_begin=0 #sec (float)
t_end=0.05 #sec (float)
avg_throughput=4*75e9 # mean bytes per sec being generated
qos='all'# choose qos packets allowed {'low','med','high','all'}
intra_nodes_list=[x for x in range(1,81)]
inter_tor_list=[1,2]
low_thru_shape_param=3 # (float)
med_thru_shape_param=5 # (float)
high_thru_shape_param=0.005 # (float)
avg_throughput_per_node=avg_throughput/len(intra_nodes_list)
intra_perc=0.8

# MAIN - traffic dset is created by default in
# traffic_dataset/<CURRENT_TIMESTAMP> as 'testN.csv', for N=1,2...
mynewfolder=get_timestamp_to_string()+'\\'
Path(myglobal.ROOT + myglobal.TRAFFIC_DATASETS_FOLDER+mynewfolder).mkdir(parents=True, exist_ok=True)
run_with_params()