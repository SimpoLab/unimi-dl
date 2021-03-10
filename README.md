# unimi-dl
[WIP]

Script in Python 3 per scaricare videolezioni dai portali usati da Unimi.

Al momento l'unico portale supportato è Ariel


# Installazione
[WIP]

Scaricare Python, youtube-dl, clonare la repo.


# Utilizzo
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


# Disclaimer
[WIP]


# Contribute
[WIP]



## TODO
Nota: i TODO non sono vincolanti.

### Funzionamento
- [ ] decidere dove creare la main directory, ossia quella con output e json. Candidati: home (windows?), directory corrente

### Flags
- [ ] scegliere path del file json degli credenziali
- [ ] scegliere path del file json degli scaricati
- [ ] scegliere path della directory dei video
- [ ] scegliere path della main directory (overridato dai soprastanti)
- [ ] generare automaticamente un template json per salvare le credenziali
- [ ] immettere credenziali (warning: shell history) - idea: invece di inserirle direttamente a riga di comando potrebbe essere un flag che attiva la richiesta di immetterle a stdin (password nascoste) a inizio esecuzione
- [ ] verbose

### Features
- [ ] pip package per installazione facile
- [ ] supportare ms stream, panopto, youtube
- [ ] creare automaticamente il json degli scaricati se non presente
- [ ] rilevare se i percorsi di directory e file sono validi, se i file sono leggibili/scrivibili, etc.
- [ ] creare directory che accomuna i video di un prefix
- [ ] log
- [ ] gestire meglio l'output in funzione di log e verbose
- [ ] se necessario, menu per scegliere tra i manifest (se possibile, parsing per capire un titolo sensato del video relativo a un manifest)
- [ ] GUI
