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

app = Flask(__name__)

firebaseConfig = {
  'apiKey': "AIzaSyCGvp-4gW3nC3fAHmnJDAx3Fbwsdzn_LRQ",
  'authDomain': "espark-356318.firebaseapp.com",
  'databaseURL': "https://espark-356318-default-rtdb.firebaseio.com",
  'projectId': "espark-356318",
  'storageBucket': "espark-356318.appspot.com",
  'messagingSenderId': "615921346526",
  'appId': "1:615921346526:web:6a37c444f53906c90c9f4f"
}
import pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("espark-a18da-firebase-adminsdk-s233j-0ad1627f54.json")
firebase_admin.initialize_app(cred)
fd = firestore.client()
fd.collection('data').document('info').set({'data':1})
@app.route('/sign_in/<input_name>/<input_name_0>/<password>/<email>',methods=['GET'])
def sign_in(input_name,input_name_0,password,email):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    lastname = input_name_0
    password = password
    email = email
    db.child(f'Users/{input_name}').set({
        'firstname':input_name,
        'lastname':lastname,
        'password':password,
        'email':email,
        'no_of_folders':0,
        'selected_plan':'',
        'have_used_trail':False,
        'timestamp_free_trail':'',
        'timestamp_paid_version':''
    })
    return {
        'firstname':input_name,
        'lastname':lastname,
        'password':password,
        'email':email,
        'selected_plan':'',
        'have_used_trail':False,
        'timestamp_free_trail':'',
        'timestamp_paid_version':''
    }

@app.route('/login/<first_name>',methods=['GET'])
def login(first_name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    try:
        referance = db.child(f'Users/{first_name}').get()
        print(dict(referance.val())['password'])
        return {"data":dict(referance.val())['password']}
    except:
        return {"data":"username not found"}
@app.route('/add_folder/<name>/<foldername>',methods=['GET'])
def add_folder(name,foldername):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    try:
        fd.collection(name).document(foldername).set({'foldername':foldername})
        return {'data':'doable'}

    except:
        print('cannot do so')    
        return {'data':"undoable"}
@app.route('/add_folder/<name>',methods=['GET'])
def update_no_of_folders(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    no_of_folders = db.child(f'Users/{name}/no_of_folders').get().val()
    db.child(f'Users/{name}').update({
        'no_of_folders':no_of_folders+1
    })
    return {'data':200,'no_of_folders':no_of_folders}
@app.route('/get_folders/<name>')
def get_folders(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    try:
        d = fd.collection(name).get()
        print(d)
        data = []
        for _ in d:
            print("The value im looking for : ")

            print(_.to_dict())
            data.append(_.to_dict()['foldername'])
        return {'data':data}

    except:
        print('cannot do so')    
        return {'data':"undoable"}

@app.route('/verify_sign_in_information/<name>/<lname>',methods=['GET'])
def verify_sign_in_information(name,lname):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    data = db.child('Users/').get().val()
    resp = '-'
    if data:
        for i in data:
            if (data[i]['lastname']+data[i]['firstname']) == (lname+name):
                resp = 'change either of the names to continue'
                break
            else:
                resp = 'good to go!'
        
        return {
      'data':resp,
      'info':data
    }
    if not data:
        return{
            'data':'good to go!',
            'info':data,
            'status':200
        }
@app.route('/get_google_content/<query>',methods=['GET'])
def get_google_content(query):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    x,y = get_google_data(query)
    return{'names':x,'urls':y}
@app.route('/add_google_content/<name>/<foldername>/<sourcename>/<sourcepath>',methods=['GET'])
def add_google_content(name,foldername,sourcename,sourcepath):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    fd.collection(name).document(foldername).collection("content_stored").add({'link':sourcepath,'name':sourcename})
    time.sleep(3)
    
    return{"status":sourcepath}
@app.route('/add_youtube_content/<name>/<foldername>/<sourcename>/<sourcepath>',methods=['GET'])
def add_youtube_content(name,foldername,sourcename,sourcepath):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    fd.collection(name).document(foldername).collection("content_stored").add({'link':'https:__www.youtube.com_watch?v='+sourcepath,'name':sourcename})
    
    return{"status":sourcepath}
@app.route('/get_youtube_data/<query>',methods=['GET'])
def get_youtube_data(query):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    videosSearch = VideosSearch(query, limit = 20).result()

    videosSearch = videosSearch['result']
    titlearray=[]
    thumbnailarray = []
    linkarray = []

    for i in videosSearch:
        print(i)
        titlearray.append(i['title'])
        thumbnailarray.append(i['thumbnails'])
        linkarray.append(i['link'])
    return{
    'titles':titlearray,
    'thumbnail':thumbnailarray,
    'link':linkarray,
    'length':len(titlearray)==len(thumbnailarray)==len(linkarray)
    }
@app.route("/load_data/<name>/<foldername>",methods=['GET'])
def load_data(name,foldername):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    stored_data = fd.collection(name).document(foldername).collection('content_stored').get()
    stored_data = list(stored_data)
    array = []
    for _ in stored_data:
        array.append(_.to_dict())
    print(stored_data)

    return{'data':array}
@app.route('/update_plan/<name>/<planname>/<timestamp>',methods=['GET'])
def update_plan_free(name,planname,timestamp):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    db.child(f'Users/{name}').update({
        'selected_plan':planname,
        'timestamp_free_trail':timestamp
    })
    return {"status":200}
@app.route("/update_plan_paid/<name>/<planname>/<timestamp>",methods=['GET'])
def update_plan_paid_version(name,planname,timestamp):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    db.child(f'Users/{name}').update({
        'selected_plan':planname,
        'timestamp_paid_version':timestamp
    })
    return{
        'status':200
    }
@app.route('/get_free_trial_disability/<name>',methods=['GET'])
def get_free_trial_disability(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    data = db.child(f"Users/{name}/have_used_trail").get().val()
    return {'data':data}
@app.route('/get_selected_plan/<name>',methods=['GET'])
def get_selected_plan(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    data = db.child(f"Users/{name}/selected_plan").get().val()
    return {"data":data}

@app.route("/store_timestamp_for_trial/<name>",methods=["GET"])
def store_timestamp_for_trial(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    db.child(f"Users/{name}").update({
        "timestamp_free_trail":str(date.today())
    })
    return {
        "data":str(date.today())
    }
@app.route("/store_timestamp_for_paid_version/<name>",methods=['GET'])
def store_timestamp_for_paid_version(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    db.child(f'Users/{name}').update({
        'timestamp_paid_version':str(date.today())
    })
    return {
        'data':str(date.today())
    }
#@app.route("/retrieve_free_trial_timestamp/<name>",methods=['GET'])
#def retrieve_free_trial_timestamp(name):
#    @after_this_request
#    def add_header(response):
#        response.headers.add('Access-Control-Allow-Origin', '*')
#        return response
#    timestamp = db.child(f"Users/{name}/timestamp_free_trial").get().val()
#    return {
#        "data":timestamp
#    }
@app.route("/set_disability_for_free_trial/<name>",methods=['GET'])
def set_disability_for_free_trial(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    db.child(f'Users/{name}').update({
        'have_used_trail':True
    })
    return{
        'status':200
    }
@app.route('/date_subtraction/<name>',methods=['GET'])
def date_subtraction(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    strfdate = db.child(f"Users/{name}/timestamp_free_trail").get().val()
    print(strfdate)
    strfdate = str(strfdate)
    strfdate = strfdate.split('-')
    array = []
    for i in strfdate:
        array.append(int(i))
    timestamp = date(array[0],array[1],array[2])
    current_date = date.today()
    subtracted_date = current_date-timestamp
    subtracted_date = str(subtracted_date)
    subtracted_date = subtracted_date.split('d')[0]
    return {
        "data":int((subtracted_date).split(':')[0])
    }
@app.route("/date_subtraction_for_paid_version/<name>",methods=['GET'])
def date_subtraction_for_paid_version(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    strfdate = db.child(f"Users/{name}/timestamp_paid_version").get().val()
    print(strfdate)
    strfdate = str(strfdate)
    strfdate = strfdate.split('-')
    array = []
    for i in strfdate:
        array.append(int(i))
    timestamp = date(array[0],array[1],array[2])
    current_date = date.today()
    subtracted_date = current_date-timestamp
    subtracted_date = str(subtracted_date)
    subtracted_date = subtracted_date.split('d')[0]
    return {
        "data":int((subtracted_date).split(':')[0])
    }

if __name__=='__main__':
    app.run(debug=True,host="localhost",port=8000)
