import csv
import numpy as np
import math
import matplotlib.pyplot as plt


def mc(benefit_p,benefit_high,g,cost,runs):
	out = []
	for i in range(runs):
		grad = []
		grad.append(np.random.uniform(g[0][0],g[0][1]))
		grad_1 = np.random.uniform(g[1][0],g[1][1])
		if grad_1<grad[0]:
			while grad_1<grad[0]:
				grad_1=np.random.uniform(g[1][0],g[1][1])
		grad.append(grad_1)
		grad_2 = np.random.uniform(g[2][0],g[2][1])
		if grad_2<grad[0]:
			while grad_2<grad[1]:
				grad_2=np.random.uniform(g[2][0],g[2][1])
		grad.append(grad_2)
		interest = 1 + np.random.uniform(0.00,0.06)
		p = np.random.random()*100
		c = None
		npv_b=0
		debt_npv=0
		if p>grad[2]:
			c=0 #failed college
			for i in range(48):
				sd=benefit_high[i][1]
				if sd<1:
					sd=1
				y_i = np.random.normal(benefit_high[i][0],sd)
				npv_b += y_i/math.pow(interest,i)
		elif p>grad[1] and p<=grad[2]:
			c = 1 #six years taken to graduate
			debt = ((np.random.normal(cost[0],cost[1])/4) * 6)/15
			debt_i = 1+np.random.uniform(0.03,0.07)
			debt_npv = 0
			for i in range(15):
				debt_npv+=(debt)/math.pow(debt_i,i)
			for i in range(48):
				sd=benefit_p[i][1]
				if sd<1:
					sd=1
				y_i = np.random.normal(benefit_p[i][0],sd)
				if i>4:
					npv_b += y_i/math.pow(interest,i)
		elif p> grad[0] and p<=grad[1]:
			c= 2 # five years taken to graduate
			debt = ((np.random.normal(cost[0],cost[1])/4) * 5)/15
			debt_i = 1+np.random.uniform(0.03,0.07)
			debt_npv = 0
			for i in range(15):
				debt_npv+=(debt)/math.pow(debt_i,i)
			for i in range(48):
				sd=benefit_p[i][1]
				if sd<1:
					sd=1
				y_i = np.random.normal(benefit_p[i][0],sd)
				if i>3:
					npv_b += y_i/math.pow(interest,i)
		else:
			c=3 # graduates in four years
			debt = np.random.normal(cost[0],cost[1])/15
			debt_i = 1+np.random.uniform(0.03,0.07)
			debt_npv = 0
			for i in range(15):
				debt_npv+=(debt)/math.pow(debt_i,i)
			for i in range(48):
				sd=benefit_p[i][1]
				if sd<1:
					sd=1
				y_i = np.random.normal(benefit_p[i][0],sd)
				if i>2:
					npv_b += y_i/math.pow(interest,i)
		print c			
		print npv_b
		out.append(npv_b-debt_npv)
	return out




def parsef(input,n):
	out = []
	with open(input, 'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			out.append([float(row['med']), float(row['sd'])])
	return out

#Public
high_b= parsef("high.csv",48)
pub_b = parsef("pub.csv",48)
pub_g = [[24.2,72.2],[47.0,88.6],[55.0,91.0]]
pub_mc = mc(pub_b, high_b, pub_g ,[13744,4905], 10000)

pri_b = parsef("pri.csv",48)
pri_g = [[68.5,83.5],[79.2,91.4],[81.0,93.0]]
pri_mc = mc(pri_b, high_b, pri_g, [15656,5714] , 10000)
print pub_mc
print pri_mc
print "Pub: mean =%f, median = %f" % (np.mean(pub_mc),np.median(pub_mc))
print "Pri: mean =%f, median = %f" % (np.mean(pri_mc),np.median(pri_mc))

plt.hist(pub_mc,bins=25,color='b', alpha=0.7, label="Public School")
plt.hist(pri_mc,bins=25,color='g', alpha=0.7, label="Private School")
plt.title("Monte Carlo Simulation: 10000 runs")
plt.xlabel("NPV(Net Benefit)")
plt.ylabel("Frequency")
plt.legend()
plt.show()