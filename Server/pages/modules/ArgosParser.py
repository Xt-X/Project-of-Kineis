# Payload format : Light(12)|Pressure(10)|Temperature(14)|Accelerometer(16x3)|Gyroscope(16x3)|CRC(16) = 148 bit



# Light Example
# 3000 lumen = 2**12
# 1500 lumen = 2**15 (2**16 /2, to get the midrange)
Light = "100000000000" # 1500


# Pressure Example
# 1050 hPa = 2**10
# 950 hPa = 0
Pressure = "1000000000" # 1000 hPa

# Temperature Example
# 85°C = 2**14
# -45°C = 0
Temperature = "10000000000000" # 20°C 2**13

# Accelerometer Example (Same for the gyro)
# 2g = 2**16
# 0g = 2**15 (2**16 /2, to get the midrange)
# -2g = 0
Accelerometer = "1000000000000000" # 0g

# Example of decoding

payload = Light + Pressure + Temperature + Accelerometer*6 + "0"*16 # Plus 16 bits of CRC
msg_soap = {1578351600: payload, #Some timestamp to test
			1578361600: payload
			}

def processRawArgos(message):

	processedData ={}
	processedData["MangOH.Sensors.Light.Level"] = {}
	processedData["MangOH.Sensors.Pressure.Pressure"] = {}
	processedData["MangOH.Sensors.Pressure.Temperature"] = {}
	processedData["MangOH.Sensors.Accelerometer.Acceleration.X"] = {}
	processedData["MangOH.Sensors.Accelerometer.Acceleration.Y"] = {}
	processedData["MangOH.Sensors.Accelerometer.Acceleration.Z"] = {}
	processedData["MangOH.Sensors.Accelerometer.Gyro.X"] = {}
	processedData["MangOH.Sensors.Accelerometer.Gyro.Y"] = {}
	processedData["MangOH.Sensors.Accelerometer.Gyro.Z"] = {}

	for timestamp in message:
		if(len(message[timestamp]) != 148):
			print("ERROR ! Argos message must be of 148 bits, received ", len(message) + " bits for timestamp " + timestamp)
			continue
		Light = convertToFloat(message[timestamp][0:12], 12, 0, 3000, "Light")
		Pressure = convertToFloat(message[timestamp][12:22], 10, 950, 1050, "Pressure")
		Temperature = convertToFloat(message[timestamp][22:36], 14, -40, 85, "Temperature")
		AccelerometerX = convertToFloat(message[timestamp][36:52], 16, -2, 2, "AccelerometerX")
		AccelerometerY = convertToFloat(message[timestamp][52:68], 16, -2, 2, "AccelerometerY")
		AccelerometerZ = convertToFloat(message[timestamp][68:84], 16, -2, 2, "AccelerometerZ")
		GyroscopeX = convertToFloat(message[timestamp][84:100], 16, 0, 125, "GyroX")
		GyroscopeY = convertToFloat(message[timestamp][100:116], 16, 0, 125, "GyroY")
		GyroscopeZ = convertToFloat(message[timestamp][116:132], 16, 0, 125, "GyroZ")

		processedData["MangOH.Sensors.Light.Level"].update({timestamp:Light})
		processedData["MangOH.Sensors.Pressure.Pressure"].update({timestamp:Pressure})
		processedData["MangOH.Sensors.Pressure.Temperature"].update({timestamp:Temperature})
		processedData["MangOH.Sensors.Accelerometer.Acceleration.X"].update({timestamp:AccelerometerX})
		processedData["MangOH.Sensors.Accelerometer.Acceleration.Y"].update({timestamp:AccelerometerY})
		processedData["MangOH.Sensors.Accelerometer.Acceleration.Z"].update({timestamp:AccelerometerZ})
		processedData["MangOH.Sensors.Accelerometer.Gyro.X"].update({timestamp:GyroscopeX})
		processedData["MangOH.Sensors.Accelerometer.Gyro.Y"].update({timestamp:GyroscopeY})
		processedData["MangOH.Sensors.Accelerometer.Gyro.Z"].update({timestamp:GyroscopeZ})

	return processedData


def convertToFloat(dataBinary,nbBits,startRange,endRange,name):
	if(len(dataBinary)!=nbBits):
		print("ERROR This data ("+name+") is encoded on " + str(nbBits) + " bits, received ", len(dataBinary))
		return -100
	intValue = int(dataBinary,2) # convert to base 10
	sensitivity = 2**nbBits / (endRange - startRange) # Sensitivity is defined as the number of bit divided by the amplitude of the input
	absScale = intValue / sensitivity  #convert to absolute scale, which go from 0 to 150 hPa for pressure
	relativeScale = absScale + startRange #convert to real scale, with the correct offset (e.g. 950 hPa to 1050 hPa for pressure)
	return relativeScale





