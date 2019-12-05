int heater = 7;

int Pot = 0;
int R=10000;
int Setpoint = 30;



void setup() {

  // put your setup code here, to run once:

    pinMode(Pot, INPUT);

    pinMode(heater, OUTPUT);

    Serial.begin(9600);



}

void loop() {

  // put your main code here, to run repeatedly:

   int Pot = analogRead(A4) ;
    Serial.println("pot reading");
    Serial.println(Pot);
   float resistance=(Pot*R)/(1023-Pot);
    Serial.println("Resistance reading");
    Serial.println(resistance);
   float T=-0.0027*resistance+52;
    Serial.println("Temperature reading");
    Serial.println(T);
    if(T < Setpoint+0.5){

            digitalWrite(heater, HIGH);
    }
    else if(T > Setpoint+0.5){

        digitalWrite(heater, LOW);

    }
    else if(Setpoint-0.5 < T < Setpoint+0.5){

            digitalWrite(heater, LOW);

        }

    delay(1000);

}
