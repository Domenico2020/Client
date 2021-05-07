import requests
import json
from cmd import Cmd
from datetime import datetime


address = 'http://192.168.114.205:12345'   #aggiornare indirizzo

class ClientPrompt(Cmd):

    '''Viene definita una classe ClientPrompt, proprio come abbiamo fatto con il ring.'''

    prompt = ' '
    intro = 'Benvenuto nel sistema di messagistica ISI. Usa ? per accedere all\'help'

    def managePrompt(prompt):
        prompt.cmdloop()

    def do_authentication(self, username, password, token):

        '''Vengono inviate le credenziali e il token alla web api. Successivamente viene richiesto un json di controllo
           per mostrare all'utente lo status della richiesta di autenticazione.'''

        #definizione credenziali e token
        user = {}
        user['username'] = username
        user['password'] = int(password)
        user['token'] = token

        #invio credenziali
        print('Richiesta di Autenticazione in corso...')
        response = requests.post(address + '/api/v1/resources/autenticazione', params = user)
        # recupero json di risposta
        response = json.dumps(response.json(), indent=4, sort_keys=False)

        #json1(tutto ok)  json2(token scaduto + token)  json3(nome utente o password errati)
        if response['status'] == 'tutto ok':
            global abilitato = True
        elif response['status'] == 'token scaduto':
            #new_token = requests.get(address + '/api/v1/resources/')
            #new_token = json.dumps(response.json(), indent=4, sort_keys=False)
            global token = response['new_token']
        else:
            #response = requests.get(address + '/api/v1/resources/statusautenticazione')
            #response = json.dumps(response.json(), indent=4, sort_keys=False)
            print(response['status']) # -----> sarà 'nome utente o password scaduta'


    def do_registration(self, username, password):

        '''Vengono inviate le credenziali del nuovo utente, con la particolarità che il token viene settato come valore
           nullo. Successivamente viene richiesto un json di controllo per mostrare all'utente lo status della richiesta
           di registrazione.'''

        #definizione credenziali e token
        user = {}
        user['username'] = username
        user['password'] = int(password)
        user['token'] = None

        #invio credenziali
        print("Richiesta di Registrazione in corso...")
        response = requests.post(address + '/api/v1/resources/registrazione', params = user)
        #recupero json di risposta
        response = json.dumps(response.json(), indent=4, sort_keys=False)  # json1(messaggio di stato)   json2(messaggio di stato + token)

        if response['status'] == 'tutto ok':
            registrato = True
        else:
            #response = requests.get(address + '/api/v1/resources/statusregistrazione')
            #response = json.dumps(response.json(), indent=4, sort_keys=False)
            print(response['status'])  # -----> sarà 'nome utente già esistente'


    def do_send(self, text, sender, receiver, timestamp, token):

        '''La function definisce una coda di messaggi in uscita: ogni 2 secondi viene controllata e vengono inviati i
           pacchetti eventualmente presenti in essa. Il pacchetto tipo è formato da un messaggio testuale, dal mittente
           e dal destinatario del messaggio, dalla data/ora di scrittura e dal token.'''

        #inserisco tutte le informazioni necessarie per il messaggio
        package = {}
        package['Text'] = text
        package['Sender'] = sender
        package['Receiver'] = argv[1]    #receiver
        package['Timestamp'] = datetime.now()
        package['Token'] = token

        #quando creo un package completo...
        response = requests.post(address + '/api/v1/resources/inviamessaggio', params = user)
        print(response['status'])

        #controlla continuamente la coda di invio
        while True:
            ThreadSendController(buffer_invio)



    def do_receive(self):

        '''La function definisce una coda di messaggi in entrata: ogni 2 secondi viene controllata e vengono stampati i
           pacchetti eventualmente presenti in essa. Il pacchetto tipo è formato da un messaggio testuale, dal mittente
           del messaggio e dalla data/ora di scrittura.'''


        buffer_entrata.append(response)

        # controlla continuamente la coda di invio
        while True:
            ThreadReceiveController(buffer_entrata)

    #def ThreadSendController(self, buffer_invio):
    #    pass

    def Receiver(self, address, ):

        response = requests.get(address + '/api/v1/resources/recuperomessaggi')
        response = json.dumps(response.json(), indent=4, sort_keys=False)

if __name__ == '__main__':

    if Abilitato:
        #puoi mandare e ricevere i messaggi

        buffer_entrata = []
