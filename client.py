import os
import requests
import json
from cmd import Cmd
from datetime import datetime
from threading import Thread
import argparse
import pickle
import time
import sys
import playsound as ps
import pprint as pp
from icecream import ic

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

    prompt = 'ISI-Client -->'
    intro = "Benvenuto nel sistema di messagistica ISI. Usa ? per accedere all'help"
    
    def do_registration(self, inp):

        #PROTOTIPO COMANDO: registration [username] <password>

        '''Vengono inviate le credenziali del nuovo utente, con la particolarità che il token viene settato come valore
           nullo. Successivamente viene richiesto un json di controllo per mostrare all'utente lo status della richiesta
           di registrazione.'''

        # all'atto della registrazione, creo un oggetto globale utente
        global utente
        utente = Utente()

        # prendo username e password da linea di comando e li associo all'oggetto utente
        result = re.search('^\[([a-zA-Z0-9]*)\]', inp)
        if bool(result):
            utente.username = result.group(1)
        result = re.search('<([a-zA-Z0-9\,\.\;\'\"\!\?<> ]*)>', inp)
        if bool(result):
            utente.password = result.group(1)

        #definizione credenziali e token
        user = {}
        user['username'] = utente.username
        user['password'] = utente.password
        #user['token'] = utente.token

        #invio credenziali e recupero json di risposta
        ic('Richiesta di Registrazione in corso...')
        response = requests.post(address + '/api/v1/resources/registration', params = user)
        response = json.dumps(response.json(), indent = 4, sort_keys = False)  # json1(tutto ok)   json2(errore di qualche tipo)

        if response['message'] == 'utente registrato correttamente':
            utente.registrato = True   # -----> l'utente è stato registrato con successo
            print('La registrazione è avvenuta con successo. Ora puoi accedere al servizio di messaggistica ISI!')
        else:
            print(response['message'])  # -----> sarà 'nome utente già esistente'

        save_path = args.cache + utente.username
        with open(save_path, 'wb') as outfile:
            pickle.dump(utente)



    def do_authentication(self):

        #PROTOTIPO COMANDO: authentication

        '''Vengono inviate le credenziali e il token alla web api. Successivamente viene richiesto un json di controllo
           per mostrare all'utente lo status della richiesta di autenticazione.'''

        #definizione credenziali e token
        user = {}
        user['username'] = utente.username
        user['password'] = utente.password
        #user['token'] = utente.token

        #invio credenziali e recupero json di risposta
        ic('Richiesta di Autenticazione in corso...')
        response = requests.get(address + '/api/v1/resources/authentication', params = user)
        response = json.dumps(response.json(), indent = 4, sort_keys = False)

        #ho 3 possibili scenari : json1(tutto ok)  json2(token scaduto + token)  json3(nome utente o password errati)
        if response['message'] == "L'UTENTE HA ANCORA IL TOKEN VALIDO":
            utente.abilitato = True    # -----> l'utente è abilitato a usare il servizio
            print('Sei online!')
        elif response['message'] == "IL TOKEN SCADUTO E' STATO AGGIORNATO, AUTENTICAZIONE RIUSCITA":
            utente.token = response['token']     # -----> aggiorno il token dell'utente
            utente.abilitato = True    # -----> l'utente è abilitato a usare il servizio
            save_path = args.cache + utente.username
            with open(save_path, 'wb') as outfile:   # -----> salvo le informazioni del profilo in un file apposito
                pickle.dump(utente)
            print('Sei online!')
        else:
            print(response['message']) # -----> sarà 'nome utente o password sbagliata'



    def do_send(self, inp):

        #PROTOTIPO COMANDO: send <text> [receiver]

        '''La function definisce una coda di messaggi in uscita: ogni 2 secondi viene controllata e vengono inviati i
           pacchetti eventualmente presenti in essa. Il pacchetto tipo è formato da un messaggio testuale, dal mittente
           e dal destinatario del messaggio, dalla data/ora di scrittura e dal token.'''

        #inserisco tutte le informazioni necessarie per il messaggio
        package = {}

        #prendo il messaggio
        result = re.search('<([a-zA-Z0-9\,\.\;\'\"\!\?<> ]*)>', inp)
        if bool(result):
            package['messaggio'] = result.group(1)

        package['mittente'] = utente.username

        #prendo il destinatario
        result = re.search('^\[([a-zA-Z0-9]*)\]', inp)
        if bool(result):
            package['destinatario'] = result.group(1)

        package['data'] = datetime.now()

        package['token'] = utente.token

        #quando creo un package completo...
        response = requests.post(address + '/api/v1/resources/send', params = package)



    def do_load(self, inp):

        '''La function carica le informazioni di un utente sul client.'''

        #DA IMPLEMENTARE PROTOCOLLI DI SICUREZZA PER OSCURARE LE INFORMAZIONI PERSONALI

        #carico dalla cache il profilo utente che voglio utilizzare
        result = re.search('^\[([a-zA-Z0-9]*)\]', inp)
        if bool(result):
            user = result.group(1)

        path = args.cache + user
        if os.path.exists(path):
            with open(path, 'rb') as fin:
                global utente
                utente = pickle.load(fin)
        else:
            pp.pprint("Il profilo indicato non è disponibile nella cache")



    def do_help(self):

        '''La function stampa una breve documentazione dei comandi implementati nel ClientPrompt.'''

        pass



    def do_address(self, inp):

        ##PROTOTIPO COMANDO: address <address>

        '''La function permette di specificare l'indirizzo degli host'''

        result = re.search('<([a-zA-Z0-9\,\.\:\/\'\"\!\?<> ]*)>', inp)
        if bool(result):
            global address
            address = result.group(1)



    def do_exit(self):

        '''La function interrompe i processi del client'''

        print('Client interrotto')
        self.close()
        sys.exit()

#----------------------------------------------------------------------------------------------------------------------#

def managePrompt(prompt):
    prompt.cmdloop()



def Receiver(address, args):

    '''La function controlla ogni 2 secondi viene controllata e vengono stampati i
       pacchetti eventualmente presenti in essa. Il pacchetto tipo è formato da un messaggio testuale, dal mittente
       del messaggio e dalla data/ora di scrittura.'''

    #definizione dei parametri del get
    user = {}
    user['username'] = utente.username
    user['token'] = user.token

    #recupero i messaggi che mi sono stati inviati
    response = requests.get(address + '/api/v1/resources/receive', params = user)
    response = json.dumps(response.json(), indent = 4, sort_keys = False)

    if len(response['messaggi']) != 0:
        ps.playsound(args.root + "notification.mp4")
        for messaggio in response['messaggi']:   # -----> stampo tutti i messaggi che sono arrivati
            pp.pprint(f"Messaggio in arrivo da {messaggio['mittente']}: --- {messaggio['messaggio']} --- {messaggio['data']}")

#----------------------------------------------------------------------------------------------------------------------#

#creo una cartella di memoria per salvare i profili utilizzati
parser = argparse.ArgumentParser()

parser.add_argument("-i1", "--cache", help = "Cartella dei Profili",
                    type = str, default = "./Cache/")

parser.add_argument("-i2", "--root", help = "Cartella Base",
                    type = str, default = "./Client/")

args = parser.parse_args()

if __name__ == '__main__':

    #logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.ERROR)

    if not os.path.exists(args.cache):
        os.mkdir(args.cache)

    prompt = ClientPrompt()

    Thread(target = managePrompt, args = (prompt,)).start()

    while True:
        time.sleep(1)
        Receiver(address)
