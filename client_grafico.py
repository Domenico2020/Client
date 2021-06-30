#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 00:58:26 2021

@author: Egidio
"""
import os
import re
import tkinter as tk
from User import Utente
import argparse
import json
import requests
import pickle
import sys
import os
import shutil
from threading import Thread
from Utility import Receiver
from datetime import datetime

#creo una cartella di memoria per salvare i profili utilizzati
parser = argparse.ArgumentParser()

parser.add_argument("-i1", "--cache", help = "Cartella dei Profili",
                    type = str, default = "./Cache/")
args = parser.parse_args()

window = tk.Tk()
global address
address = 'http://127.0.0.1:12345'

outputMessage = tk.Text()


def open_registration_form():
    global newWindow
    newWindow = tk.Toplevel()
    newWindow.wm_title('Registration Form')
    label1 = tk.Label(newWindow, text="Benvenuto nel sistema di messaggistica ISI.\nPer prima cosa, inserisci l'indirizzo del tuo host!:")
    entry1 = tk.Entry(newWindow, name='entry1')  
    button1 = tk.Button(newWindow, text='send', command=lambda:send_registration_params(newWindow))
    label1.pack()
    entry1.pack() 
    button1.pack()
    
def send_registration_params(window):
    query = window.nametowidget('entry1').get()
    # PROTOTIPO COMANDO: address <address>

    '''La function permette di specificare l'indirizzo degli host'''
    global address
    result = re.search('<([a-zA-Z0-9\,\.\:\/\'\"\!\?<> ]*)>', query)
        
    if bool(result):
        
        address = result.group(1)
        newWindow2 = tk.Toplevel()
        newWindow2.wm_title('Registration Form')
        label2 = tk.Label(newWindow2, text="L'indirizzo è stato modificato con successo...")
        button2 = tk.Button(newWindow2, text='ok', command=lambda:[f() for f in [newWindow2.destroy, pseudoPrompt]])
            
        label2.pack()    
        button2.pack()
        return address
    
def welcome():
    open_registration_form()

def pseudoPrompt():
    newWindow.destroy()
    global window2
    window2 = tk.Tk()
    window2.wm_title('Menù')
    
    def do_reg():

        #PROTOTIPO COMANDO: reg [username] <password>

        '''Vengono inviate le credenziali del nuovo utente, con la particolarità che il token viene settato come valore
           nullo. Successivamente viene richiesto un json di controllo per mostrare all'utente lo status della richiesta
           di registrazione.'''


        # all'atto della registrazione, creo un oggetto globale utente
        global utente
        utente = Utente()

        newWindow = tk.Toplevel()
        newWindow.wm_title('Registrazione Utente')
        label1 = tk.Label(newWindow, text='Username')
        entry1 = tk.Entry(newWindow, name='entry1')  
        label2 = tk.Label(newWindow, text='Password')
        entry2 = tk.Entry(newWindow, name='entry2')  
        button = tk.Button(newWindow, text='ok', command=lambda: send_query(entry1, entry2))
        
        label1.pack()
        entry1.pack() 
        label2.pack()
        entry2.pack()
        button.pack()
        
        def send_query(e1, e2):
            query1 = newWindow.nametowidget('entry1').get()
            query2 = newWindow.nametowidget('entry2').get()
            
                # prendo username e password da linea di comando e li associo all'oggetto utente
            result = re.search('^\[([a-zA-Z0-9]*)\]', query1)
            
            if bool(result):
                utente.username = result.group(1)
            
            result = re.search('<([a-zA-Z0-9\,\.\;\'\"\!\?<> ]*)>', query2)
        
            if bool(result):
                utente.password = result.group(1)
    
            #definizione credenziali e token
            user = {}
            user['username'] = utente.username
            user['password'] = utente.password
    
            #invio credenziali e recupero json di risposta
            # newWindow3 = tk.Toplevel()
            # newWindow3.wm_title('Registration Form')
            # label1a = tk.Label(newWindow3, text='Richiesta di Registrazione in corso...')
            # label1a.pack()
            # button1a = tk.Button(newWindow3, text='ok', command=newWindow3.destroy())
            # button1a.pack()
            print('Richiesta di Registrazione in corso...')
    
            response = requests.post(address + '/api/v1/resources/registration', params = user)
            r = json.loads(response.text)
            
            if r['message'] == 'utente registrato correttamente':
                # newWindow4 = tk.Toplevel()
                # newWindow4.wm_title('Registration Form')
                # label1b = tk.Label(newWindow4, text='La registrazione è avvenuta con successo. Ora puoi accedere al servizio di messaggistica ISI!')
                # label1b.pack()
                # button1b = tk.Button(newWindow4, text='ok', command=newWindow4.destroy())
                # button1b.pack()
                    
                utente.registrato = True   # -----> l'utente è stato registrato con successo
                print('La registrazione è avvenuta con successo. Ora puoi accedere al servizio di messaggistica ISI!')
            
            else:
                
                print(r['message'])  # -----> sarà 'nome utente già esistente'
    
            save_path = args.cache + utente.username
            with open(save_path, 'wb') as outfile:  # -----> creo il file del profilo
                pickle.dump(utente, outfile)

    def do_auth():
        global utente
        #PROTOTIPO COMANDO: auth

        '''Vengono inviate le credenziali e il token alla web api. Successivamente viene richiesto un json di controllo
           per mostrare all'utente lo status della richiesta di autenticazione.'''

        #definizione credenziali e token
        user = {}
        user['username'] = utente.username
        user['password'] = utente.password

        #invio credenziali e recupero json di risposta
        print('Richiesta di Autenticazione in corso...')
        
        response = requests.get(address + '/api/v1/resources/authentication', params = user)
        r = json.loads(response.text)
        
        #ho 3 possibili scenari : json1(tutto ok)  json2(token scaduto + token)  json3(nome utente o password errati)
        global thr
        if r['message'] == "L'UTENTE HA ANCORA IL TOKEN VALIDO":
            
            utente.autenticato = True    # -----> l'utente è abilitato a usare il servizio
            
            print('Sei online!')  
            
            thr = Thread(target = Receiver, args = (address, utente,))  # -----> thread di ricezione dei messaggi
            thr.start()
        
        elif r['message'] == "IL TOKEN SCADUTO E' STATO AGGIORNATO, AUTENTICAZIONE RIUSCITA" or r['message'] == "IL TOKEN E' STATO CREATO PER LA PRIMA VOLTA: ASSEGNAZIONE TOKEN RIUSCITA":
            
            utente.token = r['token']     # -----> aggiorno il token dell'utente
            utente.autenticato = True    # -----> l'utente è abilitato a usare il servizio
            
            save_path = args.cache + utente.username
            with open(save_path, 'wb') as outfile:   # -----> salvo le informazioni del profilo in un file apposito
                pickle.dump(utente,outfile)
            
            print('Sei online!')
            
            thr = Thread(target = Receiver, args = (address, utente,))
            thr.start()            
        
        else:
            
            print("Ops, qualcosa è andato storto...") # -----> sarà 'nome utente o password sbagliata'



    def do_exit():

        # PROTOTIPO COMANDO: exit

        '''La function interrompe i processi del client'''
        sys.exit()

    def do_info():
        '''La function mostra le informazioni del profilo correntemente in utilizzo'''
        newWindow = tk.Toplevel()
        newWindow.wm_title('Utente Attuale')
        
        if "utente" in globals():
            
            
            
            label1 = tk.Label(newWindow, text=f'\nUtente: {utente.username}')
            label2 = tk.Label(newWindow, text=f'Password: {utente.password}')
            label3 = tk.Label(newWindow, text=f'Token: {utente.token}')
            label4 = tk.Label(newWindow, text=f'Registrato: {utente.registrato}')
            label5 = tk.Label(newWindow, text=f'Autenticato: {utente.autenticato}')
                        
            print(f'\nUtente: {utente.username}')
            print(f'Password: {utente.password}')
            print(f'Token: {utente.token}')
            print(f'Registrato: {utente.registrato}')
            print(f'Autenticato: {utente.autenticato}')
            
            label1.pack()
            label2.pack()
            label3.pack()
            label4.pack()
            label5.pack()
       
        else:
            label6 = tk.Label(newWindow, text="Nessun utente ha effettuato l'accesso...")
            label6.pack()
            print("Nessun utente ha effettuato l'accesso...")
    
    def do_addressinfo():

        '''La function mostra l'indirizzo correntemente in utilizzo'''
        
        newWindow = tk.Toplevel()
        newWindow.wm_title('Indirizzo Attuale')
        label1 = tk.Label(newWindow, text=address)
        label1.pack()
        print(address)
        
    def do_changeaddress():
        global newWindow
        newWindow = tk.Toplevel()
        newWindow.wm_title('Cambio Indirizzo')
        label1 = tk.Label(newWindow, text="Inserisci il nuovo indirizzo del tuo host!:")
        entry1 = tk.Entry(newWindow, name='entry1')  
        button1 = tk.Button(newWindow, text='send', command=lambda:send_new_params(newWindow))
        label1.pack()
        entry1.pack() 
        button1.pack()
        def send_new_params(wnd):
            query = newWindow.nametowidget('entry1').get()
            # PROTOTIPO COMANDO: address <address>

            '''La function permette di specificare l'indirizzo degli host'''
            global address
            result = re.search('<([a-zA-Z0-9\,\.\:\/\'\"\!\?<> ]*)>', query)
        
            if bool(result):
        
                address = result.group(1)
                newWindow2 = tk.Toplevel()
                newWindow2.wm_title('Registration Form')
                label2 = tk.Label(newWindow2, text="L'indirizzo è stato modificato con successo...")
                button2 = tk.Button(newWindow2, text='ok', command=lambda:[f() for f in [newWindow2.destroy,newWindow.destroy]])
            
                label2.pack()    
                button2.pack()
                return address
            
    def do_erase():
        newWindow = tk.Toplevel()
        newWindow.wm_title('Cancella Utente')
        label1 = tk.Label(newWindow, text='Username')
        entry1 = tk.Entry(newWindow, name='entry1')  
        button = tk.Button(newWindow, text='ok', command=lambda: send_query2(entry1))
        
        label1.pack()
        entry1.pack() 
        button.pack()
        
        def send_query2(e1):
            query1 = newWindow.nametowidget('entry1').get()
            result = re.search('^\[([a-zA-Z0-9]*)\]', query1)    # seleziono l'opzione
            
            if bool(result):
                user = result.group(1)
            
            if not "utente" in globals(): 
                
                if user == 'all':
                    
                    if os.path.exists(args.cache):     # se all ed esiste, cancello tutto
                        shutil.rmtree(args.cache)
                        print('Cache eliminata con successo...')
                    else:
                        print('La cartella indicata non esiste...')
               
                else: 
                
                    profile_path = args.cache + user     #altrimenti, se esiste cancello il file selezionato
        
                    if os.path.exists(profile_path) and user != utente.username:
                        os.remove(profile_path)
                        print('Profilo eliminato con successo...')
                    else:
                        print('Il profilo selezionato non esiste o è attualmente in uso...')
                        
            else:
                print("Attualmente non è possibile cancellare profili...") 

    def do_send():

        #PROTOTIPO COMANDO: send [receiver] <text>

        '''La function definisce una coda di messaggi in uscita: ogni 2 secondi viene controllata e vengono inviati i
           pacchetti eventualmente presenti in essa. Il pacchetto tipo è formato da un messaggio testuale, dal mittente
           e dal destinatario del messaggio, dalla data/ora di scrittura e dal token.'''
        
        newWindow = tk.Toplevel()
        newWindow.wm_title('Registration Form')
        label1 = tk.Label(newWindow, text='Destinatario')
        entry1 = tk.Entry(newWindow, name='entry1')  
        label2 = tk.Label(newWindow, text='Messaggio')
        entry2 = tk.Entry(newWindow, name='entry2')  
        button = tk.Button(newWindow, text='ok', command=lambda: send_query3(entry1, entry2))
        
        
        
        label1.pack()
        entry1.pack() 
        label2.pack()
        entry2.pack()
        button.pack()   

        def send_query3(e1, e2):
            query1 = newWindow.nametowidget('entry1').get()
            query2 = newWindow.nametowidget('entry2').get()
    
            #inserisco tutte le informazioni necessarie per il messaggio
            package = {}
    
            result = re.search('^\[([a-zA-Z0-9]*)\]', query1)       #prendo il destinatario
            if bool(result):
                package['destinatario'] = result.group(1)
            result = re.search('<([a-zA-Z0-9\,\.\;\'\"\!\?<> ]*)>', query2)      #prendo il messaggio
            if bool(result):
                package['messaggio'] = result.group(1)
            
            package['mittente'] = utente.username
    
            package['data'] = datetime.now()
    
            package['token'] = utente.token
    
            #quando creo un package completo...
            requests.post(address + '/api/v1/resources/send', params = package)        
        
    button1 = tk.Button(window2, text = 'Registrazione utente', command=do_reg)
    button2 = tk.Button(window2, text = 'Autenticazione utente', command=do_auth)
    button3 = tk.Button(window2, text = 'Invia messaggi',command=do_send)
    button4 = tk.Button(window2, text = 'Carica le informazioni utente', command=do_info)
    button6 = tk.Button(window2, text = "Modifica l'indirizzo", command=do_changeaddress)
    button7 = tk.Button(window2, text = "Mostra l'indirizzo attuale", command=do_addressinfo)
    button8 = tk.Button(window2, text = 'Cancella il profilo utente', command=do_erase)
    button9 = tk.Button(window2, text = 'Esci', command = do_exit)
   
    button1.pack()
    button2.pack()
    button3.pack()
    button4.pack()
    button6.pack()
    button7.pack()
    button8.pack()
    button9.pack()
    
    
    

button = tk.Button(text = 'Apri Messaggistica', command=welcome)


button.pack()

# outputMessage.pack()

window.mainloop()

