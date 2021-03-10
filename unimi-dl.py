#!/usr/bin/env python3

import requests
import json
from sys import argv
import re
from os import listdir
import youtube_dl


def ariel_get_credentials():
    raw_json = json.load(open("unimi-dl_credentials.json", "r"))
    ariel_payload = {'hdnSilent': 'true'}
    if 'ariel_email' in raw_json:
        ariel_payload['tbLogin'] = raw_json['ariel_email']
    if 'ariel_password' in raw_json:
        ariel_payload['tbPassword'] = raw_json['ariel_password']
    return ariel_payload


def ariel_get_videos_page(videos_URL):
    with requests.Session() as s:
        ariel_login_URL = 'https://elearning.unimi.it/authentication/skin/portaleariel/login.aspx?url=https://ariel.unimi.it/'
        ariel_payload = ariel_get_credentials()
        s.post(ariel_login_URL, data=ariel_payload)  # login
        return s.get(videos_URL)


def ariel_get_manifests(videos_page):
    manifest_regex = re.compile(r"https://.*/manifest\.m3u8")
    match = manifest_regex.findall(videos_page.text)
    return match


def ariel_downloadfrommanifest(manifest, videos_URL):
    prefix = videos_URL.removeprefix("https://")
    prefix = prefix[:prefix.find(".")]
    number = filename_number(prefix)
    filename = "unimi-dl_output/" + prefix + \
        "_" + number + '.%(ext)s'
    #  filename = prefix + filename_number(prefix) + '.%(ext)s'
    ydl_opts = {'nocheckcertificate': 'true',
                'restrictfilenames': 'true', 'outtmpl': filename}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([manifest])
        # print("downloading %s as %s" % (manifest, filename))


def filename_number(prefix):
    ls = listdir("unimi-dl_output")
    file_regex = re.compile(prefix + r'_\d\d\d\.', re.IGNORECASE)
    number_regex = re.compile(r'\d+')
    retval = 1
    print(ls)
    for file in ls:
        match = file_regex.match(file)
        if match:
            num = int(number_regex.search(match.group(0)).group(0))
            if num >= retval:
                retval = num+1
    return '%03d' % retval


videos_URL = argv[1]
videos_page = ariel_get_videos_page(videos_URL)
manifests = ariel_get_manifests(videos_page)
downloaded_json = json.load(open("unimi-dl_downloaded.json", "r"))
dl_json_changed = False
for manifest in manifests:
    if manifest not in downloaded_json['ariel']:
        ariel_downloadfrommanifest(manifest, videos_URL)
        downloaded_json['ariel'].append(manifest)
        dl_json_changed = True
if dl_json_changed:
    open("unimi-dl_downloaded.json", "w").write(json.dumps(downloaded_json))
