import random
import string
import urllib.parse
from flask import Flask, redirect, request
import base64
import requests 
from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = 'http://localhost:5000'

app = Flask(__name__)
#I am creating an instance. Basically an application. It will have 2 decorators: "/login" and "/"

@app.route('/login')
#This is the first decorator. It is built for people first accessing the App and without the permisions. When a new user access "http://127.0.0.1:5000/login" they will be redirected to the permission URL
def login():
    scope = 'user-follow-read user-read-private user-read-email' #This is the special permissions, or "scopes" we are requesting to the new user.

    params = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
    }
    url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(params)
    return redirect(url) #The user will be redirected to http://127.0.0.1:5000/ and the second decorator will be run

@app.route('/')
#Once the user has given the permissions when accessing http://127.0.0.1:5000/login, we set on the first decorator that will be redirected to http://127.0.0.1:5000/, so this second one will be run
def callback():
    '''
    error = request.args.get('error')
    if error:
        return f'Callback error: {error}'
    '''

    code = request.args.get('code')
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
    }
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    response_data = response.json()

    access_token = response_data['access_token']
    refresh_token = response_data['refresh_token']
    expires_in = response_data['expires_in']

    return f'Access Token: {access_token}<br>Refresh Token: {refresh_token}<br>Expires In: {expires_in}'

# I do not need the following class in order to have the basics for running the App. I need to understand what code below does.
'''
@app.route('/refresh_token')
def refresh_token():
    refresh_token = request.args.get('refresh_token')
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    response_data = response.json()

    access_token = response_data['access_token']
    expires_in = response_data['expires_in']

    return f'Access Token: {access_token}<br>Expires In: {expires_in}'
'''

if __name__ == '__main__':
    app.run(port=5000)