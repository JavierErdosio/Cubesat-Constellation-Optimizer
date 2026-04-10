<h1 style="text-align: center;">Final Project - Engineering Degree</h1>

<h2 style="text-align: center;">Análisis y Optimización de Puntos de Lanzamiento para una Constelación Académica de CubeSats: Caso Nano 70/30</h2>

## Overview

This project focuses on the simulation and analysis of a CubeSat constellation designed to provide coverage over Argentina.

The simulated satellites are equipped with a **multispectral imaging payload**, enabling potential applications such as environmental monitoring, agriculture, and disaster management.


##  Current Status (as of April 10 2026) 


The project currently includes:

* Ground track generation
* 3D orbital visualization (video output)
* Automatic constellation optimization

These features allow for basic analysis of satellite coverage and orbital behavior.


### Ground Track Visualization

Generates the satellite ground track over Earth's surface:

![Ground Track](/assets/GroundTrack.png)



### 3D Orbit Visualization

Interactive 3D visualization built using `pyvista`, exported as a video:

![3D Orbit Visualization](assets/satelite.gif)

### Optuna optimization
Use of Optuna Library to minimize mean revisit time and creation of database with MySQL in order to display results with Optuna Dashboard 

![Optuna screenshot](assets/optuna.png)

## Roadmap / Future Work

Planned improvements include:


* Maneuver planning

  * Orbital adjustments and station-keeping

* Launch simulation

  * Modeling deployment scenarios

## Notes

This is an academic project and is actively under development.