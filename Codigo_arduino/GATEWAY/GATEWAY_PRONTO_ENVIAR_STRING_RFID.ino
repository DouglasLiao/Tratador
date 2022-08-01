//Envio de Dados para tagoIO via MQTT

#include <ArduinoJson.h>
#include "EspMQTTClient.h"
#include <Wire.h>

//variáveis para Json
#define RXp2 16
#define TXp2 17

char mensagem[40];
String recebe="";




//configurações da conexão MQTT
EspMQTTClient client
(
  "teste1", //nome da sua rede Wi-Fi
  "1234", //senha da sua rede Wi-Fi
  "mqtt.tago.io",  // MQTT Broker server ip padrão da tago
  "Default",   // username
  "b4936115-b137-429f-912b-f48227c02e77",   // Código do Token 
  "tese(loraMTQTTprojetoesp)",     // Client name that uniquely identify your device
  1883              // The MQTT port, default to 1883. this line can be omitted
);


void setup()
{
  Serial.begin(115200);
   Serial2.begin(9600, SERIAL_8N1, RXp2, TXp2);
  

}

// This function is called once everything is connected (Wifi and MQTT)
// WARNING : YOU MUST IMPLEMENT IT IF YOU USE EspMQTTClient
void onConnectionEstablished()
{}

//loop do programa
void loop()
{


if(Serial2.available()){

   recebe=Serial2.readString();
recebe.toCharArray(mensagem,40);


client.publish("teste", mensagem);


}

  


  client.loop();
}
