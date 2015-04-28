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
def w_med_sd(data,weight):
	if len(data)<2:
		return 0
	indices = np.argsort(data)
	s_data = np.array(data)[indices]
	s_weights = np.array(weight)[indices]
	c_weights = np.cumsum(s_weights)
	base = c_weights[len(c_weights)-1]
	df = 2.0 #design factor
	se_50 = df * math.sqrt( (95/float(5*base)) * math.pow(50,2))
	if se_50>48.0:
		se_50=48.0
	p_lower = (50-se_50)
	p_upper = (50+se_50)
	i_lower = None
	i_upper = None
	for i in range(len(c_weights)):
		if i_lower == None and p_lower <= (c_weights[i]/float(base))*100:
			i_lower=i
		if p_upper <= (c_weights[i]/float(base))*100:
			i_upper=i
			break
	lower_bound=0
	upper_bound=0
	if i_lower==i_upper:
		try:
			a1 = s_data[i_lower]
			a2 = s_data[i_lower+1]
			c1 = (c_weights[i_lower]/float(base)) * 100
			c2 = (c_weights[i_lower+1]/float(base)) * 100
			lower_bound= ((p_lower-c1)/(c2-c1))*(a2-a1)+a1
			upper_bound= ((p_upper-c1)/(c2-c1))*(a2-a1)+a1
		except IndexError:
			lower_bound=s_data[i_lower]
			upper_bound=s_data[i_lower]
	else:
		try:
			a1 = s_data[i_lower]
			a2 = s_data[i_lower+1]
			b1 = s_data[i_upper]
			b2 = s_data[i_upper+1]
			c1 = (c_weights[i_lower]/float(base)) * 100
			c2 = (c_weights[i_lower+1]/float(base)) * 100
			d1 = (c_weights[i_upper]/float(base)) * 100
			d2 = (c_weights[i_upper+1]/float(base)) * 100
			lower_bound= ((p_lower-c1)/(c2-c1))*(a2-a1)+a1
			upper_bound= ((p_upper-d1)/(d2-d1))*(b2-b1)+b1
		except IndexError:
			lower_bound=s_data[i_lower]
			upper_bound=s_data[i_lower]
	return 0.5*(upper_bound-lower_bound)


public = []
private = []
non = []

for i in range(45):
	public.append([i,[],[]])
	private.append([i,[],[]])

for i in range(48):
	non.append([i,[],[]])

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

with open('condensedacs2.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		try:
			age = int(row['AGEP'])
			if age>=19 and age<=66:
				non[age-19][1].append(float(row['WAGP'])*float(row['ADJINC'])*0.000001)
				non[age-19][2].append(int(row['PWGTP']))
		except ValueError:
			print row



print "Public data: " 
print public

print "Private data: " 
print private

print "High School Grad data: " 
print non

pri_total_dat = 0
pub_total_dat = 0
pri_life_median = 0
pub_life_median = 0
pri_life_mean = 0
pub_life_mean = 0
#public[age-22, [all data values],[data weights],len,mean,median,sd]
for i in range(45):
	arr_pub = np.array(public[i][1])
	arr_pub_w = np.array(public[i][2])
	arr_pri = np.array(private[i][1])
	arr_pri_w = np.array(private[i][2])
	public[i].append(np.sum(arr_pub_w))
	public[i].append(weighted_mean(arr_pub,arr_pub_w))
	public[i].append(weighted_median(arr_pub,arr_pub_w))
	public[i].append(w_med_sd(arr_pub,arr_pub_w))
	print "\n PUB:At age %d mean is %f median is %f with %d weighted points" % (i+22, public[i][4], public[i][5], public[i][3]) 
	private[i].append(np.sum(arr_pri_w))
	private[i].append(weighted_mean(arr_pri,arr_pri_w))
	private[i].append(weighted_median(arr_pri,arr_pri_w))
	private[i].append(w_med_sd(arr_pri,arr_pri_w))
	print "\n PRI:At age %d mean is %f median is %f with %d weighted points" % (i+22, private[i][4], private[i][5], private[i][3]) 
	pri_total_dat += private[i][3]
	pub_total_dat += public[i][3]
	if private[i][4]>0 : pri_life_mean += private[i][4]
	if public[i][4]>0 :pub_life_mean += public[i][4]
	if private[i][5]>0 : pri_life_median += private[i][5]
	if public[i][5]>0 :pub_life_median += public[i][5]

non_total_dat = 0
non_life_median = 0
non_life_mean = 0
#public[age-22, [all data values],[data weights],len,mean,median,sd]
for i in range(48):
	arr_non = np.array(non[i][1])
	arr_non_w = np.array(non[i][2])
	non[i].append(np.sum(arr_non_w))
	non[i].append(weighted_mean(arr_non,arr_non_w))
	non[i].append(weighted_median(arr_non,arr_non_w))
	non[i].append(w_med_sd(arr_non,arr_non_w))
	print "\n highsch:At age %d mean is %f median is %f with %d weighted points" % (i+19, non[i][4], non[i][5], non[i][3]) 
	non_total_dat += non[i][3]
	if non[i][4]>0 : non_life_mean += non[i][4]
	if non[i][5]>0 : non_life_median += non[i][5]

print "\n PUB: %d weighted data points giving lifetime salary mean %f, median %f" % (pub_total_dat, pub_life_mean, pub_life_median)
print "\n PRI: %d weighted data points giving lifetime salary mean %f, median %f" % (pri_total_dat, pri_life_mean, pri_life_median)
print "\n NON: %d weighted data points giving lifetime salary mean %f, median %f" % (non_total_dat, non_life_mean, non_life_median)

r = np.linspace(1.01,1.1,10)
for i in r:
	npv_pri_mean = 0
	npv_pri_median = 0
	npv_pub_mean = 0
	npv_pub_median = 0
	npv_non_mean = 0
	npv_non_median = 0
	for x in range(45):
		ir = math.pow(i,x)
		if private[x][4]>0 : npv_pri_mean += (private[x][4]) / ir
		if public[x][4]>0 : npv_pub_mean += (public[x][4]) / ir
		if private[x][5]>0 : npv_pri_median += (private[x][5]) / ir
		if public[x][5]>0 : npv_pub_median += (public[x][5]) / ir
	for x in range(48):
		ir = math.pow(i,x)
		if non[x][4]>0 : npv_non_mean += (non[x][4]) / ir
		if non[x][5]>0 : npv_non_median += (non[x][5]) / ir
	print "\n At %f interest rate: public NPV lifetime salary -> mean = %f median = %f" % (i-1, npv_pub_mean, npv_pub_median)
	print "\n At %f interest rate: private NPV lifetime salary -> mean = %f median = %f" % (i-1, npv_pri_mean, npv_pri_median)
	print "\n At %f interest rate: highsch NPV lifetime salary -> mean = %f median = %f" % (i-1, npv_non_mean, npv_non_median)


pub_mean = np.append(np.array([0,0,0]),[row[4] for row in public])
pri_mean = np.append(np.array([0,0,0]),[row[4] for row in private])
pub_med = np.append(np.array([0,0,0]),[row[5] for row in public])
pri_med = np.append(np.array([0,0,0]),[row[5] for row in private])
non_mean = [row[4] for row in non]
non_med = [row[5] for row in non]
f, axarr= plt.subplots(2,sharex=True)
axarr[0].plot(np.arange(19,67),pub_mean,'bs',label='Mean(public)')
axarr[0].plot(np.arange(19,67),pub_med,'b^',label='Median(public)')
axarr[0].plot(np.arange(19,67),pri_mean,'rs',label='Mean(private)')
axarr[0].plot(np.arange(19,67),pri_med,'r^',label='Median(private)')
axarr[0].plot(np.arange(19,67),non_mean,'gs',label='Mean(highsch)')
axarr[0].plot(np.arange(19,67),non_med,'g^',label='Median(highsch)')
axarr[0].set_title('Mean & Median Annual Salary at Age')
axarr[0].legend(bbox_to_anchor=(0.2, 1.0))
axarr[1].plot(np.arange(19,67),np.cumsum(pub_mean),'b-',label='Mean(public)')
axarr[1].plot(np.arange(19,67),np.cumsum(pub_med),'b--',label='Median(public)')
axarr[1].plot(np.arange(19,67),np.cumsum(pri_mean),'r-',label='Mean(private)')
axarr[1].plot(np.arange(19,67),np.cumsum(pri_med),'r--',label='Median(private)')
axarr[1].plot(np.arange(19,67),np.cumsum(non_mean),'g-',label='Mean(highsch)')
axarr[1].plot(np.arange(19,67),np.cumsum(non_med),'g--',label='Median(highsch)')
axarr[1].set_title('Mean & Median Cummulative Salary at Age')

axarr[1].legend(bbox_to_anchor=(0.2, 1.0))
plt.ylabel('US 2013 Dollars') 
plt.xlabel('Age')
plt.grid(True)

plt.show()


filenames = ['pub.csv','private.csv','high.csv']