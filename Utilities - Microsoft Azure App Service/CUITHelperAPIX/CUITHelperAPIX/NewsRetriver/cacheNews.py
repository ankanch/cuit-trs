#coding:utf-8
import os

def refreshCache(data,cachefilename):
    try:
        f = open(cachefilename,'w')
        f.write(data)
        f.close()
    except Exception as e:
        return "CACHE ERROR：refresh <br/>please contact kanch@akakanch.com<hr/>"
    return "OK<hr/>"

def checkNewNews(newsdata,cachefilename):
    sourcedata = ""
    newslist = newsdata
    try:
        f = gcs.open(cachefilename,'r')
        sourcedata = f.read()
        f.close()
    except Exception as e:
        return "CACHE ERROR：check <br/>please contact kanch@akakanch.com<hr/>"
    rawlist = sourcedata.split("<br/>")
    newslist = newsdata.split("<br/>")
    newupdate = "NO UPDATE YET"
    for news in newslist:
        if news not in rawlist:
            newupdate = newupdate + news + "<br/>"
    if newupdate != "NO UPDATE YET":
        return newupdate.replace("NO UPDATE YET","")
    return newupdate
