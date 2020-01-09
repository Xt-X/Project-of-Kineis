# Projet MangOH-Kinéis

This repository host one of our project developped at INSA Toulouse (2019/2020) as part of our IT formation. This project was developped in coordination with the Kinéis company.

## Brief summary

This project aims to developp an embedded application (on a MangOH card) which is able to switch from the cellular network (5G) to the Kinéis's satellite network (Argos) when the first one is unavailable. The card embed a lot of sensors (see below [Formatting](#Formatting)), and these sensors datas have to be transfered via the prefered network (5G/Satellite). 
Once these datas have been transfered, their endpoint is either :  

* AirVantage if transfered via the cellular connection
* Argos if transfered via the satellite connection

We have developped a django application which is responsible of fetching the sensor's data from either AirVantage or Argos and displaying the data for the user.  
We use the Rest API to fetch the data from the Airvantage platform, and a SOAP API to fetch the data from the Argos platform.  
These data are then processed and merged, and displayed in the end-user's browser via the Plotly JavaScript library.

[Example graph](https://i.imgur.com/yJdARFt.png)

# How to start the server

The webserver uses Django in back-end and jQuery,Bootstrap and Plotly in front-end. You therefore need to have Python 3 installed. Once python is installed, run :

	pip install Django zeep requests

`requests` is used to make rest request to Airvantage, and `zeep` to make SOAP request to Argos. 


# Formatting of satellite data

The sensors data sent via the satellite link are completly raw. We designed a payload format according to the precision of each sensors and the maximum available size of a payload inside a single Argos transmission.

	Light(12)|Pressure(10)|Temperature(14)|Accelerometer(16x3)|Gyroscope(16x3)|CRC(16) = 148 bits

Light : 0 to 3000 lumens : 12 bits full precision  
Pressure : 950 to 1050 hPa +/- 0.12 hPa = 833 values : 10 bits  full precision  
Temperature : -40 to 85°C +/- 0.01°C = = 12 500 values : 14 bits full precision  
Accelerometer : 16 bits per axis for resolution. The measurement range depends on the sensitivy selected.  

* -2/2 g : precision of 0,000061 g/bits (16384 bit/g)
* -16/16 g : precision of ~0,000488 g/bits (less precise) (2048 bit/g)

Gyro : 16 bits per axis as well. 
* 125 °/s : precision of ~0,00381 °/s/bits (16.4 bit/°/s)
* 2000 °/s : precision of ~0,0609 °/s/bits (less precise) (262.4 bit/°/s)

*NB : By bit, we need to note that it is stated LSB in the documentation. So we need to take care of the convention (little/big-endian) when manipulating datas.* 

Data size : 132 bits for full precision. 
Payload size :
* Using a 16bits-CRC : 132+16=148 bits **OK** -> we can simply concatenete the datas.
* Using 32bits-BCH : 164 bits **NOT OK**

**Maximum data size : 160 bits.**

To solve the BCH issue, we could take 10 bits instead of 14 for the temperature. It leads to a 0.2°C precision instead of a 0.01°C one. I really think it is enough, but it is open to discussion. We also could remove some bits from some axis.


# Commentary

According to the kinéis documentation, for our KIM-1 card power (~500mW), we could go from
60% to 85% error-free message using BCH encoding instead of CRC.
So without BCH, nearly 1/2 message is wrong (60%). It may be detrimental for our project if we 
send 3 or 4 message a day.


# References

* Sensors list : https://mangoh.io/uploaded-documents/Reference/mangOH%20Red/Discover/Reference%20Manual/mangOH_Red_Developers_Guide.pdf
* Pressure/Temperature BM280 : https://cdn-shop.adafruit.com/datasheets/BST-BMP280-DS001-11.pdf
* Gyro/Accelerometor BMI160 : https://www.mouser.com/datasheet/2/783/BST-BMI160-DS000-07-786474.pdf
* Light PNJ4K01F : https://industrial.panasonic.com/content/data/SC/ds/ds4/PNJ4K01F_E.pdf

