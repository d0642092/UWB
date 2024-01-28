#include <ESP8266WiFi.h>
#include <Servo.h>

//=============WiFi=============
char ssid[] = "WiFi-Name";
char password[] = "WiFi-Password";

//============socket============
//uint16_t = unsigned short int
const uint16_t port = 55688;
const char * host = "Server-Ip";
WiFiClient client01;

//============ Servo============
char command[20] = {};
char command01[6] = {};
char command02[6] = {};
char commandtmp[6] = {'\0'};
int cmd01 = 0;
int cmd02 = 0;
int servo1Pin = D2;
int servo2Pin = D3;
Servo myservo1;
Servo myservo2;

void motorWrite(int angle01, int angle02){
  myservo1.write(angle01);
  myservo2.write(angle02);
}

void setup() {
  // put your setup code here, to run once:
  //開啟可以 print東西的序列埠
  Serial.begin(9600);

  //連線到 名字為 ssid 的Wifi
  WiFi.begin(ssid, password);

  Serial.print("Connecting");
  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.print("Connected, IP address:");
  Serial.println(WiFi.localIP());

  //Servo連線
  myservo1.attach(servo1Pin);
  myservo2.attach(servo2Pin);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("嘗試尋找:");
  Serial.println(host);

  if(!client01.connected()){
    Serial.println("connecting...");
    if (client01.connect(host, port)){
      Serial.println("Connected to server successful!");
      client01.print("車子端");
      while(client01.connected() || client01.available()){
        //查看Server Buffer內是否尚有資訊
        if(client01.available()){
          String Control = client01.readStringUntil('\n');
//          Serial.print(Control);

          //車子指令轉換
          Control.toCharArray(command, 12);
          Serial.print("轉換後指令: ");
          Serial.println(command);
          sscanf(command, "%[^+] %[+] %[^+]", command01, commandtmp, command02);
          cmd01 = atoi(command01);
          cmd02 = atoi(command02);
          Serial.print("馬達1: ");
          Serial.println(cmd01);
          Serial.print("馬達2: ");
          Serial.println(cmd02);
          Serial.print("iDentify:");
          Serial.println(commandtmp[0]);
          if (commandtmp[0] == '+'){
            Serial.println("Sent!!");
            motorWrite(cmd01, cmd02);
          }
        }
        delay(250);
      }
    }
    else{
      Serial.println("Connection Fail");
      client01.stop();
    }
  }

  //重新尋找Server...>delayTime
  delay(1000);
}
