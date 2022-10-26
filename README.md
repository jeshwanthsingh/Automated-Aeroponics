# Automated-Aeroponics
Automate Aeroponics using IOT
The goal of our project is to make a totally automated aeroponics and greenhouse system which will reduce the necessity for human interference to the utmost possible extent. Two different chambers are going to be developed one for the shoot system and therefore the other for the basis system. this is often done to make sure that the climate of the basis system and shoot system are completely independent of every other.
The shoot chamber will host a light-weight sensor, temperature sensor, humidity sensor.

An array of white LED lights (12v 5050) is going to be fixed to the zenith of the chamber and therefore the brightness of those lights is going to be controlled consistent with the optimum candlepower different plants require for photosynthesis. The cooler (exhaust fans) is run cool the plants when the temperature is just too high.

The pump is employed to pump the water to mist makers inside the chamber. The mist makers are installed inside the chamber because it is that the main source of all the nutrients.

When the program is run, which is written in python 2.7 the temperature of the shoot part is checked and if the temperature is bigger than 22 °C then the coolers are turned on and therefore the picture of the plant is taken and sent to the user via mail alongside the opposite sensor data (LDR sensor, DHT 11 sensor,LM35 sensor), the image is additionally stored in local memory of the raspberry pi. the opposite sensor data consists of shoot temperature(LM35 sensor),root temperature(DHT11 sensor),light intensity(LDR sensor)and also humidity(DHT11 sensor).The light intensity is measured within the analog form then converted to digital form using MCP 3008,if the sunshine intensity value is bigger than 500 ,then the sunshine is put to maximum brightness otherwise it stays at 50% brightness.

Then these values will get uploaded to an open source API called 
ThingSpeak where the info is stored and also represented within the sort of graph. The users can view this data anywhere round the world from an app or browser

Hence, the target is to develop an aeroponic system which will both monitor and regulate the inside environment, and send the collected data over an online connection to a server which might process the info and display it to the user through an internet interface, which can even be wont to allow the user to regulate the aeroponic system.
![image](https://user-images.githubusercontent.com/104602113/198096682-906beb2e-30d7-4e71-9eae-bef6f0b20ad0.png)
