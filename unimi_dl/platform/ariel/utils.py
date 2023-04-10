from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

from unimi_dl.platform.session_manager.unimi import UnimiSessionManager
from unimi_dl.downloadable import Attachment

API = "/v5/frm3/"  # API version of ariel
OFFERTA_FORMATIVA = "https://ariel.unimi.it/Offerta/myof"  # offerta formativa
CONTENUTI = "ThreadList.aspx?name=contenuti"  # contents endpoint of a course


def findAllContentTables(html: str) -> list[Tag]:
    result = []
    page = BeautifulSoup(html, "html.parser")
    tbodies = page.find_all("tbody")
    for tbody in tbodies:
        if isinstance(tbody, Tag):
            result.append(tbody)
    return result


def findAllRows(tbody: Tag) -> list[Tag]:
    result = []
    trs = tbody.find_all("tr", recursive=False)  # , class_="sticky")
    for tr in trs:
        if isinstance(tr, Tag):
            result.append(tr)
    return result


def findAllAttachments(tr: Tag, base_url: str) -> list[Attachment]:
    attachments = []
    videos = findAllVideos(tr)
    documents = findAllDocuments(tr, base_url)
    attachments = attachments + videos + documents
    return attachments


def findAllVideos(tr: Tag) -> list[Attachment]:
    """
    Retrieves all the <video> in the `tr` abd creates an `Attachment` using:
        `name`: extracts the name from the `url`, which is the `manifest.m3u8`
        `url`: a http-valid url ending with `manifest.m3u8`
        `description`: the description of the post in which the video is located
        `filetype`: "video"
    """
    attachments = []
    videos = tr.find_all("video")
    for video in videos:
        url = ""
        if isinstance(video, Tag):
            url = findVideoUrl(video)

        # extracts the video name from the `manifest.m3u8`
        name = url.replace("/manifest.m3u8", "")
        name = name.split("mp4:")[-1]
        name = name.split("/")[-1]

        section_name = ""
        description = findPostDescription(tr)
        attachments.append(
            Attachment(
                name=name,
                url=url,
                section_name=section_name,
                description=description,
                filetype="video",
            )
        )

    return attachments


def findVideoUrl(video: Tag) -> str:
    url = ""
    source = video.find("source")
    if source is None or isinstance(source, NavigableString):
        return url
    url = source.get("src")
    if isinstance(url, list):
        raise Exception("Video url shouldn't be a list")

    if url is None:
        url = ""

    return url


def findAllDocuments(tr: Tag, base_url: str) -> list[Attachment]:
    attachments = []
    a_tags = tr.find_all("a", class_=["filename"])
    if a_tags:
        pass
    #        print(tr)
    #        input()
    #        print(a_tags)
    #        input()
    for a in a_tags:
        if not isinstance(a, Tag):
            continue

        name = findDocumentName(a)
        # excluding ../frm3 from the url
        url = base_url + API + getTagHref(a)[8:]
        section_name = ""
        description = findPostDescription(tr)
        attachments.append(
            Attachment(
                name=name,
                url=url,
                section_name=section_name,
                description=description,
                filetype="document",
            )
        )

    return attachments


def findDocumentName(a: Tag) -> str:
    name = a.get_text()

    return name


def getTagHref(tag: Tag) -> str:
    href = tag.get("href")

    if not isinstance(href, str):
        href = ""

    return href


def findPostDescription(tr: Tag) -> str:
    description = ""
    div = tr.find("div", class_="arielMessageBody")

    if isinstance(div, Tag):
        description = div.get_text()

    return description


def findMessageTitle(tr: Tag) -> str:
    title = ""
    h2 = tr.find("h2", class_=["arielTitle", "arielStick"])
    if isinstance(h2, Tag):
        spans = h2.select("span")
        for span in spans:  # title should be the last `span` tag
            if isinstance(span, Tag):
                title = span.get_text()
    return title


def getPageHtml(url: str) -> str:
    session = UnimiSessionManager.getSession()
    r = session.get(url)
    r.raise_for_status()
    return r.text


def findAllArielRoomsList(html: str) -> list[Tag]:
    """
    TODO: should be removed
    Finds all the `tbody` under "Sottoambienti"
    """
    rooms = []
    page = BeautifulSoup(html, "html.parser")
    forum_header = page.find("div", id="forum-header")
    if not isinstance(forum_header, Tag):
        pass
    else:
        span = forum_header.find("span", class_="postbody")
        if not isinstance(span, Tag):
            pass
        else:
            a = span.find("a")
            if isinstance(a, Tag):
                parent = a.parent
                if not isinstance(parent, Tag):
                    a.parent = Tag()
                    parent = a.parent
                    parent.parent = Tag()
                parent.name = "tr"
                tbody = parent.parent
                if isinstance(tbody, Tag):
                    tbody.name = "tbody"
                    rooms.append(tbody)

    tbodies = page.find_all("tbody", class_="arielRoomList")
    for tbody in tbodies:
        if isinstance(tbody, Tag):
            rooms.append(tbody)
    return rooms


def findAllArielThreadList(html: str) -> list[Tag]:
    """
    Finds all the `tbody` under "Archivio file"
    """
    rooms = []
    page = BeautifulSoup(html, "html.parser")
    tbodies = page.find_all("tbody", class_="arielThreadList")
    for tbody in tbodies:
        if isinstance(tbody, Tag):
            rooms.append(tbody)
    return rooms


def findAllATags(tr: Tag) -> list[Tag]:
    result = []
    a_tags = tr.find_all("a")
    for a in a_tags:
        if isinstance(a, Tag) and isinstance(a.get("href"), str):
            result.append(a)

    return result


def findTableType(tbody: Tag) -> str:
    """
    Return "room" if there are other subsections,
        "thread" if there are some contents
    """
    if tbody.has_attr("class"):
        if "arielRoomList" in tbody["class"]:
            return "room"

        if "arielThreadList" in tbody["class"]:
            return "thread"

    return ""
