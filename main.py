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
SatCount = 1
orbPlaneCount = 1
sun = True #If you have a passive sensor set to True
terrritoryResolution = 5000 #[meters] distance between dots
EPSG = 3857 #EPSG code that better represent the region of study - 3857 is for Web Mercator


#Time data
simDays = 30
hours = 23.93446944*simDays #Sidereal day 
steps = 30*60*(2*simDays) #30 seconds and 60 frames per second

#Satellite
cameraAngle = 54 #[deg]
maxAltitude = 1700 #[km] based on antenna and camera maximum values 

#Orbit
e = 0 #[-] Eccentricity
hp = 720 #[km] Periapsis altitude
inc = np.deg2rad(98.2) #[rad] Inclination
omega = np.deg2rad(270) #[rad] Argument of periapsis

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
revisitTime(olatlong,cameraAngle,Orbits,hours/steps,False,sun,terrritoryResolution,EPSG)

#3D Graph
ThreeDimGraph(hours,steps,Orbits,Video,SatCount,orbPlaneCount,cameraAngle)

tf = time()

print("Elapsed time: %.3f [seg]" %(tf-ti))
