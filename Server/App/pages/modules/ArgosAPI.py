from zeep import Client
import xml.etree.ElementTree as ET

def callArgos():
	cl = Client("http://ws-argos.cls.fr/argosDws/services/DixService?wsdl")
	response = cl.service.getXml(username="PICOU_INSA",password="MANG0H",platformId="183245",nbDaysFromNow=20,displayRawData=True)
	# there are a lot of different parameters for this function, for filtereing the output, but this one seem enough
	# 20 days is the max for argos satellite
	xmldata = ET.fromstring(response)

	xmldata = ET.parse("pages/static/sample/crafted_sample.xml").getroot()
	rawPayload = xmldata.find("program").find("satellitePass").find("message").find("collect").find("rawData").text
	msg_soap = {1572365374770: rawPayload,
				1572365373770: rawPayload
				}
	return msg_soap