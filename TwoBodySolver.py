import numpy as np
from numpy import cos,sin
from scipy.integrate import odeint



#Datos generales
muTierra = 398600 #[km^3/s^2]
R_e = 6378 #[km]
J_2 = 0.00108263
f = 0.003353 



def SatPoints(hours,steps,rogvog):
    tf = hours*3600 #Tiempo [s] 
    pasos = steps

    #Resolucion
    y0 = rogvog #Vector de estado
    t = np.linspace(0, tf, pasos)

    def ec(y,t):
        X,Y,Z,Vx,Vy,Vz = y

        #i,omega,Omega,theta,r = Keplerianos(y)

        pX,pY,pZ = 0,0,0
        pos = np.linalg.norm([X,Y,Z])
        # Ecuaciones de estado
        Ax = -muTierra*(X)/pos**3 + pX
        Ay = -muTierra*(Y)/pos**3 + pY
        Az = -muTierra*(Z)/pos**3 + pZ


        return([Vx,Vy,Vz,Ax,Ay,Az])

    sol = odeint(ec, y0, t)


    x = []
    y = []
    z = []

    for i in sol:
        x.append(i[0])
        y.append(i[1])
        z.append(i[2])

    points = np.column_stack((x,y,z))

    return points






