#include <SparkFun_TB6612.h>

#define UP_KEY 273
#define DOWN_KEY 274
#define LEFT_KEY 276
#define RIGHT_KEY 275

#define AIN1 4
#define BIN1 5
#define AIN2 2
#define BIN2 10
#define PWMA 3
#define PWMB 9
#define STBY 6

const int offsetA = 1;
const int offsetB = 1;

Motor leftMotor = Motor(AIN1, AIN2, PWMA, offsetA, STBY);
Motor rightMotor = Motor(BIN1, BIN2, PWMB, offsetB, STBY);

bool _forward, _backward, _left, _right;
int speed = 255;

void setup() {
  Serial.begin(9600);
}

void updateMotors(){
  if(_forward){
    if(_left){  // forward-left
      leftMotor.drive(speed/2);
      rightMotor.drive(speed);
    }else if(_right){ // forward-right
      leftMotor.drive(speed);
      rightMotor.drive(speed/2);
    }else{  // just forward
      leftMotor.drive(speed);
      rightMotor.drive(speed);
    }
  }else if(_backward){
    if(_left){  // backward-left
      leftMotor.drive(-speed/2);
      rightMotor.drive(-speed);
    }else if(_right){ // backward-right
      leftMotor.drive(-speed);
      rightMotor.drive(-speed/2);
    }else{  // just backward
      leftMotor.drive(-speed);
      rightMotor.drive(-speed);
    }
  }else{
    if(_left){  // just left
      rightMotor.drive(speed);
      leftMotor.drive(-speed);
    }else if(_right){ // just right
      leftMotor.drive(speed);
      rightMotor.drive(-speed);
    }else{
      leftMotor.brake();
      rightMotor.brake();
    }
  }
}

// action will be either 'd' or 'u' for key down or key up
void handleInput(int key, char action){
  if(key == UP_KEY){
    if(action == 'd' && !_forward){
      _forward = true;
      _backward = false;
    }else if(action == 'u' && _forward){
      _forward = false;
    }
  }else if(key == DOWN_KEY){
    if(action == 'd' && !_backward){
      _backward = true;
      _forward = false;
    }else if(action == 'u' && _backward){
      _backward = false;
    }
  }else if(key == LEFT_KEY){
    if(action == 'd' && !_left){
      _left = true;
      _right = false;
    }else if(action == 'u' && _left){
      _left = false;
    }
  }else if(key == RIGHT_KEY){
    if(action == 'd' && !_right){
      _right = true;
      _left = false;
    }else if(action == 'u' && _right){
      _right = false;
    }
  }
  updateMotors();
}

void loop() {
  if(Serial.available()){
    String data = Serial.readStringUntil('\n');
    int separator = data.indexOf(',');
    int key = data.substring(0, separator).toInt();
    char action = data.charAt(separator+1);
    handleInput(key, action);
  }
}
