import os
import cv2
import gdal
import ogr
import matplotlib.pyplot as plt
import numpy as np


''' 
Masks out the water by the biggest contour found in
the threshholded image
'''
def threshhold(img):
    blur = cv2.medianBlur(img, 3)
    water = cv2.inRange(blur, 2, 30)
    ret, thres = cv2.threshold(blur, 30, 255, 0)
    gray2 = img.copy()
    mask = np.zeros(thres.shape, np.uint8)

    contours, hierarchy = cv2.findContours(thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        # find largest contour in mask, use to compute minEnCircle 
        c = max(contours, key = cv2.contourArea)
        (x,y), radius = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        cv2.drawContours(mask,[c],0,255,-1)

    cv2.bitwise_not(gray2, gray2, mask)

    # TODO is the image with the masked out water needed?
    return mask


'''
Takes a TIFF- image and saves a threshholded georeferenced
TIFF, and a vectorized version. 
Returns just the area of the land?
'''
def vectorize(img, path, outputFolder, number):
    area = 0

    ''' at first a GeoTIFF '''
    tifdriver = gdal.GetDriverByName('GTiff')
    tif_layername = outputFolder + '/tif' + str(number)

    destinationFile = 'testTest_NIR.tif'

    if os.path.exists(tif_layername + ".tif"):
        # tifdriver.DeleteDataSource(tif_layername+".tif")
        print('should have deleted tif ' + str(number))

    inpuDatasetNIR = gdal.Open(path)
    rasterSizesNIR = inpuDatasetNIR.RasterXSize
    NIRArray = inpuDatasetNIR.GetRasterBand(1).ReadAsArray(0, 0, inpuDatasetNIR.RasterXSize, inpuDatasetNIR.RasterYSize)

    outputDataset = tifdriver.Create(
        tif_layername + ".tif",
        inpuDatasetNIR.RasterXSize, inpuDatasetNIR.RasterYSize,
        1,
        gdal.GDT_Byte)
    outputDataset.SetGeoTransform(inpuDatasetNIR.GetGeoTransform())
    outputDataset.SetProjection(inpuDatasetNIR.GetProjection())

    # Finally get the thresholded image
    land = threshhold(img)
    # And save it to the tif
    outputDataset.GetRasterBand(1).WriteArray(land)

    ''' shapefile here''' 
    shpdriver = ogr.GetDriverByName("ESRI Shapefile")
    dst_layername = outputFolder + '/polygonized' + str(number)
    
    if os.path.exists(dst_layername + ".shp"):
        shpdriver.DeleteDataSource(dst_layername+".shp")
        print('deleted shapefile ' + str(number))
    dst_ds = shpdriver.CreateDataSource( dst_layername + ".shp" )
    dst_layer = dst_ds.CreateLayer(dst_layername, srs = None )

    # and then also vectorize it
    gdal.Polygonize( outputDataset.GetRasterBand(1), outputDataset.GetRasterBand(1), dst_layer, -1, [], callback=None )

    for feature in dst_layer:
        # should be only one ?
        geom = feature.GetGeometryRef()
        area = geom.GetArea()

    dst_ds.Destroy()
    src_ds=None
    print("done vectorizing number... " + str(number))
    return area


if __name__ == '__main__':
    # TODO adjust the paths
    inputFolder = r"F:\Dokumente\Uni_Msc\2019_2020_WS\RSProject\studyArea3\nir_inputs"
    outputFolder = r"F:\Dokumente\Uni_Msc\2019_2020_WS\RSProject\studyArea3\nir_outputs"
    folderItems = os.listdir(inputFolder)
    tiffs = [fi for fi in folderItems if fi.endswith(".tif")]
    areas = np.zeros((len(tiffs), 1))
    differences = np.zeros((len(tiffs), 1))
    years = np.zeros((len(tiffs), 1))
    i = 0

    # Go through all the tiffs in the folder
    if (len(tiffs) > 1):
        while i < len(tiffs):
            names = os.path.splitext(tiffs[i])
            years[i] = int(names[0])
            # Read reference image
            imFilename = inputFolder + "/" + tiffs[i]
            print("Reading image : ", imFilename)
            image = cv2.imread(imFilename, cv2.IMREAD_UNCHANGED)
            print(image.dtype)
            # are any in 16bit?
            if (image.dtype == "uint16"):
                image = cv2.normalize(
                    image,  image, 0, 255, cv2.NORM_MINMAX).astype('uint8')

            area = vectorize(image, imFilename, outputFolder, i)
            # Storing difference value
            areas[i] = area/1000

            i += 1
    print(areas)

    fig, (ax1, ax2) = plt.subplots(1, 2)

    i = 0
    differences[0] = 0
    # Iterating to calculate differences
    while i < len(areas)-1 : 
        differences[i+1] = areas[i] - areas[i+1]
        i += 1

    print(differences)

    # Plot the data
    ax1.plot(years, areas, label='linear')
    ax2.plot(years, differences, label='linear')
    plt.show()