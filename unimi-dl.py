#!/usr/bin/env python3

from downloader_creator import createDownloader
import argparse
import json
import json
import logging


def main():
    parser = argparse.ArgumentParser(description="UniMi's material downloader")
    parser.add_argument("url", metavar="URL", type=str,
                        help="URL of the video(s) to download")
    parser.add_argument("-p", "--platform", metavar="platform",
                        type=str, default="ariel", choices=["ariel"], help="platform to download the video(s) from")
    parser.add_argument("-c", "--credentials", metavar="PATH",
                        type=str, default="./unimi-dl_credentials.json", help="credentials to be used for logging into the platform")
    parser.add_argument("-o", "--output", metavar="PATH",
                        type=str, default="./", help="path to download the video(s) into")
    parser.add_argument("-v", "--verbose", metavar="log level", type=str, nargs="?", default="WARNING", const="DEBUG",
                        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"], help="verbosity level")

    args = parser.parse_args()

    log_level = {
        "CRITICAL": 50,
        "ERROR": 40,
        "WARNING": 30,
        "INFO": 20,
        "DEBUG": 10,
        "NOTSET": 0
    }

    logging.basicConfig(level=log_level[args.verbose])

    videos_url = args.url
    cache = "unimi-dl_downloaded.json"
    platform = args.platform
    credentials = json.load(open(args.credentials, "r"))  # to check
    email = credentials["ariel_email"]
    password = credentials["ariel_password"]

    if email == None or password == None:
        logging.error("missing credentials")
        exit()

    downloader = createDownloader(email, password, platform)
    videos_links = downloader.get_videos(videos_url)
    with open(cache, "r+") as downloaded_json:
        downloaded = json.load(downloaded_json)
        logging.info(videos_links)
        for link in videos_links:
            if link not in downloaded[platform]:
                downloaded_json.seek(0)
                downloader.download(link, args.output)
                downloaded[platform].append(link)
                downloaded_json.write(json.dumps(downloaded))
                downloaded_json.truncate()
            # maybe substitute with json.dump ?

    logging.info("downloaded")


if __name__ == "__main__":
    main()
