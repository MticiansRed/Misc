import math
import numpy as np
import matplotlib.pyplot as plt
import csv

def GetData(file_name):
	r = []
	dpm = []
	with open(file_name, newline='') as csvfile:
		datareader = csv.reader(csvfile, delimiter=',', quotechar = '|')
		for row in datareader:
			r.append(row[0])
			dpm.append(row[1])
		r_np = np.array(r)
		dpm_np = np.array(dpm)
		res = np.vstack((r_np, dpm_np))
		res = res.astype(float)
		print(res)
		return res
		
def GetPlot(inp_data, k):
	
	plt.figure(k)
	plt.grid()
	plt.plot(inp_data[0],inp_data[1])
	plt.xlim(0, 0.006)
	plt.ylim(0,500)
	plt.xlabel(r'$Расстояние \quad от \quad оси \quad симметрии, \quad м$', fontsize = 12)
	plt.ylabel(r'$Концентрация, \quad кг/м^3$', fontsize = 12)
	#data_polyreg = np.poly1d(np.polyfit(inp_data[0], inp_data[1], 12))
	#plt.plot(inp_data[0], data_polyreg(inp_data[0]))
	#plt.show()
	
def GetRiemann(inp_data):
	set_len = len(inp_data[0])
	intsum = 0
	for i in range(set_len-1):
		dr = inp_data[0, i+1]-inp_data[0, i]
		dn = inp_data[1, i+1]-inp_data[1, i]
		intsum = intsum + dr*inp_data[1,i]+0.5*dr*dn #trapezoid formula
	return intsum
	
def Avg(inp_data): #input_data = [ .. ]
	set_len = len(inp_data)
	set_sum = 0
	for i in range(set_len):
		set_sum = set_sum+inp_data[i] 
	return set_sum/set_len
	
def Standard_Deviation(inp_data):
	avg = Avg(inp_data[1])
	sd = 0
	n = len(inp_data[0])
	for i in range(n):
		sd = sd+(inp_data[1,i]-avg)**2
	sd = sd/n
	sd = np.sqrt(sd)
	return sd
	
def GetPeak(inp_data):
	r_pk = 0
	n_pk = 0
	for i in range(len(inp_data[0])):
		if inp_data[1,i]>n_pk:
			n_pk = inp_data[1,i]
			r_pk = inp_data[0,i]
	return(r_pk, n_pk)

def Polyreg(x, y):
	data_polyreg = np.poly1d(np.polyfit(x, y, 2))
	plt.plot(x, data_polyreg(x))

def Avg_n_planes(inp_data_planes): #([inp_data_p1, inp_data_p2, inp_data_p3, inp_data_p4])
	averaged_n = []
	set_len = len(inp_data_planes[0][1])
	for i in range(set_len):
		for k in [0,1,2,3]:
			n_i_sum = inp_data_planes[k][1,i] 
		n_i = n_i_sum/4
		averaged_n.append(n_i)
	return averaged_n
		
	
		
		
dpm = [[],[],[]]

dev = [[],[],[]]
pk_r = [[],[],[]]
pk_r_avg = []
pk_n = [[],[],[]]
pk_n_avg = []
sd = [[],[],[]]
sd_avg = []
uplotarea = []
z = [0.09, 0.1065, 0.123, 0.1395, 0.156, 0.173, 0.19]
dpm[0].append(GetData('nodiffusor_p1_csv.csv'))
dpm[0].append(GetData('nodiffusor_p1.5_csv.csv'))
dpm[0].append(GetData('nodiffusor_p2_csv.csv'))
dpm[0].append(GetData('nodiffusor_p2.5_csv.csv'))
dpm[0].append(GetData('nodiffusor_p3_csv.csv'))
dpm[0].append(GetData('nodiffusor_p3.5_csv.csv'))
dpm[0].append(GetData('nodiffusor_p4_csv.csv'))

dpm[1].append(GetData('diffusor_p1_csv.csv'))
dpm[1].append(GetData('diffusor_p1.5_csv.csv'))
dpm[1].append(GetData('diffusor_p2_csv.csv'))
dpm[1].append(GetData('diffusor_p2.5_csv.csv'))
dpm[1].append(GetData('diffusor_p3_csv.csv'))
dpm[1].append(GetData('diffusor_p3.5_csv.csv'))
dpm[1].append(GetData('diffusor_p4_csv.csv'))

dpm[2].append(GetData('nozzle_p1_csv.csv'))
dpm[2].append(GetData('nozzle_p1.5_csv.csv'))
dpm[2].append(GetData('nozzle_p2_csv.csv'))
dpm[2].append(GetData('nozzle_p2.5_csv.csv'))
dpm[2].append(GetData('nozzle_p3_csv.csv'))
dpm[2].append(GetData('nozzle_p3.5_csv.csv'))
dpm[2].append(GetData('nozzle_p4_csv.csv'))


#for i in range(3):
#	avg_n_plane = Avg_n_planes( [dpm[i][0], dpm[i][1], dpm[i][2], dpm[i][3]] ) #different sets has various dim
#	for k in range(len(avg_n_plane)):
#		averaged_dpm[i][1,k] =  avg_n_plane[k]

plt.figure(0)
plt.xlim(0.08, 0.2)
plt.xlabel(r'$Расстояние \quad от \quad источника \quad порошка, \quad м$', fontsize = 12)
plt.ylabel(r'$Среднеквадратичное \quad отклонение$', fontsize = 12)
for k in range(len(dpm)):
	for j in range(len(dpm[k])):
		#pk_r[k][j] = GetPeak(dpm[k][j])[0]
		#pk_n[k][j] = GetPeak(dpm[k][j])[1]
		pk_r[k].append(GetPeak(dpm[k][j])[0])
		pk_n[k].append(GetPeak(dpm[k][j])[1])
		sd[k].append(Standard_Deviation(dpm[k][j]))

	pk_r_avg.append(Avg(pk_r[k]))
	pk_n_avg.append(Avg(pk_n[k]))
	sd_avg.append(Avg(sd[k]))
	

plt.plot(z, sd[0], color='red', label=r'$Без \quad диффузора$')
plt.scatter(z, sd[0], color='red')
#data_polyreg = np.poly1d(np.polyfit(z, sd[0], 3))
#plt.plot(z, data_polyreg(z), color = 'red')
	
plt.plot(z, sd[1], color='blue', label=r'$Конический \quad диффузор$')
plt.scatter(z, sd[1], color='blue')
#data_polyreg = np.poly1d(np.polyfit(z, sd[1], 3))
#plt.plot(z, data_polyreg(z), color = 'blue')

plt.plot(z, sd[2], color='green', label=r'$Диффузор-сопло$')
plt.scatter(z, sd[2], color='green')
#data_polyreg = np.poly1d(np.polyfit(z, sd[2], 3))
#plt.plot(z, data_polyreg(z), color = 'green')

plt.legend(loc = 'best', fontsize = 12)
plt.grid()

plt.figure()
plt.xlim(0.08, 0.2)
plt.ylim(250,600)
plt.xlabel(r'$Расстояние \quad от \quad источника \quad порошка, \quad м$', fontsize = 12)
plt.ylabel(r'$Пиковая \quad концентрация, \quad кг/м^3$', fontsize = 12)
plt.plot(z, pk_n[0], color='red', label=r'$Без \quad диффузора$')
plt.scatter(z, pk_n[0], color='red')

plt.plot(z, pk_n[1], color='blue', label=r'$Конический \quad диффузор$')
plt.scatter(z, pk_n[1], color='blue')

plt.plot(z, pk_n[2], color='green', label=r'$Диффузор-сопло$')
plt.scatter(z, pk_n[2], color='green')

plt.legend(loc = 'best', fontsize = 12)
plt.grid()

plt.figure()
plt.xlim(0.08, 0.2)

plt.xlabel(r'$Расстояние \quad от \quad источника \quad порошка, \quad м$', fontsize = 12)
plt.ylabel(r'$Координата \quad пиковой \quad концентрации, \quad м$', fontsize = 12)
plt.plot(z, pk_r[0], color='red', label=r'$Без \quad диффузора$')
plt.scatter(z, pk_r[0], color='red')

plt.plot(z, pk_r[1], color='blue', label=r'$Конический \quad диффузор$')
plt.scatter(z, pk_r[1], color='blue')

plt.plot(z, pk_r[2], color='green', label=r'$Диффузор-сопло$')
plt.scatter(z, pk_r[2], color='green')

plt.legend(loc = 'best', fontsize = 12)
plt.grid()


print(pk_r_avg)
print(pk_n_avg)

plt.figure()	
plt.plot(['Без диффузора', 'Конический диффузор', 'Диффузор-сопло'], pk_n_avg) #Average peak n for each geometry
plt.scatter(['Без диффузора', 'Конический диффузор', 'Диффузор-сопло'], pk_n_avg)

plt.xlabel(r'$Тип \quad диффузора$', fontsize = 12)
plt.ylabel(r'$Средняя \quad пиковая \quad концентрация, \quad кг/м^3$', fontsize = 12)
plt.grid()

plt.figure()	
plt.plot(['Без диффузора', 'Конический диффузор', 'Диффузор-сопло'], pk_r_avg)#Average peak n r coordinate for each geometry
plt.scatter(['Без диффузора', 'Конический диффузор', 'Диффузор-сопло'], pk_r_avg)

plt.xlabel(r'$Тип \quad диффузора$', fontsize = 12)
plt.ylabel(r'$Координата \quad  средней \quad пиковой \quad концентрации, \quad м$', fontsize = 10)
plt.grid()

plt.figure()	
plt.plot(['Без диффузора', 'Конический диффузор', 'Диффузор-сопло'], sd_avg)#Average standdev
plt.scatter(['Без диффузора', 'Конический диффузор', 'Диффузор-сопло'], sd_avg)

plt.xlabel(r'$Тип \quad диффузора$', fontsize = 12)
plt.ylabel(r'$Среднеквадратичное \quad отклонение$', fontsize = 12)
plt.grid()	



if False:
	for i in range(len(dpm)):
		GetPlot(dpm[0][i], i)
		dev[i].append(Avg_deviation(dpm[0][i], Avg_n(dpm[0][i])))
		pk_r[i].append(GetPeak(dpm[0][i])[0])
		pk_n[i].append(GetPeak(dpm[0][i])[1])
		uplotarea[i].append(GetRiemann(dpm[0][i]))
	
	plt.figure(5)
	plt.plot(z, dev)
	plt.scatter(z, dev)
	plt.xlabel(r'$Расстояние \quad от \quad источника \quad порошка, \quad м$', fontsize = 12)
	plt.ylabel(r'$Отклонение \quad от \quad средней \quad концентрации, \quad м$', fontsize = 12)
	plt.grid()

	plt.figure(6)
	plt.plot(z, pk_n)
	plt.scatter(z, pk_n)
	plt.xlabel(r'$Расстояние \quad от \quad источника \quad порошка, \quad м$', fontsize = 12)
	plt.ylabel(r'$Максимальная \quad концентрация, \quad кг/м^3$', fontsize = 12)
	plt.grid()

	plt.figure(7)
	plt.plot(z, pk_r)
	plt.scatter(z, pk_r)
	plt.xlabel(r'$Расстояние \quad от \quad источника \quad порошка, \quad м$', fontsize = 12)
	plt.ylabel(r'$Точка \quad максимальной \quad концентрации, \quad кг/м^3$', fontsize = 12)
	plt.grid()

	plt.figure(8)
	plt.plot(z, uplotarea)
	plt.scatter(z, uplotarea)
	plt.grid()


plt.show() 

	

