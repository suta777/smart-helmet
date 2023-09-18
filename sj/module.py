import cv2
import numpy as np
import os
from deepsort_module import deepsort_start
from ultralytics import YOLO
import func_road
import warning_person
import check_traffic_lights
import check_crosswalk
import check_overlap
import pygame
import time
import torch
from ffpyplayer.player import MediaPlayer
# 비동기
import asyncio