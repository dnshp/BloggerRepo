#include <Servo.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_LSM9DS1.h>
#include <Adafruit_Sensor.h>
#include <math.h>

// The points at which the horn is perfectly vertical for each motor, determined experimentally
#define aZero 80
#define bZero 85
#define cZero 90
#define dZero 80
// Constants for matrix multiplication. See http://dineshparimi.blogspot.com/2017/05/attitude-and-spin-control-of-rocket.html.
#define n1 0.5
#define n2 0.5

Servo A; Servo B; Servo C; Servo D;
Adafruit_LSM9DS1 lsm = Adafruit_LSM9DS1();
int x; int y; int w;

void setup() {
  A.attach(14);
  A.write(aZero);
  B.attach(15);
  B.write(bZero);
  C.attach(16);
  C.write(cZero);
  D.attach(17);
  D.write(dZero);

  Serial.begin(115200);
  Serial.println("Initializing");

  delay(1000);

  lsm.begin();
  lsm.setupAccel(lsm.LSM9DS1_ACCELRANGE_16G);
  lsm.setupMag(lsm.LSM9DS1_MAGGAIN_16GAUSS);
  lsm.setupGyro(lsm.LSM9DS1_GYROSCALE_2000DPS);
  Serial.println("Setup complete");
} 

void loop() {
  Serial.println("Looping");
  sensors_event_t accel, mag, gyro, temp;
  lsm.getEvent(&accel, &mag, &gyro, &temp);
  printSensorReadings(accel, gyro);
  x = asin(accel.acceleration.x / 9.81) * 180 / M_PI;
  y = asin(accel.acceleration.y / 9.81) * 180 / M_PI;
  w = gyro.gyro.z / 36;
  Serial.print("X: ");
  Serial.println(x);
  Serial.print("Y: ");
  Serial.println(y);
  Serial.print("W: ");
  Serial.println(w);
  int *angles;
  angles = getAngles(x, y, w);
  A.write(aZero + angles[0]);
  B.write(bZero + angles[1]);
  C.write(cZero + angles[2]);
  D.write(dZero + angles[3]);
  delay(250);
}

int * getAngles(int x, int y, int w) {
  int *rv = new int[4];
  rv[0] = (-n1 * x) + (n2 * w);
  rv[1] = (-n1 * y) + (n2 * w);
  rv[2] = (n1 * x) + (n2 * w);
  rv[3] = (n1 * y) + (n2 * w);
  return rv;
}

void printSensorReadings(sensors_event_t a, sensors_event_t g) {
  Serial.print("Accel X: "); Serial.print(a.acceleration.x); Serial.print(" m/s^2");
  Serial.print("\tY: "); Serial.print(a.acceleration.y);     Serial.print(" m/s^2 ");
  Serial.print("\tZ: "); Serial.print(a.acceleration.z);     Serial.println(" m/s^2 ");

  Serial.print("Gyro X: "); Serial.print(g.gyro.x);   Serial.print(" dps");
  Serial.print("\tY: "); Serial.print(g.gyro.y);      Serial.print(" dps");
  Serial.print("\tZ: "); Serial.print(g.gyro.z);      Serial.println(" dps");

  Serial.println();
}

