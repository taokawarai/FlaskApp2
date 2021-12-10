import os
import tweepy
from flask import Flask, session, redirect, render_template, request
from os.path import join, dirname
import urllib
app = Flask(__name__)

C_KEY = ''
C_SECRET = ''
CALLBACK_URL = 'http://0.0.0.0:5000'
app.config['SECRET_KEY'] = os.urandom(24)
auth = tweepy.OAuthHandler(C_KEY, C_SECRET, CALLBACK_URL)

@app.route('/')
def index():
    oauth_token = request.args.get('oauth_token',default=' ',type=str)
    oauth_verifier = request.args.get('oauth_verifier',default=' ',type=str)
    auth.request_token['oauth_token_secret'] = oauth_verifier
    if oauth_token != ' ':
        try:
            auth.get_access_token(oauth_verifier)
        except Exception as ee:
            return {}
    
        print("access token key:",auth.access_token)
        print("access token secret:",auth.access_token_secret)
        return '''
            <p>ログイン成功</p>
        '''
    return '''
        <p>ログインしてください</p>
        <p><a href="{{ url_for('twitter_auth') }}">連携アプリ認証</a></p>
    '''

@app.route('/twitter_auth', methods=['GET'])
def twitter_auth():
    # 連携アプリ認証用の URL を取得
    redirect_url = auth.get_authorization_url()
    # リダイレクト
    return redirect(redirect_url)
