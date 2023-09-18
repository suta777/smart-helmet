from vidstream import StreamingServer, AudioReceiver, CameraClient, AudioSender
import socket
import threading
import tkinter as tk
import requests


class Client:
    def __init__(self, window, server_ip):
        self.local_ip_address = socket.gethostbyname(socket.gethostname())
        self.vid_recv_port = 5003
        self.aud_recv_port = 5004
        self.vid_send_port = 5001
        self.aud_send_port = 5002
        print(
            f"client ip: {self.local_ip_address}\nvid recv port:{self.vid_recv_port}, vid send port:{self.vid_send_port}\naud recv port:{self.aud_recv_port}, aud send port:{self.aud_send_port}")

        self.server_ip = server_ip

        recvs = self.start_listening()
        self.start_camera_stream()

        label_target_ip = tk.Label(window, text='서버와 연락을 기다리는 중')
        label_target_ip.pack()

        window.protocol('WM_DELETE_WINDOW',
                        lambda: self.exit_fn(window, recvs))

    def start_listening(self):
        stream_recv = StreamingServer(
            self.local_ip_address, self.vid_recv_port)
        audio_recv = AudioReceiver(self.local_ip_address, self.aud_recv_port)
        t1 = threading.Thread(target=stream_recv.start_server)
        t2 = threading.Thread(target=audio_recv.start_server)
        t1.daemon = True
        t2.daemon = True
        t1.start()
        t2.start()

        return [stream_recv, audio_recv]

    def exit_fn(self, window, recvs):
        recvs[0].stop_server()
        recvs[1].stop_server()
        window.destroy()

    def start_camera_stream(self):
        camera_client = CameraClient(self.server_ip, self.vid_send_port)
        t3 = threading.Thread(target=camera_client.start_stream)
        t3.daemon = True
        t3.start()

        audio_sender = AudioSender(self.server_ip, self.aud_send_port)
        t4 = threading.Thread(target=audio_sender.start_stream)
        t4.daemon = True
        t4.start()


def init_video_call(server_ip):
    window = tk.Tk()
    window.title('client video call')
    window.geometry('350x30')
    Client(window, server_ip)
    window.mainloop()


def request_send(url):
    print(f"server url: {url}")
    requests.get(url)


def get_ip(url):
    hostname = url.split("//")[-1].split("/")[0].split(":")[0]
    ip_address = socket.gethostbyname(hostname)
    print(f"server ip: {ip_address}")
    return ip_address


def start_video_call(url):
    t5 = threading.Thread(target=request_send, args=(url,))
    t5.daemon = True
    t5.start()
    ip_address = get_ip(url)

    t6 = threading.Thread(target=init_video_call, args=(ip_address,))
    t6.daemon = True
    t6.start()

if __name__ == '__main__':
    start_video_call('http://192.168.0.58:5000/wc')