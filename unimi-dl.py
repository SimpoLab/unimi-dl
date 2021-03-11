#!/usr/bin/env python3

import json
import argparse
import json
import logging
import ariel


def main():
    parser = argparse.ArgumentParser(description="UniMi's material downloader")
    parser.add_argument('url', metavar='url', type=str)
    parser.add_argument('--credentials', metavar="path", type=str, default='./unimi-dl_credentials.json')
    parser.add_argument('--output', metavar="path", type=str, default='./')
    parser.add_argument('--verbose', metavar='log level', type=str, nargs='?', default='WARNING', const='DEBUG',
        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'])

    args = parser.parse_args()

    log_level = {
        'CRITICAL': 50,
        'ERROR': 40,
        'WARNING': 30,
        'INFO': 20,
        'DEBUG': 10,
        'NOTSET': 0
    }

    logging.basicConfig(level=log_level[args.verbose])

    videos_url  = args.url
    cache      = "unimi-dl_downloaded.json"
    credentials = json.load(open(args.credentials, "r"))
    ariel_email = credentials['ariel_email']
    ariel_password = credentials['ariel_password']

    if ariel_email == None or ariel_password == None:
        logging.warning("Mi servono le credenziali!")

    videos_page = ariel.get_videos_page(videos_url, ariel_email, ariel_password)
    manifests = ariel.get_manifests(videos_page)
    downloaded_json = json.load(open(cache, "r"))
    dl_json_changed = False
    logging.info(manifests)
    for manifest in manifests:
        if manifest not in downloaded_json['ariel']:
            ariel.download(manifest, args.output)
            downloaded_json['ariel'].append(manifest)
            dl_json_changed = True
    if dl_json_changed:
        open(cache, "w").write(json.dumps(downloaded_json))

    logging.info("Finito download")

if __name__ == '__main__':
    main()
