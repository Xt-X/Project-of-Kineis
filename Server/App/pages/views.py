from django.shortcuts import render
from django.http import JsonResponse
from zeep import Client

import requests, json
from datetime import datetime, timedelta

from .modules import AVapi, ArgosAPI, ArgosParser

from django.http import HttpResponse


# Step A - resource owner supplies credentials
token_url = "https://eu.airvantage.net/api/oauth/token"
RO_user = "smohanp18@gmail.com"
RO_password = "#$Kineis2020"
client_id = '847ec44018f442538b3d342c0b08fe44'
client_secret = '3b9c1a5b47ab4bcc8dfdd04acfa6c08e'


def homePageView(request):
    # client = Client('http://www.dneonline.com/calculator.asmx?wsdl')
    # client.wsdl.dump() #fetch all service available
    # result = client.service.Add(2,3)

    print("-------------------------------------------------")
    print("Request received, parameters : ")
    print(request.GET)
    print("-------------------------------------------------")

    AVapi.initCredentials(RO_user,RO_password,client_id,client_secret)

    if "nbDays" in request.GET.keys():
        nbDays = request.GET["nbDays"]
        response = AVapi.airvantageNbDays(nbDays)  # when receiving a request, fetch data from airvantageCall
        responseArgos = ArgosParser.processRawArgos(ArgosAPI.callArgos())
        merge(response, responseArgos)

        response = JsonResponse(response)
    elif "dateTo" and "dateFrom" in request.GET.keys():
        dateFrom = request.GET["dateFrom"]
        dateTo = request.GET["dateTo"]
        response = JsonResponse(AVapi.airvantageRange(dateFrom,dateTo))  # when receiving a request, fetch data from airvantageCall
    else:
        return HttpResponse('Malformed URI')

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

    return response  # then return the datas to the one who requested it (the javascript button)

#recursive merge for  nested dictionnaries
def merge(d1, d2):
    for k in d2:
        if k in d1 and isinstance(d1[k], dict) and isinstance(d2[k], dict):
            merge(d1[k], d2[k])
        else:
            d1[k] = d2[k]
    return d1

class Book(object):
    pass


class BookInstance(object):
    pass


class Author(object):
    pass


def index(request):
    """View function for home page of site."""
    """
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }
    """
    context = {
        'num_books': 5,
        'num_instances': 2,
        'num_instances_available': 2,
        'num_authors': 5,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

