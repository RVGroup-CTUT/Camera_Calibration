import numpy as np
import cv2 
import glob
import json, os
from utilities import resized_img, projectPointsErr, mean, stddev
######## Path direction #######################
image_dir = "IMG"
current_dir = os.getcwd()
image_savepath = os.path.join(current_dir, image_dir)
json_file = "data.json"
j = {}
################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################
# size of chessboard 
chessboardSize = (10,7)
size_of_chessboard_squares_mm = 5
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)
objp = objp * size_of_chessboard_squares_mm
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpointsL = [] # 2d points in image plane.
imgpointsR = [] # 2d points in image plane.
# Load and sort all images
allimages = sorted(glob.glob(image_savepath + '/' + '*.png'))
for frame_img in allimages:
    imgL_g = cv2.imread(frame_img,0)
    imgL = imgL_g.copy()
    grayL =imgL
    test_img = imgL_g.copy()
    # Find the chess board corners
    retL, cornersL = cv2.findChessboardCorners(grayL, chessboardSize, cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FAST_CHECK | cv2.CALIB_CB_NORMALIZE_IMAGE)
    # If found, add object points, image points (after refining them)
    if retL == True:
        print(frame_img)
        objpoints.append(objp)
        cornersL = cv2.cornerSubPix(grayL, cornersL, (11,11), (-1,-1), criteria)
        imgpointsL.append(cornersL)
        # Draw and display the corners
        cv2.drawChessboardCorners(imgL, chessboardSize, cornersL, retL)
        cv2.imshow('img left', resized_img(imgL,15))
        cv2.waitKey(1)
    else: 
        print("Cannot detection")
        print(frame_img)

cv2.destroyAllWindows()
# Determine the new values for different parameters
rms, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpointsL, grayL.shape[::-1],None,None)
print('RMS',rms)
proj_err = projectPointsErr(objpoints,imgpointsL, rvecs, tvecs, mtx, dist)
print("Mean reprojection error: ", mean(proj_err))
print("STD reprojection error: ", stddev(proj_err))
h,w= grayL.shape[:2]
newcameramtx, roiL= cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
# Get the undistort matrix
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
#mapx,mapy = cv2.initUndistortRectifyMap(mtx, dist, ,None,newcameramtx, grayL.shape[::-1], cv2.CV_16SC2) 
#Write json file
j['mapx'] = mapx
j['mapy'] = mapy
if json_file is not None:
    json.dump(j, open(json_file, 'wt'))
 # Get undistortion image
undis_img= cv2.remap(test_img,mapx,mapy,cv2.INTER_LINEAR)
#undis_img = cv2.remap(test_img,mapx,mapy, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
cv2.imshow('Both Images', resized_img(np.hstack([test_img, undis_img]),30))
cv2.waitkey(0)
