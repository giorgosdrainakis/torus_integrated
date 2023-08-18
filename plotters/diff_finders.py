_load=[1,3,5]
_other=[0.0074,0.0074,0.0074]
_me=[0.00042,0.0027,0.005]

for i in range(len(_load)):
	print('Load='+str(_load[i]))
	calc=100*((_me[i]-_other[i])/_other[i])
	print('decr at %='+str(calc))