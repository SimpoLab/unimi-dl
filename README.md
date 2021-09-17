<div align="center">
  <h1>unimi-dl</h1>
</div>

Script in Python 3 per scaricare videolezioni dai portali usati da Unimi.

[English](README_EN.md)



## What's new - v0.3 Menus
Major improvements to usability.

### Release notes

#### Added
- Interactive menus:
	- The videos to download are now interactively chosen from a list, unless the `-a` option is specified. This behavior doesn't apply on Panopto since every URL corresponds to one video.
	- Cleanup downloaded mode (`--cleanup-downloaded` option) lets the user choose what videos not to consider downloaded anymore (transparent API to `downloaded.json`)
	- Wipe credentials mode (`--wipe-credentials` option) lets the user delete their saved credentials
- Add to downloaded mode (`--add-to-downloaded-only` option) lets the user add the selected videos to the downloaded list without actually downloading them (differs from the `--simulate` option in that the latter doesn't add the videos to the list).
- `-a` option lets the user download all videos which were not previously downloaded (the previous default behavior)

#### Changed
- The default behavior for downloading is now the interactive choice. For the previously default behavior use `-a`
- IMPORTANT: the downloaded list now stores both the manifests and the video titles. The new format is not compatible with the old one, therefore you might have to delete `downloaded.json` (it resides in the same directory specified for `credentials.json` in `unimi-dl --help`). In this case you may find useful using `--add-to-downloaded-only` for re-adding previously downloaded videos.




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
- python 3 (>=3.8)
- ffmpeg

### Python
- requests
- youtube-dl



## Utilizzo
Tieni presente che il software è sotto heavy-development, per cui potrebbe essere necessario o utile [aggiornarlo](#Update) periodicamente.
```
usage: unimi-dl [-h] [-p platform] [-s] [--ask] [-c PATH] [-o PATH] [-v] [-a] [--version] [--simulate] [--add-to-downloaded-only] [--cleanup-downloaded]
                [--wipe-credentials]
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
                        path of the credentials json to be used for logging into the platform
  -o PATH, --output PATH
                        directory to download the video(s) into
  -v, --verbose
  -a, --all             download all videos not already present
  --version             show program's version number and exit

other modes:
  --simulate            retrieve video names and manifests, but don't download anything nor update the downloaded list
  --add-to-downloaded-only
                        retrieve video names and manifests, but don't download anything, only update the downloaded list
  --cleanup-downloaded  interactively select what videos to clean from the downloaded list
  --wipe-credentials    delete stored credentials
```

In modalità download, modalità di default quando viene inserito un URL, il software recupera i video disponibili e mostra un menu in cui l'utente seleziona quali scaricare. La selezione può essere effettuata specificando i numeri che corrispondono ai video come lista di range separati da virgole, ad esempio `1,3-5,12, 14 - 20`. Il menu non viene mostrato per la piattaforma Panopto dal momento che ad ora vi si può scaricare un solo video per volta.

Il programma tiene traccia, in un file di cache, dei video scaricati, in modo da evitare di ripeterne il download.

La modalità simulate (`--simulate`) e la modalità add to downloaded only (`--add-to-downloaded-only`) equivalgono alla modalità download se non nel fatto che la prima simula l'esecuzione senza scaricare né aggiungere alla lista degli scaricati e la seconda aggiunge solo alla lista degli scaricati, senza scaricare.

La modalità cleanup downloaded (`--cleanup-downloaded`) permette di scegliere interattivamente quali video rimuovere dalla lista degli scaricati. La selezione funziona esattamente come quella per scaricare in modalità download.

La modalità wipe credentials (`--wipe-credentials`) permette di eliminare le credenziali salvate con `--save`. Si noti che per sovrascrivere le credenziali salvate con nuove è sufficiente specificare i due flag `--save` e `--ask` contemporaneamente.


### Ariel
Usando il tuo browser, trova la pagina che contiene i video che vuoi scaricare, copiane l'URL e usalo come segue:
```
unimi-dl -p ariel "https://unsito.ariel.ctu.unimi.it/paginadelleregistrazioni"
```

### Panopto (labonline)
Usando il tuo browser, trova la pagina che contiene l'anteprima video che vuoi scaricare. L'anteprima deve apparire in un riquadro con in basso a destra la freccia :arrow_upper_right: (in gergo, un `iframe`). Copia l'URL della pagina e usalo come segue:
```
unimi-dl -p panopto "https://unsito.labonline.ctu.unimi.it/paginedellanteprima"
```




## Features
- [x] non ripetere download già effettuati
- [x] permettere l'eliminazione trasparente delle credenziali
- [x] permettere la scelta interattiva di video da scaricare o eliminare dalla cache
- [x] scaricare video da Ariel
- [x] scaricare video da Panopto
- [x] tenere salvate le credenziali
- [ ] controllare che le credenziali siano valide
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
No, non è illegale. Non stiamo facendo ridistribuzione non autorizzata. Chi ha accesso ai web player può scaricare i video. Crediamo che poter scaricare i video renda molto più semplice fruirne, potendo sfruttare, ad esempio, i vantaggi dei player offline e evitarci il fastidio di una cattiva connessione.



## Issue guideline
Se vuoi segnalarci un bug, o suggerire un miglioramento, il modo migliore per farlo è tramite una [issue](https://github.com/aclerici-unimi/unimi-dl/issues/new/choose). Ricordati di scegliere il giusto tag e, se si tratta di un bug (un malfunzionamento), includi un log. Il log è un file generato da unimi-dl che contiene informazioni utili a risolvere il bug. Puoi trovarlo in `$HOME/.local/share/unimi-dl/log.txt` su Linux, `Users\[proprio utente]\AppData\Roaming\unimi-dl\log.txt` su Windows, e `$HOME/Library/'Application Support'/unimi-dl/log.txt` su MacOS.



## Licenza
[GPL v.3](https://www.gnu.org/licenses/gpl-3.0.en.html)



## Contributing
Sul progetto [General TODO] si trovano i prossimi obiettivi stabiliti dai maintainer principali. Se hai intenzione di sviluppare una di tali feature, controlla prima che non sia negli "In progress" del progetto e nella discussion [Working on] per assicurarti che non ci stia già lavorando qualcuno. Sia se vuoi implementare uno dei sopracitati obiettivi (specialmente in questo caso), sia se vuoi sviluppare una personale idea, ti preghiamo di notificarlo nella suddetta discussion.

Se non hai accesso diretto alla repo, forkala, implementa la tua proposta di modifica in una branch nominata appropriatamente e apri una pull request.

Se sei un maintainer principale (con accesso diretto alla repo), puoi direttamente modificare il project ignorando la discussion.

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
