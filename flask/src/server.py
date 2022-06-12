from flask import Flask, session, render_template, request, redirect, url_for
from pymongo import MongoClient
import datetime
from WarzoneStats import Api, ApiGG, ParserGG
from mongoRoutes import MONGO_ROUTE
import atexit
from updateStreamers import updateStreamers
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(func=updateStreamers, trigger="interval", hours=2)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

app = Flask(__name__)
app.secret_key = 'thissecretisrequired'

myclient = MongoClient(MONGO_ROUTE)

def get_streamers():
  db = myclient["streamers"]
  collection = db["col1"]
  streamers = list(collection.find())
  return streamers

def get_user():
  if 'username' not in session:
    return None

  db = myclient["users"]
  collection = db["col1"]
  query = collection.find_one({'username':session['username']})
  print(query)
  parser = ParserGG()
  user = {
    'username': query['username'],
    'lifetime': round(query['profile']['data']['lifetime']['mode']['br_all']['properties']['kdRatio'], 2),
    'weekly': round(query['profile']['data']['weekly']['all']['properties']['kdRatio'], 2),
    'lobby': round(parser.get_average_kd_lobbies(query['apiGG']), 2)
  }
  return user
  # kds = []
  # for match in stats['matches']:
  #   kds.append(match['matchStatData']['playerAverage'])
  # averageKdLobbies = sum(kds)/len(kds)

@app.template_filter()
def streamer_lifetime_filter(streamer):
  try:
    return round(streamer['profile']['data']['lifetime']['mode']['br']['properties']['kdRatio'], 2)
  except:
    return 'null'

@app.template_filter()
def streamer_weekly_filter(streamer):
  try:
    return round(streamer['profile']['data']['weekly']['all']['properties']['kdRatio'], 2)
  except:
    return 'null'

@app.template_filter()
def streamer_lobby_kd(streamer):
  try:
    return round(streamer['kd'], 2)
  except:
    return 'null'

@app.route('/database')
def database():
  dbs = myclient.list_database_names()
  return str(dbs)

@app.route('/')
def home():
  streamers = get_streamers()
  user = get_user()
  return render_template('home.html', streamers=streamers, user=user)

@app.route('/login', methods = ['POST', 'GET'])
def login():
  username = request.form['username']
  sso = request.form['sso']
  platform = request.form['platform']
  print(username, sso, platform)

  # api = Api(username, platforms[platform], sso)
  # apiGG = ApiGG()
  
  if not loginHandler(username, platform, sso):
    return redirect(url_for('home', error=f'Something went wrong. Most likely one of sso, username or platform were incorrect. Also possible that something went wrong with the Api. Trying again may or may not solve this issue.'))

  session['username'] = username
  session['sso'] = sso
  session['platform'] = platform

  return redirect(url_for('home'))

def loginHandler(username, platform, sso):
  db = myclient["users"]
  collection = db["col1"]
  doc = collection.find_one({'username':username})
  if doc is None:
    return updateUser(username, platform, sso)
  else:
    if datetime.datetime.utcnow() - doc['last_modified'] > datetime.timedelta(hours=2):
      return updateUser(username, platform, sso)
  return True
  # if collection.find({'username': username}).count() > 0

def updateUser(username, platform, sso):
  platforms = {
    'ACTIVISION': Api.Platforms.ACTIVISION.value, 
    'BATTLENET': Api.Platforms.BATTLENET.value,
    'PSN': Api.Platforms.PSN.value,
    'XBOX': Api.Platforms.XBOX.value
  }
  platform = platforms[platform]
  api = Api(username, platform, sso)
  apiGG = ApiGG()
  profile = api.get_profile()
  stats = apiGG.get_stats(username, platform, skip=False)
  if profile['status'] != 'success':
    print(f'Something went wrong with the cod api. \n {profile}') 
    return False
  if stats is None:
    print(f'Something went wrong with ApiGG. Either incorrect username/platform or bot protection / ip banned') 
    return False

  doc = {
    'username':username,
    'platform':platform,
    'last_modified': datetime.datetime.utcnow(),
    'apiGG':stats,
    'profile':profile
  }
  db = myclient["users"]
  collection = db["col1"]
  updated = collection.update_one({'username': username}, {"$set":doc}, upsert=True)
  print(updated)
  return True

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)