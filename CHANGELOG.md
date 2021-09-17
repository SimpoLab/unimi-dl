# CHANGELOG




## v0.3.1 minor release
Installation bugfixes.


### Download
See [PyPI release page](https://pypi.org/project/unimi-dl/0.3.1)


### Release notes

#### Fixed
- minimum Python version is now 3.8




## v0.3 Menus
Major improvements to usability.


### Download
See [PyPI release page](https://pypi.org/project/unimi-dl/0.3.0)


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
- IMPORTANT: the downloaded list now stores both the manifests and the video titles. The new format is not compatible with the old one, therefore you might have to delete `downloaded.json` (it resides in the same directory specified for `credentials.json` in `unimi-dl --help`)




## v0.2.3 minor release
Better regex system.


### Download
See [PyPI release page](https://pypi.org/project/unimi-dl/0.2.3)


### Release notes

#### Changed
- More solid/defensive regex system

#### Fixed
- Compatibility with some Ariel sites (aka Silab issue no. 3)




## v0.2.2 minor release
Added simulation mode.


### Download
See release v0.2.3.


### Release notes

#### Added
- Simulate mode (`--simulate` option) retrieves video names and manifests, but doesn't download anything nor updates the downloaded list

#### Known issues
- Outputs wrong version (0.2.1 instead of 0.2.2)




## v0.2.1 minor release
Bugfix.


### Download
See [PyPI release page](https://pypi.org/project/unimi-dl/0.2.1)


### Release notes

#### Fixed
- #2




## v0.2 Panopto
Compatibility with the Panopto platform and project refactoring.


### Download
See [PyPI release page](https://pypi.org/project/unimi-dl/0.2.0)

 
### Release notes

#### Added
- Compatibility with the Panopto platform, a video streaming service used by various sites including [labonline](https://labonline.ctu.unimi.it)
- Versatile class hierarchy for the different platforms
- `--version` option
- Various improvements to already existing features

#### Fixed
- Compatibility with Python v < 3.9 (see v0.1 release)




## v0.1 Ariel
First decent working version of unimi-dl, compatible with the Ariel platform.


### Download
See [PyPI release page](https://pypi.org/project/unimi-dl/0.1.0)
 

### Release notes

#### Includes
- Compatibility with the [Ariel](https://ariel.unimi.it) platform
- [PyPI package](https://pypi.org/project/unimi-dl)
- Automatically avoid re-downloading videos
- Logging system (and `--verbose` mode)
- Possibility of saving the user's credentials
- Possibility of choosing where to download the files into

#### Known issues
- Due to some methods, this version is incompatible with Python v. < 3.9. This has been later fixed.
