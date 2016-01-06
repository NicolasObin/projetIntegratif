#!/usr/bin/env python  
from naoqi import ALProxy
motion = ALProxy("ALMotion", "10.42.0.48", 9559)

#motion.setStiffnesses("Body", 1.0)




motion.setStiffnesses("Body", 0.0)
