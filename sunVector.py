import numpy as np

def getSunVector(t_seconds):
    # Days since simulation start
    days = t_seconds / 86400.0
    
    # Vernal equinox (t=0)
    # The sun moves 360 deg in 365.25 days
    theta_sun = (days / 365.25) * 2 * np.pi 
    
    # Earth Inclination
    epsilon = np.deg2rad(23.44) 
    
    # Suns unit vector on ECI
    Sx = np.cos(theta_sun)
    Sy = np.sin(theta_sun) * np.cos(epsilon)
    Sz = np.sin(theta_sun) * np.sin(epsilon)
    
    return np.array([Sx, Sy, Sz])