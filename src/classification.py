#! /usr/bin/env python3.5

import otbApplication as otb
import os

def createFilePathsForYear(year):
    baseDataPath = "../data/{}".format(str(year))
    paths = {}
    paths["tif"] = os.path.join(baseDataPath, "{}.tif".format(year))
    paths["shp"] = os.path.join(baseDataPath, "{}.shp".format(year))
    paths["classes"] =  os.path.join(baseDataPath, "{}-classes.xml".format(year))
    paths["rates"] = os.path.join(baseDataPath, "{}-rates.csv".format(year))
    paths["samples"] = os.path.join(baseDataPath, "{}-samples.sqlite".format(year))
    paths["model"] = os.path.join(baseDataPath, "{}-model.rf".format(year))
    paths["labeledImage"] = os.path.join(baseDataPath, "{}-labeled-image.tif".format(year))
    paths["confusionMatrix"] = os.path.join(baseDataPath, "{}-confusion-matrix.csv".format(year))
    paths["lut"] = os.path.join(baseDataPath, "{}-lut-mapping-file.txt".format(year))
    paths["rgb"] = os.path.join(baseDataPath, "{}-RGB-color-image.tif".format(year))
    return paths

paths = createFilePathsForYear(2003)

# create Polygon Class Statistics Application
pcs = otb.Registry.CreateApplication("PolygonClassStatistics")
pcs.SetParameterString("in", paths['tif'])
pcs.SetParameterString("vec", paths['shp'])
pcs.SetParameterString("field", 'code')
pcs.SetParameterString("out", paths['classes'])

pcs.ExecuteAndWriteOutput()

print("Class statitstics created")