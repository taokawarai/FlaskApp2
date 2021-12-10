import os
import tweepy
from flask import Flask, session, redirect, render_template, request
from os.path import join, dirname
app = Flask(__name__)

C_KEY = 'n5uCj9rR6MS98IZe5gAoyku05'
C_SECRET = 'ljeWjqGpPgI6GUb9VOU1BdbwezzJsOcMHCYHFyzEImIZmNmhUx'
CALLBACK_URL = 'http://0.0.0.0:5000'
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    return '''
        <p>ログインしてください</p>
    '''

@app.route('/twitter_auth', methods=['GET'])
def twitter_auth():
    # tweepy でアプリのOAuth認証を行う
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET, CALLBACK_URL)
    # 連携アプリ認証用の URL を取得
    redirect_url = auth.get_authorization_url()
    # 認証後に必要な request_token を session に保存
    session['request_token'] = auth.request_token
    # リダイレクト
    return redirect(redirect_url)

def user_timeline():
    # request_token と oauth_verifier のチェック
    token = session.pop('request_token', None)
    verifier = request.args.get('oauth_verifier')
    if token is None or verifier is None:
        return False  # 未認証ならFalseを返す

    # tweepy でアプリのOAuth認証を行う
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET, CALLBACK_URL)

    # Access token, Access token secret を取得．
    auth.request_token = token
    auth.get_access_token(verifier)

    # tweepy で Twitter API にアクセス
    api = tweepy.API(auth)
    return api.user_timeline(count=100)