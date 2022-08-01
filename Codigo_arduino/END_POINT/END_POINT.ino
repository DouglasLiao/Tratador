#include <Wire.h>
#include <LiquidCrystal.h>
#include <Servo.h>
#include <Stepper.h>
#include <HX711.h>
#include <SPI.h>
#include <MFRC522.h>
#include <VL53L0X.h>

//sensor rfid
#define RST_PIN         5                   // Configurable, see typical pin layout above
#define SS_1_PIN        45  //RFID 2      // Configurable, take a unused pin, only HIGH/LOW required, must be different to SS 2
#define SS_2_PIN        46   //RFID 1      // Configurable, take a unused pin, only HIGH/LOW required, must be different to SS 1
#define SS_3_PIN        48   //RFID 0
#define NR_OF_READERS   3
byte ssPins[] = {SS_1_PIN, SS_2_PIN, SS_3_PIN};
MFRC522 mfrc522[NR_OF_READERS];   // Create MFRC522 instance.

// sensor distancia
VL53L0X sensor;
VL53L0X sensor2;

//LCD
LiquidCrystal lcd(12, 11, 10, 9, 8, 7);

// rele(moedor/misturador)
int porta_rele1 = 3;
int porta_rele2 = 4;

//SENSOR DE PESO
#define pinDT  31
#define pinSCK  30
HX711 scale;
float peso = 0;

//DEFINIÇÃO MOTOR DE PASSO
int passos = 320;
Stepper motor_passo(passos, 26,39,41,43);
 
//SERVO MOTORES
#define pinServo1 22
Servo servo_capim;
#define pinServo2 35
Servo servo_farelo;
#define pinServo3 24
Servo servo_misturador;
#define pinServo4 32
Servo servo_manjedoura;
#define pinServo5 2
Servo servo_portao;


//RTC CLOCK
 
int contador_animais_real=0;
int contador_animais = 1 ;

float contador_peso=0.12;
//horario alimentar os animais
int hora_alimento=16;
int minuto_alimento=0;

//horario soltar os animais
int hora_soltar=4;
int minuto_soltar=0;

int enter=4;
int finaliza=10;
int cont=0;

void setup() { 
//rele
 pinMode(porta_rele1, OUTPUT); 
  pinMode(porta_rele2, OUTPUT); 


// sensor distancia

  pinMode(36, OUTPUT); //antigo 9
  pinMode(38, OUTPUT); //antigo 10
  digitalWrite(36, LOW);//antigo 9
  digitalWrite(38, LOW);//antigo 10
delay(500);
  Wire.begin();
 //SENSOR
  pinMode(36, INPUT); //antigo 9
  delay(150);
  Serial.println("00");
  sensor.init(true);
  Serial.println("01");
  delay(100);
  sensor.setAddress((uint8_t)22);
  Serial.println("02");

  //SENSOR 2
  pinMode(38, INPUT);//antigo 10
  delay(150);
  sensor2.init(true);
  Serial.println("03");
  delay(100);
  sensor2.setAddress((uint8_t)25);
  Serial.println("04");
  
 Serial.println("");
  Serial.println("addresses set");
  Serial.println("");
  Serial.println("");
    sensor.setTimeout(500);
  sensor2.setTimeout(500);

//lcd
  lcd.begin(16,2);

 while (!Serial);    // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)

  SPI.begin();        // Init SPI bus

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN); // Init each MFRC522 card
    Serial.print(F("Reader "));
    Serial.print(reader);
    Serial.print(F(": "));
    mfrc522[reader].PCD_DumpVersionToSerial();
  }
  
//INICIALIZAÇÃO DO BLUETOOTH
Serial.begin(9600);

//MOTOR DE PASSO
motor_passo.setSpeed(70);

//sensor peso
 scale.begin(pinDT, pinSCK); // DEFININDO O SENSOR DE PESO
  scale.set_scale(-273333); //RESETANDO O SENSOR DE PESO
  scale.tare(); // ZERANDO A BALANÇA NO INCIO

  
// tempo atual rtc

 //servo
   servo_capim.attach(pinServo1);
  servo_capim.write(90);
  
  servo_farelo.attach(pinServo2);
  servo_farelo.write(120);
  
  servo_misturador.attach(pinServo3);
  servo_misturador.write(0);
  
 servo_manjedoura.attach(pinServo4);
  servo_manjedoura.write(100);
  
  servo_portao.attach(pinServo5);
  servo_portao.write(100);


}

void dump_byte_array(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

void loop() {

  
  while(enter==4){///


   
  delay(50);
//verifica os sensores ultrassonicos para verificar os estoques e verifica se o processo ja foi realizado.
//if(hora>=hora_programada && minuto>=minuto programado && finaliza==2)

if(finaliza==10){
  if(sensor.readRangeSingleMillimeters()<=80){
      
  lcd.setCursor(0,0);
   lcd.print("capim cheio");
   delay(1000);
   lcd.clear(); 
  }
  else{
  
  lcd.setCursor(0,0);
   lcd.print("capim vazio");
   delay(1000);
   lcd.clear(); 
    }
  if(sensor2.readRangeSingleMillimeters()<=80){
 
  lcd.setCursor(0,0);
  lcd.print("farelo cheio");
   delay(1000);
   lcd.clear(); 
  }
  else{
  
  lcd.setCursor(0,0);
   lcd.print("farelo vazio");
   delay(1000);
   lcd.clear(); }
 
   

servo_misturador.write(0);
       float peso_capim=0.5*contador_peso;

       //verificação estoques
    if(sensor.readRangeSingleMillimeters()<=80 && sensor2.readRangeSingleMillimeters()<=60) {
      servo_capim.write(0);
      finaliza=1;
      lcd.clear();
      } 

    
 while(finaliza==1){
  scale.power_up();
peso = scale.get_units(1);
      while(peso<peso_capim && cont==0){
        scale.power_up();
peso = scale.get_units(1);
        motor_passo.step(320);
             lcd.setCursor(0,0);
        lcd.print(peso);
          digitalWrite(porta_rele2, HIGH);  //Liga moedor
}
while(peso>= peso_capim && peso<contador_peso && cont<10){
   servo_capim.write(70);
  motor_passo.step(320);
    digitalWrite(porta_rele2, HIGH);  //Liga moedor
  cont ++;
  delay(50);
  }

while(peso>= peso_capim && peso<contador_peso && cont==10)
{
      lcd.clear();
     digitalWrite(porta_rele2, LOW);  //desliga moedor
scale.power_up();
peso = scale.get_units(1);
     lcd.setCursor(0,0);
 lcd.print(peso);
 motor_passo.step(0);
 servo_farelo.write(0);


  }
  if(peso>= contador_peso){
     servo_farelo.write(120);
           lcd.clear();

     //digitalWrite(porta_rele1, HIGH);  //Liga misturador
     lcd.setCursor(0,0);
   lcd.print("mis ON");
      delay(1000);
      servo_misturador.write(45);
      cont=20;
    
       

    }
//   Serial.println(peso);
if(peso <= 0.02 && cont==20){
       //digitalWrite(porta_rele1, LOW);  //desliga misturador misturador
lcd.clear();
   lcd.setCursor(0,0);
   lcd.print("mis off");
  servo_misturador.write(0);
  servo_portao.write(180);
        
  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    // Look for new cards

    if (mfrc522[reader].PICC_IsNewCardPresent() && mfrc522[reader].PICC_ReadCardSerial()) {
//      Serial.print(F("Reader "));
//      Serial.print(reader);
//      // Show some details of the PICC (that is: the tag/card)
//      Serial.print(F(": Card UID:"));
//      dump_byte_array(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size);
//      Serial.println();
//      Serial.print(F("PICC type: "));
      MFRC522::PICC_Type piccType = mfrc522[reader].PICC_GetType(mfrc522[reader].uid.sak);
//      Serial.println(mfrc522[reader].PICC_GetTypeName(piccType));

      if (reader == 2)
      {
       
        contador_animais_real ++;
            if(contador_animais_real == contador_animais){
    servo_portao.write(100);
        finaliza=3;
        cont=100;
          contador_animais_real=0;
 }
        
          delay(100);
//          Serial.print("Contador - RFID 0 = ");
//          Serial.println(contador_animais_real);
//          
      }//if (mfrc522[reader].PICC_IsNewC
       mfrc522[reader].PICC_HaltA();
      // Stop encryption on PCD
      mfrc522[reader].PCD_StopCrypto1();
  }
  }
 
  }

   
      }
      
}




/////// segunda parte






 while(finaliza==3){///
 

   delay(2000);
//lógica para soltar oa animais demanha
servo_portao.write(180);
if(contador_animais_real<=contador_animais){

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    // Look for new cards

    if (mfrc522[reader].PICC_IsNewCardPresent() && mfrc522[reader].PICC_ReadCardSerial()) {
//      Serial.print(F("Reader "));
//      Serial.print(reader);
    ////////  // Show some details of the PICC (that is: the tag/card)
//      Serial.print(F(": Card UID:"));
//Serial.println();
//      dump_byte_array(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size);
//      Serial.println();
//      Serial.print(F("PICC type: "));
      MFRC522::PICC_Type piccType = mfrc522[reader].PICC_GetType(mfrc522[reader].uid.sak);
//      Serial.println(mfrc522[reader].PICC_GetTypeName(piccType));

      if (reader == 2)
      {
       
            contador_animais_real ++;
            
        
          delay(100);
//          Serial.print("Contador - RFID 0 = ");
//          Serial.println(contador_animais_real);
          
      }//if (mfrc522[reader].PICC_IsNewC
       mfrc522[reader].PICC_HaltA();
      // Stop encryption on PCD
      mfrc522[reader].PCD_StopCrypto1();
  }
  }
if(contador_animais_real==contador_animais){
  delay(500);
  servo_portao.write(100);
 servo_manjedoura.write(140);
  delay(5000);
servo_manjedoura.write(100);
finaliza=6;
cont=0;
   }
  
  }
delay(100);
}


 for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    // Look for new cards

    if (mfrc522[reader].PICC_IsNewCardPresent() && mfrc522[reader].PICC_ReadCardSerial()) {
//      Serial.print(F("Reader "));
      Serial.print(reader);
      // Show some details of the PICC (that is: the tag/card)
      Serial.print(F(""));
      dump_byte_array(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size);
//      Serial.println();
//      Serial.print(F("PICC type: "));
      MFRC522::PICC_Type piccType = mfrc522[reader].PICC_GetType(mfrc522[reader].uid.sak);
//      Serial.println(mfrc522[reader].PICC_GetTypeName(piccType));

   mfrc522[reader].PICC_HaltA();
      // Stop encryption on PCD
      mfrc522[reader].PCD_StopCrypto1();
      }

      // Halt PICC
   
    } //if (mfrc522[reader].PICC_IsNewC
  }

}
