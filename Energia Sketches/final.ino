
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

void setup() {
    pinMode(acid_LED, OUTPUT); //pH setup
    pinMode(base_LED, OUTPUT);
    pinMode(pHpin, INPUT);
    Serial.begin(9600);

    pinMode(Pot, INPUT); //temperature setup
    pinMode(heater, OUTPUT);
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
    read_pH();
    read_temperature();
    read_speed();

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

