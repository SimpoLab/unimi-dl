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


import unimi_dl
from . import __version__ as udlv
from .multi_select import multi_select
from argparse import ArgumentParser, Namespace
from datetime import datetime
from getpass import getpass
from requests import __version__ as reqv
from unimi_dl.platform import *
from unimi_dl.course import *
from unimi_dl.downloadable import *
from unimi_dl.utility.credentials_manager import CredentialsManager
from unimi_dl.utility.download_manager import DownloadManager
from youtube_dl.version import __version__ as ytdv
import logging
import os
import platform as pt
import sys


def get_args() -> Namespace:
    parser = ArgumentParser(description=f"Unimi material downloader v. {udlv}")
    parser.add_argument(
        "-u", "--url", metavar="url", type=str, help="URL of the video(s) to download"
    )
    parser.add_argument(
        "-p",
        "--platform",
        metavar="platform",
        type=str,
        default="ariel",
        choices=unimi_dl.AVAILABLE_PLATFORMS,
        help="platform to download the video(s) from (default: all)",
    )
    parser.add_argument(
        "-s",
        "--save",
        action="store_true",
        help=f"saves credentials (unencrypted) in {unimi_dl.CREDENTIALS}",
    )
    parser.add_argument(
        "--ask", action="store_true", help="asks credentials even if stored"
    )
    parser.add_argument(
        "-c",
        "--credentials",
        metavar="PATH",
        type=str,
        default=unimi_dl.CREDENTIALS,
        help="path of the credentials json to be used for logging into the platform",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="PATH",
        type=str,
        default=os.getcwd(),
        help="directory to download the video(s) into",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="download all videos not already present",
    )
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {udlv}")
    modes = parser.add_argument_group("other modes")
    modes.add_argument(
        "--simulate",
        action="store_true",
        help="retrieve video names and manifests, but don't download anything nor update the downloaded list",
    )
    modes.add_argument(
        "--add-to-downloaded-only",
        action="store_true",
        help="retrieve video names and manifests and only update the downloaded list (no download)",
    )
    modes.add_argument(
        "--cleanup-downloaded",
        action="store_true",
        help="interactively select what videos to clean from the downloaded list",
    )
    modes.add_argument(
        "--wipe-credentials", action="store_true", help="delete stored credentials"
    )

    opts = parser.parse_args()
    return opts


def log_setup(verbose: bool) -> None:
    # silencing spammy logger
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # setting up stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    if verbose:
        logging.getLogger("youtube-dl").setLevel(logging.INFO)
        stdout_handler.setLevel(logging.INFO)
        stdout_handler.setFormatter(logging.Formatter("%(message)s"))
    else:
        stdout_handler.setLevel(logging.WARNING)
        stdout_handler.setFormatter(
            logging.Formatter("%(levelname)s: %(message)s"))

    # setting up file handler
    file_handler = logging.FileHandler(unimi_dl.LOG)
    file_handler.setFormatter(logging.Formatter(
        "%(levelname)s[%(name)s]: %(message)s"))

    # finalizing
    logging.basicConfig(level=logging.DEBUG, handlers=[
                        file_handler, stdout_handler])


def main():
    opts = get_args()
    if not os.path.isdir(unimi_dl.LOCAL):
        os.makedirs(unimi_dl.LOCAL)
    log_setup(opts.verbose)
    main_logger = logging.getLogger(__name__)

    main_logger.debug(
        f"=============job start at {datetime.now()}=============")
    main_logger.debug(
        f"""Detected system info:
    unimi-dl: {udlv}
    OS: {pt.platform()}
    Release: {pt.release()}
    Version: {pt.version()}
    Local: {unimi_dl.LOCAL}
    Python: {sys.version}
    Requests: {reqv}
    YoutubeDL: {ytdv}
    Downloaded file: {unimi_dl.DOWNLOADED}"""
    )

    main_logger.debug(
        f"""MODE: {"SIMULATE" if opts.simulate else "ADD TO DOWNLOADED ONLY" if opts.add_to_downloaded_only else "DOWNLOAD"}
    Request info:
    Platform: {opts.platform}
    Save: {opts.save}
    Ask: {opts.ask}
    All: {opts.all}
    Credentials: {opts.credentials}
    Output: {opts.output}"""
    )

    if opts.url is not None:
        opts.url = opts.url.replace("\\", "")  # sanitize url

    platform = opts.platform  # type: str

    # get credentials
    credentials_manager = CredentialsManager(opts.credentials)
    credentials = credentials_manager.getCredentials()
    email = credentials.email
    password = credentials.password
    if opts.ask or email is None or password is None:
        main_logger.info("Asking credentials")
        print("Insert credentials")
        email = input("username/email: ")
        password = getpass("password (input won't be shown): ")
        if opts.save:
            credentials_manager.setCredentials(email, password)

    download_manager = DownloadManager(unimi_dl.DOWNLOADED)

    if opts.cleanup_downloaded:
        main_logger.debug("MODE: DOWNLOADED CLEANUP")
        downloaded = download_manager.getDownloadFrom(platform)
        to_delete = multi_select(
            downloaded,
            entries_text=downloaded,
            selection_text=f"\nVideos to remove from the '{platform}' downloaded list: ",
        )
        download_manager.wipeDownloaded(platform, to_delete)

    elif opts.wipe_credentials:
        main_logger.debug("MODE: WIPE CREDENTIALS")
        main_logger.debug("Prompting user")
        choice = input(
            "Are you sure you want to delete stored credentials? [y/N]: "
        ).lower()
        if choice == "y" or choice == "yes":
            credentials_manager.wipeCredentials()
            main_logger.info("Credentials file deleted")
        else:
            main_logger.info("Credentials file kept")

    else:
        p = getPlatform(email, password, platform)

        to_download = []
        if isinstance(p, Ariel):
            courses = p.getCourses()
            selected_courses = multi_select(
                courses, courses, "Scegli il corso: "
            )  # type: list[Course]

            for course in selected_courses:
                entries = course.getSections()
                selected_sections = multi_select(
                    entries, entries, "Scegli le sezioni: "
                )  # type: list[Section]
                for section in selected_sections:
                    to_download = to_download + show(section)
        elif platform == "panopto" and opts.url is not None:
            attachments = p.getAttachments(opts.url)
            to_download = to_download + \
                (show(additional_attachments=attachments))
        else:
            print("not supported platform")
            exit(1)

        if not opts.simulate:

            def download(choice: Attachment):
                download_manager.doDownload(
                    attachment=choice,
                    dry_run=opts.add_to_downloaded_only,
                    path=opts.output,
                    platform=platform,
                )

            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(download, to_download)

        download_manager.save()

    main_logger.debug(
        f"=============job end at {datetime.now()}=============\n")


def show(
    section: Section = None, additional_attachments: list[Attachment] = []
) -> list[Attachment]:
    sections = []
    result = []
    if section is not None:
        sections = section.getSubsections()
    choices = sections + section.getAttachments() + additional_attachments  # type: ignore
    selected_choices = multi_select(
        entries=choices,
        entries_text=choices,
        selection_text="Scegli un file o una sezione ",
    )

    for choice in selected_choices:
        if isinstance(choice, Section):
            result = result + show(choice)

        if isinstance(choice, Attachment):
            result.append(choice)
    return result
