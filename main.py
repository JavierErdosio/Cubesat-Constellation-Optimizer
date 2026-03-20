import numpy as np
from stateVector import stateVector
from Keplerianos import Keplerianos
from TwoBodySolver import SatPoints
from ThreeDimGraph import ThreeDimGraph as ThreeDimGraph
from TwoDimPlot import TwoDimPlot

#Extras
Video = False
SatCount = 3


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
#Ohm = np.deg2rad(0) #[rad] Longitud del nodo ascendente
omega = np.deg2rad(270) #[rad] Argumento del perige
theta = 0

if SatCount==1:
    Ohm = 0
    theta = 0
else:
    Ohm = np.linspace(0, 2*np.pi, SatCount+1)
    Ohm = Ohm[0:SatCount]
    theta = np.linspace(0, 2*np.pi, SatCount+1)
    theta = theta[0:SatCount]

#Initial state vector
SatRogVog = {}
if SatCount==1:
    SatRogVog["Sat0"] = stateVector(e,hp,inc,Ohm,omega,theta)
else:
    for i in range(len(Ohm)):
        SatRogVog["Sat%i"%i] = stateVector(e,hp,inc,Ohm[i],omega,theta[i])



#Orbit points
Orbits = {}
for i in SatRogVog: 
    points = SatPoints(hours,steps,SatRogVog[i])
    Orbits["O"+i] = points

#Ground Track
TwoDimPlot(hours,steps,Orbits)

#3D Graph
ThreeDimGraph(hours,steps,Orbits,Video,SatCount,CameraAngle)
