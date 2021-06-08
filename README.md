# Client
Architettura dei Sistemi Distribuiti


<b>REGISTRAZIONE</b>: separate chat log window, profile cache locker


Implementazione di un Client per il Progetto ChatServer del Corso di Architettura dei Sistemi Distribuiti.


INDIRIZZO PREDEFINITO: 'http://172.20.10.12:12345' ----> è bene che l'utente come prima cosa cambi l'indirizzo predefinito del server con quello effettivo.


Il Client si basa su un <b>PROMPT</b> capace di svolgere 9 funzioni: 


<b>REGISTRAZIONE</b> --PROTOTIPO COMANDO: registration [*username:* a-zA-Z0-9] <*password:* a-zA-Z0-9,.;'"!?>

Vengono inviate le credenziali del nuovo utente.Se il processo di registrazione va a buon fine, viene aggiornato il parametro *registrato* nell'oggetto Utente appositamente creato.



<b>AUTENTICAZIONE</b> -- PROTOTIPO COMANDO: authentication 

Vengono inviate le credenziali dell'utente attuale e richiesto un token.Dopo il processo di autenticazione, il parametro *token* nell'oggetto Utente viene aggiornato qualora sia stato necessario creare un nuovo token/sostituire il token scaduto. Viene aggiornato anche il parametro *autenticato* nell'oggetto utente.



<b>INVIARE MESSAGGI</b> -- PROTOTIPO COMANDO: send <*text:* a-zA-Z0-9,.;'"!?> [*receiver:* a-zA-Z0-9] 

Viene creato un 'pacchetto' contenente un messaggio, mittente, destinatario, timestamp e token del mittente. Successivamente viene inviato alla web-api.



<b>CARICARE UN PROFILO</b> -- PROTOTIPO COMANDO: load [*username:* a-zA-Z0-9] 

Qualora l'utente specificato sia presente nella cache di memoria locale, il corrispettivo oggetto Utente viene caricato sul Client.



<b>HELP</b> -----> ANCORA DA IMPLEMENTARE -- PROTOTIPO COMANDO: help

Viene stampata una breve documentazione su tutte le function del Prompt.



<b>CAMBIARE L'INDIRIZZO HOST</b> -- PROTOTIPO COMANDO: address <*address:* a-zA-Z0-9,.;'"!?>  

Viene aggiornato l'indirizzo del server attualmente utilizzato con quello specificato.



<b>INFORMAZIONI INDIRIZZO HOST</b> -- PROTOTIPO COMANDO: addressinfo  

Viene mostrato l'indirizzo del server attualmente utilizzato.



<b>INFORMAZIONI UTENTE</b> -- PROTOTIPO COMANDO: info  

Vengono mostrate le informazioni dell'utente attualmente collegato.



<b>INTERRUZIONE DEL SERVIZIO</b> --  PROTOTIPO COMANDO: exit  

Viene interrotto il servizio del Client.



<b>GESTIONE PROFILI</b> --  PROTOTIPO COMANDO: erase [username]  

Viene eliminato il profilo selezionato dalla cache. Se viene specificato 'all', viene eliminata tutta la cache.



#------------------------#



<b>RICEVERE MESSAGGI</b> 

Ogni secondo, una funzione richiede alla web-api i messaggi in arrivo per l'utente attualmente collegato e li stampa evidenziando tutte le informazioni relative ad essi
