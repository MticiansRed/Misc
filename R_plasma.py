import numpy as np

#global vars
c = 3*10**8
eps_0 = 8.854*10**(-12)
mu_0 = 1.25663706212*10**-6
m_e = 9.1093837*10**-31
c_e = 1.60217663*10**-19
N_A = 6.02214*10**23
rho = 1.784
m_molar = 0.03995
v_m_per_N = 5*10**-15 #DOI: 10.1088/0022-3700/14/9/013
r_0 = 16*10**-3
r_c = 18.5*10**-3
l = 37.9*10**-3
w = np.pi*2*5.28*10**6
n_e_cm3 = 1*10**16 #Kornblum, G.R.; de Galan, L.  (1974). Arrangement for measuring spatial distributions in an argon induction coupled RF plasma. Spectrochimica Acta Part B: Atomic Spectroscopy, 29(9-10), 249–261.         doi:10.1016/0584-8547(74)80040-6     
n_e = n_e_cm3*10**6
P_diss = 5*10**3
N = 3
fix_coeff = 42/16 #Coefficient to fix I_coil calculated using Eckert's n_e to "experimental" data

#sigma = 2500 S/m, according to Tsivilskiy. Use this to obtain other params from formula for sigma_m: σ_m=(n_e e^2)/(m_e ε_0 )

print(fix_coeff)

#functions
def Get_v_m(v_m_per_N, m_molar, rho):
	N = N_A*rho/m_molar
	return v_m_per_N*N 
#def GetR_plasma(r_0, l, w, v_m, n_e):
#	R_p = np.sqrt( (np.pi**2*r_0**2*2*w*m_e*v_m)/(l**2*c**2*eps_0*n_e*c_e**2) )
#	return R_p
def GetCurrent(R_plasma, P_diss):
	return np.sqrt(2*P_diss/R_plasma)
def GetR_ind(r_0, l, w, v_m, n_e, mu_0, N): #7.28 in Pascal-Chambert
	R_ind = (n_e*c_e**2*w**2*mu_0**2*np.pi*r_0**4*N**2)/(2*m_e*l*v_m)
	return R_ind
def GetInductance(r_c, l, mu_0, N):
	return (mu_0*np.pi*r_c**2*N**2)/l
def GetX_l(w, L):
	return w*L
def GetCurrent_X_l(X_l, P_diss): #shows best result
	return np.sqrt(P_diss/X_l)
def GetEckerts_n_e(r_0):
	return 10**20/r_0
	
#main body
v_m = Get_v_m(v_m_per_N, m_molar, rho)
n_e_E = GetEckerts_n_e(r_0)
I_coil_X_l = GetCurrent_X_l(GetX_l(w, GetInductance(r_c, l, mu_0, N)), P_diss)
print('Given power: '+str(P_diss)+' W')
print('Calculated average collision frequency: '+str(v_m)+' 1/s')
print('Given n_e: '+str(float(n_e))+' 1/m^3')
print('Eckerts n_e: '+str(n_e_E)+' 1/m^3')
R_ind = GetR_ind(r_0, l, w, v_m, n_e, mu_0, N)
I_coil_R_ind = GetCurrent(GetR_ind(r_0, l, w, v_m, n_e, mu_0, N), P_diss)
print('Calculated R_ind active resistance: '+str(R_ind)+' Ohm')
print('Calculated R_ind active resistance using Eckerts n_e: '+str(GetR_ind(r_0, l, w, v_m, n_e_E, mu_0, N))+' Ohm')
print('Calculated coil current from R_ind: '+str(I_coil_R_ind)+' A')
print('Calculated coil current from R_ind using Eckerts n_e: '+str(GetCurrent(GetR_ind(r_0, l, w, v_m, n_e_E, mu_0, N), P_diss))+' A, '+str(fix_coeff*GetCurrent(GetR_ind(r_0, l, w, v_m, n_e_E, mu_0, N), P_diss)))
print('Calculated coil current from reactive resistance X_l: '+str(I_coil_X_l)+' A')
