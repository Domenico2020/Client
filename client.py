
import argparse
from Cprompt import ClientPrompt
import os

#----------------------------------------------------------------------------------------------------------------------#

def managePrompt(prompt):
    prompt.cmdloop()

#----------------------------------------------------------------------------------------------------------------------#

#creo una cartella di memoria per salvare i profili utilizzati
parser = argparse.ArgumentParser()

parser.add_argument("-i1", "--cache", help = "Cartella dei Profili",
                    type = str, default = "./Cache/")

args = parser.parse_args()

address = 'http://192.168.0.118:12345'  # Indirizzo predefinito

if __name__ == '__main__':

    if not os.path.exists(args.cache): 
        os.mkdir(args.cache)

    prompt = ClientPrompt()
    
    prompt.conf(args, address)

    managePrompt(prompt)
  
