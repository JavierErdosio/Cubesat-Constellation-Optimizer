import pyvista as pv
from pyvista import examples
import numpy as np


R_earth = 6378

def ThreeDimGraph(hours,n_frames,Orbits,video,SatCount,orbPlaneCount,CameraAngle):
    plotter = pv.Plotter()
    
    # Crear esfera Tierra
    earth = pv.Sphere(radius=R_earth, theta_resolution=120, phi_resolution=120)

    # generar coordenadas UV
    earth = earth.texture_map_to_sphere(inplace=True, prevent_seam=True)
    xyz = earth.points
    x, y, z = xyz[:, 0], xyz[:, 1], xyz[:, 2]

    # Calculamos longitud (u) y latitud (v) en el rango [0, 1]
    u = 0.5 + np.arctan2(y, x) / (2 * np.pi)
    v = 0.5 + np.arcsin(z / R_earth) / np.pi

    # Aplicamos las coordenadas al mesh
    earth.active_texture_coordinates = np.column_stack((u, v))

    texture = pv.read_texture("earth_texture.jpg")
    earth_actor = plotter.add_mesh(earth, texture=texture)
    # luz solar
    plotter.add_light(pv.Light(position=(1e5,0,0), focal_point=(0,0,0), intensity=1.5))

    #Estrellas
    cubemap = examples.download_cubemap_space_16k()
    _ = plotter.add_actor(cubemap.to_skybox())
    plotter.set_environment_texture(cubemap, is_srgb=True,resample=1 / 64)


    # orbit
    for i in range(orbPlaneCount):
        orbit = pv.lines_from_points(Orbits["OSat%i0"%(i)])
        plotter.add_mesh(orbit, color="red", line_width=1)

    # satelites
    sat = pv.Sphere(radius=100)
    sats = {}
    for i in range(orbPlaneCount):
        for j in range(SatCount):
            sats["satActor%i%i"%(i,j)]= plotter.add_mesh(sat, color="white",name="Sat%i%i"%(i,j))
            sats["satActor%i%i"%(i,j)].SetPosition(Orbits["OSat%i%i"%(i,j)][0])


    if video == True:
        plotter.open_movie("satelite.mp4",framerate=n_frames/30,quality=10)
        plotter.show(window_size=[1920,1080],interactive_update=True,title="Orbit Visualizer")
    else:
        plotter.show(window_size=[1920,1080],interactive_update=True,title="Orbit Visualizer")

    for i in range(n_frames):        
        for j in range(orbPlaneCount):
            for k in range(SatCount):
                sats["satActor%i%i"%(j,k)].SetPosition(Orbits["OSat%i%i"%(j,k)][i])
        earth_actor.RotateZ(360*(hours/23.93446944)/n_frames)
        plotter.add_text("Tiempo: %.3f"%(i/n_frames*hours), position='lower_left', font_size=20,color="white", name="mi_etiqueta")
        
        #Vision Cone
        for j in range(orbPlaneCount):
            for k in range(SatCount):
                direc = Orbits["OSat%i%i"%(j,k)][i]/np.linalg.norm(Orbits["OSat%i%i"%(j,k)][i])
                vecEarthRad = R_earth*direc
                cent = (Orbits["OSat%i%i"%(j,k)][i]-vecEarthRad)/2 + vecEarthRad
                heightC = np.linalg.norm(Orbits["OSat%i%i"%(j,k)][i]-vecEarthRad)
                

                cone = pv.Cone(center=cent,direction=Orbits["OSat%i%i"%(j,k)][i],height=heightC,angle=CameraAngle, resolution=30)
                cone_actor = plotter.add_mesh(cone,color="blue",opacity=0.5,name="cone%i%i"%(j,k))
        
        if video == True:
            plotter.write_frame()
        else:
            plotter.update()

    plotter.close()