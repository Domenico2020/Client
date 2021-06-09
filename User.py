# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 21:47:57 2021

@author: lollo
"""

class Utente():

    '''Viene definito un oggetto utente, che raccolga tutte le informazioni del client.'''

    def __init__(self):
        self.username = None
        self.password = None
        self.token = None
        self.registrato = False
        self.autenticato = False