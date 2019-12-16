#!/bin/bash
echo Performing LULC classification

otbcli_PolygonClassStatistics -in ../data/2003/2003.tif -vec ../data/2003/2003.shp -field Code -out ../data/2003/2003-classes.xml

otbcli_SampleSelection -in ../data/2003/2003.tif -vec ../data/2003/2003.shp -instats ../data/2003/2003-classes.xml -field Code -strategy smallest -outrates ../data/2003/rates.csv -out ../data/2003/samples.sqlite

otbcli_SampleExtraction -in ../data/2003/2003.tif -vec ../data/2003/samples.sqlite -outfield prefix -outfield.prefix.name band_ -field code

otbcli_ComputeImagesStatistics -il ../data/2003/2003.tif -out ../data/2003/image_statistics.xml

otbcli_TrainVectorClassifier -io.vd ../data/2003/samples.sqlite -cfield code -io.out ../data/2003/model.rf -classifier rf -feat band_0 band_1 band_2 band_3

otbcli_ImageClassifier -in ../data/2003/2003.tif -model ../data/2003/model.rf -out ../data/2003/labeled_image.tif

otbcli_ComputeConfusionMatrix -in ../data/2003/labeled_image.tif -ref vector -ref.vector.in ../data/2003/2003.shp -ref.vector.field code -out ../data/2003/confusion_matrix.csv

otbcli_ColorMapping -in ../data/2003/labeled_image.tif -method custom -method.custom.lut ../data/2003/lut_mapping_file.txt -out ../data/2003/RGB_color_image.tif
