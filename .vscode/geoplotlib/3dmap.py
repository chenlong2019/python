from osgeo import gdal
import cv2
gdal.UseExceptions()

ds = gdal.Open('D:/testdata/oragdata/t1/2016-spectral_00.img')
bandg = ds.GetRasterBand(1)
elevationg = bandg.ReadAsArray()

bandr = ds.GetRasterBand(2)
elevationr = bandr.ReadAsArray()

bandb = ds.GetRasterBand(3)
elevationb = bandb.ReadAsArray()

import matplotlib.pyplot as plt
nrows, ncols = elevationr.shape

elevation= cv2.merge([elevationg,elevationr,elevationb])#
# I'm making the assumption that the image isn't rotated/skewed/etc. 
# This is not the correct method in general, but let's ignore that for now
# If dxdy or dydx aren't 0, then this will be incorrect
x0, dx, dxdy, y0, dydx, dy = ds.GetGeoTransform()

x1 = x0 + dx * ncols
y1 = y0 + dy * nrows

plt.imshow(elevation, cmap='gist_earth', extent=[x0, x1, y1, y0])
plt.show()

