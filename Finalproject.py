#Final project NR426
#Dustin Polasek
# Created February 5 2019
# Identify Which parcels are owned by individuals living else where

#import modules
import arcpy
import os
import sys
from arcpy import env
import arcpy.mp as map
arcpy.env.overwriteOutput = True

#Setup try and except statement
try:
    #Set environment
    arcpy.env.workspace =r"D:\2018-2019 CSU\NR 426\FinalProject\GIS211ProjectData.gdb"
    #Clip the parcels that fall in our area of interest
    clip_in = "BoulderCoParcelsforLongmont"
    clip_layer = "Longmont_Bnd_buf"
    clip_out = clip_in + "_clp"
    mydata = "BoulderCoParcelsforLongmont.shp"

    # If elif and else statement determining if the data exists and if it is in a polygon format if it is perform the clip.
    if not arcpy.Exists(clip_in):
        print("Input data doesn't exist, exiting script...")
        sys.exit()
    elif not arcpy.Exists(clip_layer):
        print("Input data doesn't exist, exiting script...")
        sys.exit()
    elif not arcpy.Describe(clip_layer).shapetype == "Polygon":
        print("Clip layer is not a polygon, can't use it for the clip, exiting script...")
        sys.exit()
    else:
        print("All the data exists and is the right geometry. Running clip.....")
        arcpy.Clip_analysis(clip_in, clip_layer, clip_out)
        print(clip_out)

    # Create new feature field Lived_In if it does not exist
    fldList = arcpy.ListFields(clip_out, "Lived_In")
    if len(fldList) == 0:
        arcpy.AddField_management(clip_out, "Lived_In", "TEXT")
        print("Successfully created the Lived In field")
    else:
        print("Lived In field already exists")

    print("Creating the cursor...............")

    # Create new feature layer
    flayer = arcpy.MakeFeatureLayer_management(clip_out, "Compiled_address")


    streetno = "STREETNO"
    streetname = "STREETNAME"
    streetsuf = "STREETSUF"
    # update created feature Layer Compiled_Address to include street #, name, and SUF and determine if it matches row 5
    with arcpy.da.UpdateCursor(flayer, [streetno, streetname, streetsuf]) as cur:
        for row in cur:
            # Compare row 5 to the compiled address if there the same add a yes to the lived in field
            if row[5] == "Compiled_Address":
                livedin = "y"
            else:
                livedin = "n"
                cur.updateRow(row)


except Exception as e:
    print("Error: " + e.args[0])

print("Script Completed Way to go!!!")

