#!/usr/bin/env python3

import json
import argparse
import json
import logging
from downloader_creator import createDownloader

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
    cache       = "unimi-dl_downloaded.json"
    platform    = "ariel"
    credentials = json.load(open(args.credentials, "r"))
    email       = credentials["ariel_email"]
    password    = credentials["ariel_password"]

    if email == None or password == None:
        logging.warning("Mi servono le credenziali!")
        exit()

    downloader   = createDownloader(email, password, platform)
    videos_links = downloader.get_videos(videos_url)
    downloaded_json = json.load(open(cache, "r"))
    dl_json_changed = False

    logging.info(videos_links)

    for link in videos_links:
        if link not in downloaded_json[platform]:
            downloader.download(link, args.output)
            downloaded_json[platform].append(link)
            dl_json_changed = True
    if dl_json_changed:
        f = open(cache, "w")
        f.write(json.dumps(downloaded_json))

    logging.info("Finito download")

if __name__ == '__main__':
    main()
