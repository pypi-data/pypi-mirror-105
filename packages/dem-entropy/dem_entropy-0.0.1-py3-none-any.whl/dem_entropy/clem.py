#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 12:00:00 2021
@author: rgrimson
packaged using https://packaging.python.org/tutorials/packaging-projects/
https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/
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
                        help="show the output",
                        action="store_true")
    args = parser.parse_args()

    # define output filenames
    demfile = args.demfile
    path = os.path.dirname(demfile)
    fname = os.path.splitext(os.path.basename(demfile))[0]
    fext = os.path.splitext(os.path.basename(demfile))[1]

    if args.out:
        f_out = args.out
    else:
        prefix = f'entropy_{args.nbits:02d}b_{args.r:d}r_{int(100*args.delta):03d}cm_'
        if args.shift:
            prefix += 's_'
        f_out = os.path.join(path, prefix + fname + fext)

    f_png = os.path.join(os.path.dirname(f_out), os.path.splitext(os.path.basename(f_out))[0] + '.png')

    # read input
    src_raster = rasterio.open(demfile)
    dem = src_raster.read(1)

    # compute entropy map
    if args.nbits <= 8:
        dtype = np.uint8
    else:
        dtype = np.uint16
    dmax = 2**args.nbits
    shift_rep = 5

    print(f'Computing local entropy map for {dem.shape[0]:d}x{dem.shape[1]:d} image from {args.demfile:s}.')
    print(f'Local neighbors are defined using a ball of radius {args.r:d}.')
    print(f'The discretization is performed using {dmax:d} bins ({args.nbits:d} bits) of size {args.delta:.2f}.')

    if args.shift:
        print(f'Computing the average of {shift_rep:d} dem shifts to smooth discretization step artifacts.')

    intime = time.time()

    ndem = np.array((dem/args.delta) % dmax, dtype=dtype)
    ent = entropy(ndem, disk(args.r))

    if args.shift:
        for i in range(1, shift_rep):
            ndem = np.array((dem/args.delta + i/shift_rep) % dmax, dtype=dtype)
            ent += entropy(ndem, disk(args.r))
        ent /= shift_rep

    outtime = time.time()

    print(f'\nTask completed in {outtime-intime} seconds.')

    # save output geotiff
    profile = src_raster.profile

    profile.update(
        dtype=rasterio.float32,
        count=1,
        compress='lzw')

    with rasterio.open(f_out, 'w', **profile) as dst:
        dst.write(ent.astype(rasterio.float32), 1)
    print(f'Output saved as {f_out:s}')

    # export png is requested
    if args.png or args.show:
        p = 5
        plt.imshow(ent, vmin=np.nanpercentile(ent.flatten(), p), vmax=np.nanpercentile(ent.flatten(), 100-p))
        if args.png:
            plt.savefig(f_png)
            print(f'Output exported as {f_png:s}')
        if args.show:
            plt.show()


if __name__ == "__main__":
    # calling the main function
    main()
