import numpy as np
from stateVector import stateVector
from Keplerianos import Keplerianos
from TwoBodySolver import SatPoints
from ThreeDimGraph import ThreeDimGraph as ThreeDimGraph
from TwoDimPlot import TwoDimPlot
from revisitTime import revisitTime
from time import time

muEarth = 398600 #[km^3/s^2]
Re = 6378 #Earth Radius

#Extras
Video = False
SatCount = 3
orbPlaneCount = 3


#Time data
hours = 23.93446944 #Sidereal day 
steps = 30*60 #30 seconds and 60 frames per second

#Satellite
cameraAngle = 4.46 #[deg]
maxAltitude = 1700 #[km] based on antenna and camera maximum values 

#Orbit
e = 0.07306#[-] Excentricidad
hp = 600 #[km] Altura del perigeo
inc = np.deg2rad(-63.4394882) #[rad] Inclinación
omega = np.deg2rad(270) #[rad] Argumento del perigeo

RAAN = np.linspace(0, 2*np.pi, orbPlaneCount+1)
RAAN = RAAN[0:orbPlaneCount]

theta = np.linspace(0, 2*np.pi, SatCount+1)
theta = theta[0:SatCount]

#Verification that apoapsis does not exceed maximum altitude
Rmax = maxAltitude+Re
Rp = hp + Re

emax = (Rmax-Rp)/(Rmax+Rp)

if e > emax:
    print("[WARN] Apoapsis is higher than maximum altitude for your antenna or camera. Maximum excentricty = %.5f km. Selected excentricity = %.5f" %(emax,e))


#Initial state vector
SatRogVog = {}

for i in range(len(RAAN)):
    for j in range(len(theta)):
        SatRogVog["Sat%i%i"%(i,j)] = stateVector(e,hp,inc,RAAN[i],omega,theta[j])



#Orbit points
Orbits = {}
for i in SatRogVog: 
    points = SatPoints(hours,steps,SatRogVog[i])
    Orbits["O"+i] = points

#Ground Track
olatlong = TwoDimPlot(hours,steps,Orbits,True)

ti = time()
#Max and min revisit time
revisitTime(olatlong,cameraAngle,Orbits,hours/steps,False)

#3D Graph
ThreeDimGraph(hours,steps,Orbits,Video,SatCount,orbPlaneCount,cameraAngle)

tf = time()

print("Elapsed time: %.3f [seg]" %(tf-ti))
