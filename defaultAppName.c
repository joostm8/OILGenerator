/**
* This is a template of C code generated by OILGenerator by Joost Mertens
* Generated on: 2018-06-25 15:44:03.058000
* Directions are given concerning which code should be executed on which locations
* The final mapping is still user dependent.
**/

/* Includes are placed here, commonly used includes are already listed */
#include "Arduino.h"
#include <stddef.h>
#include <stdio.h>
#include <avr/io.h

/* Include Matlab includes here */

#undef ISR //Remove AVR-GCC ISR version
extern "C"{
	#include "tpl_app_config.h"
	#include "tpl_os.h"
}

void setup(void){
/* Include all initialisations here */

}

TASK(TaskA){
/* Insert Input mapping code here */

/* Step the code executed by this TASK here */

/* Insert Output mapping here */

}

TASK(TaskB){
/* Insert Input mapping code here */

/* Step the code executed by this TASK here */

/* Insert Output mapping here */

}

TASK(TaskC_Trig){
/* Insert Input mapping code here */

/* Step the code executed by this TASK here */

/* Insert Output mapping here */

}

TASK(TaskD_Trig){
/* Insert Input mapping code here */

/* Step the code executed by this TASK here */

/* Insert Output mapping here */

}

ISR(External_CLK){
/* Insert Input mapping code here */

/* Step the code executed by this ISR here */

/* Insert Output mapping here */

}

ISR(PIN_ISR){
/* Insert Input mapping code here */

/* Step the code executed by this ISR here */

/* Insert Output mapping here */

}

/*
EOF
*/