int heater = 7;
int Pot = 0;
int R = 10000;
int Setpoint = 30;

void setup()
{
    pinMode(Pot, INPUT);
    pinMode(heater, OUTPUT);
    Serial.begin(9600);
}

void loop()
{
    int Pot = analogRead(A4) ;
    float resistance=(Pot*R)/(1023-Pot);
    float T=-0.0027*resistance+52;
    Serial.print("<temperature,");
    Serial.print(T);
    Serial.println(">");
    
    if(T < Setpoint+0.5)
        digitalWrite(heater, HIGH);
    
    else if(T > Setpoint+0.5)
        digitalWrite(heater, LOW);
    
    else if(Setpoint-0.5 < T < Setpoint+0.5)
        digitalWrite(heater, LOW);
    
    if (Serial.available() > 0 && Serial.read() == '<')
    {
        char input[25];
        int charsRead = Serial.readBytesUntil('>', input, 25);
        input[charsRead] = '\0';
        char* subsystem = strtok(input, ",");
        char* ptr2 = strtok(NULL, ",");
        Serial.print(ptr);
        Serial.print(" ");
        Serial.println(ptr2);
        double val = atof(ptr2);
        
        if (val != Setpoint)
            Setpoint = val;
    }
    delay(200);
}
