#include "WiFi.h"
#include "ESPAsyncWebServer.h"
#include <HTTPClient.h>

const char* ssid = "ESP32-Access-Point";
const char* password = "123456789";
const char* SlaveServerName = "http://192.168.4.2/post";

