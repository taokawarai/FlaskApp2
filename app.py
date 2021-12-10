import os
import tweepy
from flask import Flask, session, redirect, render_template, request
app = Flask(__name__)

CONSUMER_KEY = 'n5uCj9rR6MS98IZe5gAoyku05'
CONSUMER_SECRET = 'n5uCj9rR6MS98IZe5gAoyku05'
CALLBACK_URL = 'https://flask-water-tweet.azurewebsites.net/'
app.config['SECRET_KEY'] = os.urandom(24)
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        oauth_token = request.args.get('oauth_token', default = None, type=str)
        oauth_verifier = request.args.get('oauth_verifier',default = None, type=str)
        if oauth_token == None:
            return render_template("index.html", isAuthed = False)
        try:
            auth.request_token['oauth_token_secret'] = oauth_verifier
            auth.get_access_token(oauth_verifier)
        except Exception as e:
            return ''' <p>エラー</p> '''
        return render_template("index.html", isAuthed = True)
    elif request.method == 'POST':
        auth.set_access_token(auth.access_token, auth.access_token_secret)
        api = tweepy.API(auth)
        msg = "水を " + str(request.form["msg"]) + " mL飲んだ`"
        api.update_status(msg)
        return render_template("index.html", isAuthed = True)

@app.route('/twitter_auth', methods=['GET'])
def twitter_auth():
    redirect_url = auth.get_authorization_url()
    return redirect(redirect_url)
