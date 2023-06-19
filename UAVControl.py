import time
import math
import ffmpeg
import numpy as np
from UAV import UAV
import  cv2
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

def  drone_control_test(uav):
    longitude = 113.022687
    latitude = 23.147928

    #uav.takeoff_to_point(latitude,longitude)
    uav.flight_authority_grab()
    uav.drc_mode_enter()
    # x=float(input("x"))
    #
    # while(True):
    #     time.sleep(0.15)
    #     uav.drone_control(0,0,0,90)

    # uav.camera_aim(False,0,0)
    pass

def cout_angle(x0,y0,x,y):
    x1=math.fabs(x)
    lx=x1-x0
    ly=y-y0
    len=math.sqrt(lx*lx+ly*ly)
    angle=math.acos(ly/len)
    if(x<0):
        return 0-angle
    return angle

def initPoint(x,y,width,height):
    return int(x-width/2),int(height/2-y)

def track(x0, y0, width, height):
    k1 = x0 / width *2
    x = k1 * 17
    k2 = y0 / height*2
    y = 17 * k2
    sita = cout_angle(0,0,x0,y0)
    k3 = sita / math.pi
    w = k3 * 90
    if(w<=60 and w>0):
        w=w+30
    if(w>=-60 and w<0):
        w=w-30
    return -x, y, w

def OnMouseAction(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        x,y=initPoint(x,y,960,720)
        print(x, y)
        x,y,w=track(x,y,960,720)
        print(str(x)+" "+str(y)+" "+str(w))
        #uav.drone_control(y, x, 0,w)
        uav.drone_control(y, -x, 0,0)
def Stream(str,uav):
    cap = cv2.VideoCapture(str)
    # 调用cv2方法获取cap的视频帧（帧：每秒多少张图片）
    # fps = self.cap.get(cv2.CAP_PROP_FPS)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    # 获取cap视频流的每帧大小
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size = (width, height)
    print(size)
    ret, image = cap.read()
    cv2.namedWindow("test")
    cv2.setMouseCallback("test",OnMouseAction)
    while (image is None):
        ret, image = cap.read()
        print("Nome")
    num = 1
    while (cap.isOpened()):
        if (ret):
            # if ret == True:
            # outVideo.write(image)
            #print(num)
            num = num + 1
            cv2.imshow("test",image)
            cv2.waitKey(20)

            cap.grab()  # .read() = .grab() followed by .retrieve()

            success, im = cap.retrieve()
            if success:
                image = im
            else:
                print("failed")
def Stream2(source,uav):
    args = {"rtsp_transport": "tcp"}    # 添加参数 获
    probe = ffmpeg.probe(source)
    cap_info = next(x for x in probe['streams'] if x['codec_type'] == 'video')
    print("fps: {}".format(cap_info['r_frame_rate']))
    width = cap_info['width']           # 获取视频流的宽度
    height = cap_info['height']         #取视频流的高度
    up, down = str(cap_info['r_frame_rate']).split('/')
    fps = eval(up) / eval(down)
    print("fps: {}".format(fps))    # 读取可能会出错错误
    process1 = (
        ffmpeg
        .input(source)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .overwrite_output()
        .run_async(pipe_stdout=True)
    )
    cv2.namedWindow("test")
    cv2.setMouseCallback("test",OnMouseAction)

    num = 1
    while (True):
        in_bytes = process1.stdout.read(width * height * 3)  # 读取图片
        if not in_bytes:
            break
        # 转成ndarray
        in_frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([height, width, 3])
        )
        frame = cv2.resize(in_frame, (960, 720))  # 改变图片尺寸
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # 转成BGR
        cv2.imshow("test", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    process1.kill()

uav = UAV("4TADL2L0010027", broker, port, client_id)
def run():

    #takeoff_to_point_test()
    #flight_authority_grab_test()
    #drone_control_test()

    x = input("step1")
    drone_control_test(uav)
    x = input("step2")
    Stream2("rtmp://139.159.148.93/live/"+str(x),uav)
    pass



if __name__ == '__main__':

    run()