#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main (void)
{
    // if (Serial.available() > 0 and Serial.read(1) == '<')
    // {
        char input_string[]= "ph,1.5";
        char delim[]= ",";
        char* ptr = strtok(input_string, delim);
        printf("%s\n", ptr);
        char* ptr2 = strtok(NULL, delim);
        printf("%s\n", ptr2);
        double val = atof(ptr2);

        printf("%lf\n", val+1);

    // } 
}
