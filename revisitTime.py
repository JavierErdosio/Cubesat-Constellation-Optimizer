import geopandas as gpd
import numpy as np
from shapely.geometry import Point
from sunVector import getSunVector


def revisitTime(olatlong,cameraAngle,Orbits,dt,optuna,Sun,terrritoryResolution,EPSG):

    cameraAngle = np.deg2rad(cameraAngle)
    
    #Import territory polygon
    territory = gpd.read_file("territory.geojson")

    # Territory limits in deg
    territory_deg = territory.to_crs(epsg=4326)
    min_lon, min_lat, max_lon, max_lat = territory_deg.total_bounds

    #Project from lat-long to EPSG code of choice
    territory = territory.to_crs(epsg=EPSG) #EPSG of choice (meters)

    #Get rectangular shape of territory
    xmin,ymin, xmax, ymax =territory.total_bounds

    #Divide rectangular shape in dots
    res = terrritoryResolution #meters
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
        valid_sats = []

        # Current time in seconds
        t_current = i * dt * 3600

        sun_vector = getSunVector(t_current)

        for j in data:
            if Sun:
                r_sat = Orbits[j][i]
                
                r_sat_norm = r_sat / np.linalg.norm(r_sat)
                
                # Scalar product to obtain cosine of the angle between the sun and the satellite
                dot_product = np.dot(sun_vector, r_sat_norm)
                
                # Day/Night filter
                min_sun_elevation = np.sin(np.deg2rad(10)) 
                
                if dot_product < min_sun_elevation:
                        continue # skip due to night

            satPoints.append(Point(olonglat[j][i][0],olonglat[j][i][1]))
            satAltitude.append(Point(np.linalg.norm(Orbits[j][i]),0))
            valid_sats.append(j) 
        
        alt = gpd.GeoSeries(satAltitude,valid_sats)
        sat = gpd.GeoSeries(satPoints,valid_sats,crs="EPSG:4326")
        
        # Filter sats by lat-long with a margin
        margin = 10 # margin deg (approx 1000 km)
        
        mask_deg = (sat.geometry.x > min_lon - margin) & \
                   (sat.geometry.x < max_lon + margin) & \
                   (sat.geometry.y > min_lat - margin) & \
                   (sat.geometry.y < max_lat + margin)
        
        sat = sat[mask_deg]
        alt = alt[mask_deg]

        if not sat.empty:
            sat = sat.to_crs(epsg=EPSG) 
            coordsSat = np.array([[p.x, p.y] for p in sat])
            altSats = np.array([p.x for p in alt])

            # Extract x coordinate and makes subtraction
            dx = coords[:, 0][:, None] - coordsSat[:, 0][None, :] 
            dy = coords[:, 1][:, None] - coordsSat[:, 1][None, :]

            dist = dx**2 + dy**2
            swath = ((altSats-6378)*np.tan(cameraAngle/2)*1000)**2   

            covered = dist <= swath

            coveredByAny = np.any(covered, axis=1)

            cov.append(coveredByAny)

            percentageCovered = sum(coveredByAny)/len(coords)*100
            perCov.append(percentageCovered)
        else:
            perCov.append(0)
            cov.append(np.zeros(len(coords)))
    
    
    if not optuna:
        print("Maximum simultaneus coverage %.3f"%max(perCov))
    covArray = np.array(cov)
    pointsObserved = np.sum(np.any(covArray, axis=0))
    if pointsObserved < len(coords):
        if not optuna:
            print("[WARN] %i points observed and %i missed during the simulated time (%.2f %% coverage)" %(pointsObserved,len(coords)-pointsObserved,pointsObserved*100/len(coords)))
    
    #Revisit gaps
    revisitGaps = [] 
    for idx in range(covArray.shape[1]):
        coveredSeries = covArray[:, idx]
        coverIndex = np.where(coveredSeries)[0]

        if len(coverIndex) > 1:
            gaps = np.diff(coverIndex) 
        
            validGaps = gaps[gaps > 0]
            validGapsHours = validGaps * dt
            validGapsHours = validGapsHours[validGapsHours > 0.033]
            
            if len(validGapsHours) > 0:
                revisitGaps.extend(validGapsHours)
    

    # Statistics
    if len(revisitGaps) > 0:
        revisitGaps = np.array(revisitGaps)

        
        
        maxRevisitTime = revisitGaps.max()
        medianRevisitTime = np.median(revisitGaps)
        meanRevisitTime = revisitGaps.mean()
        minRevisitTime = revisitGaps.min()

        Q1 = np.quantile(revisitGaps,0.25)
        Q3 = np.quantile(revisitGaps,0.75)
        IQR = Q3-Q1
        LB = Q1-0.5*IQR
        UB = Q3 +0.5*IQR

        if LB < 0:
            LB = 0
        
        if UB > maxRevisitTime:
            UB = Q3

        filteredRevisitGaps = revisitGaps[(revisitGaps > LB) & (revisitGaps < UB)]
        filteredMeanRevisitTime = filteredRevisitGaps.mean()

        if not optuna:
            print("Max revisit time (observed area): %.2f hours" %maxRevisitTime)
            print("Median revisit time (observed area): %.2f hours" %medianRevisitTime)
            print("Mean revisit time (observed area): %.2f hours" %meanRevisitTime)
            print("Filtered mean revisit time (observed area): %.2f hours" %filteredMeanRevisitTime)
            print("Min revisit time (observed area): %.2f hours" %minRevisitTime)
    else:
        if not optuna:
            print("No revisits detected")
        meanRevisitTime = 23.93
    
    return filteredMeanRevisitTime,pointsObserved*100/len(coords)