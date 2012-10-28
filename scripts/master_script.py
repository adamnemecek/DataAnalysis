#
# Script name: master_script.py
# Author: Kevin Dinkel
# Created: 10/2/2012
# Description: This script takes a list of filenames, finds & centroids stars in 
# the files, calculates an attitude quaternion with each file, and utimately produces
# plots of roll, pitch, and yaw of the DayStar system over time.
#

###################################################################################
# Must import this for every script in this directory in order to use our modules!!
###################################################################################
import script_setup

###################################################################################
# Import modules from analysis (the correct way to do it):
###################################################################################
from analysis import centroid as centroid
from analysis import editcentroidlist as starmatcher
from analysis import qmethod as qmethod
from util import imgutil as imgutil
from db import RawData as database
from itertools import izip, islice
import cPickle as pickle
import time

###################################################################################
# Main
###################################################################################
# Analysis Details:
# Daytime Burst: 15 (low gain)
# Nighttime Burst: 179

# Get desired filenames from database:
db = database.Connect()
fnames = db.select('select raw_fn from rawdata where burst_num = 145 limit 3').raw_fn.tolist()
#fnames = db.find('raw_fn','burst_num = 145 limit 5').raw_fn.tolist()
n = len(fnames)

tic = time.clock()
print 'Starting analysis.'
centroids = []
for count,fname in enumerate(fnames):
    # Display status:
    print 'Loading and centroiding filename ' + str(count+1) + ' of ' + str(n) + '.'
    
    # Load the image:
    image = imgutil.loadimg(fname,from_database=True)
    
    # Find stars in image:
    centers = centroid.findstars(image)
    
    # Get centroids:
    centroids.append(centroid.imgcentroid(image,centers))

# Pickle the found centroids for safekeeping :)
# To load later: centroids = pickle.load( open( "saved_centroids.p", "rb" ) )
pickle.dump( centroids, open( "saved_centroids_" + time.strftime("%Y-%m-%d_%H:%M:%S", time.gmtime()) + ".pk", "wb" ) )

# Match Stars: 
print 'Matching stars.'
matched_centroids = []
for count,(centlistA,centlistB) in enumerate(izip(centroids, islice(centroids, 1, None))):
    print 'Comparing centroid list: ' + str(count+1) + ' to ' + str(count+2) + '.'
    matched_centroids.append(starmatcher.matchstars(centlistA,centlistB))

# Find quaternions:
print 'Find quaternions.'
quats = []
for count,matched in enumerate(matched_centroids):
    # Project 2d vectors into 3d space:
    Vi2d,Vb2d = zip(*matched)
    Vi = starmatcher.project3D(Vi2d)
    Vb = starmatcher.project3D(Vb2d)
    # Run the Q-Method:
    quats.append(qmethod.qmethod(Vi,Vb))

print quats

toc = time.clock()
print 'Total time: ' + str(toc - tic) + ' s'