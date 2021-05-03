# -*- coding: utf-8 -*-
"""
Created on Mon May  3 14:24:38 2021

@author: Domenico
"""

import xmlrpc.client
import datetime

#proxy = xmlrpc.client.ServerProxy('htttp://192.168.76.205:12345')
proxy = xmlrpc.client.ServerProxy('htttp://localhost:12345')

today = proxy.today()

converted = datetime.datetime.strptime(today.value, '%Y%m%dT%H: %M: %S')
print('Today: {}'.format(converted.strftime('%d/%m/%Y, %H: %M')))
