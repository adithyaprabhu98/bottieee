#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define MIN_PULSE_WIDTH       650
#define MAX_PULSE_WIDTH       2350
#define DEFAULT_PULSE_WIDTH   1500
#define FREQUENCY             50
// our servo # counter
uint8_t servonum = 0;
int a = 120;
int b = 60;
int de = 250;

String pos = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
int t1=90,t2=90,t3=90,t4=90,t5=90,t6=90,t7=90,t8=90;


void setup() {
  // initialize serial:
  Serial.begin(115200);
  // reserve 200 bytes for the pos:
  pos.reserve(200);
  pwm.begin();
  pwm.setPWMFreq(FREQUENCY);
}

void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {
    //Serial.print(pos);
    t1 = getValue(pos,',',0).toInt(); 
    t2 = getValue(pos,',',1).toInt();
    t3 = getValue(pos,',',2).toInt(); 
    t4 = getValue(pos,',',3).toInt();
    t5 = getValue(pos,',',4).toInt(); 
    t6 = getValue(pos,',',5).toInt();
    t7 = getValue(pos,',',6).toInt(); 
    t8 = getValue(pos,',',7).toInt();
    // clear the string:
    pos = "";
    stringComplete = false;
    Serial.print(t1); Serial.print(',');
    Serial.print(t2); Serial.print(',');
    Serial.print(t3); Serial.print(',');
    Serial.print(t4); Serial.print(',');
    Serial.print(t5); Serial.print(',');
    Serial.print(t6); Serial.print(',');
    Serial.print(t7); Serial.print(',');
    Serial.println(t8);
  }
/*  pwm.setPWM(0, 0, pulseWidth(t1));
  delay(5);
  pwm.setPWM(1, 0, pulseWidth(t2));
  delay(5);
  pwm.setPWM(2, 0, pulseWidth(t3));
  delay(5);
  pwm.setPWM(3, 0, pulseWidth(t4));
  delay(5);
  pwm.setPWM(4, 0, pulseWidth(t5));
  delay(5);
  pwm.setPWM(5, 0, pulseWidth(t6));
  delay(5);
  pwm.setPWM(6, 0, pulseWidth(t7));
  delay(5);
  pwm.setPWM(7, 0, pulseWidth(t8));
  delay(5);
*/  
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the pos:
    pos += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    } 
  }
}

String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

int pulseWidth(int angle)
{
  int pulse_wide, analog_value;
  pulse_wide   = map(angle, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
  analog_value = int(float(pulse_wide) / 1000000 * FREQUENCY * 4096);
  //Serial.println(analog_value);
  return analog_value;
}
