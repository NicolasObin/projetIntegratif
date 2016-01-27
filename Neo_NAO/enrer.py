#!/usr/bin/env python
# -*- encoding: UTF-8 -*- 

import Audio_recording
import loca
import direction
import carto
import time

import matplotlib.pyplot as plt 
from Tkinter import * 
import numpy as np

from PIL import Image



robotIP= 'nao.local'
PORT = 9559
Audio_recording.record(robotIP)
