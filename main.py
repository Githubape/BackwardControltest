import time

from UAV import UAV

sn="4TADL2L0010027"
broker = '218.192.100.219'
port = 1883
topic = "thing/product/"+sn+"/services"
# generate client ID with pub prefix randomly
client_id = f'backward-contolor'


def camera_aim_test():

    # mqtt=Mqtt(broker,port,client_id)
    # mqtt.publish(topic,MQTT_MSG)
    uav = UAV("4TADL2L0010027", broker, port, client_id)
    x = 0.5
    y = 0.5
    while (True):
        x = float(input("x:"))
        y = float(input("y:"))
        uav.camera_aim(False, x, y)
    # uav.camera_aim(False,0,0)
    pass

def takeoff_to_point_test():
    uav = UAV("4TADL2L0010027", broker, port, client_id)
    longitude = 113.022687
    latitude = 23.147928
    uav.takeoff_to_point(latitude,longitude)

    # uav.camera_aim(False,0,0)
    pass

def flight_authority_grab_test():
    uav = UAV("4TADL2L0010027", broker, port, client_id)

    uav.flight_authority_grab()

    # uav.camera_aim(False,0,0)
    pass

def drc_mode_enter_test():
    uav = UAV("4TADL2L0010027", broker, port, client_id)

    uav.drc_mode_enter()

    # uav.camera_aim(False,0,0)
    pass

def  drone_control_test():
    longitude = 113.022687
    latitude = 23.147928
    uav = UAV("4TADL2L0010027", broker, port, client_id)
    #uav.takeoff_to_point(latitude,longitude)
    uav.flight_authority_grab()
    uav.drc_mode_enter()
    x=float(input("x"))

    while(True):
        time.sleep(0.15)
        uav.drone_control(0,0,0,90)

    # uav.camera_aim(False,0,0)
    pass

def run():

    # takeoff_to_point_test()
    # flight_authority_grab_test()
    drone_control_test()
    pass



if __name__ == '__main__':
    run()