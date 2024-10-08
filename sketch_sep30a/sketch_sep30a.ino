#include <WiFi.h>
#include <WiFiUdp.h>
#include "DHTesp.h"
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <coap-simple.h>  // Thư viện CoAP Simple




#define DHTpin 4
DHTesp dht;




//----Thay đổi thành thông tin của bạn---------------
const char* ssid = "Khó cho t quá";      // Wifi connect
const char* password = "";    // Password
// const char* ssid = "OPPO A3s";
// const char* password = "12345678";  

// const char* ssid = "Tanhhoang";
// const char* password = "123456789";  



const char* mqtt_server = "103.57.223.140";
//const char* mqtt_server = "172.20.10.3"; // Thay đổi thành địa chỉ IP của MQTT Broker
const int mqtt_port = 1883;
const char* mqtt_username = "client";      // User
const char* mqtt_password = "1";      // Password
//--------------------------------------------------




WiFiClient espClient;
PubSubClient mqttClient(espClient);
WiFiUDP udp;            // Sử dụng WiFiUDP thay vì WiFiClient
Coap coap(udp);         // Khởi tạo Coap với UDP




unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (50)
char msg[MSG_BUFFER_SIZE];




// Định nghĩa chân cho đèn LED tích hợp
#define LED_BUILTIN 2




// Khai báo biến toàn cục cho lệnh LED
String ledCommand = "";
bool ledCommandReceived = false;



unsigned long idle_time_core_0 = 0;
unsigned long idle_time_core_1 = 0;
unsigned long last_check_time = 0;
unsigned long total_ticks = 0;




// Hàm chuyển đổi BSSID từ chuỗi sang mảng uint8_t
void parseBSSID(String bssidStr, uint8_t* bssid) {
  int values[6];
  if (6 == sscanf(bssidStr.c_str(), "%x:%x:%x:%x:%x:%x",
                 &values[0], &values[1], &values[2],
                 &values[3], &values[4], &values[5])) {
    for (int i = 0; i < 6; ++i) {
      bssid[i] = (uint8_t) values[i];
    }
  }
}


void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Scanning networks...");
 
  int numberOfNetworks = WiFi.scanNetworks();
  if (numberOfNetworks == 0) {
    Serial.println("No networks found. Please check your WiFi settings.");
    return;
  }


  int bestRSSI = -9999; // Đặt giá trị RSSI nhỏ nhất ban đầu
  int bestNetworkIndex = -1;
  String bestBSSID = ""; // Biến lưu BSSID tốt nhất
 
  // Quét qua tất cả các mạng và tìm mạng có cùng SSID với tín hiệu tốt nhất
  for (int i = 0; i < numberOfNetworks; i++) {
    String networkSSID = WiFi.SSID(i);
    int networkRSSI = WiFi.RSSI(i);
    String networkBSSID = WiFi.BSSIDstr(i); // Lấy BSSID của mạng


    Serial.print(i);
    Serial.print(": ");
    Serial.print(networkSSID);
    Serial.print(" (RSSI: ");
    Serial.print(networkRSSI);
    Serial.print(", BSSID: ");
    Serial.print(networkBSSID);
    Serial.println(")");


    // So sánh SSID và chọn mạng có tín hiệu mạnh nhất
    if (networkSSID == ssid && networkRSSI > bestRSSI) {
      bestRSSI = networkRSSI;
      bestNetworkIndex = i;
      bestBSSID = networkBSSID; // Lưu lại BSSID của mạng tốt nhất
    }
  }


  // Kiểm tra nếu tìm được mạng có SSID phù hợp
  if (bestNetworkIndex != -1) {
    Serial.print("Connecting to best network with SSID: ");
    Serial.println(ssid);
    Serial.print("Best RSSI: ");
    Serial.println(bestRSSI);
    Serial.print("BSSID: ");
    Serial.println(bestBSSID);


    // Chuyển đổi BSSID từ chuỗi sang mảng uint8_t
    uint8_t bssidArray[6];
    parseBSSID(bestBSSID, bssidArray);


    // Kết nối đến mạng WiFi với SSID và BSSID tốt nhất
    WiFi.begin(ssid, password, 0, bssidArray);


    // Chờ kết nối WiFi thành công
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }


    Serial.println();
    Serial.println("WiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("No matching network found. Please check your SSID and password.");
  }
}






// Kết nối lại với MQTT Broker
void reconnect() {
  // Chỉ thử kết nối MQTT khi Wi-Fi đã được kết nối
  if (WiFi.status() == WL_CONNECTED) {
    while (!mqttClient.connected()) {
      Serial.print("Attempting MQTT connection...");
      String clientID =  "ESPClient-123";
   


      // Thử kết nối tới MQTT Broker
      if (mqttClient.connect(clientID.c_str(), "root", "root")) {
        Serial.println("connected");
        mqttClient.subscribe("esp32/dht11");
      } else {
        Serial.print("failed, rc=");
        Serial.print(mqttClient.state());
        Serial.println(" try again in 5 seconds");
        delay(5000);  // Đợi 5 giây trước khi thử lại
      }
    }
  } else {
    // Nếu không có Wi-Fi, thông báo và không thử kết nối MQTT
    Serial.println("WiFi not connected, cannot connect to MQTT.");
  }
}






// Xử lý yêu cầu CoAP để điều khiển LED
void handleCoapLedControl(CoapPacket &packet, IPAddress ip, int port) {
  String incomingMessage = "";
  for (int i = 0; i < packet.payloadlen; i++) {
    incomingMessage += (char)packet.payload[i];
  }
  Serial.println("CoAP Message received: " + incomingMessage);




  // Lưu lệnh để xử lý sau
  ledCommand = incomingMessage;
  ledCommandReceived = true;

  // Gửi phản hồi về cho client CoAP
  const char* responsePayload = "Command received";
  size_t payloadLen = strlen(responsePayload);
  coap.sendResponse(ip, port, packet.messageid, responsePayload, payloadLen);
}




// Thiết lập CoAP server
void setupCoap() {
  coap.server(handleCoapLedControl, "ledControl");
  coap.start();
}




// Callback cho tin nhắn MQTT
void callback(char* topic, byte* payload, unsigned int length) {
  String incomingMessage = "";
  for (int i = 0; i < length; i++) {
    incomingMessage += (char)payload[i];
  }
  Serial.println("Message arrived [" + String(topic) + "] " + incomingMessage);
}

//DO CPU
void setup_idle_tasks() {
  // Task nhàn rỗi cho Core 0
  xTaskCreatePinnedToCore([](void *param) {
    while (true) {
      idle_time_core_0++;
      vTaskDelay(1);  // Mỗi tick sẽ đếm thời gian nhàn rỗi
    }
  }, "IdleTask0", 1024, NULL, 1, NULL, 0);

  // Task nhàn rỗi cho Core 1
  xTaskCreatePinnedToCore([](void *param) {
    while (true) {
      idle_time_core_1++;
      vTaskDelay(1);  // Mỗi tick sẽ đếm thời gian nhàn rỗi
    }
  }, "IdleTask1", 1024, NULL, 1, NULL, 1);
}

// Hàm tính toán và in mức độ sử dụng CPU
void print_cpu_usage() {
  unsigned long currentTime = millis();
  unsigned long total_ticks_elapsed = currentTime - last_check_time;

  // Tính phần trăm sử dụng CPU cho từng lõi
  float cpu_usage_core_0 = 100.0 * (1 - (float)idle_time_core_0 / total_ticks_elapsed);
  float cpu_usage_core_1 = 100.0 * (1 - (float)idle_time_core_1 / total_ticks_elapsed);

  Serial.print("CPU Core 0 Usage: ");
  Serial.print(cpu_usage_core_0);
  Serial.println("%");

  Serial.print("CPU Core 1 Usage: ");
  Serial.print(cpu_usage_core_1);
  Serial.println("%");

  // Reset thời gian idle
  idle_time_core_0 = 0;
  idle_time_core_1 = 0;
  last_check_time = currentTime;
}



// Gửi tin nhắn MQTT
void publishMessage(const char* topic, String payload, boolean retained) {
  if (mqttClient.publish(topic, payload.c_str(), retained)) {
    Serial.println("Message published [" + String(topic) + "]: " + payload);
  }
}




void setup() {
  Serial.begin(9600);
  while (!Serial) delay(1);




  dht.setup(DHTpin, DHTesp::DHT11);




  setup_wifi();
  mqttClient.setServer(mqtt_server, mqtt_port);
  mqttClient.setCallback(callback);




  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);  // Tắt đèn mặc định (HIGH vì hoạt động logic ngược)


  setup_idle_tasks(); // Khởi tạo các task nhàn rỗi

  setupCoap();  // Khởi tạo CoAP server
}




unsigned long timeUpdate = millis();
void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi lost connection. Reconnecting...");
    setup_wifi();  // Thử kết nối lại Wi-Fi
  }
  if (!mqttClient.connected()) {
    reconnect();
  }
  mqttClient.loop();




  // Xử lý CoAP
  coap.loop();


  if (millis() - last_check_time >= 1000) {
      print_cpu_usage();
    }


  // Kiểm tra lệnh điều khiển LED từ CoAP
  if (ledCommandReceived) {
    if (ledCommand == "OFF") {
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("LED turned OFF");
    } else if (ledCommand == "ON") {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("LED turned ON");
    }
    ledCommandReceived = false;  // Reset cờ sau khi xử lý
  }




  // Đọc cảm biến DHT11 và gửi qua MQTT
  if (millis() - timeUpdate > 5000) {
    delay(dht.getMinimumSamplingPeriod());
    float h = dht.getHumidity();
    float t = dht.getTemperature();




    DynamicJsonDocument doc(1024);
    doc["humidity"] = h;
    doc["temperature"] = t;
    char mqtt_message[128];
    serializeJson(doc, mqtt_message);
    publishMessage("esp32/dht11", mqtt_message, true);




    timeUpdate = millis();
  }
}


