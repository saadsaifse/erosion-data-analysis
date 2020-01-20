# Erosion Data Analysis

## Download Data

Download that data from [here](https://drive.google.com/drive/folders/1S0LurFVSTzLy_mXiFXXyjemajqTX9Aof?usp=sharing) and copy it inside the `./data` folder. Then you can specify the path for the specific data folder inside `./src/classification.py` file.

## Satellite Image Classification
We are using Orfeo library to classify satellite imagery. We have used their Python API in order to make it reproducible and also to make it coherent with our other python based modules.

### Classification usage on Mac
Install Mac distribution of Orfeo library. As of now it only works with Python 3.5, so make sure that you have that installed as well.

After the installation, you have to change paths in `otbenv.profile` file in the root of this repository. 

- Change `OTB_APPLICATION_PATH` to your Orfeo's applications installation path
- Change `PATH` to your Orfeo's installation bin path
- Change `PYTHONPATH` to the python 3.5 path on your machine

Once paths are specified, you have to source this script before running the classification script. Use `source otbenv.profile` command to source all environment variables into your existing terminal.

Execute `classificaiton.py` from the `src` directory using `python3.5 classification.py`.