#coding:utf-8
import logging
import os
import cloudstorage as gcs
import webapp2
from google.appengine.api import app_identity

bucket_name = os.environ.get('BUCKET_NAME',app_identity.get_default_gcs_bucket_name())
write_retry_params = gcs.RetryParams(backoff_factor=1.1)
cachepath = '/' + bucket_name +'/'

def refreshCache(data,cachefilename):
    try:
        gcs_file = gcs.open(cachepath+cachefilename,
                      'w',
                      content_type='text/plain',
                      retry_params=write_retry_params)
        gcs_file.write(data)
        gcs_file.close()
    except Exception as e:
        return "CACHE ERROR：refresh <br/>please contact kanch@akakanch.com<hr/>"
    return "OK<hr/>"

def checkNewNews(newsdata,cachefilename):
    sourcedata = ""
    newslist = newsdata
    try:
        gcs_file = gcs.open(cachepath+cachefilename,
                      retry_params=write_retry_params)
        sourcedata = gcs_file.read()
        gcs_file.close()
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
