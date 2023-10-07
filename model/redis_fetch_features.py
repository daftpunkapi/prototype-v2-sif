import redis
import pandas as pd
import json

def redis_fetch_features(sessionId):

    r = redis.Redis(
            host='INSERT_YOUR_HOST',
            port=17789,   
            password='INSERT_YOUR_KEY')    
    try:
        response = r.ping()
        if response:
            print('Successfully connected to Redis')
    except redis.exceptions.ConnectionError as e:
        print(f'Failed to connect to Redis: {e}')

    keys = ['clicks_table:'+sessionId, 'cursor_table:'+sessionId]
    redis_features = pd.DataFrame()
    for key in keys:
        value = r.get(key)
        if value is not None:
            value_dict = json.loads(value.decode('utf-8'))
            df = pd.DataFrame.from_dict(value_dict, orient='index').T
            redis_features = pd.concat([redis_features, df], axis=1)
        
    return redis_features
