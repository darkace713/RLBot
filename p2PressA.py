import pyvjoy
import time

#Pythonic API, item-at-a-time

p2 = pyvjoy.VJoyDevice(2)

time.sleep(1.5)

p2.data.lButtons = 1 #press A
p2.update()

time.sleep(0.1)

p2.data.lButtons = 0 #Release all
p2.update()