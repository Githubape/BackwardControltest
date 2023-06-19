import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer
import cv2

async def consume_webrtc_stream(offer):
    # 创建RTCPeerConnection对象
    pc = RTCPeerConnection()

    # 创建本地媒体流传输对象
    player = MediaPlayer("webrtc://139.159.148.93/live/4TADL2L0010027")  # 根据需要替换为实际的视频输入设备

    # 添加本地媒体流传输到RTCPeerConnection
    pc.addTrack(player.video)

    # 设置远程描述
    await pc.setRemoteDescription(offer)

    # 创建应答
    answer = await pc.createAnswer()

    # 设置本地描述
    await pc.setLocalDescription(answer)

    # 打印生成的SDP（会话描述协议）
    print(pc.localDescription)

    # 等待远程媒体流传输的连接
    @pc.on("track")
    def on_track(track):
        print("Received track:", track.kind)
        player.audio = track

        # 处理视频流
        @track.on("ended")
        async def on_ended():
            # 停止视频处理
            await player.stop()

        @track.on("recv")
        async def on_recv():
            # 获取视频帧
            frame = player.video.frame(width=1280, height=720)

            # 显示视频帧
            cv2.imshow("WebRTC Stream", frame)
            cv2.waitKey(1)

    # 等待远程连接关闭
    await pc.wait_closed()

async def main():
    # 创建RTCPeerConnection并生成offer
    pc = RTCPeerConnection()
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    # 将offer传递给消费者
    await consume_webrtc_stream(pc.localDescription)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
