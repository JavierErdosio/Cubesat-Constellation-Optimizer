# Results validation - CYGNSS constellation
## Reference

| Constellation | Sat. Count | Orb. plane count | Sat. separation | Periapsis altitude | Eccentricity | Inclination |    FOV    | Reference |
|:-------------:|:----------:|:----------------:|:---------------:|:------------------:|:------------:|:-----------:|:---------:|:-----------:|
|    Landsat    |      2     |         1        |    180 [deg]    |      705 [km]      |       0      |     98.2    |  15 [deg] | [eoportal](https://www.eoportal.org/satellite-missions/landsat-9) |
|    Oceansat   |      1     |         1        |        -        |      720 [km]      |       0      |     98.2    |  90 [deg] | [eoportal](https://www.eoportal.org/satellite-missions/oceansat-3) |
|     CYGNSS    |      8     |         1        |    0.8 [deg]    |      510 [km]      |       0      |      35     | 111 [deg] | [eoportal](https://www.eoportal.org/satellite-missions/cygnss) |
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

After running the simulation the following results where obtained:

| Constellation | Expected mean revisit time | Simulated mean revisit time |  Error  |
|:-------------:|:--------------------------:|:---------------------------:|:-------:|
|    Landsat    |     8 days (192 hours)     |   8.43 days (202.42 hours)  | 5.375 % |
|    Oceansat   |      2 days (48 hours)     |   1.996 days (47.92 hours)  |  -0.2 % |
|     CYGNSS    |           6 hours          |   Results yet not satisf.   |    -    |