import pyvista as pv
import numpy as np
import copy
from numpy import cos,sin

plotter = pv.Plotter(title="Ground Track")
chart = pv.Chart2D()

chart.background_texture = pv.read_texture("earth_texture.jpg")
chart.x_range = [-180,180]
chart.y_range = [-90,90]

#Curtis equation 4.55
def R3(theta):
    R = np.array(
        [[  cos(theta) , sin(theta) , 0],
         [ -sin(theta) , cos(theta) , 0],
         [    0        ,      0     , 1]]
    ) 

    return R

#Curtis Algorithm 4.1
def latlong(rvec):
    #Longitude = Right Ascention
    #Latitude = Declination

    r = np.linalg.norm(rvec)

    l = rvec[0]/r
    m = rvec[1]/r
    n = rvec[2]/r

    lat = np.rad2deg(np.asin(n))

    long = np.rad2deg(np.arctan2(m, l))

    return lat,long

def TwoDimPlot(hours,steps,Orbits):
    thetaECEF=[]
    steps = np.linspace(0,hours,steps)

    for i in steps:
        thetaECEF.append((i/hours*2*np.pi))
        
    
    OrbitsECEF = {}
    for i in Orbits:
        OrbitsECEF[i] = copy.deepcopy(Orbits[i])
        for j in range(len(Orbits[i])):
            OrbitsECEF[i][j] = np.matmul(R3(thetaECEF[j]),Orbits[i][j])

    olatlong = {}
    for i in OrbitsECEF:
        olatlong[i] = [[],[]]
        for j in OrbitsECEF[i]:
            lat,long = latlong(j)
            if len(olatlong[i][1]) > 0 and abs(long - olatlong[i][1][-1]) > 180:
                olatlong[i][0].append(np.nan) 
                olatlong[i][1].append(np.nan)
            olatlong[i][0].append(lat) 
            olatlong[i][1].append(long)

    colors = ["red", "blue", "green"]
    j = 0
    for i in olatlong:
        chart.line(olatlong[i][1],olatlong[i][0],width=2,label=i,color = colors[j])
        j = j + 1
        if j > 2: j=0



    plotter.add_chart(chart)

    plotter.show(window_size=[1920,960],title="Ground Track")
    return olatlong

