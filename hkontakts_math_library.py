import numpy as np
import matplotlib.pyplot as plt
	
def LinearInterpolation(x_array, x_array_extended, y_array): #линейная интерполяция
	dx = x_array[1]-x_array[0]
	dx_extended = x_array_extended[1]-x_array_extended[0] #!!!Пофиксить интерполяцию, чтобы можно было интерполировать из набора данных с неравномерным распределением иксов (считать число шагов n по dx от x[i] до x[i+1] каждый раз заново)
	y_array_extended = []
	k = []
	b = []
	i = 0
	for i in range(len(x_array)-1):
		dy = y_array[i+1]-y_array[i]
		k.append(dy/dx)
		b.append(y_array[i])
		y_array_extended.append(y_array[i])
		for n in range(int( dx/dx_extended )-1):
			y_array_extended.append(k[i]*(n+1)*dx_extended+b[i])
	y_array_extended.append(y_array[-1])
	return y_array_extended
		
def Fourier(x_array_extended, y_array_extended, n): #разложение в ряд Фурье
	T = x_array_extended[-1]-x_array_extended[0]
	dx_extended = x_array_extended[1]-x_array_extended[0]
	w = 2*3.14159265/T
	print('w = '+str(w))
	a = [0]*(n+1)
	b = [0]*(n+1)
	y_Fourier = [0]*len(x_array_extended)
	for i in range(len(x_array_extended)-1): #интегрируем от -T/2 до T/2 (по всей рассчетной области для нахождения коэфф. a0
		a[0]+=(2/T)*y_array_extended[i]*dx_extended
	print('a[0] = '+str(a[0]))
	for k in np.arange(1, n+1, 1).tolist():
		for i in range(len(x_array_extended)-1): #интегрируем от -T/2 до T/2 (по всей рассчетной области) для нахождения остальных коэффициентов
			a[k]+=(2/T)*y_array_extended[i]*np.cos(k*w*x_array_extended[i])*dx_extended
			b[k]+=(2/T)*y_array_extended[i]*np.sin(k*w*x_array_extended[i])*dx_extended
		print('a[k] = '+str(a[k]) + ' b[k] = '+str(b[k]))
	for i in range(len(x_array_extended)):
		y_Fourier[i] += a[0]/2
		for k in np.arange(1, n+1, 1).tolist():
			y_Fourier[i] += a[k]*np.cos(k*w*x_array_extended[i])+b[k]*np.sin(k*w*x_array_extended[i])
			print('y_Fourier = ' + str(y_Fourier[i])+' x = ' + str(x_array_extended[i]) + ' i = '+str(i) + ' k = ' + str(k))
	return y_Fourier
	

def GradToRad(x): #Быстро перевести список из градусов в радианы
	return ( np.dot(x, 3.14159265/180) ).tolist()
	
def ErrorFunction(x_array, f_compare, f_reference): #Функция ошибки по y. Возвращает среднее отклонение в %
	err_array = []
	for x in x_array:
		err_array.append( abs(f_compare[x]-f_reference[x]) )
	return sum(err_array)/len(err_array)
	
def Tester(n_steps):
	data_x = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
	data_y = [2, 3, 4, 2, 20, 21, 25, 19, 5, 4, 2, 4]
	step = (data_x[1]-data_x[0])/n_steps
	data_x_extended = np.arange(data_x[0], data_x[-1]+step, step).tolist()
	data_y_interpolated = LinearInterpolation(data_x, data_x_extended, data_y)
	y_Fourier = Fourier(data_x_extended, data_y_interpolated, 100)
	plt.plot(data_x_extended, y_Fourier, 'r--', label=r'$График \quad функции,\quad аппроксимированной \quad рядом \quad Фурье $')
	plt.plot(data_x, data_y, color='blue', label=r'$График \quad по \quad исходным \quad данным$')
	plt.xlabel(r'$x$', fontsize = 14)
	plt.ylabel(r'$y$', fontsize = 14)
	plt.legend(loc='best', fontsize = 14)
	plt.grid()
	plt.show()
	return 0
	
Tester(100)

def Mikhailovs_godograph(Tf_coeffs, w_max=50, step=0.1): #!В ПРОЦЕССЕ! использовать символьные вычисления???
	Tf=0
	for i in range(Tf_coeffs):
		Tf+=(Tf_coeffs[i]*1j)**(len(Tf_coeffs)-i)
	def x_w(w):
		return real(w)
	
	def y_w(w):
		return im(w)
		
	w_np = np.arange(0, w_max, step)
	w = w_np.tolist()
	x_out = []
	y_out = []
	for i in w:
		x_out.append(x_w(i))
		y_out.append(y_w(i))
		print('w = '+str(i)+' X =  '+str( x_w(i) )+' Y =  '+str( y_w(i) ))
	x_out_np = np.array(x_out)
	y_out_np = np.array(y_out)
	plt.plot(x_out_np, y_out_np)
	plt.grid()
	plt.show()
	return 0

	
