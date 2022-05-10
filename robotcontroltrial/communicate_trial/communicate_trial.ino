String Ary[5];
int z;
String cmd;
void split(String msg){
  int i=0;
  int j=0;
  String temp="";
while ( j<msg.length()) {
  
  if (msg.charAt(j)==',') {
    Ary[i]=temp;
    temp="";
    i++;
  }
  else {
    temp=temp+msg.charAt(j);
    }
     j++;
  }
 Ary[msg.length()-1]=temp;
 
}
int GetValue(String pstring){
  char vtemp[10];
  pstring.toCharArray(vtemp,sizeof(vtemp));
  return atof(vtemp);
}
void setup(){
  Serial.begin(115200);
  
}
void loop(){
//  x=1;
//  y=2;
//  z=y+x;
//  Serial.print(x);  
//Serial.print(',');
//Serial.print(y);
//Serial.print(',');
//Serial.println(z);
//delay(1000);
while(Serial.available()==0){
}
cmd=Serial.readStringUntil('\r');Serial.flush();
split(cmd);
Serial.flush();
//Serial.print((Ary[0]));Serial.print(" ");
//Serial.print((Ary[1]));Serial.print(" ");
//Serial.print((Ary[2]));Serial.print(" ");
//Serial.print((Ary[3]));Serial.print(" ");
//Serial.println(Ary[4]);Serial.print(" ");
Serial.println(cmd);

}
