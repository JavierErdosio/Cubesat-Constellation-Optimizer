import numpy as np
from stateVector import stateVector
from Keplerianos import Keplerianos
from TwoBodySolver import SatPoints
from ThreeDimGraph import ThreeDimGraph as ThreeDimGraph
from TwoDimPlot import TwoDimPlot

#Extras
Video = False
SatCount = 3
orbPlaneCount = 2


#Time data
#hours = 24
hours = 23.93446944 #Sidereal day 
steps = 30*60

#Satellite
CameraAngle = 4.46 #[deg]

#Orbit
e = 0.74 #[-] Excentricidad
hp = 600 #[km] Altura del perigeo
inc = np.deg2rad(-63.4394882) #[rad] Inclinación
omega = np.deg2rad(270) #[rad] Argumento del perigeo

RAAN = np.linspace(0, 2*np.pi, orbPlaneCount+1)
RAAN = RAAN[0:orbPlaneCount]

theta = np.linspace(0, 2*np.pi, SatCount+1)
theta = theta[0:SatCount]


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
TwoDimPlot(hours,steps,Orbits)

#3D Graph
ThreeDimGraph(hours,steps,Orbits,Video,SatCount,orbPlaneCount,CameraAngle)
