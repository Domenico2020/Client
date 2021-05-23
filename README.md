# Client
Architettura dei Sistemi Distribuiti

Implementazione di un Client per il Progetto ChatServer del Corso di Architettura dei Sistemi Distribuiti.

INDIRIZZO PREDEFINITO: '127.0.0.1:12345' ----> è bene che l'utente come prima cosa cambi l'indirizzo predefinito del server con quello reale.

Il Client si basa su un prompt capace di svolgere 9 funzioni: 

*REGISTRAZIONE* --
PROTOTIPO COMANDO: registration [*username:* a-zA-Z0-9] <*password:* a-zA-Z0-9,.;'"!?>
Vengono inviate le credenziali del nuovo utente.Se il processo di registrazione va a buon fine, viene aggiornato il parametro *registrato* nell'oggetto Utente appositamente creato.

*AUTENTICAZIONE* -- 
PROTOTIPO COMANDO: authentication 
Vengono inviate le credenziali dell'utente attuale e richiesto un token.Dopo il processo di autenticazione, il parametro *token* nell'oggetto Utente viene aggiornato qualora sia stato necessario creare un nuovo token/sostituire il token scaduto.

*INVIARE MESSAGGI* --
PROTOTIPO COMANDO: send <*text:* a-zA-Z0-9,.;'"!?> [*receiver:* a-zA-Z0-9] 
Viene creato un 'pacchetto' contenente un messaggio, mittente, destinatario, timestamp e token del mittente. Successivamente viene inviato alla web-api.

*CARICARE UN PROFILO* --
PROTOTIPO COMANDO: load [*username:* a-zA-Z0-9] 
Qualora l'utente specificato sia presente nella cache di memoria locale, il corrispettivo oggetto Utente viene caricato sul Client.

*HELP* -----> ANCORA DA IMPLEMENTARE --
PROTOTIPO COMANDO: help
Viene stampata una breve documentazione su tutte le function del Prompt.

*CAMBIARE L'INDIRIZZO HOST* --
PROTOTIPO COMANDO: address <*address:* a-zA-Z0-9,.;'"!?>  
Viene aggiornato l'indirizzo del server attualmente utilizzato con quello specificato.

*INFORMAZIONI INDIRIZZO HOST* --
PROTOTIPO COMANDO: addressinfo  
Viene mostrato l'indirizzo del server attualmente utilizzato.

*INFORMAZIONI UTENTE* --
PROTOTIPO COMANDO: info  
Vengono mostrate le informazioni dell'utente attualmente collegato.

*INTERRUZIONE DEL SERVIZIO* --  
PROTOTIPO COMANDO: exit  
Viene interrotto il servizio del Client.

#------------------------#

*RICEVERE MESSAGGI* --
Ogni secondo, una funzione richiede alla web-api i messaggi in arrivo per l'utente attualmente collegato e li stampa evidenziando tutte le informazioni relative ad essi
