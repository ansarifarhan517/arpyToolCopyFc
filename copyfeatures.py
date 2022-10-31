# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params0 = arcpy.Parameter(
            displayName="Input Features Class Of Data to be Ploted",
            name='in_features1',
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input",
        ) 
        params1 = arcpy.Parameter(
            displayName="Input Features Class Of points where data shoul be ploted ",
            name='in_features2',
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input",
        ) 
        params2 = arcpy.Parameter(
            displayName="Output Features Class 2",
            name='in_features3',
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Output"
        )
        return [params0,params1,params2]
        

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        try:
            arcpy.env.workspace = r'C:\Users\test\Documents\ArcGIS\Projects\TressSample\TressSample.gdb'
            arcpy.env.overwriteOutput = True
            arcpy.env.addOutputsToMap = True
            #Taking Input Multipatch Layers From Users
            inFeatures      = parameters[0].valueAsText
            points_fc       = parameters[1].valueAsText
            outFeatures     = parameters[2].valueAsText

            arcpy.AddMessage(inFeatures)
            arcpy.AddMessage(points_fc)

            sr = arcpy.Describe(points_fc).spatialReference # spatial reference
            arcpy.AddMessage(sr)
            data_geom = arcpy.da.SearchCursor(inFeatures, 'SHAPE@', spatial_reference=sr).next() # get first line
            arcpy.AddMessage(data_geom[0])


            datas = [] # temporary line container
            points_count = int(arcpy.GetCount_management(points_fc).getOutput(0)) # count points
            arcpy.AddMessage(datas)

            for i in range(points_count):
                datas.append(data_geom[0]) # create trees/data copies


            arcpy.CopyFeatures_management(datas, outFeatures) # write lines to feature class
    
            points = arcpy.da.SearchCursor(points_fc, 'SHAPE@XY', spatial_reference=sr) # load points to list for later
            with arcpy.da.UpdateCursor(outFeatures,['SHAPE@XY'],spatial_reference=sr) as cursor: # loop through line copies, collecting line centroid 
                for row in cursor:
                    cur_point = points.next() # get next point geometry
                    cursor.updateRow([(cur_point[0][0], cur_point[0][1])]) # move line feature centroid to new location
        except:
            arcpy.AddMessage('Error')


        

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
