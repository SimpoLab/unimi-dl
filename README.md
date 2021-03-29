<div align="center">
  <h1>unimi-dl</h1>
</div>

Script in Python 3 per scaricare videolezioni dai portali usati da Unimi.

## Quickstart
[WIP]


## Dipendenze
- youtube-dl
- ffmpeg
- python 3
- requests


## Utilizzo
Al momento l'unico portale supportato è Ariel.

```
usage: unimi-dl.py [-h] [-p platform] [-s] [--ask] [-c PATH] [-o PATH] [-v]
                   URL

UniMi material downloader

positional arguments:
  URL                   URL of the video(s) to download

optional arguments:
  -h, --help            show this help message and exit
  -p platform, --platform platform
                        platform to download the video(s) from
  -s, --save            saves credentials (unencrypted) in
                        /home/sgorblex/.local/share/unimi-dl
  --ask                 asks credentials even if stored
  -c PATH, --credentials PATH
                        credentials to be used for logging into the platform
  -o PATH, --output PATH
                        path to download the video(s) into
  -v, --verbose		verbose output
```

Ad esempio:
```
python unimi-dl.py "https://unsito.ariel.ctu.unimi.it/paginadelleregistrazioni"
```


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
