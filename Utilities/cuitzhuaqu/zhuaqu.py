#coding=utf-8
import urllib2


def getHtml(url):
    page = urllib2.urlopen(url,timeout=5)
    html = page.read()
    return html