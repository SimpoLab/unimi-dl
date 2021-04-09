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
from json.decoder import JSONDecodeError
from requests import __version__ as reqv
from youtube_dl.version import __version__ as ytdv
from unimi_dl.__init__ import __version__ as version
import argparse
import json
import logging
import os
import pathlib
import platform as pt
import sys

from .downloader.downloader_creator import createDownloader


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

    parser = argparse.ArgumentParser(
        description=f"Unimi material downloader v. {version}")
    parser.add_argument("url", metavar="URL", type=str,
                        help="URL of the video(s) to download")
    parser.add_argument("-p", "--platform", metavar="platform",
                        type=str, default="ariel", choices=["ariel"],
                        help="platform to download the video(s) from (default: ariel)")
    parser.add_argument("-s", "--save", action="store_true",
                        help=f"saves credentials (unencrypted) in {local}/credentials.json")
    parser.add_argument("--ask", action="store_true",
                        help=f"asks credentials even if stored")
    parser.add_argument("-c", "--credentials", metavar="PATH",
                        type=str, default=os.path.join(
                            local, "credentials.json"),
                        help="path of the credentials json to be used for logging into the platform")
    parser.add_argument("-o", "--output", metavar="PATH",
                        type=str, default=os.getcwd(), help="directory to download the video(s) into")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    # init
    log = os.path.join(local, "log.txt")
    cache = os.path.join(local, "downloaded.json")
    url = args.url.replace("\\", "")
    platform = args.platform

    logging.basicConfig(filename=log, level=logging.DEBUG)
    main_logger = logging.getLogger("main")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_loglevel = logging.WARNING
    if args.verbose:
        stdout_loglevel = logging.INFO
    stdout_handler.setLevel(stdout_loglevel)
    main_logger.addHandler(stdout_handler)

    main_logger.debug("=============job-start=============")
    main_logger.debug(f"""Detected system info:
    unimi-dl: {version}
    OS: {pt.platform()}
    Release: {pt.release()}
    Version: {pt.version()}
    Local: {local}
    Python: {sys.version}
    Requests: {reqv}
    YoutubeDL: {ytdv}
    Cache: {cache}""")

    main_logger.debug(f"""Request info:
    URL: {url}
    Platform: {platform}
    Save: {args.save}
    Ask: {args.ask}
    Credentials: {args.credentials}
    Output: {args.output}""")

    email = None
    password = None
    creds = {}
    if os.path.isfile(args.credentials):
        with open(args.credentials, "r") as cred_json:
            try:
                creds = json.load(cred_json)
            except JSONDecodeError:
                main_logger.warning("Error parsing credentials json")
            try:
                email = creds[platform]["email"]
                password = creds[platform]["password"]
            except KeyError:
                pass

    if email == None or password == None or args.ask:
        main_logger.info(f"Asking credentials for platform '{platform}'")
        print(f"Credentials for '{platform}'")
        email = input(f"username/email: ")
        password = getpass(f"password (input won't be shown): ")
        if args.save:
            creds[platform] = {"email": email, "password": password}
            head, _ = os.path.split(args.credentials)
            if not os.access(head, os.W_OK):
                main_logger.warning(f"Can't write to directory {head}")
            else:
                with open(args.credentials, "w") as new_credentials:
                    new_credentials.write(json.dumps(creds))
                    main_logger.info(
                        f"Credentials saved succesfully in {local}")

    downloader = createDownloader(email, password, platform, stdout_loglevel)
    videos_links = downloader.get_videos(url)
    link_list = ""
    for link in videos_links:
        link_list += f"\t{url}\n"
    main_logger.info("Links:\n{}".format(link_list.removesuffix("\n")))

    downloaded = {platform: []}
    if not os.path.isfile(cache):
        dl_json = open(cache, "w")
    else:
        dl_json = open(cache, "r+")
        if os.stat(cache).st_size:
            try:
                downloaded = json.load(dl_json)
            except json.decoder.JSONDecodeError:
                main_logger.warning("Error parsing cache json")

    if not os.access(args.output, os.W_OK):
        main_logger.warning(f"can't write to directory {args.output}")
    else:
        for link in videos_links:
            main_logger.info(
                f"Not downloading {link} since it'd already been downloaded")
            if link not in downloaded[platform]:
                downloader.download(link, args.output)
                downloaded[platform].append(link)

                dl_json.seek(0)
                dl_json.write(json.dumps(downloaded))
                dl_json.truncate()
        dl_json.close()

        main_logger.info("Downloaded completed")
