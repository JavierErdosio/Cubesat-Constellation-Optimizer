import numpy as np


muTierra = 398600 #[km^3/s^2]


def Keplerianos(StateVector):
    y = StateVector

    r0 = np.array([y[0],y[1],y[2]])
    v0 = np.array([y[3],y[4],y[5]])

    #1)
    r = np.linalg.norm(r0) #Modulo vector posicion

    #2)
    v = np.linalg.norm(v0) #Modulo velocidad

    #3)
    vr = (v0 @ r0)/r #Velocidad radial (@ hace producto punto)

    #4)
    h_vec = np.cross(r0,v0) #Vector momento angular especifico actual

    #5)
    h = np.linalg.norm(h_vec) #Momento angular especifico actual

    #6)
    i = np.acos(h_vec[2]/h) #Inclinacion

    #7)
    N_vec = np.cross(np.array([0,0,1]),h_vec) #Vector que define la linea de los nodos

    #8)
    N = np.linalg.norm(N_vec)

    #9)
    if N_vec[1] < 0:
        Omega = 2*np.pi-np.acos(N_vec[0]/N) #Ascencion recta
    else:
        Omega = np.acos(N_vec[0]/N)

    #10)
    e_vec = 1/muTierra*((v**2 - muTierra/r)*r0 - r*vr*v0) #Vector excentricidad

    #11)
    e = np.linalg.norm(e_vec) #Excentricidad

    #12)
    if e_vec[2]<0:
        omega = 2*np.pi-np.acos((N_vec @ e_vec)/(N*e)) #Argumento del perigeo
    else:
        omega = np.acos((N_vec @ e_vec)/(N*e))

    #13)
    theta = np.acos((e_vec @ r0)/(e*r)) #Anomalia verdadera actual

    return(h,i,omega,Omega,theta,e)