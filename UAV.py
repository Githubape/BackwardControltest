from datetime import datetime
import json
from Mqtt import Mqtt
import  requests



def gettimestap():
    dt=datetime.now()
    ts=datetime.timestamp(dt)
    return ts

topic_head="thing/product/"
topic_service="/services"

camera_aim_msg = {
    'bid': 'uavcontrol',
    'tid':'cameraaim',
    'timestamp': 0,
    'method': 'camera_aim',
    "data":{
        "payload_index": "67-0-1",
        "camera_type": "zoom",
        "locked": False,
        "x": 0.5,
        "y": 0.5
}
}
#飞行控制权抢夺 service
flight_authority_grab_msg={
    'bid': 'uavcontrol',
    'tid':'flightauthoritygrab',
    'timestamp': 0,
	"method": "flight_authority_grab",
	"data": {}
}

#进入指令飞行控制模式 services
drc_mode_enter_msg={
    'bid': 'uavcontrol',
    'tid':'drcmodeenter',
    'timestamp': 0,
	"method": "drc_mode_enter",
	"data": {
		"mqtt_broker": {
			"address": "ws://139.159.148.93:8083/mqtt",
			"client_id": "sn_a",
			"username": "admin",
			"password": "admin",
			"expire_time": 1672744922,
			"enable_tls": True
		},
		"osd_frequency": 10,
		"hsi_frequency": 1
	}
}

topic_down="/drc/down"
#飞行控制 down
drone_control_msg={
	"method": "drone_control",
	"data": {
		"seq": 526,
		"x": 2.34,
		"y": -2.45,
		"h": 2.76,
		"w": 2.86
	}
}
#一键起飞
takeoff_to_point_msg={
    'bid': 'uavcontrol',
    'tid':'takeofftopoint',
	"timestamp": 0,
	"method": "takeoff_to_point",
	"data": {
		"target_latitude": 113.022687,
		"target_longitude": 23.147928,
		"target_height": 100,
		"security_takeoff_height": 100,
		"flight_id": "ABDEAC21DCADDA",
		"rth_altitude": 100,
		"max_speed": 12,
        "rc_lost_action": 2,
        "exit_wayline_when_rc_lost": 0
	}
}


# 将字典转换为 JSON 字符串
#json_str = json.dumps(data)


class UAV:
    def __init__(self,sn,broker,port,client_id):
        self.sn=sn
        self.broker=broker
        self.port=port
        self.client_id=client_id
        self.defaut_payload="39-0-7"
        self.mqtt=Mqtt(self.broker,self.port,self.client_id)
        self.msgcount=0
        self.drccount=0

    def camera_aim(self,locked,x,y):
        camera_aim=camera_aim_msg
        camera_aim['timestamp']=gettimestap()
        camera_aim['data']['locked']=locked
        camera_aim['data']['x']=x
        camera_aim['data']['y']=y
        self.msgcount=self.msgcount+1
        camera_aim['tid']= camera_aim['tid']+str(self.msgcount)
        json_str=json.dumps(camera_aim)
        self.mqtt.publish(topic_head+self.sn+topic_service,json_str)

    def flight_authority_grab(self):
        flight_authority_grab=flight_authority_grab_msg
        flight_authority_grab["timestamp"]=gettimestap()
        self.msgcount=self.msgcount+1
        flight_authority_grab['tid']= flight_authority_grab['tid']+str(self.msgcount)
        json_str = json.dumps( flight_authority_grab)
        self.mqtt.publish(topic_head + self.sn + topic_service, json_str)
        pass

    def drc_mode_enter(self):
        #获取动态用户名密码
        def getauthen():
            headers = {'Content-Type': 'application/json',
                       'x-auth-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3b3Jrc3BhY2VfaWQiOiJlM2RlYTBmNS0zN2YyLTRkNzktYWU1OC00OTBhZjMyMjgwNjkiLCJzdWIiOiJDbG91ZEFwaVNhbXBsZSIsInVzZXJfdHlwZSI6IjEiLCJuYmYiOjE2ODU3NzMxNjAsImxvZyI6IkxvZ2dlcltjb20uZGppLnNhbXBsZS5jb21tb24ubW9kZWwuQ3VzdG9tQ2xhaW1dIiwiaXNzIjoiREpJIiwiaWQiOiJhMTU1OWU3Yy04ZGQ4LTQ3ODAtYjk1Mi0xMDBjYzQ3OTdkYTIiLCJleHAiOjE3NzIxNzMxNjAsImlhdCI6MTY4NTc3MzE2MCwidXNlcm5hbWUiOiJhZG1pblBDIn0.yue-t-XS8scPL5TBKbPgGjNctmUuMiwoFrdLFJLK-dA'}

            datas = json.dumps({"clientId": "81", "expireSec": "797"})
            r = requests.post(
                "http://218.192.100.219:8018/control/api/v1/workspaces/e3dea0f5-37f2-4d79-ae58-490af3228069/drc/connect",
                data=datas, headers=headers)
            if(r.text==""):
                print("connection failed")
                return "failed"

            rdic=json.loads(r.text)

            if(rdic["message"]!="success"):
                print("get authen failed")
                return "failed"

            return rdic

        drc_mode_enter=drc_mode_enter_msg
        drc_mode_enter["timestamp"]=gettimestap()
        self.msgcount=self.msgcount+1
        drc_mode_enter['tid']= drc_mode_enter['tid']+str(self.msgcount)

        authen=getauthen()
        if(authen=="failed"):
            print("get authen failed")
            return -1

        drc_mode_enter["data"]["mqtt_broker"]["address"]=authen["data"]["address"]
        drc_mode_enter["data"]["mqtt_broker"]["username"]=authen["data"]["username"]
        drc_mode_enter["data"]["mqtt_broker"]["password"]=authen["data"]["password"]
        drc_mode_enter["data"]["mqtt_broker"]["client_id"]=authen["data"]["client_id"]
        drc_mode_enter["data"]["mqtt_broker"]["expire_time"]=authen["data"]["expire_time"]
        drc_mode_enter["data"]["mqtt_broker"]["enable_tls"]=authen["data"]["enable_tls"]

        json_str = json.dumps( drc_mode_enter)
        self.mqtt.publish(topic_head + self.sn + topic_service, json_str)

    def drone_control(self,x,y,h,w):
        drone_control=drone_control_msg
        self.drccount = self.drccount + 1
        drone_control["data"]['seq'] = gettimestap()*1000
        drone_control["data"]["x"]=x
        drone_control["data"]["y"] = y
        drone_control["data"]["h"] = h
        drone_control["data"]["w"] = w

        json_str = json.dumps( drone_control)
        self.mqtt.publish(topic_head + self.sn + topic_down, json_str)

    def takeoff_to_point(self,latitude,longitude):
        takeoff_to_point=takeoff_to_point_msg
        takeoff_to_point["timestamp"]=gettimestap()
        self.msgcount=self.msgcount+1
        takeoff_to_point['tid']= takeoff_to_point['tid']+str(self.msgcount)

        takeoff_to_point["data"]["target_latitude"]=latitude
        takeoff_to_point["data"]["target_longitude"]=longitude
        json_str = json.dumps( takeoff_to_point)
        self.mqtt.publish(topic_head + self.sn + topic_service, json_str)


#headers = {'Content-Type': 'application/json'}


# headers = {'Content-Type': 'application/json',
#            'x-auth-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3b3Jrc3BhY2VfaWQiOiJlM2RlYTBmNS0zN2YyLTRkNzktYWU1OC00OTBhZjMyMjgwNjkiLCJzdWIiOiJDbG91ZEFwaVNhbXBsZSIsInVzZXJfdHlwZSI6IjEiLCJuYmYiOjE2ODU3NzMxNjAsImxvZyI6IkxvZ2dlcltjb20uZGppLnNhbXBsZS5jb21tb24ubW9kZWwuQ3VzdG9tQ2xhaW1dIiwiaXNzIjoiREpJIiwiaWQiOiJhMTU1OWU3Yy04ZGQ4LTQ3ODAtYjk1Mi0xMDBjYzQ3OTdkYTIiLCJleHAiOjE3NzIxNzMxNjAsImlhdCI6MTY4NTc3MzE2MCwidXNlcm5hbWUiOiJhZG1pblBDIn0.yue-t-XS8scPL5TBKbPgGjNctmUuMiwoFrdLFJLK-dA'}
#
# datas = json.dumps({"clientId": "81", "expireSec": "797"})
# r = requests.post(
#     "http://218.192.100.219:8018/control/api/v1/workspaces/e3dea0f5-37f2-4d79-ae58-490af3228069/drc/connect",
#     data=datas, headers=headers)
# print(r.text)