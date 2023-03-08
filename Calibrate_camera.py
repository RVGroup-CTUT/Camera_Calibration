import numpy as np
import cv2 
import glob
import json, os
from utils import resized_img, projectPointsErr, mean, stddev
import argparse
######## Path direction #######################
image_dir = "IMG"
current_dir = os.getcwd()
path = os.path.join(current_dir, image_dir)
json_file = "data.json"
j = {}
# GET PATH INPUT AND OUTPUT
parser = argparse.ArgumentParser("Code processing")
parser.add_argument("-i", "--input", help="path of image", type=str, default= path)
parser.add_argument("-o", "--output", help="direction of output", type=str, default= None)
args = parser.parse_args()
image_savepath = args.input
path_out = args.output
if not os.path.exists(path_out):
    os.mkdir(path_out)
################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################
# size of chessboard 
chessboardSize = (10,7)
size_of_chessboard_squares_mm = 8
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
        cv2.imshow('img left', resized_img(imgL,100))
        cv2.waitKey(1)
    else: 
        print("Cannot detection")
        print(frame_img)

cv2.destroyAllWindows()
# Determine the new values for different parameters
rms, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpointsL, grayL.shape[::-1],None,None)
print('RMS',rms)
proj_err = projectPointsErr(objpoints,imgpointsL, rvecs, tvecs, mtx, dist)
print("Mean reprojection error: ", proj_err)
h,w= grayL.shape[:2]
newcameramtx, roiL= cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
#-------------------------------------Way 1 ------------------
undis_img1 = cv2.undistort(test_img, mtx, dist, None, newcameramtx)
cv2.imshow('Both Images1', resized_img(np.hstack([test_img, undis_img1]),100))
cv2.imwrite("img1.png",undis_img1)
cv2.waitKey(0)
#---------------------- WAY 2----------------------
# Get the undistort matrix
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
#mapx,mapy = cv2.initUndistortRectifyMap(mtx, dist, ,None,newcameramtx, grayL.shape[::-1], cv2.CV_16SC2) 
# Get undistortion image
undis_img2= cv2.remap(test_img,mapx,mapy,cv2.INTER_LINEAR)
#undis_img = cv2.remap(test_img,mapx,mapy, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
cv2.imshow('Both Images', resized_img(np.hstack([test_img, undis_img2]),100))
cv2.imwrite("img2.png",undis_img2)
cv2.waitKey(0)

print("Saving parameters!")
cv_file = cv2.FileStorage(path_out + "/"+ 'parmeters.txt', cv2.FILE_STORAGE_WRITE)
cv_file.write('mapx', mapx)
cv_file.write('mapy', mapy)
cv_file.write('mtx', mtx)
cv_file.write('dist', dist)
cv_file.release()
#Write json file
# Extend the JSONEncoder class
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
j['mtx'] = mtx
j['dist'] = dist
if json_file is not None:
    json.dump(j, open(path_out + "/" + json_file, 'wt'), cls=NumpyEncoder)
print("STD reprojection error: ", mean(proj_err))