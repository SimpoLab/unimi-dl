import youtube_dl
import json
import requests
import re
import logging
from os import listdir

def get_credentials():
    raw_json = json.load(open("unimi-dl_credentials.json", "r"))
    payload = {'hdnSilent': 'true'}
    if 'ariel_email' in raw_json:
        payload['tbLogin'] = raw_json['ariel_email']
    if 'ariel_password' in raw_json:
        payload['tbPassword'] = raw_json['ariel_password']
    return payload


def get_videos_page(videos_URL):
    with requests.Session() as s:
        login_URL = 'https://elearning.unimi.it/authentication/skin/portaleariel/login.aspx?url=https://ariel.unimi.it/'
        payload = get_credentials()
        logging.info(f'payload = {payload}')
        s.post(login_URL, data=payload)  # login
        return s.get(videos_URL)

def get_manifests(videos_page):
    manifest_regex = re.compile(r"https://.*/manifest\.m3u8")
    match = manifest_regex.findall(videos_page.text)
    return match


def download(manifest, videos_URL):
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
