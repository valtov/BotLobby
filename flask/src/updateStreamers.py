from pymongo import MongoClient
from mongoRoutes import MONGO_ROUTE
from WarzoneStats import Api, ApiGG, ParserGG
import datetime

def updateStreamers():
    myclient = MongoClient(MONGO_ROUTE)
    db = myclient["streamers"]
    collection = db["col1"]
    sso = 'MTYwNTYyOTI5Njk3NDMxMDc0Nzk6MTY1NTc1MjkwMDM0NTplOTgyMGU5YTc3ZmQxOWVhYzNmNjk0OTVkNzkyMmViNw'
    parserGG = ParserGG()
    apiGG = ApiGG()
    for streamer in collection.find():
        platformGG = streamer['platform']
        platform = platformGG if platformGG != 'acti' else 'uno'
        username = streamer[platformGG]
        print(f'About to process {username} on {platform}')
        if 'last_modified' in streamer:
            if datetime.datetime.utcnow() - streamer['last_modified'] <= datetime.timedelta(hours=1):
                print(f'Skipping...')
                continue
        api = Api(username, platform, sso)
        profile = api.get_profile()
        stats = apiGG.get_stats(username, platformGG)
        kd = parserGG.get_average_kd_lobbies(stats)
        updated = collection.update_one({'battle': streamer['battle']}, {"$set":{'profile':profile, 'stats':stats, 'kd':kd, 'last_modified': datetime.datetime.utcnow()}}, upsert=True)
        print(updated)

if __name__ == '__main__':
    updateStreamers()