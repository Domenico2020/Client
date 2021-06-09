# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 21:48:31 2021

@author: lollo
"""

import time
import requests
import chime
import json

#--------------------------------------------------------------------------------------------------------------------#

def Receiver(address, utente):

    '''La function controlla ogni 2 secondi viene controllata e vengono stampati i
       pacchetti eventualmente presenti in essa. Il pacchetto tipo è formato da un messaggio testuale, dal mittente
       del messaggio e dalla data/ora di scrittura.'''

    #definizione dei parametri del get
    while True:
        
        time.sleep(10)
        
        user = {}
        user['username'] = utente.username
        user['token'] = utente.token
    
        #recupero i messaggi che mi sono stati inviati
        response = requests.get(address + '/api/v1/resources/receive', params = user)
        response = json.loads(response.text)
        
        if len(response['messaggi']) != 0:
            
            chime.success()
            
            for messaggio in response['messaggi']:   # -----> stampo tutti i messaggi che sono arrivati
                print(f"Messaggio in arrivo da {messaggio['mittente']}: --- {messaggio['messaggio']} --- {messaggio['data']}")
                response['messaggi'].remove(messaggio)