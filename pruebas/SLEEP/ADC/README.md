Documentacion ADC con el modo SLEEP

En el ESP32-C6, el ADC no puede usarse como fuente de reinicio o �wake-up� porque pertenece al dominio anal�gico del chip, el cual se 
desactiva completamente durante los modos de sue�o (light sleep o deep sleep) para reducir el consumo de energ�a.

Esto implica que el ADC no conserva su referencia, ni puede realizar conversiones o generar interrupciones mientras el microcontrolador est� dormido.

Cuando el ESP32-C6 �despierta� del modo de sue�o (light sleep o deep sleep) y observas que el pin ADC parece ponerse en alto, en realidad 
no es el ADC �poni�ndolo en alto�, sino un efecto secundario del proceso de reinicializaci�n del pin.

El pin del ADC del ESP32-C6 parece ponerse en alto al �despertar� porque el sistema lo inicializa moment�neamente como una entrada 
digital con resistencia de pull-up, no porque el ADC genere un nivel alto; eso es propio de "despertar".

