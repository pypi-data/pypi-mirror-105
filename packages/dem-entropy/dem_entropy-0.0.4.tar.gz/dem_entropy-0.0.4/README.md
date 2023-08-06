# DEM Entropy Package

Computes entorpy map from a DEM given as GeoTIFF. Rafael Grimson May 2021.
See https://gitlab.com/rgrimson/dem_entropy for las version and details.

usage: clem [-h] [-out OUT] [-delta DELTA] [-r R] [-nbits NBITS] [-shift]
            [-png] [-show] [--version]
            demfile

positional arguments:
  demfile       DEM file to use as input for entropy computation

optional arguments:
  -h, --help    show this help message and exit
  -out OUT      output filename
  -delta DELTA  discretization height
  -r R          radius of local windows for entropy computation (default is 2)
  -nbits NBITS  use nbits for discretization instead of 8bits
  -shift        average over shifted the dem to avoid atifacts
  -png          save as png the output
  -show         show the output entropy map in a new window
  --version     show program's version number and exit