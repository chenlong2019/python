# Import system modules
import os
import sys
import arcpywwww
from arcpy import env

# Set workspace
env.workspace = "D:\\bysj\\file"

# Set local variables
out_folder_path = "D:\\bysj\\file"
out_name = "chen44444.gdb"

# Execute CreateFileGDB
arcpy.CreateFileGDB_management(out_folder_path, out_name)

