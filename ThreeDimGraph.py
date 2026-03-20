import pyvista as pv
from pyvista import examples
import numpy as np


R_earth = 6378

def ThreeDimGraph(hours,n_frames,Orbits,video,SatCount,CameraAngle):
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
    for i in range(SatCount):
        orbit = pv.Spline(Orbits["OSat%i"%i], 1000)
        plotter.add_mesh(orbit, color="red", line_width=3)

    # satelites
    sat = pv.Sphere(radius=400)
    sats = {}
    for i in range(SatCount):
        sats["satActor%i"%i] = plotter.add_mesh(sat, color="white",name="Sat%i"%i)
        sats["satActor%i"%i].SetPosition(Orbits["OSat%i"%i][0])


    if video == True:
        plotter.open_movie("satelite.mp4",framerate=n_frames/30,quality=10)
        plotter.show(window_size=[1920,1080],interactive_update=True,title="Orbit Visualizer")
    else:
        plotter.show(window_size=[1920,1080],interactive_update=True,title="Orbit Visualizer")

    for i in range(n_frames):
        
        for j in range(SatCount):
            sats["satActor%i"%j].SetPosition(Orbits["OSat%i"%j][i])
        earth_actor.RotateZ(360*(hours/23.93446944)/n_frames)
        plotter.add_text("Tiempo: %.3f"%(i/n_frames*hours), position='lower_left', font_size=20,color="white", name="mi_etiqueta")
        
        #Vision Cone
        for j in range(SatCount):
            cone = pv.Cone(center=Orbits["OSat%i"%j][i]/2,direction=Orbits["OSat%i"%j][i],height=np.linalg.norm(Orbits["OSat%i"%j][i]),angle=CameraAngle, resolution=100)
            cone_actor = plotter.add_mesh(cone,color="blue",opacity=0.5,name="cone%i"%j)
        
        if video == True:
            plotter.write_frame()
        else:
            plotter.update()

    plotter.close()