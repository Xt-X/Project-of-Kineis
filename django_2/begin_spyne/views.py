#-*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse
# import logging
# logging.basicConfig(level=logging.DEBUG)
#from spyne import Application, rpc, ServiceBase,Integer, Unicode
from spyne import Application,rpc,ServiceBase,Iterable,Integer,Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne import Iterable
from spyne.protocol.xml import XmlDocument
# from spyne.protocol.json import JsonDocument
from spyne.server.django import DjangoApplication
from django.views.decorators.csrf import csrf_exempt
import json
from referral_service_app import models
from xml.etree import ElementTree

class HelloWorldService(ServiceBase):
    @rpc(Unicode, _returns=Iterable(Unicode))
    def ess_information(ctx, data):
        dic = {"a":1,"b":2}
        return HttpResponse(json.dumps(dic))

application = Application([HelloWorldService],
    tns='spyne.examples.hello',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# This module resides in a package in your Django
# project.

information_app = csrf_exempt(DjangoApplication(application))