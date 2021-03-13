#!/usr/bin/env python3

from downloader_creator import createDownloader
import argparse
import json
import logging
import pathlib
import sys
import os
import getpass

def get_datadir() -> pathlib.Path:
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """

    home = pathlib.Path.home()

    if sys.platform == "win32":
        return home / "AppData/Roaming"
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"
    else:
        raise NotImplementedError

def main():
    local = os.path.join(get_datadir(), "unimi-dl")
    os.mkdir(local)

    parser = argparse.ArgumentParser(description="UniMi's material downloader")
    parser.add_argument("url", metavar="URL", type=str,
        help="URL of the video(s) to download")
    parser.add_argument("-p", "--platform", metavar="platform",
        type=str, default="ariel", choices=["ariel"], 
        help="platform to download the video(s) from")
    parser.add_argument("-s", "--save", action="store_true",
        help=f"Saves credentials in {local}")
    parser.add_argument("-c", "--credentials", metavar="PATH",
        type=str, default=os.path.join(local, "credentials.json"), 
        help="credentials to be used for logging into the platform")
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

    #init
    logging.basicConfig(level=log_level[args.verbose])
    logging.debug(f"local = {local}")
    cache = os.path.join(local, "downloaded.json")

    try:
        with open(args.credentials, "r") as cred:
            credentials = json.load(cred)  # to check
    except FileNotFoundError:
        credentials = {}

    videos_url = args.url
    platform = args.platform

    try:
        email = credentials[platform]["email"]
        password = credentials[platform]["password"]
    except KeyError:
        #handled in the following 
        email = None
        password = None

    #checking
    if email == None or password == None:
        logging.warning(f"Missing credentials for platform '{platform}'")
        email    = input(f"Insert your username/email for '{platform}' platform\nusername/email=")
        password = getpass.getpass(f"Insert your password for the user '{email}' and '{platform}' platform (Note that input won't be shown)\n")

        if args.save:
            credentials[platform] = {"email" : email}
            credentials[platform] = {"password" : password}
            with open(args.credentials, "w") as new_credentials:
                new_credentials.write(json.dumps(credentials))

            logging.info(f"Credentials saved succesfully in {local}")

    downloader = createDownloader(email, password, platform)
    videos_links = downloader.get_videos(videos_url)
    with open(cache, "rw") as downloaded_json:
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
