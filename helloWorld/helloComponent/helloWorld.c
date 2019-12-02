#include "legato.h"

#include"interfaces.h"

#include <stdlib.h>
#include <stdio.h>

const char ch1[]="EXT_ADC1";
//le_result_t le_pos_Get3DLocation();
void itoa(int value, char*result,int radix,int size_of_result){
    char *p;
    char *firstdig;
    char temp;
    p = result;
    firstdig = p;
    for(int i=0;i<size_of_result;i++){
        if(value>0){
            *p++ =(char) (value%radix);
            value = value/radix;
        }
        else{
            *p++ = (char)(0);
        }
    }
   *p-- = '\0';
    //Invers the chaine of character.
   do{
        temp = *p;
        *p = *firstdig;
        *firstdig = temp;
        p--;
        firstdig++;
    }while(firstdig < p);
}
COMPONENT_INIT
{
	int value;
	int latitudeReading;
	int longitudeReading;
	int hAccuracyReading;
	int altitudeReading;
	int vAccuracyReading;
	puts("Hello, world.");
	le_adc_ReadValue(ch1,&value) ;
	char binbuf[12];
	itoa(value,binbuf,2,sizeof(binbuf));
	for(int i=0;i<sizeof(binbuf);i++){
	  LE_INFO("%d",binbuf[i]);
	}
	le_result_t posRes = le_pos_Get3DLocation(
        &latitudeReading,
        &longitudeReading,
        &hAccuracyReading,
        &altitudeReading,
        &vAccuracyReading);
	if (posRes == LE_OK){
	  latitudeReading = latitudeReading/1000000.0;
	  longitudeReading = longitudeReading/1000000.0;
	}
	LE_INFO("The value of lightSensor = %d",value);
	LE_INFO("The value of latitude = %d",latitudeReading);
	LE_INFO("The value of longitude = %d",longitudeReading);
}
