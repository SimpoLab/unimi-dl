# unimi-dl
Script in Python 3 per scaricare videolezioni dai portali usati da Unimi.

Al momento l'unico portale supportato è Ariel


## Installazione
[WIP]

Scaricare Python, youtube-dl, clonare la repo.


## Utilizzo
[WIP]

Per ora (presto diventerà più comodo) è necessario un file `unimi-dl_credentials.json` con le proprie credenziali esplicitate come segue:

```json
{
	"ariel_email": "tua_email",
	"ariel_password": "tua_password"
}
```

e un file `unimi-dl_downloaded.json` che conterrà i manifest dei video già scaricati (per evitare di riscaricarli), che inizialmente deve avere il seguente contenuto:
```json
{
	"ariel": [
	]
}
```

```
python unimi-dl.py "https://unsito.ariel.ctu.unimi.it/paginadelleregistrazioni"
```


## Disclaimer
[WIP]

No, non è illegale.


## Contributing
Sul progetto [General TODO] si trovano i prossimi obiettivi stabiliti dai mantainer principali. Se hai intenzione di sviluppare una di tali feature, controlla prima che non sia negli "In progress" del progetto e nella discussion [Working on] per assicurarti che non ci stia già lavorando qualcuno. Sia se vuoi implementare uno dei sopracitati obiettivi (specialmente in questo caso), sia se vuoi sviluppare una personale idea, ti preghiamo di notificarlo nella suddetta discussion.

Se non hai accesso diretto alla repo, forkala, implementa la tua proposta di modifica in una branch nominata appropriatamente e apri una pull request.

Se sei un mantainer principale (con accesso diretto alla repo), puoi direttamente modificare il project ignorando la discussion.

[Working on]: (https://github.com/aclerici-unimi/unimi-dl/discussions/categories/working-on)
[General TODO]: (https://github.com/aclerici-unimi/unimi-dl/projects/1)


### Code etiquette
- inserire la documentazione quantomeno nelle funzioni e classi principali
- ogni portale ha un modulo suo
- inserire più [type hinting] possibile
- usare la libreria standard a meno che sia particolarmente scomodo
- gli import vanno in ordine alfabetico (`:sort`)
- delimitare le stringhe con `"`

[type hinting]: (https://realpython.com/lessons/type-hinting/)
