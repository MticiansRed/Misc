import numpy as np
import csv
import matplotlib.pyplot as plt
import math 

def GetData(file_name): #[[stroka_1_content],[stroka_2_content],[stroka_3_contet] ...]
	data = []
	data_T = []
	i=-1
	with open(file_name, newline='') as csvfile:
		datareader = csv.reader(csvfile, delimiter=',', quotechar = '|')
		for row in datareader:
			i=i+1
			data.append([])
			for j in range(len(row)):
				data[i].append(row[j])

		for i in range(len(data)):
			for j in range(len(data[0])):
				try:
					data[i][j] = float(data[i][j])
				except Exception:
					pass
		for i in range(len(data[0])): #Транспонируем полученную матрицу так, чтобы в строках были записаны столбцы исходного датасета
			data_T.append([])		  # это нужно для удобства дальнейшей работы
			for j in range(len(data)):
				data_T[i].append(data[j][i])
		#print('Read data:')
		#for i in range(len(data_T)):
		#	print(data_T[i])
		return data_T
		
def GetParticleData(inp_data, n_prt, stt_flag = ['((xy/key/label particle-',')'], end_flag = [')']):
	ParticleData = [[],[]]
	in_s = 0
	for i in range(len(inp_data[0])):
		if inp_data[0][i] == end_flag[0]:
			in_s = 0
		if in_s == 1:
			ParticleData[0].append(inp_data[0][i]) 
			ParticleData[1].append(inp_data[1][i])
		if inp_data[0][i] == stt_flag[0]+str(n_prt)+stt_flag[1]:
			in_s = 1
	#print(ParticleData)
	return(ParticleData)

def Line( x_start, x_end, y_pos, style, color, label_local):
	x_field = np.dot( list(range(int(x_start*1e+3), int(x_end*1e+3+1))), 1e-3 )
	y_field = [y_pos]*len(x_field)
	plt.plot(x_field, y_field,style+color, label = label_local)

def IsMolten(inp_data, T_melt, t_melt):
	i = len(inp_data[0])-1
	criterion = 1
	while inp_data[0][i]>(inp_data[0][-1]-t_melt):
		if inp_data[1][i]<T_melt:
			criterion = 0
		i-=1
	return criterion

def MoltenPath(inp_data, T_melt):
	t_melt_field = []
	T_melt_field = []
	for i in range(len(inp_data[0])):
		if inp_data[1][i]>T_melt:
			t_melt_field.append(inp_data[0][i])
			T_melt_field.append(inp_data[1][i])
	return [t_melt_field, T_melt_field]
	

#vars
T_melt = 1943
T_boil = 3560
t_melt = 0.0018899546279491828
n_molten = 0
#getting data
dataset = GetData('ParticleTrackXYfile_csv.csv')
AllParticles = []
for n in range(1,44):
	AllParticles.append(GetParticleData(dataset, n))
#main body
plt.figure()
plt.grid()
for particle_data in AllParticles:
	x_field = particle_data[0]
	y_field = particle_data[1]
	plt.plot(x_field, y_field, linewidth = 0.5)
	n_molten+=IsMolten(particle_data, T_melt, t_melt)
	plt.plot(MoltenPath(particle_data, T_melt)[0], MoltenPath(particle_data, T_melt)[1], 'r', linewidth = 1.0)
	
plt.xlabel(r'$Время\quadполета\quadчастицы,\quadс$', fontsize = 12)
plt.ylabel(r'$Температура\quadчастицы,\quadК$', fontsize = 12)
	
Line(0,0.28, T_boil, '--', 'b', r'$Температура\quadкипения$' )
Line(0,0.28, T_melt, '--', 'r', r'$Температура\quadплавления$'  )
plt.legend(loc = 'upper left', bbox_to_anchor=(0, 0.9) )
print('Число расплавленных частиц:')
print(n_molten)
print('Число нерасплавленных частиц:')
print(43-n_molten)
print('Коэффициент сфероидизации:')
print(n_molten/43)
plt.show()
