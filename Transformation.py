import velodyne_decoder as vd
import pandas as pd
import numpy as np
import csv
import os
import datetime

from csv import reader
from gps import *


def rotm2eulZYX(Rotm: np.ndarray) -> list:
    # Extract individual rotation elements from the rotation matrix
    sy = np.sqrt(Rotm[0, 0] ** 2 + Rotm[1, 0] ** 2)

    if sy < 1e-6:
        # Singular case: sy is close to zero
        roll = np.arctan2(-Rotm[1, 2], Rotm[1, 1])
        pitch = np.arctan2(-Rotm[2, 0], sy)
        yaw = 0
    else:
        roll = np.arctan2(Rotm[2, 1], Rotm[2, 2])
        pitch = np.arctan2(-Rotm[2, 0], sy)
        yaw = np.arctan2(Rotm[1, 0], Rotm[0, 0])

    # Convert angles to degrees
    euler_angles = np.array(
        [np.rad2deg(yaw), np.rad2deg(pitch), np.rad2deg(roll)])
    return euler_angles


def eulXYZ2rotmENU(eulAngIn: list) -> np.ndarray:
    # Euler angles around the XYZ (pitch, roll, heading) axes
    pitch = np.deg2rad(eulAngIn[0])  # Pitch angle (X-RIGHT)
    roll = np.deg2rad(eulAngIn[1])  # Roll angle (Y-FWD)
    heading = np.deg2rad(eulAngIn[2])  # Heading angle (Z-Up)

    # Rotation matrix of X-Right axis
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(pitch), np.sin(pitch)],
                   [0, -np.sin(pitch), np.cos(pitch)]])

    # Rotation matrix of Y-Fwd axis
    Ry = np.array([[np.cos(roll), 0, -np.sin(roll)],
                   [0, 1, 0],
                   [np.sin(roll), 0, np.cos(roll)]])

    # Rotation matrix of Z-Up axis
    Rz = np.array([[np.cos(heading), np.sin(heading), 0],
                   [-np.sin(heading), np.cos(heading), 0],
                   [0, 0, 1]])

    # Compute the composite rotation matrix
    rot_matrix = np.dot(Rx, np.dot(Ry, Rz))
    return rot_matrix


def getNavENU(navSolIn: pd.DataFrame) -> list:
    pitch = navSolIn.loc[:, 7]
    roll = navSolIn.loc[:, 8]
    heading = navSolIn.loc[:, 9]
    eulerAng = [pitch, roll, heading]
    transVector = navSolIn.loc[:, 2:4]

    return pitch, roll, heading, eulerAng, transVector


def HDL64Unix2GPS(pcap_file, unix_start, unix_end):
    config = vd.Config(model='HDL-64E', rpm=300,
                       min_range=3.5, max_range=85, gps_time=True)
    time_range=(unix_start, unix_end)
    # Initialize a list to save
    cloud_arrays = []
    timestamp = []
    for stamp, points in vd.read_pcap(pcap_file, config=config, time_range=time_range):
        cloud_arrays.append(points)
        timestamp.append(stamp)
    # Convert to numpy format
    timestamp_TPE = np.array(timestamp)
    # Convert the local timezone (GMT+ 8 hour) to Greenwich Mean Time (GMT)
    timestamp_GMT = timestamp_TPE - 28800
    # Initialize a list to save the convertion data
    # Make sure the timestamp is GMT and set the leapsecond as 18
    GPS_lidar = []
    for i in timestamp_GMT:
        GPS_lidar.append(utc_to_weekseconds(i, 18))
    # Convert to numpy format
    GPS_lidar = np.array(GPS_lidar)
    # select the GPS second column only
    GPS_second_lidar = GPS_lidar[:, 4]

    return GPS_second_lidar, cloud_arrays


def VLP16Unix2GPS(pcap_file, unix_start, unix_end):
    config = vd.Config(model='VLP-16', rpm=600,
                       min_range=3.5, max_range=85, gps_time=True)
    time_range=(unix_start, unix_end)
    # Initialize a list to save
    cloud_arrays = []
    timestamp = []
    for stamp, points in vd.read_pcap(pcap_file, config=config, time_range=time_range):
        cloud_arrays.append(points)
        timestamp.append(stamp)
    # Convert to numpy format
    timestamp_TPE = np.array(timestamp)
    # Convert the local timezone (GMT+ 8 hour) to Greenwich Mean Time (GMT)
    timestamp_GMT = timestamp_TPE - 28800
    # Initialize a list to save the convertion data
    # Make sure the timestamp is GMT and set the leapsecond as 18
    GPS_lidar = []
    for i in timestamp_GMT:
        GPS_lidar.append(utc_to_weekseconds(i, 18))
    # Convert to numpy format
    GPS_lidar = np.array(GPS_lidar)
    # select the GPS second column only
    GPS_second_lidar = GPS_lidar[:, 4]

    return GPS_second_lidar, cloud_arrays







# resolve the issue of 1D array -> 2D array (suck NUMPY!!!!!!!!)
""
# test = np.array( [lidar_pos[:, 2], ]).T
# print(np.shape(test))
# type(test)
""
