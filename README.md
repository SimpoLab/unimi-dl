<div align="center">
  <h1>unimi-dl</h1>
</div>

Script in Python 3 per scaricare videolezioni dai portali usati da Unimi.



## Quickstart
```
pip3 install unimi-dl
unimi-dl --help
```



## Installazione
- Installa ffmpeg e python3 se non presenti
- Scegli uno dei seguenti metodi:

### Con pip (consigliato)
- Installa python3-pip se non presente
- Installa unimi-dl:
```
pip3 install unimi-dl
unimi-dl --help
```

### Clonando con git
- Installa git se non presente
- Installa le [dipendenze](#Dipendenze) se non presenti
- Clona la repo:
```
git clone https://github.com/SimpoLab/unimi-dl.git
```
- Usa il software dalla directory della repo:
```
cd unimi-dl
python3 -m unimi_dl --help
```
Nota: con questo metodo è necessario tenere la repo clonata per fare uso del software.



## Dipendenze

### Esterne
- python 3
- ffmpeg

### Python
- requests
- youtube-dl



## Utilizzo
Al momento l'unico portale supportato è Ariel. Tieni presente che il software è sotto heavy-developement, per cui potrebbe essere necessario o utile [aggiornarlo](#Update) periodicamente.
```
usage: unimi-dl [-h] [-p platform] [-s] [--ask] [-c PATH] [-o PATH] [-v]
                   URL

Unimi material downloader

positional arguments:
  URL                   URL of the video(s) to download

optional arguments:
  -h, --help            show this help message and exit
  -p platform, --platform platform
                        platform to download the video(s) from (default: ariel)
  -s, --save            saves credentials (unencrypted) on disk for future use
  --ask                 asks credentials even if stored
  -c PATH, --credentials PATH
                        path of the credentials json to be used for logging into
			the platform
  -o PATH, --output PATH
                        directory to download the video(s) into
  -v, --verbose		verbose output
```

Il programma tiene traccia, in un file di cache, dei video scaricati, in modo da evitare di ripeterne il download. Per forzare il redownload di uno o più video è sufficiente editare o eliminare tale file. In futuro il programma includerà un modo più automatizzato/user-friendly per farlo.

### Ariel
Usando il tuo browser, trova la pagina che contiene i video che vuoi scaricare, copiane l'URL e usalo come segue:
```
unimi-dl "https://unsito.ariel.ctu.unimi.it/paginadelleregistrazioni"
```
Il programma scaricherà tutti i video della pagina non presenti nella cache.



## Features
- [x] scaricare video da Ariel
- [x] tenere salvate le credenziali
- [x] non ripetere download già effettuati
- [ ] controllare che le credenziali siano valide
- [ ] permettere la scelta interattiva di video da scaricare o eliminare dalla cache
- [ ] scaricare video da Panopto
- [ ] scaricare video da Microsoft Stream



## Update
Il metodo di aggiornamento dipende dal metodo di installazione:

### Con pip
```
pip3 install --upgrade unimi-dl
```

### Con git
```
cd /percorso/della/repo/unimi-dl
git pull
```
(Oppure eliminare la repo e ripetere l'installazione)



## Disclaimer
No, non è illegale. Non stiamo facendo ridistribuzione non autorizzata. Chi ha accesso ai web player può scaricare i video. Crediamo che poter scaricare i video renda molto più semplice fruirne, potendo sfruttare, ad esempio, i vantaggi dei player e evitarci il fastidio di una cattiva connessione.



## Issue guideline
Se vuoi segnalarci un bug, o suggerire un miglioramento, il modo migliore per farlo è tramite una [issue](https://github.com/aclerici-unimi/unimi-dl/issues/new/choose). Ricordati di scegliere il giusto tag e, se si tratta di un bug (un malfunzionamento) includi un log. Il log è un file generato da unimi-dl che contiene informazioni utili a risolvere il bug. Puoi trovarlo in `$HOME/.local/share/unimi-dl/log.txt` su Linux, `Users\[proprio utente]\AppData\Roaming\unimi-dl\log.txt` su Windows, e `$HOME/Library/'Application Support'/unimi-dl/log.txt` su MacOS.



## Licenza
[GPL v.3](https://www.gnu.org/licenses/gpl-3.0.en.html)



## Contributing
Sul progetto [General TODO] si trovano i prossimi obiettivi stabiliti dai mantainer principali. Se hai intenzione di sviluppare una di tali feature, controlla prima che non sia negli "In progress" del progetto e nella discussion [Working on] per assicurarti che non ci stia già lavorando qualcuno. Sia se vuoi implementare uno dei sopracitati obiettivi (specialmente in questo caso), sia se vuoi sviluppare una personale idea, ti preghiamo di notificarlo nella suddetta discussion.

Se non hai accesso diretto alla repo, forkala, implementa la tua proposta di modifica in una branch nominata appropriatamente e apri una pull request.

Se sei un mantainer principale (con accesso diretto alla repo), puoi direttamente modificare il project ignorando la discussion.

[Working on]: https://github.com/aclerici-unimi/unimi-dl/discussions/categories/working-on
[General TODO]: https://github.com/aclerici-unimi/unimi-dl/projects/1


### Code etiquette
- inserire la documentazione quantomeno nelle funzioni e classi principali
- ogni portale ha un modulo suo
- inserire più [type hinting] possibile
- usare la libreria standard a meno che sia particolarmente scomodo
- gli import vanno in ordine alfabetico (`:sort`)
- delimitare le stringhe con `"`
- [best practice comuni]
- per l'implementazione di nuove feature creare sempre un branch

[type hinting]: https://realpython.com/lessons/type-hinting/
[best practice comuni]: https://github.com/naming-convention/naming-convention-guides/tree/master/python
