#! /usr/bin/env python3.5

import otbApplication as otb
import os

# Parameters
sampleSelectionStrategy = "smallest"
classifier = "rf" # Random forest

def createFilePathsForYear(year):
    baseDataPath = "../data/25.01.20/{}".format(str(year))
    paths = {}
    paths["tif"] = os.path.join(baseDataPath, "{}.tif".format(year))
    paths["shp"] = os.path.join(baseDataPath, "{}.shp".format(year))
    paths["classes"] =  os.path.join(baseDataPath, "{}-classes.xml".format(year))
    paths["rates"] = os.path.join(baseDataPath, "{}-rates.csv".format(year))
    paths["samples"] = os.path.join(baseDataPath, "{}-samples.sqlite".format(year))
    paths["model"] = os.path.join(baseDataPath, "{}-model.rf".format(year))
    paths["labeledImage"] = os.path.join(baseDataPath, "{}-labeled-image.tif".format(year))
    paths["confusionMatrix"] = os.path.join(baseDataPath, "{}-confusion-matrix.csv".format(year))
    paths["lut"] = "../lut_mapping_file.txt" # use the same lookup table file
    paths["rgb"] = os.path.join(baseDataPath, "{}-RGB-color-image.tif".format(year))
    paths["imageStatistics"] = os.path.join(baseDataPath, "{}-image-statistics.xml".format(year))
    return paths

# for x in [1990, 1999, 2003, 2008, 2011, 2019]:
#     paths = createFilePathsForYear(x)

paths = createFilePathsForYear(2019)

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

# Train Vector Classifier
print("Training Vector Classifier...")
vectorClassifier = otb.Registry.CreateApplication("TrainVectorClassifier")
vectorClassifier.SetParameterStringList("io.vd", [paths['samples']])
vectorClassifier.SetParameterString("cfield", 'code')
vectorClassifier.SetParameterString("io.out", paths['model'])
vectorClassifier.SetParameterString("classifier", classifier)
vectorClassifier.SetParameterStringList("feat", ['band_0', 'band_1', 'band_2', 'band_3'])
vectorClassifier.ExecuteAndWriteOutput()
print("Vector Classifier trained")

# Classify Images
print("Classifying image...")
imageClassifier = otb.Registry.CreateApplication("ImageClassifier")
imageClassifier.SetParameterString("in", paths['tif'])
imageClassifier.SetParameterString("model", paths['model'])
imageClassifier.SetParameterString("out", paths['labeledImage'])
imageClassifier.ExecuteAndWriteOutput()
print("Image Classified")

# Compute Confusion matrix
print("Computing confusion matrix...")
cm = otb.Registry.CreateApplication("ComputeConfusionMatrix")
cm.SetParameterString("in", paths['labeledImage'])
cm.SetParameterString("ref", "vector")
cm.SetParameterString("ref.vector.in", paths['shp'])
cm.SetParameterString("ref.vector.field", "code")
cm.SetParameterString("out", paths['confusionMatrix'])
cm.ExecuteAndWriteOutput()
print("Confusion matrix computed")

# Color mapping
print("Perform color mapping")
colorMapping = otb.Registry.CreateApplication("ColorMapping")
colorMapping.SetParameterString("in", paths['labeledImage'])
colorMapping.SetParameterString("method", "custom")
colorMapping.SetParameterString("method.custom.lut", paths['lut'])
colorMapping.SetParameterString("out", paths['rgb'])
colorMapping.ExecuteAndWriteOutput()
print("Color mapping done")



