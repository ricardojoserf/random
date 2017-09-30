#!/bin/sh


echo "Introduca un número (1, 2 o 3) 
		\n 1: Opción 1 
		\n 2: Opción 2 
		\n 3: Opción 3"

read opt	

if [ $opt = "1" ]; then
   	echo 'Escenario básico'

elif [ $opt = "2" ]; then
	echo 'Escenario avanzado'

elif [ $opt = "3" ]; then
	echo 'Destruyendo escenario...'

else
	echo 'Introduzca 1, 2 o 3'

fi