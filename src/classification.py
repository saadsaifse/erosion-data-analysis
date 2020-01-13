#! /usr/bin/env python3.5

import otbApplication as otb
import os

# Parameters
sampleSelectionStrategy = "smallest"

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
    paths["imageStatistics"] = os.path.join(baseDataPath, "{}-image-statistics.xml".format(year))
    return paths

paths = createFilePathsForYear(2003)

# Create Polygon Class Statistics
print("Creating class statitstics...")
pcs = otb.Registry.CreateApplication("PolygonClassStatistics")
pcs.SetParameterString("in", paths['tif'])
pcs.SetParameterString("vec", paths['shp'])
pcs.SetParameterString("field", 'code')
pcs.SetParameterString("out", paths['classes'])
pcs.ExecuteAndWriteOutput()
print("Class statitstics created")

# Select samples
print("Selecting samples...")
sampleSelection = otb.Registry.CreateApplication("SampleSelection")
sampleSelection.SetParameterString("in", paths['tif'])
sampleSelection.SetParameterString("vec", paths['shp'])
sampleSelection.SetParameterString("instats", paths['classes'])
sampleSelection.SetParameterString("field", 'code')
sampleSelection.SetParameterString("strategy", sampleSelectionStrategy)
sampleSelection.SetParameterString("outrates", paths['rates'])
sampleSelection.SetParameterString("out", paths['samples'])
sampleSelection.ExecuteAndWriteOutput()
print("Samples selected")

# Extract samples
print("Extracting samples...")
sampleExtraction = otb.Registry.CreateApplication("SampleExtraction")
sampleExtraction.SetParameterString("in", paths['tif'])
sampleExtraction.SetParameterString("vec", paths['samples'])
sampleExtraction.SetParameterString("outfield", 'prefix')
sampleExtraction.SetParameterString("outfield.prefix.name", 'band_')
sampleExtraction.SetParameterString("field", 'code')
sampleExtraction.ExecuteAndWriteOutput()
print("Samples extracted")

# Compute image statistics
print("Computing image statistics...")
imageStatistics = otb.Registry.CreateApplication("ComputeImagesStatistics")
imageStatistics.SetParameterStringList("il", [paths['tif']])
imageStatistics.SetParameterString("out", paths['imageStatistics'])
imageStatistics.ExecuteAndWriteOutput()
print("Image statistics computed")
