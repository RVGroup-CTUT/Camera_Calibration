import numpy as np
import cv2 as cv
import glob
import json, os
def resized_img(img,percent):
    width = int(img.shape[1] * percent / 100)
    height = int(img.shape[0] * percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized
def projectPointsErr(objpoints,imgpoints, rvecs, tvecs, mtx, dist):
    mean_error = []
    proj_error=0
    total_points=0
    for i in range(len(objpoints)):
        reprojected_points, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        # reprojected_points=reprojected_points.reshape(-1,2)
        proj_error = np.sum(np.abs(imgpoints[i]-reprojected_points)**2)
        total_points = len(objpoints[i])
        
        #print("imgpointsL",imgpointsL)
        mean_error.append([i,round(np.sqrt(proj_error/total_points),2)])
    return mean_error
def mean(data): 
    return sum(data) / len(data) 
 
def stddev(data): 
    squared_data = [x*x for x in data] 
    return (mean(squared_data) - mean(data)**2)**.5 
######## Path direction #######################
image_dir = "IMG_VIEWS"
current_dir = os.getcwd()
image_savepath = os.path.join(current_dir, image_dir)



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
allimages = sorted(glob.glob(image_savepath + '/' + '*.jpg'))
for frame_img in allimages:
    imgL_g = cv2.imread(frame_img,0)
    imgL = imgL_g.copy()
    grayL =imgL
    # Find the chess board corners
    retL, cornersL = cv.findChessboardCorners(grayL, chessboardSize, cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FAST_CHECK | cv2.CALIB_CB_NORMALIZE_IMAGE)
