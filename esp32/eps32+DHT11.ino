#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#include <DHT.h>
#include <DHT_U.h>
#define DHTPIN 14

DHT dht(DHTPIN, DHT11);

BLEServer* pServer = NULL;
BLECharacteristic* ble_temp = NULL;
BLECharacteristic* ble_humidity = NULL;

bool deviceConnected = false;
bool oldDeviceConnected = false;
uint32_t temp_in_cels = 0;
uint32_t humidity_in_proc = 0;

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/
#define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define TEMP_IN_CELS_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"
#define HUMIDITY_IN_PROC_UUID "3e1b86b6-5b88-11ed-9b6a-0242ac120002"
class MyServerCallbacks: public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) {
    deviceConnected = true;
  };
  void onDisconnect(BLEServer* pServer) {
    deviceConnected = false;
  }
};
void setup() {
  Serial.begin(115200);
  dht.begin();
  // Create the BLE Device
  BLEDevice::init("ESP32");
  // Create the BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  // Create the BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);
  // Create a BLE Characteristic
  ble_temp = pService->createCharacteristic(
    TEMP_IN_CELS_UUID,
    BLECharacteristic::PROPERTY_READ |
    BLECharacteristic::PROPERTY_NOTIFY
  );

  //humidity 
  ble_humidity = pService->createCharacteristic(
    HUMIDITY_IN_PROC_UUID,
    BLECharacteristic::PROPERTY_READ |
    BLECharacteristic::PROPERTY_NOTIFY
  );

  // Create a BLE Descriptor
  ble_temp->addDescriptor(new BLE2902());
  ble_humidity->addDescriptor(new BLE2902());

  // Start the service
  pService->start();
  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x0); // set value to 0x00 to not advertise this parameter
  BLEDevice::startAdvertising();
  Serial.println("Waiting a client connection to notify...");
}
void loop() {
  // notify changed value
  if (deviceConnected) {
    temp_in_cels = dht.readTemperature();
    humidity_in_proc = dht.readHumidity();
    ble_temp->setValue((uint8_t*)&temp_in_cels, 1);
    ble_temp->notify();
    ble_humidity->setValue((uint8_t*)&humidity_in_proc, 1);
    ble_humidity->notify();
    delay(3); // bluetooth stack will go into congestion, if too many packets are sent, in 6 hours test i
    //was able to go as low as 3ms
  }
  // disconnecting
  if (!deviceConnected && oldDeviceConnected) {
    delay(500); // give the bluetooth stack the chance to get things ready
    pServer->startAdvertising(); // restart advertising
    Serial.println("start advertising");
    oldDeviceConnected = deviceConnected;
  }
  // connecting
  if (deviceConnected && !oldDeviceConnected) {
    // do stuff here on connecting
    oldDeviceConnected = deviceConnected;
  }
}