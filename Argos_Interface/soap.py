from zeep import Client
cl = Client("test.wsdl") #or "http://ws-argos.cls.fr/argosDws/services/DixService?wsdl"
xmldata = cl.service.getXml(username="PICOU_INSA",password="MANG0H",platformId="183245",nbDaysFromNow=20,displayRawData=True)
#there are a lot of different parameters for this function, for filtereing the output, but this one seem enough
