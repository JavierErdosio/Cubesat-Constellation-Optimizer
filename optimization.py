import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import matplotlib.pyplot as plt


def revisitTime(olatlong,cameraAngle,Orbits):

    cameraAngle = np.deg2rad(cameraAngle)
    
    #Import territory polygon
    territory = gpd.read_file("territory.geojson")

    #Project to web mercator
    territory = territory.to_crs(epsg=3857) #web mercator (meters)

    #Get rectangular shape of territory
    xmin,ymin, xmax, ymax =territory.total_bounds

    #Divide rectangular shape in dots
    res = 20000 #meters
    xCoords = np.arange(xmin, xmax, res)
    yCoords = np.arange(ymin, ymax, res)
    xx, yy = np.meshgrid(xCoords, yCoords)
    xx = xx.ravel()
    yy = yy.ravel()

    #Get coordinates of points in meters
    points = gpd.GeoSeries([Point(x, y) for x, y in zip(xx, yy)], crs=territory.crs)
    mask = points.within(territory.union_all())
    pointsWithin = points[mask]
    coords = np.array([[p.x, p.y] for p in pointsWithin])

    #Territory center
    cx = np.mean(coords[:,0])
    cy = np.mean(coords[:,1])
    
    data=[]
    for i in olatlong:
        data.append(i)

    olonglat = {} #Reshaped and prepared for future use
    for i in olatlong:
        longlat = []
        for j in range(len(olatlong[i][0])):
            if not np.isnan(olatlong[i][1][j]) and not np.isnan(olatlong[i][0][j]):
                longlat.append(np.array([olatlong[i][1][j],olatlong[i][0][j]]))
        olonglat[i]=np.array(longlat)   
    
    perCov = []
    cov = []
    for i in range(len(olonglat[data[0]])):
        satPoints=[]
        satAltitude = []
        for j in data:
            satPoints.append(Point(olonglat[j][i][0],olonglat[j][i][1]))
            satAltitude.append(Point(np.linalg.norm(Orbits[j][i]),0)) 
        
        alt = gpd.GeoSeries(satAltitude,data)
        sat = gpd.GeoSeries(satPoints,data,crs="EPSG:4326")
        sat = sat.to_crs(epsg=3857)
        
        

        coordsSat = np.array([[p.x, p.y] for p in sat])
        altSats = np.array([p.x for p in alt])

        if len(coordsSat) != 0:
            #Filter sats within range
            dx_sat = coordsSat[:,0] - cx
            dy_sat = coordsSat[:,1] - cy
            dist_sat = np.sqrt(dx_sat**2 + dy_sat**2)
            mask = dist_sat < 4000000   #4000km
            coordsSat = coordsSat[mask]
            altSats = altSats[mask]

            #Extracts x coordinate and makes subtraction
            dx = coords[:, 0][:, None] - coordsSat[:, 0][None, :] 
            dy = coords[:, 1][:, None] - coordsSat[:, 1][None, :]

            dist = dx**2 + dy**2
            swath = ((altSats-6378)*np.tan(cameraAngle)*1000/2)**2   

            covered = dist <= swath

            coveredByAny = np.any(covered, axis=1)

            cov.append(coveredByAny)

            percentageCovered = sum(coveredByAny)/len(coords)*100
            perCov.append(percentageCovered)
        else:
            perCov.append(0)
            cov.append(np.zeros(len(coords)))

    print("Maximum simultaneus coverage %.3f"%max(perCov))
    covArray = np.array(cov)
    pointsObserved = np.sum(np.any(covArray, axis=0))
    if pointsObserved < len(coords):
        print("[WARN] %i points observed and %i missed during the simulated time (%.2f %% coverage)" %(pointsObserved,len(coords)-pointsObserved,pointsObserved*100/len(coords)))
    
