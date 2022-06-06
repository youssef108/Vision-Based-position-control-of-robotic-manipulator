
String cmd;
// Include the AccelStepper library:
#include <AccelStepper.h>
#include <MultiStepper.h>


// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver:
//base
#define dirPin_b 2
#define stepPin_b 3
#define motorInterfaceType 1
////Joint12
#define dirPin_12 12
#define stepPin_12 13
//joint 1
#define dirPin_1 10
#define stepPin_1 11
//joint 2
#define dirPin_2 8
#define stepPin_2 9
//joint 3
#define dirPin_3 4
#define stepPin_3 5


// Create a new instance of the AccelStepper class:
 //Create a new instance of the AccelStepper class:
AccelStepper stepperbase = AccelStepper(motorInterfaceType, stepPin_b, dirPin_b);
AccelStepper stepper12 = AccelStepper(motorInterfaceType, stepPin_12, dirPin_12);
AccelStepper stepper1 = AccelStepper(motorInterfaceType, stepPin_1, dirPin_1);
AccelStepper stepper2 = AccelStepper(motorInterfaceType, stepPin_2, dirPin_2);
AccelStepper stepper3 = AccelStepper(motorInterfaceType, stepPin_3, dirPin_3);
MultiStepper steppers;

String joint_step2[5];
int joint_status = 0;
int Done=0;
void split(String msg){
    int i=0;
    int j=0;
    String temp="";
  while ( j<msg.length()) {
    
    if (msg.charAt(j)==',') {
      joint_step2[i]=temp;
      temp="";
      i++;
    }
    else {
      temp=temp+msg.charAt(j);
      }
       j++;
    }
   joint_step2[msg.length()-1]=temp;
 
}

void setup() {
  Serial.begin(115200);
   // Configure each stepper
   stepperbase.setMaxSpeed(1700);
  stepper12.setMaxSpeed(500);
  stepper1.setMaxSpeed(500);
  stepper2.setMaxSpeed(2500);
  stepper3.setMaxSpeed(500); 
  // Then give them to MultiStepper to manage
  steppers.addStepper(stepperbase);
  steppers.addStepper(stepper12);
  steppers.addStepper(stepper1);
  steppers.addStepper(stepper2);
  steppers.addStepper(stepper3);
}

void loop() {
  while(Serial.available()==0){
  }
  cmd=Serial.readStringUntil('\r');Serial.flush();

  //if (joint_status == 1) // If command callback (arm_cb) is being called, execute stepper command
    split(cmd);
    long positions[5]={0,0,0,0,0};  // Array of desired stepper positions must be long
//    positions[0] = joint_step2[0].toInt(); 
    //positions[1] = joint_step2[1].toInt(); 
    //positions[2] = joint_step2[2].toInt(); 
//    positions[3] = joint_step2[3].toInt(); 
    positions[4] = joint_step2[4].toInt(); 
//   stepper3.move(joint_step2[4].toInt());
//   stepper3.run();
    steppers.moveTo(positions);
    //nh.spinOnce();
    steppers.runSpeedToPosition();// Blocks until all are in position
    
   
    Serial.print(positions[0]);
    Serial.print(" ");
     Serial.print(positions[1]);
    Serial.print(" ");
     Serial.print(positions[2]);
    Serial.print(" ");
     Serial.print(positions[3]);
    Serial.print(" ");
     Serial.println(positions[4]);
     //Serial.println("Done");
            
  joint_status = 0;
  delay(1);
  
}
