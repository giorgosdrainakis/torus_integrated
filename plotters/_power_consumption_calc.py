import math

dcn='fat-tre2e'

if dcn=='fat-tree':
	print(str('dcn='+str(dcn)))
	# fat-tree
	_layers=[3]
	_ports_per_switch=[16,24,32,48]
	_rate_per_trx=[10e9]

	for rate_per_trx in _rate_per_trx:
		for ports_per_switch in _ports_per_switch:
			power_per_trx=0.1*rate_per_trx*1e-9 #rotos
			power_per_switch=6*ports_per_switch #rotos
			total_switches=(5/4)*(ports_per_switch**2)
			total_servers=0.25*(ports_per_switch**3)
			trxs=total_servers
			power_trx=trxs*power_per_trx
			power_switch=total_switches*power_per_switch
			power_total=power_trx+power_switch
			thru_total=trxs*rate_per_trx

			print('----------  fat-tree --------------')
			#print('rate_per_trx='+str(rate_per_trx))
			print('ports_per_switch='+str(ports_per_switch))
			#print('total_switches='+str(total_switches))
			print('total_servers='+str(total_servers))
			print('power_trx='+str(power_trx))
			print('power_switch='+str(power_switch))
			print('power_total='+str(power_total))
			print('thru_total TBPS='+str(thru_total*1e-12))
			print('-------------------------------------------')
else:
	print(str('dcn='+str(dcn)))
	# ours
	_servers_per_tor=[32]
	_tors=[256]
	for servers_per_tor in _servers_per_tor:
		for tors in _tors:
			intra_links=4
			intra_bridge=1
			intra_control=1
			intra_speed=100e9
			inter_links=4
			inter_bridge=1
			inter_speed=40e9

			ports_per_switch=4
			power_per_switch=6*ports_per_switch #rotos

			if intra_speed==100e9:
				intra_power_per_trx=3.5 #dacon,  #https://www.fibermall.com/blog/optical-transceiver-technology-trends-of-data-center-in-2022.htm
			elif intra_speed==10e9:
				intra_power_per_trx = 1 #dacon,
			elif intra_speed==25e9:
				intra_power_per_trx = 1.2 #dacon,
			elif intra_speed==40e9:
				intra_power_per_trx = 1.5 #dacon,

			if inter_speed==100e9:
				inter_power_per_trx=3.5 #dacon,  #https://www.fibermall.com/blog/optical-transceiver-technology-trends-of-data-center-in-2022.htm
			elif inter_speed==10e9:
				inter_power_per_trx = 1 #dacon,
			elif inter_speed==25e9:
				inter_power_per_trx = 1.2 #dacon,
			elif inter_speed==40e9:
				inter_power_per_trx = 1.5 #dacon,


			total_servers = tors*servers_per_tor
			thru_total=0.9*(tors*intra_speed*(intra_links+intra_bridge))

			power_intra=total_servers*(intra_links+intra_control+intra_bridge)*intra_power_per_trx
			power_inter=tors*power_per_switch+(tors*inter_links*inter_power_per_trx)+(tors*inter_bridge*intra_power_per_trx)
			power_total=power_inter+power_intra

			print('----------  ours --------------')
			print('total_servers='+str(total_servers))
			print('power_intra='+str(power_intra))
			print('power_inter='+str(power_inter))
			print('power_total='+str(power_total))
			print('thru_total TBPS='+str(thru_total*1e-12))
			print('-------------------------------------------')