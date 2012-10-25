#
# Script name: centroid_test.py
# Author: Kevin Dinkel
# Created: 10/2/2012
# Description: This script centroids some stars.
#

###################################################################################
# Must import this for every script in this directory in order to use our modules!!
###################################################################################
import script_setup

###################################################################################
# Import modules from analysis (the correct way to do it):
###################################################################################
from analysis import centroid as centroid
from util import imgutil as imgutil
from util import submethods as subm
#import matplotlib.pyplot as plt

###################################################################################
# Main
###################################################################################
image = imgutil.loadimg('/home/kevin/Desktop/img_1348368011_459492_00146_00000_1.dat')
 
image = subm.colmeansub(image)
centroids = centroid.centroid(image)

imgutil.dispimg(image,5)
imgutil.circstars(image,centroids,25)
