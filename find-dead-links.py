import requests
from bs4 import BeautifulSoup
from sys import argv


def find_dead_links(url, depth):
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("[" + url + "] is a bad link")
        return
    soup = BeautifulSoup(r.text, "html.parser")

    allLinks = []
    for elem in soup.find_all("a"):
        link = elem.get("href")
        if link.startswith("/"):
            if url.endswith("/"):
                link = url[:-1] + link
            else:
                link = url + link
        if link not in allLinks:
            allLinks.append(link)

    goodLinks = []
    print("On page [" + url + "]:")
    for link in allLinks:
        if not link.startswith("#"):
            try:
                newReq = requests.get(link)
                if newReq.status_code not in [200, 302]:
                    print("\t[" + link + "] is a bad link")
                else:
                    goodLinks.append(link)
            except:
                print("\t[" + link + "] is a bad link")

    if depth > 0:
        for link in goodLinks:
            find_dead_links(link, depth-1)


if __name__ == "__main__":
    if len(argv) not in [2, 3]:
        print("USAGE: find-dead-links <URL> [-<depth>]")
        exit(1)
    depth = 0
    for opt in argv[1:]:
        if opt.startswith("-"):
            try:
                depth = int(opt[1:])
            except ValueError:
                print("Invalid value for depth: {}".format(opt[1:]))
                exit(1)
        else:
            url = opt

    find_dead_links(url, depth)
