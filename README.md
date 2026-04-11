<h1 style="text-align: center;">Final Project - Engineering Degree</h1>

<h2 style="text-align: center;">Análisis y Optimización de Puntos de Lanzamiento para una Constelación Académica de CubeSats: Caso Nano 70/30</h2>

## Overview

This project focuses on the simulation and analysis of a CubeSat constellation designed to provide coverage over Argentina.

The simulated satellites are equipped with a **multispectral imaging payload**, enabling potential applications such as environmental monitoring, agriculture, and disaster management.

## Table of content
1) [Current Status](#current-status-as-of-april-10-2026)
2) [Roadmap / Future Work](#roadmap--future-work)
3) [How to use](#how-to-use)
4) [Notes](#notes)


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

  * Parking to final orbit

* Launch simulation

  * Modeling of launchs
  * Use of optuna to generate database for launch selection

## How to use
1) Install dependencies:

  ```
  pip install numpy scipy shapely pyvista geopandas optuna cryptography pymysql
  ```

2) Generate `territory.geojson`.
3) Modify `optimization.py` with your constellation parameters and your database user and password.
4) Run `optimization.py` to minimize mean revisit time or modify and run `main.py` to view ground track and a 3D animation of your constellation.

### MySQL and Optuna dashboard

If you don't have a MySQL server nor an Optuna dashboard server, both can be created using docker. Modify for your application:
```
sudo docker run --name optuna-mysql -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=optuna_db -p 3306:3306 -d mysql:latest
```

After having a MySQL server running run `optimization.py` with your user and password to generate the optuna database. If this step isn't done, the following command will give a database version error.

```
sudo docker run -it --name optuna-dashboard -d --rm -p 8080:8080 ghcr.io/optuna/optuna-dashboard mysql+pymysql://root:password@localhost:3306/optuna_db
```

Optuna dashboard will be available at [http://localhost:8080](http://localhost:8080).

## Notes

This is an academic project and is actively under development.