import os
import sys
import arcpy
from arcpy import env

from xml.dom import minidom
from compiler.ast import Node
from platform import node
from ast import NodeVisitor

#Set workspace
sourceDir = os.path.abspath(os.path.dirname(sys.argv[0]))  # source dir
env.workspace = sourceDir


def createShapefile(path, filename):
    #Set local variables
    outPath = path + "/output"
    fileName = filename
    geometryType = "POINT"
    # Creating a spatial reference object
    spatialReference = arcpy.SpatialReference(path+"/projected/WGS1984.prj")

    # Execute CreateFeatureclass
    arcpy.CreateFeatureclass_management(
        outPath, fileName, geometryType, "#", "DISABLED", "DISABLED", spatialReference)
    print "Create Shapefile success!"

    return


def addFieldToShapefile(filename, fieldname, fieldtype):
    # Execute AddField for new fields
    arcpy.AddField_management(
        sourceDir+"\\output\\"+filename, fieldname, fieldtype)
    print fieldname

    return


def readXML(xmlfilename, shpfilename):
    xmlDoc = minidom.parse(sourceDir+"\\input\\"+xmlfilename)
    items = xmlDoc.getElementsByTagName("wfs:member")
    #=print rootNode.toxml()
    # Create insert cursor for table
    #
    rows = arcpy.InsertCursor(sourceDir+"\\output\\"+shpfilename)
    print rows, type(rows)
    fc = sourceDir+"\\output\\"+shpfilename
    cursor = arcpy.da.InsertCursor(fc, ["SHAPE@XY"])
    for item in items:
        row = rows.newRow()
        print row
        scenicName = item.getElementsByTagName("gml:name")[0]
        row.NAME = scenicName.firstChild.data
        # print "scenicname:" + scenicName.firstChild.data
        scenicLngLon = item.getElementsByTagName("gml:pos")[0]
        LNGLAT = scenicLngLon.firstChild.data
        # print LNGLAT
        strscenicLngLon = str(LNGLAT)
        # print strscenicLngLon
        strLngLon = strscenicLngLon.split(' ')
        # print strLngLon[0]
        row.LNG = float(strLngLon[0])
        # print "lng:" +scenicLng.firstChild.data
        row.LAT = float(strLngLon[1])
        # print "lat:" + scenicLat.firstChild.data
        scenicFrom = item.getElementsByTagName("pku:type")[0]
        row.FROM_ = scenicFrom.firstChild.data
        # print "from:" +scenicFrom.firstChild.data
        rows.insertRow(row)
        xy = (float(strLngLon[0]), float(strLngLon[1]))
        # print xy
        cursor.insertRow([xy])
        # print cursor
    return


createShapefile(sourceDir, "features.shp")

addFieldToShapefile("features.shp", "NAME", "TEXT")
addFieldToShapefile("features.shp", "LNG", "DOUBLE")
addFieldToShapefile("features.shp", "LAT", "DOUBLE")
addFieldToShapefile("features.shp", "FROM", "TEXT")

readXML("features.xml", "features.shp")
