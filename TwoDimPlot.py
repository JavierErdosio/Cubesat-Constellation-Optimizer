import pyvista as pv
import numpy as np

plotter = pv.Plotter()
chart = pv.Chart2D()

chart.background_texture = pv.read_texture("earth_texture.jpg")
chart.x_range = [-180,180]
chart.y_range = [-90,90]

def TwoDimPlot(hours,steps):
    thetaECEF=[]
    for i in steps:
        if i/hours*2*np.pi < np.pi:
            thetaECEF.append(np.rad2deg(i/hours*2*np.pi))
        else:
            thetaECEF.append(np.rad2deg(np.pi-i/hours*2*np.pi))
    return thetaECEF

x = TwoDimPlot(23.93446944,np.linspace(0,23.93446944,1000))
y = np.zeros_like(x)

chart.line(x,y,width=2)

# SATELITE
sat = chart.line([x[0],x[1]],[y[0],y[1]],width=3,color="white")

plotter.add_chart(chart)



for i in range(len(x)):
    sat.update(x[i],y[i])
    plotter.render()

plotter.show(window_size=[1920,960],title="2D Plot")