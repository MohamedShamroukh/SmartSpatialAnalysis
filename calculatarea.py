#
#
#
#((copyrights))>>>>>>>>>>>>>>>>>>>>>
# created by: Mohamed shamroukh Under the Supervision of Prof.Mohamed Alkhuzamy Aziz
print "created by: Mohamed shamroukh Under the Supervision of Prof.Mohamed Alkhuzamy Aziz"
#((python libraries))>>>>>>>>>>>>>>>>>>>
# importing analysis module
import time
start_time = time.time()
import arcpy
import os
#((workspace variables))>>>>>>>>>>>>>>>>>>>>
outpath3 = r"D:\mawork\local\area1"
dirpath = r"D:\mawork\local\outs2"
arcpy.env.workspace = dirpath
arcpy.env.overwriteOutput = True
#((calculate area Analysis Algorithm))>>>>>>>>>>>>>>>>>>>
# Use the ListFeatureClasses function to return a list of shapefiles.
featureclasses = arcpy.ListFeatureClasses()
# loop through the list of shape files and add field then calc the sum
for ifc in featureclasses:
 outtable = os.path.join(outpath3, ifc)
 arcpy.AddGeometryAttributes_management(ifc, "AREA", "METERS","SQUARE_KILOMETERS", "")
 arcpy.Statistics_analysis(ifc, outtable, statistics_fields="POLY_AREA SUM", case_field="")
 print ifc+' done'
 # 5
print "analysis has been completed"
# time elapsed
elapsed_time = time.time() - start_time
time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
print "elapsed time: ", elapsed_time



