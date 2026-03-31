import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import matplotlib.pyplot as plt


lat = -48.66
lon = -70


sat = gpd.GeoSeries([Point(lon,lat),Point(lon+2,lat+2)],["sat0","sat1"],crs="EPSG:4326")
sat = sat.to_crs(epsg=3857)

#Import territory polygon
territory = gpd.read_file("territory.geojson")

#Project to web mercator
territory = territory.to_crs(epsg=3857) #web mercator (meters)

#Get rectangular shape of terrytory
xmin,ymin, xmax, ymax =territory.total_bounds

#Divide rectangular shape in dots
res = 20000 #meters
x_coords = np.arange(xmin, xmax, res)
y_coords = np.arange(ymin, ymax, res)
xx, yy = np.meshgrid(x_coords, y_coords)
xx = xx.ravel()
yy = yy.ravel()

#Get coordinates of points in meters
points = gpd.GeoSeries([Point(x, y) for x, y in zip(xx, yy)], crs=territory.crs)
mask = points.within(territory.union_all())
satMask = sat.within(territory.union_all())
puntos_dentro = points[mask]
satsDentro = sat[satMask]




coords = np.array([[p.x, p.y] for p in puntos_dentro])
coordsSat = np.array([[p.x, p.y] for p in satsDentro])

print(f"Cantidad de puntos dentro de Argentina: {len(coords)}")
print(f"Cantidad de satelites dentro de Argentina: {len(coordsSat)}")

dx = coords[:, 0][:, None] - coordsSat[:, 0][None, :]
dy = coords[:, 1][:, None] - coordsSat[:, 1][None, :]

dist = dx**2 + dy**2
rad = (39000/2)**2          #Modificar para swath real

covered = dist <= rad

coveredByAny = np.any(covered, axis=1)


percentageCovered = sum(coveredByAny)/len(coords)*100

print("Cobertura porcentual: %.3f" %percentageCovered)
