import urllib
import json
import time

from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from random import randint


app = Flask(__name__)

class stateNum(ndb.Model):
    x = ndb.IntegerProperty()
    

# A simple welcome page
@app.route('/')
def main_page():
    return render_template('home.html')

@app.route('/button')
def button():
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    loop_control = True
    iterator = 0
    while loop_control:
        state_number = randint(1, 10000000)
        q = stateNum.query(stateNum.x == state_number)
        fetched = q.fetch()
        if fetched:
            iterator = iterator + 1
            if iterator == 100000000:
                return "Error. The database is full. Tell Tyler to flush the state IDs."
        else:
            loop_control = False
    params = {'client_id': '712092341542-l4hvudljfnimieo0a6l579aj2dmpq7j1.apps.googleusercontent.com', 'redirect_uri': 'http://oauth2-assignment-cs496.appspot.com/oauth',
    'scope': 'email', 'response_type': 'code', 'state': state_number}
    args = urllib.urlencode(params)
    new_state = stateNum(x=state_number)
    new_state.put()
    return redirect(base_url + '?' + args)

@app.route('/oauth')
def oauth():
    returned_code = request.args.get('code', type = str)
    returned_state = request.args.get('state', type = int)
    q = stateNum.query()
    fetched = q.fetch()
    match = 0
    for val in fetched:
        if val.x == returned_state:
            match = 1
    if match == 0:
        return "ERROR. Somehow you broke it. You don't have a valid state number."
    headers = {'code': returned_code, 'client_id': '712092341542-l4hvudljfnimieo0a6l579aj2dmpq7j1.apps.googleusercontent.com', 'client_secret': 'nAsZxAVGm8Bn2tEL64AzawUj',
               'redirect_uri': 'http://oauth2-assignment-cs496.appspot.com/oauth', 'grant_type': 'authorization_code'}
    google_url = 'https://www.googleapis.com/oauth2/v4/token'
    auth_url = 'https://www.googleapis.com/plus/v1/people/me'
    print '2'
    data = urllib.urlencode(headers)
    post_result = urlfetch.fetch(url=google_url, method=urlfetch.POST, payload=data, validate_certificate=True)
    print post_result.content
    content = json.loads(post_result.content)
    token = "Bearer %s" % content['access_token']
    accessed_data = urlfetch.fetch(url=auth_url, method=urlfetch.GET, headers={'Authorization': token})
    accessed_content = json.loads(accessed_data.content)
    fname = accessed_content['name']['givenName']
    lname = accessed_content['name']['familyName']
    return render_template('name.html', first_name = fname, last_name = lname, state_number = returned_state)


@app.route('/name')
def authorized():
    return render_template('name.html')


@app.route('/googlee69d7f12dab0219a.html')
def verification():
    return render_template('googlee69d7f12dab0219a.html')