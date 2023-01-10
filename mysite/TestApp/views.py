from django.shortcuts import render

# Create your views here.

from . import data_api

import threading

def startup():
    print('start up')

    x = threading.Thread(target=data_api.run_sockets)
    x.start()

startup()

def index(response, id):

    print(id)

    cripto = ''

    try:
        cripto = data_api.dict_values[id]
        print(cripto)

    except KeyError:
        if id == 'EXIT':
            data_api.running_Technical_Analysis = False
            cripto = 'Finalizar conexion socket'
        elif id == 'START':
            if data_api.running_Technical_Analysis == True:
                data_api.running_Technical_Analysis = False
            data_api.running_Technical_Analysis = True
            startup()
            cripto = 'Comenzar conexion socket'


    return render(response, 'TestApp/index.html', {'cripto' : cripto})

def home(response):
    return render(response, "TestApp/home.html", {})

