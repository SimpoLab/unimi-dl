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

from requests_html import HTMLSession
import requests


#from .platform import Platform

#get_credential_type_url = "https://login.microsoftonline.com/common/GetCredentialType?mkt=zh-CN"
login_url = "https://login.microsoftonline.com/common/login"
cookies_url = "https://web.microsoftstream.com/" #post
video_url = "https://web.microsoftstream.com/video/6da2a1a5-7574-4993-a823-34dad667d44b?list=trending"
get_credential_type = "https://login.microsoftonline.com/common/GetCredentialType?mkt=zh-CN"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}

get_credential_type_payload = {
    "username": "zhifan.chen@studenti.unimi.it",
    "isOtherIdpSupported": False,
    "checkPhones": False,
    "isRemoteNGCSupported": True,
    "isCookieBannerShown": False,
    "isFidoSupported": False,
    "originalRequest": "rQIIAYWSO2_TUACF66YEFYmH-AUdkJCQmlzfG5ekUpHyqN26yU3sxHZ8GZB97WA7fmHfJnHEyIAEAgYmRiSWTogJMQASGxMzEn-ACTHBhvsLOMOZvnOGo3Orwtf4_Rt0JqAZdZu7jjvb221Yrr3bdBDYtXmh6d62eTprIrkqANAQUHb90rVbd_7efFP5iJ9uf3_75LEknnE7HmNpvl-vL127Fvk0S_JkxnKWuVZUo0lUf89x3zjubDPfQ7cF1AKtvSZqNOBeswVqZGJCHMjBsKcwYhwuiQ8AhgPQNw4LMzIZkQZgsNYEHGgr0psXA6lkDHOJg2NGIrPA3ZKXZL_kheHEZOdZ0lOQCRVAJur8--bVYfuUefDcksxfu783t2dJFt1Lk5y9qjyrDFM3Pna6SRy7lNXOMTdmPrWYn8SjLEndjPluftBW2qWOz03ux3JIpLAgBga65AHnqLMe-s2FA3W_H_GpieQFha3IOcKARrpnj4XAhmAxgsJCg2Fsh_pSgV5owrw1GJOyh4S07KQBnzhH6pKuk0UfOcgpBGYZuLARXpBYOTVhi_WX3qkNhYBoLHRJ3rGgMHcitSCxE9IjUg6mFeOpN1IN4UTttVdYx2GZ5R0gDs2o5auSmBKk5oMgFG1E4VAj_LjXwYOIiZqkn4x1LIx9Prb0cGXH6ZxOOzlZd1R7ep_XQpJPQRpZkryyDVnFE1UxfdAwgerZa69hB1QwRLEgmnOo6gpT5ytM-RYigYOmgM8UPfXGE8-w1qKnz3G5m5jqOm1okaOPkS6b2uG7SrW8TJTEXytXyu1j39lJs2Tmh-63Le7n1ia48meLe32hPOLAf3T35Y_n-NPD4vWXM2nj64X6aDTrPTBBPW13LXgf1Oup90Do4yJvTsky6IJJRzlxi8mkD48P-H3-RZV7Ua3-qnKPL2582P7vjT9f3vgH0",
    "country": "IT",
    "forceotclogin": False,
    "isExternalFederationDisallowed": False,
    "isRemoteConnectSupported": False,
    "federationFlags": 0,
    "isSignup": False,
    "flowToken": "AQABAAEAAAD--DLA3VO7QrddgJg7WevrKfvy_I58wUZ--Qv1nqCDjzrg2AKdBiG2f1WTT4bdLRYyculE5ecVzUdwM5DEV9g-vxGk_Z33n92NO9WB31Gpg_Aw18Vr_e46bLd_43z5IHX8KpCi_am99QlO7CeVDwjucG27KGALtc9kgllAzHH752kTTP1zSeUPA_3_j6aU1fDCIWUwbTbkdag1_-ckW3YlUTYkeHN5eww21LgQrDnIdBfTZTWZ5ORFam9ZHPcaA59r05l8PwbdGYLrJZ0TbFFuxIyuoJ7h0o23zSG5G3kOqaE1BzqZ-k8pElZWV0ImLB5cePZn41Ju4jhmaLKAu3l6-X4Ov1QEvzYRaEVk0wgXiniZM8KRLMIysSJERNNp_TNXtraHBf2WE1fpEUhWWEGzSCbvHdjd_SaJuNOQ8ZedZshJDR3v7PrbeBsg5CeSkOL8SyjZNhYDtCMMFi_vgg1iuv8MwzwgNjOKBv6eKXuNo8Zc2k5X3a-w0LLAhgaYwR0qXCsywJxruR48xMtsoPVjht3q3NBvasgeKLCXD_AHCCAA",
    "isAccessPassSupported": True
}

login_payload = {
    "i13": "0",
    "login": "zhifan.chen@studenti.unimi.it",
    "loginfmt": "zhifan.chen@studenti.unimi.it",
    "type": "11",
    "LoginOptions": "3",
    "lrt": "true",
    "lrtPartition": "prod2",
    "hisRegion": "eur1",
    "hisScaleUnit": "2",
    "passwd": "Simone@2",
    "ps": "2",
    "psRNGCDefaultType": "",
    "psRNGCEntropy": "",
    "psRNGCSLK": "",
    "canary": "/yaEz4hOr3DbK6let36VbMimUPttXwuxmPzj10mCTeY=6:1",
    "ctx": "rQIIAYWSvW_bRgDFTclR4AJJixYJOmboVMASjxQZ0YADSJZImzaPIs0P85aCH0eT0h2pkCfJJpAhW5ApyJQW6JKt7uap6NSumTx3aIEuBToZ7dJulf-CvuEND7_p4fdlG3TB3hdxKolpjAe7CU7l3X6Io91BIvK7EZAG-GkE4nQg6h2J5_uSWH360Sef3_79-NHP78bff_3tq2evyYsr7knG2KLe6_XWOOrSPK7KukxZzSoc0m5c0t4PHHfDcVetWhafSrIiKLwi8yJQgNzvGr49R1ogGc4Rg74rGqc8b8yGFyfOHEDtiCHfuoTNXIROkhkzPTO1CYC-AQx_woLGEoI7fmzPT_yJAKnL4Bjl5vi8v9kIpGr2S-tjc7hkmXBXZZU3-K_WTlpW9KtFWbNv2r-2zAUujpKDsihwzLp3GC5YHocsL4tpVS5wxXJc7w-t4SZHd6WfFDpBGrlEPuQNLeOTw1Fj5oNVInj5CQWLQNRXsaDQ5BDyMfWy6FSaRQK_mgrSyhVIERFvbQkZCYRaMaxsGQnSDLmMYFSPoIaCmKpyLCYknKgHlmgbBtF1l180WEOuqcHGAdnU9-wVpLYaN96hcab6pobmAX-xDoukdCbsORTREjV2aQvnAJ-NUsdTbOzb6FT1XDS31sbhuWR7yLNdWAbiaBmOR9Ces0s01usEKFUCEh5OFN0b62akqseeo6fWHDWJpqhQIM-TCSmt2UjHnk5DSjLbl1zPgwtDAORM0InbjGDoDK_bnY0CtCw-tB9uvizy5MmiKtOc4Jtt7s_tFv_wn23u_b2NWO3ff_vsj3-_O377_ua2fHm99eFer3cZTpp-ZlbiODqWCWai7EVGTt0pY2fr5QWdNjPA0wMHB_vyHnjT4d50Orcd7tX9rR93_lfLnx5s_Qc1",
    "hpgrequestid": "13dfe203-f9e7-4ba9-92a2-d0f06f81b200",
    "flowToken": "AQABAAEAAAD--DLA3VO7QrddgJg7WevreKasLmdU6mrvkj7peWv0xmEO3u1N8OSMfTDFdsZ7bwhsWxDyhrFIMG60bStFqX9Izj0LLo648ypKWa7O01TZAVoDfb2WF2PETSKQsT2NQRkEEJR_3nAzOzL4lNepu60egJjz82uySHx2v5dQKpzYG67uMFMGwCitrOMV6s1qfvFiE5CY0sikS-VckokokkeSRrzFwZGLeiUrlUljPt6__ObMUhBqBsK7kVHBelFdsxn5qTJW9mQpJTWThLmjdt13zDT6TII4hOczG5hj0sn5-VTCm3w9NInm2yxprsLg4B0q2BdnuX_JFBvYOWBaWTj2nDLw0DLzb0kbfvbZyEry2AlYikCOeo5CMVL7DEBNJk149DyZ_Xu0v-yhT6EKzCID4aJ_rDRV06cKMs4hqSZcBNXAcv08ktZmLDQcj04E-UHUs7UDsj6BOcmTjxGY2QVJePJRcX2ml0Ml4OZ_PASG5ax87FbDMeRpRA07m4fTOL6s36QcGLAo4UfXyRCvhvIjIAA",
    "PPSX": "",
    "NewUser": "1",
    "FoundMSAs": "",
    "fspost": "0",
    "i21": "0",
    "CookieDisclosure": "0",
    "IsFidoSupported": "1",
    "isSignupPost": "0",
    "i2": "1",
    "i17": "",
    "i18": "",
    "i19": "170201"
}

session = requests.Session()
#print(response.cookies.items())
#response = session.post(get_credential_type_url, json=get_credential_type_payload)
response = session.post(login_url, json=login_payload, headers=headers)
response1 = session.get(url=video_url)
with open("response.html", "w") as r:
    r.write(response1.text)
    print(response1.text)
    print(response1.cookies)
    print(f"status code = {response1.status_code}")
