import numpy as np
import pyvista as pv
from stateVector import stateVector
from TwoBodySolver import SatPoints
from ThreeDimGraph import ThreeDimGraph as ThreeDimGraph
from TwoDimPlot import TwoDimPlot
from revisitTime import revisitTime
import optuna

dataBaseUser = ""
dataBasePassword = ""
dataBaseURL = "localhost"
dataBasePort = "3306"
studyName = "constellationOptimization"
trials = 500


def optimization(trial):
    #Variables
    SatCount = trial.suggest_int('SatCount', 5, 40)
    orbPlaneCount = trial.suggest_int('orbPlaneCount', 3, 10)
    e = trial.suggest_float('e', 0.0, 0.5, step=0.001) #[-] Eccentricity
    hp = trial.suggest_int('hp', 600, 1700,step=10) #[km] Perigee

    #Constants
    inc = np.deg2rad(-63.4394882) #[rad] Inclination
    omega = np.deg2rad(270) #[rad] Argumento del perigeo
    Re = 6378
    Rmax = 1700 + Re
    if e > (Rmax - (hp + Re)) / (Rmax + (hp + Re)):
        raise optuna.TrialPruned() #Optuna abort

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
    
    pv.close_all()

    return(mrt)


#Optuna Optimizer
opt = optuna.create_study(direction='minimize',storage="mysql+pymysql://%s:%s@%s:%s/optuna_db"%(dataBaseUser,dataBasePassword,dataBaseURL,dataBasePort),study_name=studyName,load_if_exists=True)
opt.optimize(optimization, n_trials=trials,gc_after_trial=True)

#Results
print('Best parameters:')
for key, value in opt.best_params.items():
    print(f'{key}: {value}')