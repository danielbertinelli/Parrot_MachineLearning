from pyardrone import ARDrone
import  time
drone = ARDrone()
drone.emergency()
drone.navdata_ready.wait()
bateria = drone.state.vbat_low
print(bateria)
drone.trim()
drone.takeoff()
drone.hover()
time.sleep(8)
#
# t=time.time()
# while time.time()-t<=1:
#     drone.move(forward=0.1)
#
# time.sleep(8)
#
# while time.time()-t<=1:
#     drone.move(backward=0.1)
#
# time.sleep(8)
#
# drone.land()