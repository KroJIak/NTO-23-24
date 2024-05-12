/*
    Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleServer.cpp
    Ported to Arduino ESP32 by Evandro Copercini
*/

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLECharacteristic.h>
#include <BLE2902.h>

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

#define CHARACTERISTIC_SENSOR_0_UUID "31a685ee-c764-4098-80d8-d3064801dee7"
#define CHARACTERISTIC_SENSOR_1_UUID "23b74619-5ed0-4bf1-b982-364c343bdba4"

#define CHARACTERISTIC_COMMANDS_UUID "a30de044-d90b-4db9-a8bf-609fc9f5fa84"

#define CHARACTERISTIC_SERIAL_NUMBER_UUID   "6f8ea403-3643-44e4-bbb4-d29555351bc8"


#define SENSOR_RESPONSE_LENGTH 4

#define DIGITAL_PIN_1 4
#define DIGITAL_PIN_2 7
#define DIGITAL_PIN_3 8
#define DIGITAL_PIN_4 11
#define DIGITAL_PIN_5 12

#define SENSOR_TYPE_NONE 0
#define SENSOR_TYPE_LINE 1
#define SENSOR_TYPE_LED  2
#define SENSOR_TYPE_LIGHT 3
#define SENSOR_TYPE_TOUCH 4
#define SENSOR_TYPE_PROXIMITY 5
#define SENSOR_TYPE_ULTRASONIC 6
#define SENSOR_TYPE_COLOR 7


#define A1 1
#define A2 2
#define A3 3
#define A4 4
#define A5 5

bool deviceConnected = false;





class ISensor {
  public:
    virtual byte getType();
    virtual void reset();
    virtual void iteration(byte data, byte data2);
    virtual boolean isReady();
    virtual byte* getResult();
    
    //virtual uint16_t& getResult();

    virtual void debugSetValue(uint16_t value);
};



class AnalogSensor: public ISensor {
    int pin;
    byte type = 0;

    uint16_t byteResult = 0;

  public:
    AnalogSensor(int pin, byte type) {
      this -> pin = pin;
      this -> type = type;
      pinMode(pin, INPUT);

      //Let's set 1 to digital out
      //So that the the lamps light
      switch (pin) {
        case A1: {
            pinMode(DIGITAL_PIN_1, OUTPUT);
            break;
          }
        case A2: {
            pinMode(DIGITAL_PIN_2, OUTPUT);
            break;
          }
        case A3: {
            pinMode(DIGITAL_PIN_3, OUTPUT);
            break;
          }
        case A4: {
            pinMode(DIGITAL_PIN_4, OUTPUT);
            break;
          }
        case A5: {
            pinMode(DIGITAL_PIN_5, OUTPUT);
            break;
          }
      }
    };

   void  debugSetValue(uint16_t value){

       byteResult = value;
    
   }

    byte getType() {
      return type;
    }


    void reset() {
      byteResult = 0;
    }


    void iteration(byte data, byte data2) {
      byteResult = analogRead(pin) >> 2;
    }

    boolean isReady() {
      return true;
    }

   byte* getResult() {
      return new byte[SENSOR_RESPONSE_LENGTH] {0, 0, 0, byteResult};
    }

  /*  uint16_t& getResult() {
      
      return byteResult;
    } */
};



ISensor* sensors[5];


class MyCallbackHandler: public BLECharacteristicCallbacks {
   
 void onRead(BLECharacteristic* pCharacteristic) {
     Serial.println("onRead");
 }
 void onWrite(BLECharacteristic* pCharacteristic) {
    // Do something because a new value was written.
     Serial.println("onWrite");

    
 }

};


class SerialNumberCallbackHandler: public BLECharacteristicCallbacks {
   
 void onRead(BLECharacteristic* pCharacteristic) {
     Serial.println("onRead");
 }
 void onWrite(BLECharacteristic* pCharacteristic) {
    // Do something because a new value was written.
     Serial.println("onWrite");

    
 }
 
};


class SensorCallback_0: public BLECharacteristicCallbacks {
   
 void onRead(BLECharacteristic* pCharacteristic) {
     Serial.println("SensorCallback_0 onRead");

     pCharacteristic->setValue(sensors[0]->getResult(),SENSOR_RESPONSE_LENGTH);
 }
 void onWrite(BLECharacteristic* pCharacteristic) {
    // Do something because a new value was written.
     Serial.println("onWrite");

    
 }
 
};

class SensorCallback_1: public BLECharacteristicCallbacks {
   
 void onRead(BLECharacteristic* pCharacteristic) {
     Serial.println("SensorCallback_1 onRead");

     pCharacteristic->setValue(sensors[1]->getResult(),SENSOR_RESPONSE_LENGTH);
 }
 void onWrite(BLECharacteristic* pCharacteristic) {
    // Do something because a new value was written.
     Serial.println("onWrite");

    
 }
 
};


class CommandsCallbackHandler: public BLECharacteristicCallbacks {
   
 void onRead(BLECharacteristic* pCharacteristic) {
     Serial.println("onRead");
 }
 void onWrite(BLECharacteristic* pCharacteristic) {
    // Do something because a new value was written.
     Serial.println("onWrite");

     std::string str = pCharacteristic->getValue();
    const char * value = str.c_str();
    Serial.println(value);
 }
 
};


class ServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
      Serial.println("onConnect");
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
       Serial.println("onDisconnect");
    }
};

class MySecurity : public BLESecurityCallbacks {

  uint32_t onPassKeyRequest(){
        ESP_LOGI(LOG_TAG, "PassKeyRequest");
    return 123456;
  }
  void onPassKeyNotify(uint32_t pass_key){
        ESP_LOGI(LOG_TAG, "The passkey Notify number:%d", pass_key);
  }
  bool onConfirmPIN(uint32_t pass_key){
        ESP_LOGI(LOG_TAG, "The passkey YES/NO number:%d", pass_key);
      vTaskDelay(5000);
    return true;
  }
  bool onSecurityRequest(){
      ESP_LOGI(LOG_TAG, "SecurityRequest");
    return true;
  }

  void onAuthenticationComplete(esp_ble_auth_cmpl_t cmpl){
    ESP_LOGI(LOG_TAG, "Starting BLE work!");
  }
  
};



void setup() {
  Serial.begin(115200);
  Serial.println("Starting BLE work!");

  sensors[0]  = new AnalogSensor(A1, SENSOR_TYPE_LINE);
  sensors[1]  = new AnalogSensor(A2, SENSOR_TYPE_LINE);
  sensors[2]  = new AnalogSensor(A3, SENSOR_TYPE_LINE);
  sensors[3]  = new AnalogSensor(A4, SENSOR_TYPE_LINE);
  sensors[4]  = new AnalogSensor(A5, SENSOR_TYPE_LINE);

  BLEDevice::init("ESP32");
  BLEDevice::setEncryptionLevel(ESP_BLE_SEC_ENCRYPT);
  /*
   * Required in authentication process to provide displaying and/or input passkey or yes/no butttons confirmation
   */
  BLEDevice::setSecurityCallbacks(new MySecurity());
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new ServerCallbacks());
  
  BLEService *pService = pServer->createService(SERVICE_UUID);


  BLECharacteristic *sensor_0_characteristic = pService->createCharacteristic(
                                         CHARACTERISTIC_SENSOR_0_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_NOTIFY
                                       );

  sensors[0]->debugSetValue(23) ;
  sensor_0_characteristic->setValue(sensors[0]->getResult(),SENSOR_RESPONSE_LENGTH);
  sensor_0_characteristic->setCallbacks(new SensorCallback_0());
  
   // https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.descriptor.gatt.client_characteristic_configuration.xml
  // Create a BLE Descriptor
  sensor_0_characteristic->addDescriptor(new BLE2902());
/////////////////////////////////////////////

 /////////////////////////////////////////

  BLECharacteristic *sensor_1_characteristic = pService->createCharacteristic(
                                         CHARACTERISTIC_SENSOR_1_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_NOTIFY
                                       );

  sensors[1]->debugSetValue(56) ;
  sensor_1_characteristic->setValue(sensors[1]->getResult(),SENSOR_RESPONSE_LENGTH);
  sensor_1_characteristic->setCallbacks(new SensorCallback_1());
  
   // https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.descriptor.gatt.client_characteristic_configuration.xml
  // Create a BLE Descriptor
  sensor_1_characteristic->addDescriptor(new BLE2902());
/////////////////////////////////////////////

 /////////////////////////////////////////

  BLECharacteristic *commands_characteristic = pService->createCharacteristic(
                                         CHARACTERISTIC_COMMANDS_UUID,
                                         BLECharacteristic::PROPERTY_WRITE |
                                         BLECharacteristic::PROPERTY_NOTIFY
                                       );

  commands_characteristic->setCallbacks(new CommandsCallbackHandler());
  
   // https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.descriptor.gatt.client_characteristic_configuration.xml
  // Create a BLE Descriptor
  commands_characteristic->addDescriptor(new BLE2902());
/////////////////////////////////////////////

 /////////////////////////////////////////

  BLECharacteristic *serial_number_characteristic = pService->createCharacteristic(
                                         CHARACTERISTIC_SERIAL_NUMBER_UUID ,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_NOTIFY
                                       );

  serial_number_characteristic->setValue("ROBBO-00000-00003-R-00000-00000-00000000000000000222");
  serial_number_characteristic->setCallbacks(new SerialNumberCallbackHandler());
  
   // https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.descriptor.gatt.client_characteristic_configuration.xml
  // Create a BLE Descriptor
  serial_number_characteristic->addDescriptor(new BLE2902());
/////////////////////////////////////////////
  
  
  pService->start();
  BLEAdvertising *pAdvertising = pServer->getAdvertising();
  pAdvertising->start();

  BLESecurity *pSecurity = new BLESecurity();
  pSecurity->setKeySize();
  pSecurity->setAuthenticationMode(ESP_LE_AUTH_REQ_SC_ONLY);
  pSecurity->setCapability(ESP_IO_CAP_IO);
  pSecurity->setInitEncryptionKey(ESP_BLE_ENC_KEY_MASK | ESP_BLE_ID_KEY_MASK);

  Serial.println("Characteristics defined!");
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(2000);
}
