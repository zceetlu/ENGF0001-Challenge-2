
int pHpin=A1; //pH vars
int acid_LED=39;
int base_LED=40;
float F=9.6485309e4;
float R=8.314510;
int T=290;
float V_supply=0.66;
float C=2.302585;
float pH;
float a;
float b;
float pHmin = 6.5;
float pHmax = 7.5;

int heater = 7; //temperature vars
int Pot = 0;
int R = 10000;
int Setpoint = 30; //should be 28-33
 
//stirring vars
int readCurrent = 35;//read Iout from photo-interrupter sq wave
int controlMotor = 32 ; //output PWM to motot
int Vcc1 = 40; // interupter
int Vcc2 = 39; // LED on interrupter
int GND1 = 18;
int GND2 = 17;

int motorSpeed = 255;
int recordTime =0;
int recordRotation=0;
int lastCurrent = 0;
int newCurrent=0;

int lowerRange = 200; // brm lower range for the motor = 600
int upperRange = 1000; // brm upper range for the motor = 620

void setup() {
    pinMode(acid_LED, OUTPUT); //pH setup
    pinMode(base_LED, OUTPUT);
    pinMode(pHpin, INPUT);

    pinMode(Pot, INPUT); //temperature setup
    pinMode(heater, OUTPUT);
    
    pinMode(readCurrent,INPUT); //stirring setup
    pinMode(controlMotor,OUTPUT);
    pinMode(Vcc1,OUTPUT);
    pinMode(Vcc2,OUTPUT);
    pinMode(GND1,OUTPUT);
    pinMode(GND2,OUTPUT);
    Serial.begin(9600);
}

void update_variables() {
    if (Serial.available() > 0 && Serial.read() == '<')
    {
        char input[25];
        int charsRead = Serial.readBytesUntil('>', input, 25);
        input[charsRead] = '\0';
        char* subsystem = strtok(input, ",");
        char* ptr2 = strtok(NULL, ",");
        double value = atof(ptr2);
        if (strcmp("pH", subsystem)==1) {
            pH = value;
        }
        else if (strcmp("temperature", subsystem)==1) {
            temperature = value;
        }
        else if (strcmp("speed", subsystem)==1) {
            motorspeed = value;
        }
    }
    delay(200);
}

void read_pH()
{
    float V_pot = analogRead(A1);
     //float t=((T-298)*0.000198+0.05916)*7;
    float V = V_pot*3.3/1012.0;      //used for test board

    //read pH value from UI if available here
    float pH = 7.0+((F*(V_supply-V))/(R*T*C));

         if (pH < pHmin) {
               digitalWrite(base_LED, HIGH);
               digitalWrite(acid_LED, LOW);
           }
           if (pH > pHmax) {
               digitalWrite(base_LED, LOW);
               digitalWrite(acid_LED, HIGH);
               Serial.print("<pH,");
               Serial.println(pH);
           }
           else {
               digitalWrite(acid_LED, LOW);
               digitalWrite(base_LED, LOW);
           }
}

void read_temperature()
{}

void read_speed()
{}

void loop() {
    if (Serial.available() > 0) {
        update_variables();
    }
    else {
        read_pH();
        read_temperature();
        read_speed();
    }

    Serial.print("<pH,");
    Serial.print(pH);
    Serial.println(">");
    delay(200);
    Serial.print("<temperature,");
    Serial.print(temperature);
    Serial.println(">");
    delay(200);
    Serial.print("<speed,");
    Serial.print(speed);
    Serial.println(">");
    delay(200);
}

