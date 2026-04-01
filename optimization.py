import geopandas as gpd
import numpy as np
from shapely.geometry import Point


def revisitTime(olatlong):
    
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
    puntos_dentro = points[mask]
    coords = np.array([[p.x, p.y] for p in puntos_dentro])
    
    
    
    
    data=[]
    for i in olatlong:
        data.append(i)

    perCov = []
    for i in range(len(olatlong[data[0]][0])):
        satPoints=[]
        for j in olatlong:
            if i > len(olatlong[j][1])-1:
                satPoints.append(Point(olatlong[j][1][-1],olatlong[j][0][-1]))            
            else:
                satPoints.append(Point(olatlong[j][1][i],olatlong[j][0][i]))        
        
        sat = gpd.GeoSeries(satPoints,data,crs="EPSG:4326")
        sat = sat.to_crs(epsg=3857)
        satMask = sat.within(territory.union_all())
        satsDentro = sat[satMask]
        coordsSat = np.array([[p.x, p.y] for p in satsDentro])

        #print(f"Cantidad de puntos dentro de Argentina: {len(coords)}")
        #print(f"Cantidad de satelites dentro de Argentina: {len(coordsSat)}")

        if len(coordsSat) != 0:
            dx = coords[:, 0][:, None] - coordsSat[:, 0][None, :]
            dy = coords[:, 1][:, None] - coordsSat[:, 1][None, :]

            dist = dx**2 + dy**2
            rad = (39000/2)**2          #Modificar para swath real

            covered = dist <= rad

            coveredByAny = np.any(covered, axis=1)


            percentageCovered = sum(coveredByAny)/len(coords)*100
            perCov.append(percentageCovered)
        else:
            perCov.append(0)

        #print("Cobertura porcentual: %.3f" %percentageCovered)
    
    print(max(perCov))
    
        
