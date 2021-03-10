#!/usr/bin/env python3

import json
from sys import argv
from os import listdir
import re
import argparse
import logging
import ariel

def main():
    parser = argparse.ArgumentParser(description="UniMi's material downloader")
    parser.add_argument('url', metavar='url', type=str)
    parser.add_argument('--credentials', metavar="path", type=str, default='./unimi-dl_credentials.json')
    parser.add_argument('--output', metavar="path", type=str, default='./')
    parser.add_argument('--verbose', metavar='log level', type=str, default='WARNING', 
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

    videos_url = args.url
    credentials = json.load(open(args.credentials, "r"))
    ariel_email = credentials['ariel_email']
    ariel_password = credentials['ariel_password']

    videos_page = ariel.get_videos_page(videos_url, ariel_email, ariel_password)
    manifests = ariel.get_manifests(videos_page)
    downloaded_json = json.load(open("unimi-dl_downloaded.json", "r"))
    dl_json_changed = False
    logging.info(manifests)
    for manifest in manifests:
        logging.info("manifest = " + manifest + "\n")
        if manifest not in downloaded_json['ariel']:
            ariel.download(manifest, videos_url)
            downloaded_json['ariel'].append(manifest)
            dl_json_changed = True
    if dl_json_changed:
        open("unimi-dl_downloaded.json", "w").write(json.dumps(downloaded_json))
    logging.info("Finito download")

if __name__ == '__main__':
    main()
