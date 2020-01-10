# Note that, if the input raster is multiband, the data blocks will also be
# multiband, having dimensions (bands, rows, columns).  Otherwise, they will
# have dimensions of (rows, columns).

import arcpy
import numpy
import os

# Input raster
filein = os.path.join(os.getcwd(),r"D:\\shapedata\\2016-spectral1.img")

# Output raster (after processing)
fileout = os.path.join(os.getcwd(),r"D:\\shapedata\\blockprocessingrdb22.img")

# Size of processing data block
#  where memorysize = datatypeinbytes * numbands * blocksize^2
blocksize = 512

# ----------------------------------------------------------------------------
# Create raster object from file
myRaster = arcpy.Raster(filein)

# Set environmental variables for output
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = filein
arcpy.env.cellSize = filein

# Loop over data blocks
filelist = []
blocknum = 0
for x in range(0, myRaster.width, blocksize):
    for y in range(0, myRaster.height, blocksize):

        # Lower left coordinate of block (in map units)
        mx = myRaster.extent.XMin + x * myRaster.meanCellWidth
        my = myRaster.extent.YMin + y * myRaster.meanCellHeight
        # Upper right coordinate of block (in cells)
        lx = min([x + blocksize, myRaster.width])
        ly = min([y + blocksize, myRaster.height])
        #   noting that (x, y) is the lower left coordinate (in cells)

        # Extract data block
        myData = arcpy.RasterToNumPyArray(myRaster, arcpy.Point(mx, my),
                                          lx-x, ly-y)
        myData=myData.astype('float64')
        # PROCESS DATA BLOCK -----------------------------
        # e.g., Calculate mean of each cell of all bands.
        myData -= numpy.mean(myData, axis=0, keepdims=True)
        # ------------------------------------------------

        # Convert data block back to raster
        myRasterBlock = arcpy.NumPyArrayToRaster(myData, arcpy.Point(mx, my),
                                                 myRaster.meanCellWidth,
                                                 myRaster.meanCellHeight)

        # Save on disk temporarily as 'filename_#.ext'
        filetemp = ('_%i.' % blocknum).join(fileout.rsplit('.',1))
        myRasterBlock.save(filetemp)

        # Maintain a list of saved temporary files
        filelist.append(filetemp)
        blocknum += 1

# Mosaic temporary files
arcpy.Mosaic_management(';'.join(filelist[1:]), filelist[0])
if arcpy.Exists(fileout):
    arcpy.Delete_management(fileout)
arcpy.Rename_management(filelist[0], fileout)

# Remove temporary files
for fileitem in filelist:
    if arcpy.Exists(fileitem):
        arcpy.Delete_management(fileitem)

# Release raster objects from memory
del myRasterBlock
del myRaster