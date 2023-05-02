# Docker

L'utilizzo di Docker serve per creare un ambiente di sviluppo omogeneo.

## Inizializzazione

1. Nella root del progetto copiare `credentials.json`

```bash
cp ~/.local/share/unimi-dl/credentials.json ./
```

2. Buildare il container

```bash
docker-compose up
```

## Utilizzo

Si usa come unimi-dl passandogli gli argomenti ed opzioni.

```bash
docker-compose run unimi_dl
```

Se viene aggiornato il `Dockerfile` o `docker-compose.yml` è opportuno eseguire:

```bash
docker-compose down
docker-compose up --build
```
