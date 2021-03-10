import youtube_dl
import json
import requests
import re
import logging
from os import listdir
from os import path

def get_videos_page(videos_url: str, ariel_email: str, ariel_password: str):
    with requests.Session() as s:
        login_url = 'https://elearning.unimi.it/authentication/skin/portaleariel/login.aspx?url=https://ariel.unimi.it/'

        #login
        payload = {'hdnSilent': 'true'}
        payload['tbLogin'] = ariel_email
        payload['tbPassword'] = ariel_password
        logging.info(f'payload = {payload}')
        s.post(login_url, data=payload)
        return s.get(videos_url)

def get_manifests(videos_page) -> list[str]:
    manifest_regex = re.compile(r"https://.*/manifest\.m3u8")
    match = manifest_regex.findall(videos_page.text)
    logging.debug(match)
    return match

def download(manifest_url: str, videos_url: str, dst_dir: str):
#    prefix = videos_url.removeprefix("https://")
#    prefix = prefix[:prefix.find(".")]
    filename = manifest_url.removeprefix("https://videolectures.unimi.it/vod/mp4:")
    filename = filename.removesuffix("/manifest.m3u8")
    filename = filename.replace('%','%%'); #escaping % for youtube-dl
    filename = path.join(dst_dir, filename)
    logging.debug(f'Downloading {manifest_url} and saved as {filename}')
    #number = filename_number(prefix)
#    filename = "unimi-dl_output/" + prefix + \
#        "_" + number + '.%(ext)s'
    #  filename = prefix + filename_number(prefix) + '.%(ext)s'
    ydl_opts = {'nocheckcertificate': 'true',
                'restrictfilenames': 'true', 'outtmpl': filename}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([manifest_url])
        # print("downloading %s as %s" % (manifest, filename))

def filename_number(prefix):
    ls = listdir("unimi-dl_output")
    file_regex = re.compile(prefix + r'_\d\d\d\.', re.IGNORECASE)
    number_regex = re.compile(r'\d+')
    retval = 1
    logging.info(ls)
    for file in ls:
        match = file_regex.match(file)
        if match:
            num = int(number_regex.search(match.group(0)).group(0))
            if num >= retval:
                retval = num+1
    return '%03d' % retval
