# ((copyrights))
# created by: Mohamed Shamroukh Under the guidance and supervision of Prof.Mohamed Alkhuzamy Aziz
# ((python libraries and modules-importing analysis module))
import os
import arcpy
# ((workspace variables))
CITYNAME = arcpy.GetParameterAsText(0)
string = arcpy.GetParameterAsText(1)
SERVICECODE = string.upper()
INPUTPOINTSERVICE = arcpy.GetParameterAsText(2)
INPUTBORDER = arcpy.GetParameterAsText(3)
INPUTURBAN = arcpy.GetParameterAsText(4)
AREA = arcpy.GetParameterAsText(5)
# workspace
WorkSpace = arcpy.GetParameterAsText(6)
arcpy.env.workspace = WorkSpace
arcpy.env.scratchWorkspace = WorkSpace
arcpy.env.overwriteOutput = True
input_GRAPHtemp = arcpy.GetParameterAsText(7)
arcpy.AddMessage("analysis is going to start applying geo-processing on: >>>>>.....{}>>>>>".format(SERVICECODE))

# ((planning criteria- egyptian planning criteria))
# 1 educational services
if SERVICECODE == "KG": distance = 500  # kindergarten
elif SERVICECODE == "SC1": distance = 750  # Elementary school
elif SERVICECODE == "SC2":  distance = 2000  # Preparatory school
elif SERVICECODE == "SC3": distance = 5000  # high school
# 2 health care services
elif SERVICECODE == "AMBC":  distance = 3500  # ambulance station #3500-7000
elif SERVICECODE == "HC":  distance = 3000  # health center
elif SERVICECODE == "HS2": distance = 20000  # central hospital
elif SERVICECODE == "HS3": distance = 50000  # primary hospital
# educational / specialized hospital   # not defined so it could be more than that
# 3 religious services
elif SERVICECODE == "MSQ": distance = 1000  # mosque
elif SERVICECODE == "CHR": distance = 1000  # church    # notice the population
 # 4 fire stations and post office  services (other)
elif SERVICECODE == "FIR": distance = 1600  # fire stations           # sa criteria
elif SERVICECODE == "PST1": distance = 5000  # post office 1
elif SERVICECODE == "PST2":distance = 2000  # post office  2
else:
    arcpy.AddMessage("please make sure that you named your input as its illustrated in the tool help ")
# ((Analysis Algorithm))
# 1
Output_buffer = os.path.join(WorkSpace, CITYNAME + SERVICECODE + '_SRVcov')
arcpy.Buffer_analysis(INPUTPOINTSERVICE, Output_buffer, float(distance), "FULL", "ROUND", "ALL", "", "PLANAR")
arcpy.AddMessage("coverage analysis has been completed")
# 2
Output_clip = os.path.join(WorkSpace, CITYNAME + SERVICECODE + '_citySRV')
arcpy.Clip_analysis(Output_buffer, INPUTBORDER, Output_clip, "")
arcpy.AddMessage("bordering clipping has been completed")
# 3
Output_served = os.path.join(WorkSpace, CITYNAME + SERVICECODE + '_SRVbuiltup')
arcpy.Intersect_analysis([Output_clip, INPUTURBAN], Output_served, "ALL", "", "INPUT")
arcpy.AddMessage("served built up Area from service coverage overlapping analysis has been completed")
# 4
Output_unserved = os.path.join(WorkSpace, CITYNAME + SERVICECODE + '_unSRVbuiltup')
arcpy.SymDiff_analysis(INPUTURBAN, Output_served, Output_unserved, "ALL", "")
arcpy.AddMessage("unserved built up Area from service coverage overlapping analysis has been completed")
# 5
arcpy.AverageNearestNeighbor_stats(INPUTPOINTSERVICE, "EUCLIDEAN_DISTANCE", "GENERATE_REPORT", float(AREA))
arcpy.AddMessage("average nearest neighbor generated according to the input area")
arcpy.AddMessage("CREATING COVERAGE GRAPH ")
# 6 CREATING COVERAGE GRAPH
# adding area field to the served built up area
arcpy.AddGeometryAttributes_management(Output_served, "AREA", "METERS", "SQUARE_KILOMETERS", "")
arcpy.AddField_management(Output_served, "COV_area", "DOUBLE", 9, "", "", "COV_area", "NULLABLE")
arcpy.CalculateField_management(Output_served, "COV_area", "!POLY_AREA!", "PYTHON_9.3")
arcpy.AddMessage("adding area field to the covered built up area ")
# adding area field to the unserved built up area
arcpy.AddGeometryAttributes_management(Output_unserved, "AREA", "METERS", "SQUARE_KILOMETERS", "")
arcpy.AddField_management(Output_unserved, "UNCOV_area", "DOUBLE", 9, "", "", "UNCOV_area", "NULLABLE")
arcpy.CalculateField_management(Output_unserved, "UNCOV_area", "!POLY_AREA!", "PYTHON_9.3")
arcpy.AddMessage("adding area field to the uncovered built up area ")
out_graph_name = SERVICECODE + "_Graph"
out_graph_bmp = SERVICECODE + "Graph.bmp"
graph = arcpy.Graph()
input_data_served = Output_served
input_data_unserved = Output_unserved
# Create the graph
graph = arcpy.Graph()
# Add a vertical bar series to the graph
graph.addSeriesBarVertical(input_data_served, "COV_area")
graph.addSeriesBarVertical(input_data_unserved, "UNCOV_area")
# Specify the title of the Graph
graph.graphPropsGeneral.title = SERVICECODE + ' ' + "service coverage"
# Output a graph, which is created in-memory
arcpy.MakeGraph_management(input_GRAPHtemp, graph, out_graph_name)
# Save the graph as an image
arcpy.SaveGraph_management(out_graph_name, out_graph_bmp, "MAINTAIN_ASPECT_RATIO", 600, 375)
arcpy.AddMessage("Graph for services coverage created ")
arcpy.AddMessage("analysis has been completed")
arcpy.AddMessage('created by: Mohamed Shamroukh Under the guidance and supervision of Prof.Mohamed Alkhuzamy Aziz')
