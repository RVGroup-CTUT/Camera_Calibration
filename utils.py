import numpy as np
import cv2 
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
    return sum(data[0,:]) / len(data) 
 
def stddev(data): 
    squared_data = [x*x for x in data] 
    return (mean(squared_data) - mean(data)**2)**.5 
# The thinh