import requests
import json
from cmd import Cmd
from datetime import datetime
from threading import Thread

#----------------------------------------------------------------------------------------------------------------------#

class Utente():

    '''Viene definita un oggetto utente, che raccolga tutte le informazioni del client.'''

    def __init__(self):
        self.username = None
        self.password = None
        self.token = None
        self.registrato = False
        self.autenticato = False

#----------------------------------------------------------------------------------------------------------------------#

class ClientPrompt(Cmd):

    '''Viene definita una classe ClientPrompt, proprio come abbiamo fatto con il ring.'''

    prompt = ' '
    intro = "Benvenuto nel sistema di messagistica ISI. Usa ? per accedere all'help"



    def do_authentication(self, input, token):

        #PROTOTIPO COMANDO: authentication username password

        '''Vengono inviate le credenziali e il token alla web api. Successivamente viene richiesto un json di controllo
           per mostrare all'utente lo status della richiesta di autenticazione.'''

        #all'atto dell'autenticazione, creo un oggetto globale utente
        global utente = Utente()

        #prendo username e password da linea di comando e li associo all'oggetto utente
        global utente.username = argv[1]
        global utente.password = argv[2]

        #definizione credenziali e token
        user = {}
        user['username'] = utente.username
        user['password'] = utente.password
        user['token'] = utente.token

        #invio credenziali e recupero json di risposta
        print('Richiesta di Autenticazione in corso...')
        response = requests.post(address + '/api/v1/resources/autenticazione', params = user)
        response = json.dumps(response.json(), indent = 4, sort_keys = False)

        #ho 3 possibili scenari : json1(tutto ok)  json2(token scaduto + token)  json3(nome utente o password errati)
        if response['status'] == 'tutto ok':
            global utente.abilitato = True    # -----> l'utente è abilitato a usare il servizio
            print('Sei online!')
        elif response['status'] == 'token scaduto':
            global token = response['new_token']     # -----> aggiorno il token dell'utente
            global abilitato = True    # -----> l'utente è abilitato a usare il servizio
            print('Sei online!')
        else:
            print(response['status']) # -----> sarà 'nome utente o password scaduta'



    def do_registration(self, input):

        #PROTOTIPO COMANDO: registration username password

        '''Vengono inviate le credenziali del nuovo utente, con la particolarità che il token viene settato come valore
           nullo. Successivamente viene richiesto un json di controllo per mostrare all'utente lo status della richiesta
           di registrazione.'''

        # all'atto della registrazione, creo un oggetto globale utente
        global utente = Utente()

        # prendo username e password da linea di comando e li associo all'oggetto utente
        global utente.username = argv[1]
        global utente.password = int(argv[2])

        #definizione credenziali e token
        user = {}
        user['username'] = utente.username
        user['password'] = utente.password
        user['token'] = utente.token

        #invio credenziali e recupero json di risposta
        print("Richiesta di Registrazione in corso...")
        response = requests.post(address + '/api/v1/resources/registrazione', params = user)
        response = json.dumps(response.json(), indent = 4, sort_keys = False)  # json1(messaggio di stato)   json2(messaggio di stato + token)

        if response['status'] == 'tutto ok':
            global utente.registrato = True   # -----> l'utente è stato registrato con successo
            print('La registrazione è avvenuta con successo. Ora puoi accedere al servizio di messaggistica ISI!')
        else:
            print(response['status'])  # -----> sarà 'nome utente già esistente'



    def do_send(self, input, username, token):

        #PROTOTIPO COMANDO: send text receiver

        '''La function definisce una coda di messaggi in uscita: ogni 2 secondi viene controllata e vengono inviati i
           pacchetti eventualmente presenti in essa. Il pacchetto tipo è formato da un messaggio testuale, dal mittente
           e dal destinatario del messaggio, dalla data/ora di scrittura e dal token.'''

        #inserisco tutte le informazioni necessarie per il messaggio
        package = {}
        package['Text'] = argv[1]
        package['Sender'] = username
        package['Receiver'] = argv[2]    #receiver
        package['Timestamp'] = datetime.now()
        package['Token'] = token

        #quando creo un package completo...
        response = requests.post(address + '/api/v1/resources/inviamessaggio', params = user)
        print(response['status'])



    def do_logout(self):

        '''La function disconnette l'utente dal servizio di messaggistica.'''

        pass



    def do_help(self):

        '''La function stampa una breve documentazione dei comandi implementati nel ClientPrompt.'''

        pass

#----------------------------------------------------------------------------------------------------------------------#

def managePrompt(prompt):
    prompt.cmdloop()


def Receiver(address):

    '''La function definisce una coda di messaggi in entrata: ogni 2 secondi viene controllata e vengono stampati i
       pacchetti eventualmente presenti in essa. Il pacchetto tipo è formato da un messaggio testuale, dal mittente
       del messaggio e dalla data/ora di scrittura.'''

    #recupero i messaggi che mi sono stati inviati
    response = requests.get(address + '/api/v1/resources/recuperomessaggi')
    response = json.dumps(response.json(), indent = 4, sort_keys = False)

    for messaggio in response['messaggi']:   # -----> stampo tutti i messaggi che sono arrivati
        print(f"Messaggio in arrivo da {messaggio['mittente']}: --- {messaggio['text']} --- {messaggio['timestamp']}")


if __name__ == '__main__':

    #logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.ERROR)

    #main non ancora completo

    address = 'http://192.168.114.205:12345'

    if utente.Registrato and utente.Autenticato:    #se l'utente è autorizzato (registrato + autenticato) il client può partire
        #puoi mandare e ricevere i messaggi

        Thread(target = managePrompt, args = (prompt,)).start()

        while True:
            Receiver(address)
