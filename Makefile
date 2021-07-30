USERNAME=`cut ~/.local/share/unimi-dl/credentials.json -d '"' -f4`
PASSWORD=`cut ~/.local/share/unimi-dl/credentials.json -d '"' -f8`

tests:
	USERNAME=$(USERNAME) PASSWORD=$(PASSWORD) python3 -m unittest unimi_dl/test/test_*.py

test_ariel:
	USERNAME=$(USERNAME) PASSWORD=$(PASSWORD) python3 -m unittest unimi_dl/test/test_ariel.py

test_utility:
	USERNAME=$(USERNAME) PASSWORD=$(PASSWORD) python3 -m unittest unimi_dl/test/test_utility.py

setup:
	#ln -sf ~/.local/share/unimi-dl/credentials.json credentials.json
