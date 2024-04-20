import csv
import numpy as np
import math
import matplotlib.pyplot as plt

def GetData(file_name):
	I = []
	la = []
	with open(file_name, newline='') as csvfile:
		datareader = csv.reader(csvfile, delimiter=',', quotechar = '|')
		for row in datareader:
			la.append(row[0])
			I.append(row[1])
		la_np = np.array(la)
		I_np = np.array(I)
		res = np.vstack((la_np, I_np))
		res = res.astype(float)
		print(res)
		return res
def GetEps(spec_data):
	max_dist = 0
	for i in range(len(spec_data[1])-1):
		dist = spec_data[1,i+1]-spec_data[1,i]
		if dist>max_dist:
			max_dist = dist
	return max_dist

def PlotSpectrum(spec_data, la_lim_bot = 300, la_lim_top = 800, I_lim = 8000, trp=1):
	#plt.figure()
	plt.xlim(la_lim_bot, la_lim_top)
	plt.ylim(0, I_lim)
	plt.grid()
	plt.plot(spec_data[0], spec_data[1], alpha=trp)
	plt.xlabel(r'$Длина \quad волны, \quad нм$', fontsize = 12) 
	plt.ylabel(r'$Интенсивность,\quad отн. \quad ед.$', fontsize = 12)
	#plt.show() 
	
def GetPeak(spec_data):
	la_pk = 0
	I_pk = 0
	i_pk = 0
	for i in range(len(spec_data[0])):
		if spec_data[1,i]>I_pk:
			I_pk = spec_data[1,i]
			la_pk = spec_data[0,i]
			i_pk = i
	return[la_pk, I_pk, i_pk]

def GetFWHM(spec_data, eps = 100):
	la_pk, I_pk = GetPeak(spec_data)[0], GetPeak(spec_data)[1]
	i_pk = GetPeak(spec_data)[2]
	i_step = i_pk
	i_right_border = len(spec_data[1])-1
	while ( (abs(I_pk/2-spec_data[1,i_step])>=eps) and (i_step>0) ):
		i_step = i_step-1
		la_left = spec_data[0, i_step]
	i_step = i_pk
	while ( (abs(I_pk/2-spec_data[1,i_step])>=eps) and (i_step<i_right_border) ):
		i_step = i_step+1
		la_right = spec_data[0, i_step]
	FWHM_la = la_right - la_left
	return FWHM_la
	
def GetFWHM_sym(spec_data, eps = 100):
	la_pk, I_pk = GetPeak(spec_data)[0], GetPeak(spec_data)[1]
	i_pk = GetPeak(spec_data)[2]
	i_step = i_pk
	while ( (abs(I_pk/2-spec_data[1,i_step])>=eps) and (i_step>0) ):
		i_step = i_step-1
		la_left = spec_data[0, i_step]
	FWHM_la = (la_pk - la_left)*2
	return FWHM_la		

#spectrum(T)--- 
spec_T = []
I_pk_T = []
la_pk_T = []
for T in range(-5, 50, 5):
	filename = str(T)+'.csv'
	spec_T.append(GetData(filename))
	I_pk_T.append(GetPeak(GetData(filename))[1])
	la_pk_T.append(GetPeak(GetData(filename))[0])
	
plt.figure()
for i in range(len(spec_T)):
	PlotSpectrum(spec_T[i], 620, 690, trp = 0.5)
plt.plot(la_pk_T, I_pk_T, color = 'red')
plt.scatter(la_pk_T, I_pk_T, color = 'red')
	
	

#FWHM---
fwhm = []
for i in range(len(spec_T)):
	fwhm.append(GetFWHM_sym(spec_T[i], GetEps(spec_T[i])))
	print(fwhm[i])

T = range(-5, 50, 5)
plt.figure()
plt.grid()
plt.plot(T, fwhm, alpha = 0.5)
plt.scatter(T, fwhm, color = 'red')
polyreg = np.poly1d(np.polyfit(T, fwhm, 5))
plt.plot(T, polyreg(T), color = 'green')

#spectrum(current)---
spec_j = []
for j in map(lambda x: x/10.0, range(10, 55, 5)):
	filename = str(j)+'_ma.csv'
	spec_j.append(GetData(filename))
for j in range(5, 35, 5):
	filename = str(j)+'_ma.csv'
	spec_j.append(GetData(filename))
	
plt.figure()
for i in range(len(spec_j)):
	PlotSpectrum(spec_j[i], 620, 690, 12000)

plt.show()

	
