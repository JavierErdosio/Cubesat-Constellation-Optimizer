# Results validation
## Reference

| Constellation | Sat. Count | Orb. plane count | Sat. separation | Periapsis altitude | Eccentricity |    Inclination    |    FOV    | Sensor type | Reference |
|:-------------:|:----------:|:----------------:|:---------------:|:------------------:|:------------:|:-----------------:|:---------:|:-----------:|:-----------:|
|    Landsat    |      2     |         1        |    180 [deg]    |      705 [km]      |       0      |     98.2 [deg]    |  15 [deg] |   Passive   |[eoportal](https://www.eoportal.org/satellite-missions/landsat-9) |
|    Oceansat   |      1     |         1        |        -        |      720 [km]      |       0      |     98.2 [deg]    |  90 [deg] |   Passive   |[eoportal](https://www.eoportal.org/satellite-missions/oceansat-3) |
|      TRMM     |      1     |         1        |        -        |      403 [km]      |       0      |      35 [deg]     |  95 [deg] |   Active    |[eoportal](https://www.eoportal.org/satellite-missions/trmm) & [NASA Presentation](https://gpm.nasa.gov/sites/default/files/meeting_files/2021_IPWG_Workshop/PMM.ACCP_.pdf)|
## Results
Taking into consideration Puerto Rico's territory (following ` territory.geojson `):

```
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            [
              -67.36054702427634,
              18.603248124257206
            ],
            [
              -67.36054702427634,
              17.77172773786721
            ],
            [
              -65.52783907545542,
              17.77172773786721
            ],
            [
              -65.52783907545542,
              18.603248124257206
            ],
            [
              -67.36054702427634,
              18.603248124257206
            ]
          ]
        ],
        "type": "Polygon"
      }
    }
  ]
}


```

After running the 3 simulations of each constellation, the following average results where obtained:

| Constellation | Expected mean revisit time | Simulated mean revisit time |  Error  |
|:-------------:|:--------------------------:|:---------------------------:|:-------:|
|    Landsat    |     8 days (192 hours)     |   7.77 days (186.58 hours)  | -3.00 % |
|    Oceansat   |      2 days (48 hours)     |   1.996 days (47.90 hours)  | -0.2 %  |
|      TRMM     |     $\approx$ 11.5 hours   |         11.23 hours         | -2.32 % |