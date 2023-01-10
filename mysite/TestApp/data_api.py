
import time
import requests
import websocket, json
import threading

errors = []

stables = {
    'usdt' : [],
    'busd' : [],
}
def get_listed_pairs():
    global errors

    try:
        global usdt
        global busd

        stables['usdt'] = []
        stables['busd'] = []

        url = 'https://www.binance.com/fapi/v1/ticker/price'
        response = requests.get(url)
        print('response: ' + str(response.json()) )
        symbols = list(response.json())
        for dic in symbols:
            separacion = []
            for letra in dic['symbol']:
                separacion.append(letra)
            if separacion[-4] + separacion[-3] + separacion[-2] + separacion[-1] == 'BUSD':
                stables['busd'].append(dic['symbol'])
            if separacion[-4] + separacion[-3] + separacion[-2] + separacion[-1] == 'USDT':
                stables['usdt'].append(dic['symbol'])
        print(len(symbols))
        print(len(stables['usdt']))
        print(len(stables['busd']))

        stables['usdt'] = sorted(stables['usdt'])
        stables['busd'] = sorted(stables['busd'])

        print(stables['usdt'])
        print(stables['busd'])
    except Exception as e:
        errors.append('{}'.format(e))
        print('get_listed_pairs {}'.format(errors))


socket_list = []
timeframes = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
dict_values = {}
def sockets():
    #funcion para la creacion de SOCKETS para conexiones SOCKETs necesarias en tiempo real

    global errors

    try:
        global dict_values
        dict_values = {}

        global socket_list
        socket_list = []

        for key in stables:
            ind_cero = list(stables[key])[0]

            for cripto in stables[key]:
                dict_values[cripto] = {}
                for tframe in timeframes:
                    dict_values[cripto][tframe] = {
                        'open time' : [''],
                        'close time' : [''],
                        'open' : [0],
                        'close' : [0]
                        }

            for tframe in timeframes:
                SOCKET = 'wss://fstream.binance.com/stream?streams={}'.format(ind_cero.lower()) + '@kline_{}'.format(tframe)
                for cripto in stables[key]:
                    if cripto == ind_cero:
                        pass
                    else:
                        SOCKET = SOCKET + "/{}".format(cripto.lower())+ '@kline_{}'.format(tframe)
                socket_list.append(SOCKET)

        #print(socket_list)

    except Exception as e:
        errors.append('{}'.format(e))
        print('sockets {}'.format(errors))


running_Technical_Analysis = True
def on_open(ws):
    pass
    print('opened connection')

def on_close(ws):
    print('closed connection')

def in_on_message(message):
    global errors

    try:

        global dict_values

        json_message = json.loads(message)

        symbol = json_message['data']['s']
        vela = json_message['data']['k']
        openn = vela['o']
        closee = vela['c']
        time_open = time.ctime((int(vela['t']))/1000)
        time_close = time.ctime((int(vela['T']))/1000)

        tframe = vela['i']

        if vela['x']:
            dict_values[symbol][tframe]['open time'].append(time_open)
            dict_values[symbol][tframe]['close time'].append(time_close)
            dict_values[symbol][tframe]['open'].append(openn)
            dict_values[symbol][tframe]['close'].append(closee)

    except Exception as e:
        errors.append('{}'.format(e))
        print('in_on_message {}'.format(errors))

#{'stream': 'trxbusd@kline_4h', 'data': {'e': 'kline', 'E': 1672966698036, 's': 'TRXBUSD', 'k': {'t': 1672963200000, 'T': 1672977599999, 's': 'TRXBUSD', 'i': '4h', 'f': 8482607, 'L': 8484423, 'o': '0.0536540', 'c': '0.0537910', 'h': '0.0538440', 'l': '0.0534610', 'v': '10666314', 'n': 1817, 'x': False, 'q': '572018.1067970', 'V': '6006624', 'Q': '322100.6568260', 'B': '0'}}}

def on_message(ws, message):
    #funcion al establecer conexion web socket

    global errors

    try:
        if running_Technical_Analysis == False:
            print('conexion socket terminada')
        ws.keep_running = running_Technical_Analysis #!!!

        x = threading.Thread(target=in_on_message, args=[message])
        x.start()
    except Exception as e:
        errors.append('{}'.format(e))
        print('on_message {}'.format(errors))

def run_sockets():
    try:
        get_listed_pairs()
        print('stables: ' + str(stables))
        '''
        sockets()
        print(dict_values['BTCUSDT'])
        for SOCKET in socket_list:
            #print(SOCKET)
            ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
            x = threading.Thread(target=ws.run_forever)
            x.start()
        '''
    except Exception as e:
        errors.append('{}'.format(e))
        print('run_sockets {}'.format(errors))


#run_sockets()

#print(dict_values)


