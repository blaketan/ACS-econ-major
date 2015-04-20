import csv
import numpy as np
import math
import matplotlib.pyplot as plt

def weighted_median(data,weight):
	if len(data)==0:
		return 0
	new_list=[]
	for i in range(len(data)):
		for j in range(weight[i]):
			new_list.append(data[i])
	new_list.sort
	median = (len(new_list)+1)/2.0
	if median % 1 ==0.5:
		return (new_list[int(median-1.5)]+new_list[int(median-0.5)])/2.0
	else:
		return new_list[int(median-1)]

def weighted_mean(data,weight):
	if len(data)==0:
		return 0
	else:
		return np.average(data,weights=weight)



public = []
private = []

for i in range(45):
	public.append([i,[],[]])
	private.append([i,[],[]])

with open('condensedacs.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row['SCH']=='2' and row['WKL']=='1': #public
			age = int(row['AGEP'])
			if age>=22 and age<=66 and int(row['WAGP'])>1:
				public[age-22][1].append(float(row['WAGP'])*float(row['ADJINC'])*0.000001)
				public[age-22][2].append(int(row['PWGTP']))
		elif row['SCH']=='3' and row['WKL']=='1': #private
			age = int(row['AGEP'])
			if age>=22 and age<=66 and int(row['WAGP'])>1:
				private[age-22][1].append(float(row['WAGP'])*float(row['ADJINC'])*0.000001)
				private[age-22][2].append(int(row['PWGTP']))

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
#public[age-22, [all data values],[data weights],len,mean,median]
for i in range(45):
	arr_pub = np.array(public[i][1])
	arr_pub_w = np.array(public[i][2])
	arr_pri = np.array(private[i][1])
	arr_pri_w = np.array(private[i][2])
	public[i].append(np.sum(arr_pub_w))
	public[i].append(weighted_mean(arr_pub,arr_pub_w))
	public[i].append(weighted_median(arr_pub,arr_pub_w))
	print "\n PUB:At age %d mean is %f median is %f with %d weighted points" % (i+22, public[i][4], public[i][5], public[i][3]) 
	private[i].append(np.sum(arr_pri_w))
	private[i].append(weighted_mean(arr_pri,arr_pri_w))
	private[i].append(weighted_median(arr_pri,arr_pri_w))
	print "\n PRI:At age %d mean is %f median is %f with %d weighted points" % (i+22, private[i][4], private[i][5], private[i][3]) 
	pri_total_dat += private[i][3]
	pub_total_dat += public[i][3]
	if private[i][4]>0 : pri_life_mean += private[i][4]
	if public[i][4]>0 :pub_life_mean += public[i][4]
	if private[i][5]>0 : pri_life_median += private[i][5]
	if public[i][5]>0 :pub_life_median += public[i][5]


print "\n PUB: %d weighted data points giving lifetime income mean %f, median %f" % (pub_total_dat, pub_life_mean, pub_life_median)
print "\n PRI: %d weighted data points giving lifetime income mean %f, median %f" % (pri_total_dat, pri_life_mean, pri_life_median)

r = np.linspace(1.01,1.1,10)
for i in r:
	npv_pri_mean = 0
	npv_pri_median = 0
	npv_pub_mean = 0
	npv_pub_median = 0
	for x in range(45):
		ir = math.pow(i,x)
		if private[x][4]>0 : npv_pri_mean += (private[x][4]) / ir
		if public[x][4]>0 : npv_pub_mean += (public[x][4]) / ir
		if private[x][5]>0 : npv_pri_median += (private[x][5]) / ir
		if public[x][5]>0 : npv_pub_median += (public[x][5]) / ir

	print "\n At %f interest rate: public NPV income -> mean = %f median = %f" % (i-1, npv_pub_mean, npv_pub_median)
	print "\n At %f interest rate: private NPV income -> mean = %f median = %f" % (i-1, npv_pri_mean, npv_pri_median)


pub_mean = [row[4] for row in public]
pri_mean = [row[4] for row in private]
pub_med = [row[5] for row in public]
pri_med = [row[5] for row in private]
f, axarr= plt.subplots(2,sharex=True)
axarr[0].plot(np.arange(22,67),pub_mean,'bs',label='Mean(public)')
axarr[0].plot(np.arange(22,67),pub_med,'b^',label='Median(public)')
axarr[0].plot(np.arange(22,67),pri_mean,'rs',label='Mean(private)')
axarr[0].plot(np.arange(22,67),pri_med,'r^',label='Median(private)')
axarr[0].set_title('Mean & Median Annual Salary at Age')
axarr[0].legend(bbox_to_anchor=(0.2, 1.0))
axarr[1].plot(np.arange(22,67),np.cumsum(pub_mean),'b-',label='Mean(public)')
axarr[1].plot(np.arange(22,67),np.cumsum(pub_med),'b--',label='Median(public)')
axarr[1].plot(np.arange(22,67),np.cumsum(pri_mean),'r-',label='Mean(private)')
axarr[1].plot(np.arange(22,67),np.cumsum(pri_med),'r--',label='Median(private)')
axarr[1].set_title('Mean & Median Cummulative Salary at Age')

axarr[1].legend(bbox_to_anchor=(0.2, 1.0))
plt.ylabel('US 2013 Dollars') 
plt.xlabel('Age')
plt.grid(True)

plt.show()
