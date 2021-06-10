# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 21:43:59 2021

@author: lollo
"""

from cmd import Cmd
from User import Utente
import re
import json
import requests
import pickle
from threading import Thread
from Utility import Receiver
import os
import sys
import shutil
from datetime import datetime

#-------------------------------------------------------------------------------------------------------------------#

class ClientPrompt(Cmd):

    '''Viene definita una classe ClientPrompt, proprio come abbiamo fatto con il ring.'''

    prompt = 'ISI-Client --> '
    intro = "Benvenuto nel sistema di messaggistica ISI.\nPer prima cosa, inserisci l'indirizzo del tuo host!"
    
    

    def conf(self, args, address):
        
        '''Configurazione dei parametri del prompt.'''
        
        self.args = args
        self.address = address



    def do_reg(self, inp):

        #PROTOTIPO COMANDO: reg [username] <password>

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

        #invio credenziali e recupero json di risposta
        print('Richiesta di Registrazione in corso...')

        response = requests.post(self.address + '/api/v1/resources/registration', params = user)
        r = json.loads(response.text)
        
        if r['message'] == 'utente registrato correttamente':
            
            utente.registrato = True   # -----> l'utente è stato registrato con successo
            print('La registrazione è avvenuta con successo. Ora puoi accedere al servizio di messaggistica ISI!')
        
        else:
            
            print(r['message'])  # -----> sarà 'nome utente già esistente'

        save_path = self.args.cache + utente.username
        with open(save_path, 'wb') as outfile:  # -----> creo il file del profilo
            pickle.dump(utente, outfile)



    def do_auth(self, inp):

        #PROTOTIPO COMANDO: auth

        '''Vengono inviate le credenziali e il token alla web api. Successivamente viene richiesto un json di controllo
           per mostrare all'utente lo status della richiesta di autenticazione.'''

        #definizione credenziali e token
        user = {}
        user['username'] = utente.username
        user['password'] = utente.password

        #invio credenziali e recupero json di risposta
        print('Richiesta di Autenticazione in corso...')
        
        response = requests.get(self.address + '/api/v1/resources/authentication', params = user)
        r = json.loads(response.text)
        
        #ho 3 possibili scenari : json1(tutto ok)  json2(token scaduto + token)  json3(nome utente o password errati)
        global thr
        if r['message'] == "L'UTENTE HA ANCORA IL TOKEN VALIDO":
            
            utente.autenticato = True    # -----> l'utente è abilitato a usare il servizio
            
            print('Sei online!')  
            
            thr = Thread(target = Receiver, args = (self.address, utente,))  # -----> thread di ricezione dei messaggi
            thr.start()
        
        elif r['message'] == "IL TOKEN SCADUTO E' STATO AGGIORNATO, AUTENTICAZIONE RIUSCITA" or r['message'] == "IL TOKEN E' STATO CREATO PER LA PRIMA VOLTA: ASSEGNAZIONE TOKEN RIUSCITA":
            
            utente.token = r['token']     # -----> aggiorno il token dell'utente
            utente.autenticato = True    # -----> l'utente è abilitato a usare il servizio
            
            save_path = self.args.cache + utente.username
            with open(save_path, 'wb') as outfile:   # -----> salvo le informazioni del profilo in un file apposito
                pickle.dump(utente,outfile)
            
            print('Sei online!')
            
            thr = Thread(target = Receiver, args = (self.address, utente,))
            thr.start()            
        
        else:
            
            print("Ops, qualcosa è andato storto...") # -----> sarà 'nome utente o password sbagliata'



    def do_send(self, inp):

        #PROTOTIPO COMANDO: send [receiver] <text>

        '''La function definisce una coda di messaggi in uscita: ogni 2 secondi viene controllata e vengono inviati i
           pacchetti eventualmente presenti in essa. Il pacchetto tipo è formato da un messaggio testuale, dal mittente
           e dal destinatario del messaggio, dalla data/ora di scrittura e dal token.'''

        #inserisco tutte le informazioni necessarie per il messaggio
        package = {}

        result = re.search('^\[([a-zA-Z0-9]*)\]', inp)       #prendo il destinatario
        if bool(result):
            package['destinatario'] = result.group(1)
        result = re.search('<([a-zA-Z0-9\,\.\;\'\"\!\?<> ]*)>', inp)      #prendo il messaggio
        if bool(result):
            package['messaggio'] = result.group(1)
        
        package['mittente'] = utente.username

        package['data'] = datetime.now()

        package['token'] = utente.token

        #quando creo un package completo...
        requests.post(self.address + '/api/v1/resources/send', params = package)
        


    def do_load(self, inp):

        # PROTOTIPO COMANDO: load [username]

        '''La function carica le informazioni di un utente sul client.'''

        #DA IMPLEMENTARE PROTOCOLLI DI SICUREZZA PER OSCURARE LE INFORMAZIONI PERSONALI

        #carico dalla cache il profilo utente che voglio utilizzare
        result = re.search('^\[([a-zA-Z0-9]*)\]', inp)
        
        if bool(result):
            user = result.group(1)

        path = self.args.cache + user
        if os.path.exists(path):
            with open(path, 'rb') as fin:
                
                global utente
                utente = pickle.load(fin)
                
                if utente.autenticato == True and utente.registrato == True:
                    thr = Thread(target = Receiver, args = (self.address, utente,))    # se abilitato, faccio partire anche il thread di ricezione
                    thr.start()
        
        else:
            
            print("Il profilo indicato non è disponibile nella cache")
            
        

    def do_help(self, inp):

        # PROTOTIPO COMANDO: help

        '''La function stampa una breve documentazione dei comandi implementati nel ClientPrompt.'''

        print("\nLISTA DELLE AZIONI ATTUALMENTE DISPONIBILI:")
        print("\nREGISTRAZIONE: registrazione al servizio dell'utente specificato ------> reg [username] <password>")
        print("\nAUTENTICAZIONE: autenticazione dell'utente in uso ------> auth")
        print("\nSEND: invio di un messaggio a un utente ------> send [username] <messaggio>")
        print("\nLOAD: caricamento di un profilo già presente nella cache (ANCORA SPERIMENTALE!) ------> load [username]")
        print("\nADDRESS: permette di modificare l'indirizzo dell'host ------> address <address>")
        print("\nADDRESSINFO: permette di visualizzare l'indirizzo dell'host ------> addressinfo")
        print("\nINFO: permette di visualizzare le informazioni sull'utente ------> info")
        print("\nERASE: permette di eliminare profili dalla cache (o la cache se il tag è 'all') ------> erase [all] / erase [username]")
        print("\nEXIT: interruzione del servizio ------> exit")



    def do_address(self, inp):

        # PROTOTIPO COMANDO: address <address>

        '''La function permette di specificare l'indirizzo degli host'''

        result = re.search('<([a-zA-Z0-9\,\.\:\/\'\"\!\?<> ]*)>', inp)
        
        if bool(result):
            self.address = result.group(1)
            
            print("L'indirizzo è stato modificato con successo...")




    def do_exit(self, inp):

        # PROTOTIPO COMANDO: exit

        '''La function interrompe i processi del client'''

        print('Servizio Interrotto')
        
        sys.exit()



    def do_info(self, inp):

        # PROTOTIPO COMANDO: info

        '''La function mostra le informazioni del profilo correntemente in utilizzo'''

        if "utente" in globals():
            
            print(f'\nUtente: {utente.username}')
            print(f'Password: {utente.password}')
            print(f'Token: {utente.token}')
            print(f'Registrato: {utente.registrato}')
            print(f'Autenticato: {utente.autenticato}')
       
        else:
            
            print("Nessun utente ha effettuato l'accesso...")



    def do_addressinfo(self, inp):

        # PROTOTIPO COMANDO: addressinfo

        '''La function mostra l'indirizzo correntemente in utilizzo'''

        print(self.address)



    def do_erase(self, inp):

        # PROTOTIPO COMANDO: erase [username]   -----> usare all per eliminare tutta la cache

        '''La function elimina il profilo indicato da linea di comando. Se viene specificato all, cancella tutta la cache dei profili.'''

        result = re.search('^\[([a-zA-Z0-9]*)\]', inp)    # seleziono l'opzione
        
        if bool(result):
            user = result.group(1)
        
        if not "utente" in globals(): 
            
            if user == 'all':
                
                if os.path.exists(self.args.cache):     # se all ed esiste, cancello tutto
                    shutil.rmtree(self.args.cache)
                    print('Cache eliminata con successo...')
                else:
                    print('La cartella indicata non esiste...')
           
            else: 
            
                profile_path = self.args.cache + user     #altrimenti, se esiste cancello il file selezionato
    
                if os.path.exists(profile_path) and user != utente.username:
                    os.remove(profile_path)
                    print('Profilo eliminato con successo...')
                else:
                    print('Il profilo selezionato non esiste o è attualmente in uso...')
                    
        else:
            print("Attualmente non è possibile cancellare profili...")