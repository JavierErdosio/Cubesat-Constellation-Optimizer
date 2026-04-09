import numpy as np
from stateVector import stateVector
from TwoBodySolver import SatPoints
from ThreeDimGraph import ThreeDimGraph as ThreeDimGraph
from TwoDimPlot import TwoDimPlot
from revisitTime import revisitTime
import optuna



def optimization(trial):
    #Variables
    SatCount = trial.suggest_int('SatCount', 5, 40)
    orbPlaneCount = trial.suggest_int('orbPlaneCount', 3, 10)
    e = trial.suggest_float('e', 0.0, 1.0, step=0.001) #[-] Eccentricity
    hp = trial.suggest_int('hp', 600, 1700,step=10) #[km] Perigee

    #Constants
    inc = np.deg2rad(-63.4394882) #[rad] Inclinación
    omega = np.deg2rad(270) #[rad] Argumento del perigeo
    Re = 6378
    Rmax = 1700 + Re
    if e > (Rmax - (hp + Re)) / (Rmax + (hp + Re)):
        raise optuna.TrialPruned() # Le dice a Optuna que aborte este intento

    #Time data
    hours = 23.93446944 #Sidereal day 
    steps = 30*60 #30 seconds and 60 frames per second

    #Satellite
    cameraAngle = 4.46 #[deg]

    #Orbit
    RAAN = np.linspace(0, 2*np.pi, orbPlaneCount+1)
    RAAN = RAAN[0:-1]

    theta = np.linspace(0, 2*np.pi, SatCount+1)
    theta = theta[0:-1]

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
    olatlong = TwoDimPlot(hours,steps,Orbits,False)

    #Max and min revisit time
    mrt,cov =  revisitTime(olatlong,cameraAngle,Orbits,hours/steps,True)

    if cov < 95:
        raise optuna.TrialPruned()
    
    return(mrt)


#Optuna Optimizer
opt = optuna.create_study(direction='minimize')
opt.optimize(optimization, n_trials=500)

#Results
print('Mejores parámetros:')
for key, value in opt.best_params.items():
    print(f'{key}: {value}')