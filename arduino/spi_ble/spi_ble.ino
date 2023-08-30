//
/*
    Based on Neil Kolban example for IDF:https://github.com/nkolban/ESP32_BLE_Arduino/blob/master/examples/BLE_uart/BLE_uart.ino
    Create a BLE server that, once we receive a connection, will send periodic notifications.
    The service advertises itself as: 6E400001-B5A3-F393-E0A9-E50E24DCCA9E
    Has a characteristic of: 6E400002-B5A3-F393-E0A9-E50E24DCCA9E - used for receiving data with "WRITE" 
    Has a characteristic of: 6E400003-B5A3-F393-E0A9-E50E24DCCA9E - used to send data with  "NOTIFY"

    The design of creating the BLE server is:
    1. Create a BLE Server
    2. Create a BLE Service
    3. Create a BLE Characteristic on the Service
    4. Create a BLE Descriptor on the characteristic
    5. Start the service.
    6. Start advertising.
*/
// #define GPIO_0to31SET_REG   *((volatile unsigned long *)GPIO_OUT_W1TS_REG)
// #define GPIO_0to31CLR_REG   *((volatile unsigned long *)GPIO_OUT_W1TC_REG)
// #define GPIO_32to48SET_REG   *((volatile unsigned long *)GPIO_OUT1_W1TS_REG)
// #define GPIO_32to48CLR_REG   *((volatile unsigned long *)GPIO_OUT1_W1TC_REG)
    #define PDN   3//6  //
    #define RSTN 46//4  //
    #define EXEC 14//5  //
#include <SPI.h>
// Define ALTERNATE_PINS to use non-standard GPIO pins for SPI bus
    #define VSPI_MISO   21//CDTO//37  //GPIO37
    #define VSPI_MOSI   45//CDTI//35  //GPIO35
    #define VSPI_SCLK   47//36  //GPIO36
    #define VSPI_SS     48//39 //GPIO39

#if CONFIG_IDF_TARGET_ESP32S2 || CONFIG_IDF_TARGET_ESP32S3
#define VSPI FSPI
#endif

static const int spiClk = 8000000; // 8 MHz
SPISettings mySPISettings = SPISettings(spiClk, MSBFIRST, SPI_MODE0);

String py_input;
int rx_buf = 0;
int add = 0;
int wdata = 0;
uint8_t rddata = 0;
uint16_t rddata_16b = 0;
uint8_t flg_exec = 0;

unsigned long t_st, t_sp;



//uninitalised pointers to SPI objects
SPIClass * vspi = NULL;


#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

BLEServer *pServer = NULL;
BLECharacteristic * pCharacteristic;
bool deviceConnected = false;
bool oldDeviceConnected = false;
float txValue = 0;

std::string rxValue;
String str_rx;
const int MTU_SIZE = 512;
// See the following for generating UUIDs:
// https://www.uuidgenerator.net/
#define SERVICE_UUID           "6E400001-B5A3-F393-E0A9-E50E24DCCA9E" // UART service UUID
#define CHARACTERISTIC_UUID_RX "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID_TX "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"


class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
        deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
        deviceConnected = false;
    }
};

class MyCallbacks: public BLECharacteristicCallbacks {
    void onRead(BLECharacteristic *pCharacteristic) {
        char txString[8]; // make sure this is big enuffz
            dtostrf(txValue, -1, 0, txString); // float_val, min_width, digits_after_decimal, char_buffer
            // Serial.print("TxData");
            // Serial.println(txString);
            pCharacteristic->setValue(txString);
    }

    void onWrite(BLECharacteristic *pCharacteristic) {
      // std::string rxValue = pCharacteristic->getValue();
        rxValue = pCharacteristic->getValue();

        // if (rxValue.length() > 0) {
            // Serial.println("*********");
            // Serial.print("Received Value: ");
            // for (int i = 0; i < rxValue.length(); i++)
                // Serial.print(rxValue[i]);
                // Serial.println();
                // Serial.println("*********");
        // }
    }
};

//State define 
const int W_DAT = 256;
const int R_DAT = 257;
const int R_PG = 258;
const int PDN_CTRL = 259;
const int RSTN_CTRL = 260;
const int EXE_CTRL = 261;
const int EXE_CTRL_ONLY = 262;
const int FFT_CAPT = 263;
const int FFT_EXEC = 264;


////////////////////////////////////////////////
//SPI Function Start
////////////////////////////////////////////////
void w_spi(SPIClass *spi, byte add, byte data) {
    //use it as you would the regular arduino SPI API
    uint16_t txdata;
    txdata = (add << 8) + data;
    // spi->beginTransaction(SPISettings(mySPISettings));
    // digitalWrite(spi->pinSS(), LOW); //pull SS slow to prep other end for transfer
    // GPIO_32to48CLR_REG = 0x000000B8;
    spi->transfer16(txdata);
    // digitalWrite(spi->pinSS(), HIGH); //pull ss high to signify end of data transfer
    // GPIO_32to48SET_REG = 0x000000B8;
    // spi->endTransaction();
}

uint8_t r_spi(SPIClass *spi, byte add, byte data) {
    //use it as you would the regular arduino SPI API
    uint16_t txdata;
    uint16_t buf;
    uint8_t rd;
    txdata = (add << 8) + data;

    // spi->beginTransaction(SPISettings(mySPISettings));
    // digitalWrite(spi->pinSS(), LOW); //pull SS slow to prep other end for transfer
    // GPIO_32to48CLR_REG = 0x000000B8;
    buf = spi -> transfer16(txdata);
    // digitalWrite(spi->pinSS(), HIGH); //pull ss high to signify end of data transfer
    // GPIO_32to48SET_REG = 0x000000B8;
    // spi->endTransaction();
    rd = buf & 0xFF;
    return rd;
}

uint16_t r_spi_16b(SPIClass *spi) {
    //use it as you would the regular arduino SPI API
    uint16_t rd_16b;

    // spi->beginTransaction(SPISettings(mySPISettings));
    // digitalWrite(spi->pinSS(), LOW); //pull SS slow to prep other end for transfer
    // GPIO_32to48CLR_REG = 0x000000B8;
    rd_16b = spi -> transfer16(0xFFFF);
    // digitalWrite(spi->pinSS(), HIGH); //pull ss high to signify end of data transfer
    // GPIO_32to48SET_REG = 0x000000B8;
    // spi->endTransaction();
    return rd_16b;
}
////////////////////////////////////////////////
//SPI Function End
////////////////////////////////////////////////

////////////////////////////////////////////////
//Pin Function Start
////////////////////////////////////////////////
void pdn_ctrl(int sig) {
    if( sig == 1){
        digitalWrite(PDN, HIGH);
        // Serial.println("PDN HIGH");
    }
    else{
        digitalWrite(PDN, LOW);
        // Serial.println("PDN LOW");
    }
}

void rstn_ctrl(int sig) {
    if( sig == 1){
        digitalWrite(RSTN, HIGH);
        // Serial.println("RSTN HIGH");
    }
    else{
        digitalWrite(RSTN, LOW);
        // Serial.println("RSTN LOW");
    }
}

uint8_t exec_ctrl(int sig){
    if( sig == 1){
        digitalWrite(EXEC, HIGH);
        return 1;
        // Serial.println("EXEC HIGH");
    }
    else{
        digitalWrite(EXEC, LOW);
        return 0;
        // Serial.println("EXEC LOW");
    }
}
////////////////////////////////////////////////
//Pin Function End
////////////////////////////////////////////////

////////////////////////////////////////////////
//Charp Function Start
////////////////////////////////////////////////
void wait_state(SPIClass* spi, uint8_t add, uint8_t state_num){
    uint8_t rd = 0;
    //while (rd < state_num){
    while (rd != state_num){
        rd = r_spi(spi, add, 0x00);
        //Serial.println(rd);
        rd &= 0x0F;
        //Serial.println(rd);
    }
}
////////////////////////////////////////////////
//Charp Function End
////////////////////////////////////////////////


void setup() {
// USB Serila Setting
    Serial.begin(115200);

////////////////////////////////////////////////
//Pin Setting Start
////////////////////////////////////////////////
    pinMode(PDN, OUTPUT);
    pinMode(RSTN, OUTPUT);
    pinMode(EXEC, OUTPUT);
    digitalWrite(PDN, LOW);
    digitalWrite(RSTN, LOW);
    digitalWrite(EXEC, LOW);
////////////////////////////////////////////////
//Pin Setting End
////////////////////////////////////////////////

////////////////////////////////////////////////
//SPI Setting Start
////////////////////////////////////////////////
    //initialise two instances of the SPIClass attached to VSPI and HSPI respectively
    vspi = new SPIClass(VSPI);
    vspi->begin(VSPI_SCLK, VSPI_MISO, VSPI_MOSI, VSPI_SS); //SCLK, MISO, MOSI, SS
    //set up slave select pins as outputs as the Arduino API
    //doesn't handle automatically pulling SS low
    // pinMode(vspi->pinSS(), OUTPUT); //VSPI SS
    vspi -> setHwCs(true);
    vspi -> beginTransaction(mySPISettings);
////////////////////////////////////////////////
//SPI Setting End
////////////////////////////////////////////////

////////////////////////////////////////////////
//BLE Setting Start
////////////////////////////////////////////////
    // esp_ble_conn_update_params_t conn_params;
    // conn_params.latency = 0;
    // conn_params.max_int = 0x07; //*1.25ms = 7.5ms
    // conn_params.min_int = 0x06; //*1.25ms = 7.5ms
    // conn_params.timeout = 0x0A; //*10ms = 500ms
    // Serial.print("conn_params.latency:");
    // Serial.println(conn_params.latency);
    // Serial.print("conn_params.max_int:");
    // Serial.println(conn_params.max_int);
    // Serial.print("conn_params.min_int:");
    // Serial.println(conn_params.min_int);
    // Serial.print("conn_params.timeout:");
    // Serial.println(conn_params.timeout);
    // esp_ble_gap_update_conn_params(&conn_params);

  // Create the BLE Device
    BLEDevice::init("ESP32 UART Test");
    BLEDevice::setMTU(MTU_SIZE+3);//3=BLE Header size
  // Create the BLE Server
    pServer = BLEDevice::createServer();
    pServer->setCallbacks(new MyServerCallbacks());

  // Create the BLE Service
    BLEService *pService = pServer->createService(SERVICE_UUID);

  // Create a BLE Characteristic
    pCharacteristic = pService->createCharacteristic(
                CHARACTERISTIC_UUID_TX,
                BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
    );
    pCharacteristic->addDescriptor(new BLE2902());
    pCharacteristic->setCallbacks(new MyCallbacks());

    BLECharacteristic * pCharacteristic = pService->createCharacteristic(
                CHARACTERISTIC_UUID_RX,
                BLECharacteristic::PROPERTY_WRITE
    );

    pCharacteristic->setCallbacks(new MyCallbacks());

    uint8_t macBT[6];
    esp_read_mac(macBT, ESP_MAC_BT);
    Serial.printf("[Bluetooth] Mac Address = %02X:%02X:%02X:%02X:%02X:%02X\r\n", macBT[0], macBT[1], macBT[2], macBT[3], macBT[4], macBT[5]);
    // Start the service
    pService->start();

    // Start advertising
    pServer->getAdvertising()->start();
    Serial.println("Waiting a client connection to notify...");
////////////////////////////////////////////////
//BLE Setting End
////////////////////////////////////////////////
}

void loop() {
    if (deviceConnected) {
        if (rxValue.length() > 0) {
            // Serial.println("Receive Data in loop");
            Serial.print("rxValuelength=");
            Serial.println(rxValue.length());
            for (int i = 0; i < rxValue.length(); i++){
                str_rx += rxValue[i];
            }
            rxValue = "";
            Serial.print("str_rx=");
            Serial.println(str_rx);
            // Serial.println(sizeof(str_rx));

            int int_rx[8];
            int cmdnum;
            char txString[8];
            // String txString_temp;
            // String txString_buf;
            // char txString_all[MTU_SIZE];
            uint8_t rd_buf [512];
            cmdnum = stringToIntValues( str_rx, int_rx, ',');
            // Serial.print("cmdnum=");
            // Serial.println(cmdnum);

            switch(int_rx[0]){
                case W_DAT:
                    w_spi(vspi, int_rx[1], int_rx[2]);
                    break;
                case R_DAT:
                    //Serial.print("vspi=");
                    //Serial.println(vspi);
                    rd_buf[0] = r_spi(vspi, int_rx[1], 0x00);
                    txValue = float(rd_buf[0]);
                    //pCharacteristic->setValue(rd_buf[0], 1);
                    //pCharacteristic->setValue(rd_buf, 1);
                    pCharacteristic->setValue(&rd_buf[0], 1);
                    pCharacteristic->notify(); // Send the value to the app!
                    break;
                case R_PG:
                    for (int j = 0; j<128; j++){
                        rd_buf[j] = r_spi(vspi, 128+j, 0x00);
                        txValue = float(rd_buf[j]);
                    }
                    pCharacteristic->setValue(rd_buf, 128);
                    pCharacteristic->notify(); // Send the value to the app!
                    break;
                case PDN_CTRL:
                    pdn_ctrl(int_rx[1]);
                    break;
                case RSTN_CTRL:
                    rstn_ctrl(int_rx[1]);
                    break;
                case EXE_CTRL_ONLY:
                    exec_ctrl(int_rx[1]);
                    break;
                case EXE_CTRL:
                    flg_exec = exec_ctrl(int_rx[1]);
                    if (flg_exec == 1){
                        while (deviceConnected && rxValue.length() == 0){
                            t_st = millis();
                            //wait_state(vspi, 0x08, 0x0F);//Wait STBY
                            //wait_state(vspi, 0x08, 0x0F);//Wait TRX
                            //wait_state(vspi, 0x09, 0x0F);//Wait RPU_DONE
                            //wait_state(vspi, 0x88, 0x03);//Wait STBY
                            //Serial.println("STBY state");
                            //wait_state(vspi, 0x88, 0x04);//Wait TRX
                            //Serial.println("TRX state");
                            wait_state(vspi, 0x89, 0x0C);//Wait RPU_DONE
                            //wait_state(vspi, 0x89, 0x07);//Wait RCFAR_DONE
                            //Serial.println("RCFAR_DONE");
                            // st = millis();
                            //w_spi(vspi, 0x02, 0x03);//To Page 3 "Not access to 0x02 since ECC error(bug) is detected "
                            w_spi(vspi, 0x0A, 0x10);//TGTLST_HOLD
                            w_spi(vspi, 0x0A, 0x11);//SEQRD_ST
                            for (int i = 0; i<int_rx[3]; i++){
                                delayMicroseconds(5000);
                                for (int j = 0; j<int_rx[4+i]; j++){
                                    rddata_16b = r_spi_16b(vspi);
                                    txValue = float(rddata_16b);
                                    // randomSeed(analogRead(16)); //For Debug
                                    // rddata_16b = random(0, 65535); //For Debug
                                    rd_buf [2*j]     = rddata_16b;
                                    rd_buf [2*j+1] = rddata_16b >> 8;
                                }
                                pCharacteristic->setValue(rd_buf, 2*int_rx[4+i]);
                                pCharacteristic->notify(); // Send the value to the app!
                                // Serial.println(2*int_rx[4+i]);
                            }
                            //w_spi(vspi, 0x02, 0x03);//To Page 3 "Not access to 0x02 since ECC error(bug) is detected "
                            w_spi(vspi, 0x0A, 0x10);//TGTLST_HOLD
                            w_spi(vspi, 0x0A, 0x00);//TGTLST_UPDATE
                            t_sp = millis();
                            // Serial.println(t_sp-t_st);
                            while (t_sp-t_st < int_rx[2]){
                                t_sp = millis();
                                // Serial.println(t_sp-t_st);
                                // delay(1);
                            }
                            Serial.print(t_sp-t_st);
                            Serial.println("msec");
                        }
                    }
                    else{
                        Serial.println("Finish TargetList Read");
                    }
                    break;
                case FFT_CAPT:
                    for(int tag = 0; tag<16; tag++){
                        w_spi(vspi, 29, tag);//0x1D(d'29)にtagを書く(tag選択)
                        for (int i = 0; i<int_rx[1]; i++){//int_rx[1]=tagあたりの読み出す回数(510byte(=85bin)/回) ※1binあたり6byteのため
                            for (int j = 0; j<(int_rx[2+i]/6); j++){//int_rx[2]=1回目の読み出しバイト数(例:510),int_rx[3]=2回目の読み出しバイト数(例:258) [510+258]/6=128bin
                                w_spi(vspi, 30, j+(i*85));//0x1E(d'30)に0~41を書く(bin0からbin41までの計42binを読む)
                                for (int k = 31; k<34; k++){//0x1F(d'31)~0x21(d'33)を読んで(j=0のときは)rd_buf[0]~rd_buf[2]に格納(Iデータ)
                                    rd_buf[(k-31)+(j*6)] = r_spi(vspi, 128+k, 0x00);
                                    txValue = float(rd_buf[(k-31)+(j*6)]);
                                }
                                for (int k = 34; k<37; k++){//0x22(d'34)~0x24(d'36)を読んで(j=0のときは)rd_buf[3]~rd_buf[5]に格納(Qデータ)
                                    rd_buf[(k-31)+(j*6)] = r_spi(vspi, 128+k, 0x00);
                                    txValue = float(rd_buf[(k-31)+(j*6)]);
                                }
                            }
                            pCharacteristic->setValue(rd_buf, int_rx[2+i]);
                            pCharacteristic->notify(); // Send the value to the app!
                        }
                    }
                    break;
                case FFT_EXEC:
                    flg_exec = exec_ctrl(int_rx[1]);
                    //delay(500);
                    if (flg_exec == 1){
                        while (deviceConnected && rxValue.length() == 0){
                            //delay(100);
                            t_st = millis();
                            //wait_state(vspi, 0x88, 0x03);//Wait STBY
                            //Serial.println("STBY state");
                            //wait_state(vspi, 0x88, 0x04);//Wait TRX
                            //Serial.println("TRX state");
                            wait_state(vspi, 0x89, 0x02);//Wait RFFT_DONE
                            //wait_state(vspi, 0x89, 0x0C);//Wait RPU_DONE
                            ////wait_state(vspi, 0x89, 0x07);//Wait RCFAR_DONE
                            //Serial.println("RCFAR_DONE");
                            // st = millis();
                            //w_spi(vspi, 0x02, 0x03);//To Page 3 "Not access to 0x02 since ECC error(bug) is detected "
                            w_spi(vspi, 0x0A, 0x10);//TGTLST_HOLD

                            for(int tag = 0; tag<16; tag++){
                                w_spi(vspi, 29, tag);//0x1D(d'29)にtagを書く(tag選択)
                                for (int i = 0; i<int_rx[3]; i++){//int_rx[3]=tagあたりの読み出す回数(510byte(=85bin)/回) ※1binあたり6byteのため
                                    delayMicroseconds(5000);
                                    for (int j = 0; j<(int_rx[4+i]/6); j++){//int_rx[4]=1回目の読み出しバイト数(例:510),int_rx[5]=2回目の読み出しバイト数(例:258) [510+258]/6=128bin
                                        w_spi(vspi, 30, j+(i*85));//0x1E(d'30)でbinを指定する。0 to 84 and 0(85) to 42(127)  , 510/6=85,  258/6=43
                                        for (int k = 31; k<34; k++){//0x1F(d'31)~0x21(d'33)を読んで(j=0のときは)rd_buf[0]~rd_buf[2]に格納(Iデータ)
                                            rd_buf[(k-31)+(j*6)] = r_spi(vspi, 128+k, 0x00);
                                            //txValue = float(rd_buf[(k-31)+(j*6)]);
                                            //if(k==32){Serial.println(txValue);}
                                        }
                                        for (int k = 34; k<37; k++){//0x22(d'34)~0x24(d'36)を読んで(j=0のときは)rd_buf[3]~rd_buf[5]に格納(Qデータ)
                                            rd_buf[(k-31)+(j*6)] = r_spi(vspi, 128+k, 0x00);
                                            //txValue = float(rd_buf[(k-31)+(j*6)]);
                                        }
                                    }
                                    int getArrayLength = sizeof(rd_buf);
                                    Serial.print("rd_buf= ");
                                    Serial.print(int_rx[4+i]);
                                    Serial.print(" / ");
                                    Serial.print(getArrayLength);
                                    Serial.println(" byte");
                                    pCharacteristic->setValue(rd_buf, int_rx[4+i]);
                                    pCharacteristic->notify(); // Send the value to the app!
                                }
                            }
                            //w_spi(vspi, 0x02, 0x03);//To Page 3 "Not access to 0x02 since ECC error(bug) is detected "
                            //w_spi(vspi, 0x0A, 0x10);//TGTLST_HOLD
                            w_spi(vspi, 0x0A, 0x00);//TGTLST_UPDATE
                            t_sp = millis();
                            // Serial.println(t_sp-t_st);
                            while (t_sp-t_st < int_rx[2]){
                                t_sp = millis();
                                // Serial.println(t_sp-t_st);
                                // delay(1);
                            }
                            //Serial.print(t_sp-t_st);
                            //Serial.println("msec");
                        }
                    }
                    else{
                        Serial.println("Finish FFT Capture");
                    }
                default:
                    rx_buf = int_rx[0];
            }
        // str_rx = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0";
        // cmdnum = stringToIntValues( str_rx, int_rx, ',');
        int_rx[8] = {0};
        str_rx = "";
        txValue = 0;
        }
    }

    // disconnecting
    if (!deviceConnected && oldDeviceConnected) {
        delay(500); // give the bluetooth stack the chance to get things ready
        pServer->startAdvertising(); // restart advertising
        Serial.println("restart advertising");
        oldDeviceConnected = deviceConnected;
    }
    // connecting
    if (deviceConnected && !oldDeviceConnected) {
		// do stuff here on connecting
        oldDeviceConnected = deviceConnected;
    }
}

int stringToIntValues(String str, int value[], char delim) {
    int k = 0;
    int j = 0;
    char text[8];

    for (int i = 0; i <= str.length(); i++) {
        char c = str.charAt(i);
        if ( c == delim || i == str.length() ) {
            text[k] = '\0';
            value[j] = atoi(text);
            j++;
            k = 0;
            // Serial.print("func j=");
            // Serial.println(j);
        } else {
            text[k] = c;
            k++;
        }
    }
    return j;
}
