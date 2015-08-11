from bs4 import BeautifulSoup
import requests
import sys


def get_txt_href(link):
    """Given <a> tag, returns the tuple (txt, web_address)"""
    # XXX: handle cases where <a> nests other tags
    children = list(link.children)
    if len(children) >= 1:
        txt = children[0]
    else:
        txt = '_'
    return (txt, link.get('href'))


def is_external(href):
    return href.startswith('http')


def wikitext_link(txt, href):
    return "[%s %s]" % (href, txt)


def bullet(txt):
    """
    Given a txt return the bulleted form
    """
    return "* " + txt + "\n"


def wikitext(ur):
    r = requests.get(url)

    data = r.text
    soup = BeautifulSoup(data)
    links = list(soup.find_all('a'))
    href_txt = [get_txt_href(link) for link in links]

    wikitext_lines = [bullet(wikitext_link(txt, href))
                      for txt, href in href_txt if is_external(href)]
    return "".join(wikitext_lines)


if __name__ == "__main__":
    url = sys.argv[1]
    print(wikitext(url))
