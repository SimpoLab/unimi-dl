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


from __future__ import annotations
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
from .multi_select import WrongSelectionError, multi_select
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
    if not set(["--cleanup-downloaded", "--wipe-credentials"]) & set(sys.argv):
        parser.add_argument("url", metavar="URL", type=str,
                            help="URL of the video(s) to download")
    parser.add_argument("-p", "--platform", metavar="platform",
                        type=str, default="ariel", choices=["ariel", "panopto"],
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
    parser.add_argument("-a", "--all", action="store_true",
                        help="download all videos not already present")
    parser.add_argument('--version', action='version',
                        version=f"%(prog)s {udlv}")
    modes = parser.add_argument_group("other modes")
    modes.add_argument("--simulate", action="store_true",
                       help=f"retrieve video names and manifests, but don't download anything nor update the downloaded list")
    modes.add_argument("--add-to-downloaded-only",
                       action="store_true", help="retrieve video names and manifests, but don't download anything, only update the downloaded list")
    modes.add_argument("--cleanup-downloaded", action="store_true",
                       help="interactively select what videos to clean from the downloaded list")
    modes.add_argument("--wipe-credentials",
                       action="store_true", help="delete stored credentials")

    opts = parser.parse_args()
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


def get_credentials(credentials_path: str, ask: bool, save: bool) -> tuple[str, str]:
    main_logger = logging.getLogger(__name__)
    email = None
    password = None
    creds = {}
    if os.path.isfile(credentials_path):
        with open(credentials_path, "r") as credentials_file:
            try:
                creds = json_load(credentials_file)
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
            head, _ = os.path.split(credentials_path)
            if not os.access(head, os.W_OK):
                main_logger.warning(f"Can't write to directory {head}")
            else:
                with open(credentials_path, "w") as new_credentials:
                    new_credentials.write(json_dumps(creds))
                    main_logger.info(
                        f"Credentials saved succesfully in {credentials_path}")
    return email, password


def get_downloaded(downloaded_path: str) -> tuple[dict[str, dict[str, str]], TextIOWrapper]:
    main_logger = logging.getLogger(__name__)
    downloaded_dict = {}
    if not os.path.isfile(downloaded_path):
        downloaded_file = open(downloaded_path, "w")
    else:
        downloaded_file = open(downloaded_path, "r+")
        if os.stat(downloaded_path).st_size:
            try:
                downloaded_dict = json_load(downloaded_file)
            except JSONDecodeError:
                main_logger.warning(
                    f"Error parsing downloaded json. Consider deleting {downloaded_path}")
    return downloaded_dict, downloaded_file


def download(output_basepath: str, manifest_dict: dict[str, str], downloaded_dict: dict, downloaded_file: TextIOWrapper, simulate: bool, add_to_downloaded_only: bool):
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
        for filename in manifest_dict:
            manifest = manifest_dict[filename]
            if manifest not in downloaded_dict:
                output_path = os.path.join(output_basepath, filename)
                ydl_opts["outtmpl"] = output_path + ".%(ext)s"
                main_logger.info(f"Downloading {filename}")
                if not simulate:
                    if not add_to_downloaded_only:
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([manifest])
                    downloaded_dict[manifest] = filename

                    downloaded_file.seek(0)
                    downloaded_file.write(json_dumps(downloaded_dict))
                    downloaded_file.truncate()
            else:
                main_logger.info(
                    f"Not downloading {filename} since it'd already been downloaded")
        downloaded_file.close()

    main_logger.info("Downloaded completed")


def cleanup_downloaded(downloaded_path: str) -> None:
    main_logger = logging.getLogger(__name__)
    downloaded_dict, downloaded_file = get_downloaded(downloaded_path)

    if len(downloaded_dict) == 0:
        main_logger.warning("The downloaded list is empty!")
        return
    choices = list(downloaded_dict.keys())
    entt = list(downloaded_dict.values())
    main_logger.debug("Prompting user")
    try:
        chosen = multi_select(choices, entries_text=entt,
                              selection_text="\nVideos to remove from the downloaded list: ")
    except WrongSelectionError:
        main_logger.error("Your selection is not valid")
        exit(1)
    main_logger.debug(f"{len(chosen)} names chosen")
    if len(chosen) != 0:
        for manifest in chosen:
            downloaded_dict.pop(manifest)
        downloaded_file.seek(0)
        downloaded_file.write(json_dumps(downloaded_dict))
        downloaded_file.truncate()
    downloaded_file.close()
    main_logger.info("Cleanup done")


def wipe_credentials(credentials_path: str) -> None:
    main_logger = logging.getLogger(__name__)
    if not os.path.isfile(credentials_path):
        main_logger.warning("Credentials file not found")
        return
    main_logger.debug("Prompting user")
    choice = input(
        "Are you sure you want to delete stored credentials? [y/N]: ").lower()
    if choice == "y" or choice == "yes":
        os.remove(credentials_path)
        main_logger.info("Credentials file deleted")
    else:
        main_logger.info("Credentials file kept")


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

    if opts.cleanup_downloaded:
        main_logger.debug("MODE: DOWNLOADED CLEANUP")
        cleanup_downloaded(downloaded_path)
        main_logger.debug(
            f"=============job end at {datetime.now()}=============\n")
        exit(0)
    elif opts.wipe_credentials:
        main_logger.debug("MODE: WIPE CREDENTIALS")
        wipe_credentials(opts.credentials)
        main_logger.debug(
            f"=============job end at {datetime.now()}=============\n")
        exit(0)

    opts.url = opts.url.replace("\\", "")
    main_logger.debug(f"""MODE: {"SIMULATE" if opts.simulate else "ADD TO DOWNLOADED ONLY" if opts.add_to_downloaded_only else "DOWNLOAD"}
    Request info:
    URL: {opts.url}
    Platform: {opts.platform}
    Save: {opts.save}
    Ask: {opts.ask}
    All: {opts.all}
    Credentials: {opts.credentials}
    Output: {opts.output}""")

    email, password = get_credentials(opts.credentials, opts.ask, opts.save)

    all_manifest_dict = getPlatform(
        email, password, opts.platform).get_manifests(opts.url)

    if len(all_manifest_dict) == 0:
        main_logger.warning("No videos found")
    else:
        if opts.all or opts.platform == "panopto":
            manifest_dict = all_manifest_dict
        else:
            try:
                selection = multi_select(
                    list(all_manifest_dict.keys()), selection_text="\nVideos to download: ")
            except WrongSelectionError:
                main_logger.error("Your selection is not valid")
                exit(1)
            manifest_dict = {
                name: all_manifest_dict[name] for name in selection}

        if len(manifest_dict) != 0:
            main_logger.info(f"Videos: {list(manifest_dict.keys())}")

            downloaded_dict, downloaded_file = get_downloaded(downloaded_path)

            download(opts.output, manifest_dict, downloaded_dict,
                     downloaded_file, opts.simulate, opts.add_to_downloaded_only)
            downloaded_file.close()
    main_logger.debug(
        f"=============job end at {datetime.now()}=============\n")
