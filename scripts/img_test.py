# File: IMG_TEST.PY
# Author: Nick Truesdale 
# Date: Oct 29, 2012
#
# Description:

# Initial Imports
import sys, os

# Get the directory above the directory this file is in
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

# More imports
import numpy as np
import copy as cp

# Addtl imports for main script
from util import imgutil as imgutil
from analysis import submethods as sm
from analysis import centroid as centroid


# Load the image:
image = imgutil.loadimg('/home/sticky/Daystar/img_1348368011_459492_00146_00000_1.dat')
image2 = imgutil.loadimg('/home/sticky/Daystar/img_1348355543_717188_00015_00000_0.dat', load_full=True)

#img = sm.colmeansub(image)
img2 = sm.colmeansub(image2)
img3 = sm.darkcolsub(image2)


img3 = np.delete(img3, np.r_[1080:1080+32], 0)

#imgutil.dispimg(image2,2)
imgutil.dispimg(img2,2)

imgutil.dispimg(img3,2)



