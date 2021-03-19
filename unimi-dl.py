#!/usr/bin/env python3

# Copyright (C) 2021 Alessandro Clerici Lorenzini and Zhifan Chen.
#
# This file is part of unimi-dl.
#
# unimi-dl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# unimi-dl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with unimi-dl.  If not, see <https://www.gnu.org/licenses/>.


from getpass import getpass
import argparse
import json
from json.decoder import JSONDecodeError
import logging
import os
import pathlib
import sys

from downloader_creator import createDownloader


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

    if not os.path.isdir(local):
        os.makedirs(local)

    parser = argparse.ArgumentParser(description="UniMi's material downloader")
    parser.add_argument("url", metavar="URL", type=str,
                        help="URL of the video(s) to download")
    parser.add_argument("-p", "--platform", metavar="platform",
                        type=str, default="ariel", choices=["ariel"],
                        help="platform to download the video(s) from")
    parser.add_argument("-s", "--save", action="store_true",
                        help=f"saves credentials in {local}")
    parser.add_argument("--ask", action="store_true",
                        help=f"asks credentials even if stored")
    parser.add_argument("-c", "--credentials", metavar="PATH",
                        type=str, default=os.path.join(
                            local, "credentials.json"),
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

    # init
    logging.basicConfig(level=log_level[args.verbose])
    logging.debug(f"local = {local}")
    cache = os.path.join(local, "downloaded.json")
    videos_url = args.url
    platform = args.platform

    email = None
    password = None
    creds = {}
    if os.path.isfile(args.credentials):
        with open(args.credentials, "r") as cred_json:
            try:
                creds = json.load(cred_json)
            except JSONDecodeError:
                pass
            try:
                email = creds[platform]["email"]
                password = creds[platform]["password"]
            except KeyError:
                pass
    if email == None or password == None or args.ask:
        logging.info(f"Missing credentials for platform '{platform}'")
        print("Credentials for '{platform}'")
        email = input(f"username/email: ")
        password = getpass(f"password (input won't be shown): ")
        if args.save:
            creds[platform] = {"email": email, "password": password}
            with open(args.credentials, "w") as new_credentials:
                new_credentials.write(json.dumps(creds))
            logging.info(f"Credentials saved succesfully in {local}")

    downloader = createDownloader(email, password, platform)
    videos_links = downloader.get_videos(videos_url)
    downloaded = {platform: []}
    if not os.path.isfile(cache):
        dl_json = open(cache, "w")
    else:
        dl_json = open(cache, "r+")
        try:
            downloaded = json.load(dl_json)
        except json.decoder.JSONDecodeError:
            pass

    logging.info(videos_links)
    for link in videos_links:
        if link not in downloaded[platform]:
            downloader.download(link, args.output)
            downloaded[platform].append(link)

            dl_json.seek(0)
            dl_json.write(json.dumps(downloaded))
            dl_json.truncate()

    logging.info("downloaded")


if __name__ == "__main__":
    main()
