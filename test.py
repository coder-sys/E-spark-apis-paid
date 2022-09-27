from flask import Flask,after_this_request
import time

from youtubesearchpython import VideosSearch

from googlesearch import search

from bs4 import BeautifulSoup
import requests

from datetime import date,timedelta,datetime
def get_google_data(query):
    array = []
    array_urls = []

    for url in search(query,12):
        print (url)
        array_urls.append(url)
        data = requests.get(url)
        soup = BeautifulSoup(data.text,'html.parser')
        for _ in soup.find_all('title'):
            print(_.get_text())
            array.append(_.get_text())
        if len(array) > 29:
            break
    return [array,array_urls]
x = get_google_data('hello world')