import csv
import numpy as np
import math

public = []
private = []

for i in range(45):
	public.append([i,[]])
	private.append([i,[]])

with open('condensedacs.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row['SCH']=='2' and row['WKL']=='1': #public
			age = int(row['AGEP'])
			if age>=22 and age<=66:
				public[age-22][1].append(float(row['WAGP'])*float(row['ADJINC'])*0.000001)
		elif row['SCH']=='3' and row['WKL']=='1': #private
			age = int(row['AGEP'])
			if age>=22 and age<=66:
				private[age-22][1].append(float(row['WAGP'])*float(row['ADJINC'])*0.000001)
print "Public data: " 
print public

print "Private data: " 
print private

pri_total_dat = 0
pub_total_dat = 0
pri_life_median = 0
pub_life_median = 0
pri_life_mean = 0
pub_life_mean = 0
#public[age-22, [all data values],mean,median]
for i in range(45):
	arr_pub = np.array(public[i][1])
	arr_pri = np.array(private[i][1])
	public[i].append(len(arr_pub))
	public[i].append(np.mean(arr_pub))
	public[i].append(np.median(arr_pub))
	print "\n PUB:At age %d mean is %f median is %f with %d data points" % (i+22, public[i][3], public[i][4], public[i][2]) 
	private[i].append(len(arr_pri))
	private[i].append(np.mean(arr_pri))
	private[i].append(np.median(arr_pri))
	print "\n PRI:At age %d mean is %f median is %f with %d data points" % (i+22, private[i][3], private[i][4], private[i][2]) 
	pri_total_dat += private[i][2]
	pub_total_dat += public[i][2]
	if private[i][3]>0 : pri_life_mean += private[i][3]
	if public[i][3]>0 :pub_life_mean += public[i][3]
	if private[i][4]>0 : pri_life_median += private[i][4]
	if public[i][4]>0 :pub_life_median += public[i][4]


print "\n PUB: %d data points giving lifetime income mean %f, median %f" % (pub_total_dat, pub_life_mean, pub_life_median)
print "\n PRI: %d data points giving lifetime income mean %f, median %f" % (pri_total_dat, pri_life_mean, pri_life_median)

r = np.linspace(1.01,1.1,10)
for i in r:
	npv_pri_mean = 0
	npv_pri_median = 0
	npv_pub_mean = 0
	npv_pub_median = 0
	for x in range(45):
		ir = math.pow(i,x)
		if private[x][3]>0 : npv_pri_mean += (private[x][3]) / ir
		if public[x][3]>0 : npv_pub_mean += (public[x][3]) / ir
		if private[x][4]>0 : npv_pri_median += (private[x][4]) / ir
		if public[x][4]>0 : npv_pub_median += (public[x][4]) / ir

	print "\n At %f interest rate: public NPV income -> mean = %f median = %f" % (i-1, npv_pub_mean, npv_pub_median)
	print "\n At %f interest rate: private NPV income -> mean = %f median = %f" % (i-1, npv_pri_mean, npv_pri_median)



