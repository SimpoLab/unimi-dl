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
unimi-dl.py [-h] [-p platform] [-s] [-c PATH] [-o PATH] [-v [log level]] URL

UniMi's material downloader

positional arguments:
  URL                   URL of the video(s) to download

optional arguments:
  -h, --help            show this help message and exit
  -p platform, --platform platform
                        platform to download the video(s) from
  -s, --save            Saves credentials in /home/<user>/.local/share/unimi-dl
  -c PATH, --credentials PATH
                        credentials to be used for logging into the platform
  -o PATH, --output PATH
                        path to download the video(s) into
  -v [log level], --verbose [log level]
                        verbosity level
```

Ad esempio:
```
python unimi-dl.py "https://unsito.ariel.ctu.unimi.it/paginadelleregistrazioni"
```


## Configurazione
File di cache, log e di configurazione `credentials.json` (opzionale ai fini del funzionamento che serve per memorizzare le credenziali per ogni piattaforma) si trovano in

linux: ~/.local/share/unimi-dl/
macOS: ~/Library/Application Support/unimi-dl/
windows: C:/Users/<USER>/AppData/Roaming/unimi-dl/

```json
{
    "{piattaforma1}": {
        "email": "tua email",
        "password": "tua password"
    },
    ...
}
```


## Disclaimer
[WIP]

No, non è illegale.


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
