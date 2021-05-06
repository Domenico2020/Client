import requests
import json
from cmd import Cmd


address = 'http://192.168.114.205:12345'   #aggiornare indirizzo

class ClientPrompt(Cmd):

    def __init__(self):
        pass

    def do_authentication(self, username, password, token):

        user = {}
        user['username'] = username
        user['password'] = int(password)
        user['token'] = token

        print('Richiesta di Autenticazione in corso...')
        requests.post(address + '/api/v1/resources/', params = user)
        response = requests.get(address + '/api/v1/resources/')
        response = json.dumps(response.json(), indent=4, sort_keys=False)   #json1(tutto ok)  json2(token scaduto + token)  json3(nome utente o password errati)
        if response['status'] == 'tutto ok':
            global abilitato = True
        elif response['status'] == 'token scaduto':
            new_token = requests.get(address + '/api/v1/resources/')
            new_token = json.dumps(response.json(), indent=4, sort_keys=False)
            global token = new_token['token']
        else:
            response = requests.get(address + '/api/v1/resources/')
            response = json.dumps(response.json(), indent=4, sort_keys=False)
            print(response['status']) # -----> sarà 'nome utente o password scaduta'


    def do_registration(self, username, password):

        user = {}
        user['username'] = username
        user['password'] = int(password)
        user['token'] = None

        print("Richiesta di Registrazione in corso...")
        requests.post(address + '/api/v1/resources/', params = user)
        response = requests.get(address + '/api/v1/resources/')
        response = json.dumps(response.json(), indent=4, sort_keys=False)  # json1(messaggio di stato)   json2(messaggio di stato + token)
        if response['status'] == 'tutto ok':
            abilitato = True
            global token = response['token']
        else:
            response = requests.get(address + '/api/v1/resources/')
            response = json.dumps(response.json(), indent=4, sort_keys=False)
            print(response['status'])  # -----> sarà 'nome utente già esistente'


    def do_send(self, text, sender, receiver, timestamp, token):

        package = {}
        package['Text'] = text
        package['Sender'] = sender
        package['Receiver'] = receiver
        package['Timestamp'] = timestamp
        package['Token'] = token

        try:
            requests.post(address + '/api/v1/resources/', params = package)
        except:
            print("Attenzione! C'è stato un errore nell'invio del messaggio...")

    def do_receive(self):

        try:
            response = requests.get(address + '/api/v1/resources/')
            response = json.dumps(response.json(), indent = 4, sort_keys = False)
            print('-' * 80)
            print(response)
        except:
            print("Attenzione! C'è stato un errore nella ricezione del messaggio...")


if __name__ == '__main__':

# pila per send e receive message: messaggi in entrata e in uscita vengono messi in attesa e un thread con temporizzazione invia tutto il
# contenuto della pila

    if Abilitato = True:
        puoi mandare e ricevere i messaggi
