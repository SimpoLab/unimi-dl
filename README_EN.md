# unimi-dl
[Italiano](README.md) | English

Python 3 script for downloading video lessons from the portals used by Unimi.




## Quickstart
```
pip3 install unimi-dl
unimi-dl --help
```



## Installation
- Install ffmpeg and python3 if not present
- Choose one of the following methods:

### Via pip (suggested)
- Install python3-pip if not present
- Install unimi-dl:
```
pip3 install unimi-dl
unimi-dl --help
```

### By cloning with git
- Install git if not present
- Install the [dependencies](#Dependencies) if not present
- Clone the repo:
```
git clone https://github.com/SimpoLab/unimi-dl.git
```
- Use the software from the repo directory:
```
cd unimi-dl
python3 -m unimi_dl --help
```
Note: with this method it is necessary to keep the cloned repo in order to use the software.



## Dependencies

### External
- python 3 (>=3.8)
- ffmpeg

### Python
- requests
- youtube-dl



## Usage
Keep in mind that the software is under heavy-development, therefore it may be necessary or useful to [update it](#Update) regularly.
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

In download mode, the default mode when inserting a URL, the software retrieved the available videos and shows a menu in which the used selects which ones to download. The selection can be made by specifying the numbers corresponding to the videos as a comma separated list of ranges, e.g. `1,3-5,12, 14 - 20`. The menu won't be shown for the Panopto platform since only one video can be downloaded at a time in it at the moment.

The program keeps track, in a cache file, of the downloaded videos, in order to avoid repeating the download.

Simulate and add to downloaded only modes are equivalent to download mode, except the former simulates the execution without downloading nor adding to the downloaded list, and the latter only adds to the downloaded list, without downloading.

Cleanup downloaded mode lets the user interactively choose which videos to remove from the downloaded list. The selection works exactly like the download mode one.

Wipe credentials mode lets the user delete the credentials saved with `--save`. Note that in order to overwrite the saved credentials with new ones it is sufficient to specify both the flags `--save` and `--ask` at the same time.


### Ariel
With your browser, find the page which contains the videos you want to download, then copy its URL and use it as follows:
```
unimi-dl -p ariel "https://asite.ariel.ctu.unimi.it/videospage"
```

### Panopto (labonline)
With your browser, find the page which contains the preview of the video you want to download. The preview has to appear in a square with the :arrow_upper_right: in the lower right corner (to use a slang word, an `iframe`). Copy the URL of the page and use it as follows:
```
unimi-dl -p panopto "https://asite.labonline.ctu.unimi.it/previewpage"
```




## Features
- [x] do not repeat already done downloads
- [x] allow to delete the credentials transparently
- [x] allow to interactively choose what videos to download or delete from the cache
- [x] download videos from Ariel
- [x] download videos from Panopto
- [x] keep the credentials saved
- [ ] check if the credentials are valid
- [ ] download videos from Microsoft Stream



## Update
The update method depends on the installation method:

### With pip
```
pip3 install --upgrade unimi-dl
```

### With git
```
cd /repo/path/unimi-dl
git pull
```
(Or delete the repo and repeat the installation)



## Disclaimer
No, it is not illegal. We are not doing unauthorized redistribution. Who has access to the web player can download the videos. We believe that being able to download the videos makes way easier making use of them, making possible to use, for example, the advantages of an offline player and avoid the annoyance of a bad connection.



## Issue guideline
If you want to report a bug, or suggest an enhancement, the best way to do it is via an [issue](https://github.com/aclerici-unimi/unimi-dl/issues/new/choose). Remember to choose the right tag and, if it's the case of a bug (a malfunction), include a log. A log is a file generated by unimi-dl which contains information useful in solve the bug. You can find it in `$HOME/.local/share/unimi-dl/log.txt` on Linux, `Users\[your user]\AppData\Roaming\unimi-dl\log.txt` on Windows, e `$HOME/Library/'Application Support'/unimi-dl/log.txt` on MacOS.



## Licence
[GPL v.3](https://www.gnu.org/licenses/gpl-3.0.en.html)



## Contributing
On the project [General TODO] you can find the next objectives chosen by the main maintainers. If you want to develop one of such features, check first it is not in the "In progress" column and in the discussion [Working on] to be sure nobody is already working on it. Both if you want to implement one of said features or a personal idea, we ask you yo report it in said discussion.

If you don't have direct access to the repo, fork it, implement your proposal in an appropriately named branch and open a pull request.

If you are a main maintainer (with direct access to the repo), you can directly modify the project, ignoring the discussion.

[Working on]: https://github.com/aclerici-unimi/unimi-dl/discussions/categories/working-on
[General TODO]: https://github.com/aclerici-unimi/unimi-dl/projects/1


### Code etiquette
- insert documentation, at least in the main functions and classes
- each portal has its own module
- insert as much [type hinting] as possible
- use the standard library if it isn't particularly uncomfortable
- sort imports in alphabetic order (`:sort`)
- the string delimiter is `"`
- [common best practices]
- always create a branch for implementing new features

[type hinting]: https://realpython.com/lessons/type-hinting/
[common best practices]: https://github.com/naming-convention/naming-convention-guides/tree/master/python
