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


from argparse import ArgumentParser, Namespace
from datetime import datetime
from getpass import getpass
from io import TextIOWrapper
from json import dumps as json_dumps, load as json_load
from json.decoder import JSONDecodeError
import logging
import os
from pathlib import Path
import platform as pt
import sys

from requests import __version__ as reqv
import youtube_dl
from youtube_dl.version import __version__ as ytdv

from . import __version__ as udlv
from .platform import getPlatform


def get_data_dir() -> Path:
    """ Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming """

    home = Path.home()

    if sys.platform == "win32":
        return home / "AppData/Roaming"
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"
    else:
        raise NotImplementedError


def get_args(local: str) -> Namespace:
    parser = ArgumentParser(
        description=f"Unimi material downloader v. {udlv}")
    parser.add_argument("url", metavar="URL", type=str,
                        help="URL of the video(s) to download")
    parser.add_argument("-p", "--platform", metavar="platform",
                        type=str, default="ariel", choices=["ariel", "panopto"],
                        help="platform to download the video(s) from (default: ariel)")
    parser.add_argument("-s", "--save", action="store_true",
                        help=f"saves credentials (unencrypted) in {local}/credentials.json")
    parser.add_argument("--simulate", action="store_true",
                        help=f"retrieve video names and manifests, but don't download anything nor update the downloaded list")
    parser.add_argument("--ask", action="store_true",
                        help=f"asks credentials even if stored")
    parser.add_argument("-c", "--credentials", metavar="PATH",
                        type=str, default=os.path.join(
                            local, "credentials.json"),
                        help="path of the credentials json to be used for logging into the platform")
    parser.add_argument("-o", "--output", metavar="PATH",
                        type=str, default=os.getcwd(), help="directory to download the video(s) into")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument('--version', action='version',
                        version=f"%(prog)s {udlv}")

    opts = parser.parse_args()
    opts.url = opts.url.replace("\\", "")
    return opts


def log_setup(verbose: bool, local: str) -> None:
    # silencing spammy logger
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # setting up stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    if verbose:
        stdout_handler.setLevel(logging.INFO)
        stdout_handler.setFormatter(
            logging.Formatter("%(message)s"))
    else:
        stdout_handler.setLevel(logging.WARNING)
        stdout_handler.setFormatter(
            logging.Formatter("%(levelname)s: %(message)s"))

    # setting up file handler
    file_handler = logging.FileHandler(os.path.join(local, "log.txt"))
    file_handler.setFormatter(logging.Formatter(
        "%(levelname)s[%(name)s]: %(message)s"))

    # finalizing
    logging.basicConfig(level=logging.DEBUG, handlers=[
                        file_handler, stdout_handler])


def get_credentials(credentials_file: str, ask: bool, save: bool) -> tuple[str, str]:
    main_logger = logging.getLogger(__name__)
    email = None
    password = None
    creds = {}
    if os.path.isfile(credentials_file):
        with open(credentials_file, "r") as cred_json:
            try:
                creds = json_load(cred_json)
            except JSONDecodeError:
                main_logger.warning("Error parsing credentials json")
            try:
                email = creds["email"]
                password = creds["password"]
            except KeyError:
                pass

    if email == None or password == None or ask:
        main_logger.info(f"Asking credentials")
        print(f"Insert credentials")
        email = input(f"username/email: ")
        password = getpass(f"password (input won't be shown): ")
        if save:
            creds = {"email": email, "password": password}
            head, _ = os.path.split(credentials_file)
            if not os.access(head, os.W_OK):
                main_logger.warning(f"Can't write to directory {head}")
            else:
                with open(credentials_file, "w") as new_credentials:
                    new_credentials.write(json_dumps(creds))
                    main_logger.info(
                        f"Credentials saved succesfully in {credentials_file}")
    return email, password


def get_downloaded(downloaded_path: str, platform: str) -> tuple[dict[str, list[str]], TextIOWrapper]:
    main_logger = logging.getLogger(__name__)
    downloaded_list = {platform: []}
    if not os.path.isfile(downloaded_path):
        downloaded_file = open(downloaded_path, "w")
    else:
        downloaded_file = open(downloaded_path, "r+")
        if os.stat(downloaded_path).st_size:
            try:
                downloaded_list = json_load(downloaded_file)
                if platform not in downloaded_list:
                    downloaded_list[platform] = []
            except JSONDecodeError:
                main_logger.warning("Error parsing downloaded json")
    return downloaded_list, downloaded_file


def download(output_basepath: str, manifest_list: list[tuple[str, str]], downloaded_list: dict, downloaded_file: TextIOWrapper, platform: str, simulate: bool):
    main_logger = logging.getLogger(__name__)
    if not os.access(output_basepath, os.W_OK):
        main_logger.error(f"can't write to directory {output_basepath}")
        exit(1)
    else:
        ydl_opts = {
            "v": "true",
            "nocheckcertificate": "true",
            "restrictfilenames": "true",
            "logger": logging.getLogger("youtube-dl")
        }
        for (filename, manifest) in manifest_list:
            if manifest not in downloaded_list[platform]:
                output_path = os.path.join(output_basepath, filename)
                ydl_opts["outtmpl"] = output_path + ".%(ext)s"
                main_logger.info(f"Downloading {filename}")
                if not simulate:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([manifest])
                    downloaded_list[platform].append(manifest)

                    downloaded_file.seek(0)
                    downloaded_file.write(json_dumps(downloaded_list))
                    downloaded_file.truncate()
            else:
                main_logger.info(
                    f"Not downloading {filename} since it'd already been downloaded")
        downloaded_file.close()

    main_logger.info("Downloaded completed")


def main():
    local_path = os.path.join(get_data_dir(), "unimi-dl")
    if not os.path.isdir(local_path):
        os.makedirs(local_path)

    opts = get_args(local_path)
    downloaded_path = os.path.join(local_path, "downloaded.json")
    log_setup(opts.verbose, local_path)
    main_logger = logging.getLogger(__name__)

    main_logger.debug(
        f"=============job start at {datetime.now()}=============")
    main_logger.debug(f"""Detected system info:
    unimi-dl: {udlv}
    OS: {pt.platform()}
    Release: {pt.release()}
    Version: {pt.version()}
    Local: {local_path}
    Python: {sys.version}
    Requests: {reqv}
    YoutubeDL: {ytdv}
    Downloaded file: {downloaded_path}""")
    main_logger.debug(f"""Request info:
    URL: {opts.url}
    Platform: {opts.platform}
    Save: {opts.save}
    Ask: {opts.ask}
    Simulate: {opts.simulate}
    Credentials: {opts.credentials}
    Output: {opts.output}""")

    email, password = get_credentials(opts.credentials, opts.ask, opts.save)

    manifest_list = getPlatform(
        email, password, opts.platform).get_manifests(opts.url)

    main_logger.info(f"Videos: {[video for video, _ in manifest_list]}")

    downloaded_list, downloaded_file = get_downloaded(
        downloaded_path, opts.platform)

    download(opts.output, manifest_list, downloaded_list,
             downloaded_file, opts.platform, opts.simulate)
    main_logger.debug(
        f"=============job end at {datetime.now()}=============\n")
