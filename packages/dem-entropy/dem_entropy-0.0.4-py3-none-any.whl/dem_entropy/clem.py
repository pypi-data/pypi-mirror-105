#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 12:00:00 2021
@author: rgrimson
packaged using https://packaging.python.org/tutorials/packaging-projects/
https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/
testear con flake el estilo
"""
# import lybraries and funcions
import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import rasterio
import time
from skimage.morphology import disk
from skimage.filters.rank import entropy

ver = '0.0.3'

def main():
    # parse commmand line parameters
    parser = argparse.ArgumentParser(description="Computes entorpy map from a DEM given as GeoTIFF.\nSee https://gitlab.com/rgrimson/dem_entropy for more details.\nRafael Grimson May 2021.")
    parser.add_argument("demfile",
                        help="DEM file to use as input for entropy computation")
    parser.add_argument("-out",
                        type=str,
                        help="output filename")
    parser.add_argument("-delta",
                        type=float,
                        help="discretization height",
                        default=0.5)
    parser.add_argument("-r",
                        type=int,
                        help="radius of local windows for entropy computation (default is 2)",
                        default=2)
    parser.add_argument("-nbits",
                        type=int,
                        help="use nbits for discretization instead of 8bits",
                        default=8)
    parser.add_argument("-shift",
                        help="average over shifted the dem to avoid atifacts",
                        action="store_true")
    parser.add_argument("-png",
                        help="save as png the output",
                        action="store_true")
    parser.add_argument("-show",
                        help="show the output entropy map in a new window",
                        action="store_true")
    parser.add_argument('--version',
    					action='version',
                    	version='%(prog)s '+ver)
    args = parser.parse_args()
    compute_local_entropy_map(args.demfile,
                              out=args.out,
                              nbits=args.nbits,
                              r=args.r,
                              delta=args.delta,
                              shift=args.shift,
                              png=args.png,
                              show=args.show,
                              save=True,
                              verbose=True)

def compute_local_entropy_map(demfile, out=None, nbits=8, r=2, delta=0.5, 
                              shift=False, png=False, show=False, save=False, 
                              verbose=False):
    # define output filenames
    path = os.path.dirname(demfile)
    fname = os.path.splitext(os.path.basename(demfile))[0]
    fext = os.path.splitext(os.path.basename(demfile))[1]

    if out:
        f_out = out
    else:
        prefix = f'entropy_{nbits:02d}b_{r:d}r_{int(100*delta):03d}cm_'
        if shift:
            prefix += 's_'
        f_out = os.path.join(path, prefix + fname + fext)

    f_png = os.path.join(os.path.dirname(f_out), 
                         os.path.splitext(os.path.basename(f_out))[0] + '.png')

    # read input
    src_raster = rasterio.open(demfile)
    dem = src_raster.read(1)

    # compute entropy map
    if nbits <= 8:
        dtype = np.uint8
    else:
        dtype = np.uint16
    dmax = 2**nbits
    shift_rep = 5

    if verbose:
        print(f'Computing local entropy map for {dem.shape[0]:d}x{dem.shape[1]:d} image from {demfile:s}.')
        print(f'Local neighbors are defined using a ball of radius {r:d}.')
        print(f'The discretization is performed using {dmax:d} bins ({nbits:d} bits) of size {delta:.2f}.')
        intime = time.time()
        if shift:
            print(f'Computing the average of {shift_rep:d} dem shifts to smooth discretization step artifacts.')
        

    ndem = np.array((dem/delta) % dmax, dtype=dtype)
    ent = entropy(ndem, disk(r))

    if shift:
        for i in range(1, shift_rep):
            ndem = np.array((dem/delta + i/shift_rep) % dmax, dtype=dtype)
            ent += entropy(ndem, disk(r))
        ent /= shift_rep

    if verbose:
        outtime = time.time()
        print(f'\nTask completed in {outtime-intime} seconds.')

    # save output geotiff
    if save:
        profile = src_raster.profile
    
        profile.update(
            dtype=rasterio.float32,
            count=1,
            compress='lzw')
    
        with rasterio.open(f_out, 'w', **profile) as dst:
            dst.write(ent.astype(rasterio.float32), 1)
        if verbose:        
            print(f'Output saved as {f_out:s}')

    # creat image for simple view if requested (to save png or simply show)
    if png or show:
        p = 5
        plt.imshow(ent, vmin=np.nanpercentile(ent.flatten(), p), 
                        vmax=np.nanpercentile(ent.flatten(), 100-p))
        if png:
            plt.savefig(f_png)
            print(f'Output exported as {f_png:s}')
        if show:
            plt.show()
    return ent


if __name__ == "__main__":
    # calling the main function
    main()

# -------------------------
# *check style:
#     flake8 ./dem_entropy/clem.py
# -------------------------
# *local instalation:
#     sudo pip3 install -e .
# -------------------------
# *prepare distribution:
#     ?sudo python3 setup.py install
#     python3 setup.py sdist bdist_wheel
#     twine upload dist/*
# -------------------------
# *install using pip:
#     pip install dem_entropy

