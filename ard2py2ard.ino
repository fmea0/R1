//DECLARACION MOTORES Y ULTRASONIDO
// Motor1 Banda 
#define motor10 3
#define motor11 1
#define motor12 2
// Motor posicionador
#define motor20 6
#define motor21 4
#define motor22 5
//Motor rechazador
#define motor30 9
#define motor31 7
#define motor32 8
//Ultrasonido
#define trigger 12
#define echo    13
//Declaracion de variables
int velBanda;
int velSel;
int counter = 0;
long duracion;
long cm;
bool bandera = false;
char clase;
int pos = 99;

void setup ()
{
  //SERIAL
  Serial.begin(9600);
  //MOTOR1
  pinMode(motor10, OUTPUT);
  pinMode(motor11, OUTPUT);
  pinMode(motor12, OUTPUT);
  velBanda = 140;
  //MOTOR2
  pinMode(motor20, OUTPUT);
  pinMode(motor21, OUTPUT);
  pinMode(motor22, OUTPUT);
  //velSel = 130;
  //ULTRASONIDO
  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT);
  //
}
void loop(){
  //activarBanda();
  //pararBanda();
  ultrasonido();
  pararSel();
  Serial.println(bandera);
  Serial.println(cm);
  if(pos == 99){
    iniciarBandeja();
  }
  
  if(cm>5){activarBanda();}
  else{
    pararBanda();
    delay(3000);
    bandera = true;
    delay(5000);
  }
if(bandera){Serial.println('8');}//envia un 1 a python

 
if(Serial.available()>0){
  clase = Serial.read();// recibe un byte
  switch(clase){
    case '1':
    // enviar a lugar 1
    bandpos(1);
    activarBanda();
    delay(5000);
    bandera = false;
          
    delay(300);
    break;
    case '2':
    // enviar a lugar 2
    bandpos(2);
    activarBanda();
    delay(5000);
    bandera = false;
    
    delay(300);
    break;
    case '3':
    // enviar a lugar 3
    bandpos(3);
    activarBanda();
    delay(5000);
    bandera = false;
    delay(300);
    break;
    case '4':
    // enviar a lugar 4
    bandpos(4);
    activarBanda();
    delay(5000);
    bandera = false;
    delay(300);
    break;
    default:
    //dejar correr y patearle con motor de arriba
     
    delay(300);
    break;
    }
   }
}
void activarBanda(){
  digitalWrite(motor11, HIGH);
  digitalWrite(motor12, LOW);
  analogWrite(motor10, velBanda);
}
void pararBanda(){
  digitalWrite(motor11, LOW);
  digitalWrite(motor12, LOW);
  analogWrite(motor10, velBanda);
}
void ultrasonido(){
  //analogWrite(cincov, 255);
  digitalWrite(trigger, LOW);
  //long duracion, cm;

  //Pulso de 10 us
  //digitalWrite(12, HIGH);
  digitalWrite(trigger, HIGH);
  delayMicroseconds(10);
  //digitalWrite(12,LOW);
  digitalWrite(trigger, LOW);
  duracion = pulseIn(echo, HIGH); //Longitud del pulso en 11 en us

  //Convierte el tiempo de recepcion del eco en distancia
  cm = duracion/58;

  //Imprime valores
  //Serial.print(cm);
  //Serial.println(" cm");
  //Serial.print(duracion);
  //Serial.println(" echo");
  delay(50);
}
void movAsc(int vel){
  digitalWrite(motor21, HIGH);
  digitalWrite(motor22, LOW);
  analogWrite(motor20, vel);
}
void movDesc(int vel){
  digitalWrite(motor21, LOW);
  digitalWrite(motor22, HIGH);
  analogWrite(motor20, vel);
}
void iniciarBandeja(){
  movDesc(255);
    delay(600);
    pos = 0;
}
void pararSel(){
  digitalWrite(motor21, LOW);
  digitalWrite(motor22, LOW);
}
void bandeja01(){
    //Posicion1
    movAsc(140);
    delay(3300);
    pos = 1;
    pararSel();
    //delay(5000);
}

void bandeja12(){
    //Posicion2
    movAsc(140);
    delay(3000);
    pararSel();
    //delay(5000);
    pos = 2;
}
void bandeja23(){
    //Posicion3
    movAsc(140);
    delay(3000);
    pararSel();
    //delay(5000);
    pos = 3;
}
void bandeja34(){
  //Posicion4
    movAsc(140);
    delay(3000);
    pararSel();
    //delay(5000);
    pos = 4;    
}
void bandeja43(){
    //Posicion3
    movDesc(140);
    delay(2500);
    pararSel();
    //delay(5000);
    pos = 3; 
}
void bandeja32(){
    //Posicion2
    movDesc(140);
    delay(2500);
    pararSel();
    //delay(5000);
    pos = 2;
}
void bandeja21(){
    //Posicion1
    movDesc(140);
    delay(2500);
    pararSel();
    //delay(5000);
    pos = 1;  
}
void bandpos(int posi){
  if(posi == 1){
      if(pos == 0){
        bandeja01();
      }else if(pos == 2){
        bandeja21();
      }else if(pos == 3){
        bandeja32();
        bandeja21();
      }else if(pos == 4){
        bandeja43();
        bandeja32();
        bandeja21();
      }
  }else if(posi == 2){
      if(pos == 0){
        bandeja01();
        bandeja12();
      }else if(pos == 1){
        bandeja12();
      }else if(pos == 3){
        bandeja32();
      }else if(pos == 4){
        bandeja43();
        bandeja32();
      }
  }else if(posi == 3){
      if(pos == 0){
        bandeja01();
        bandeja12();
        bandeja23();
      }else if(pos == 1){
        bandeja12();
        bandeja23();
      }else if(pos == 2){
        bandeja23();
      }else if(pos == 4){
        bandeja43();
      }
  }else if(posi == 4){
      if(pos == 0){
        bandeja01();
        bandeja12();
        bandeja23();
        bandeja34();
      }else if(pos == 1){
        bandeja12();
        bandeja23();
        bandeja34();
      }else if(pos == 2){
        bandeja23();
        bandeja34();
      }else if(pos == 3){
        bandeja34();
      }
  }
}
