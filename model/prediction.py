import pandas as pd
import joblib
from model.redis_fetch_features import redis_fetch_features

classifier = joblib.load('model/classifier.joblib')

def risk_predict(sessionId,IP_country_code,paste_count):
    
    ip_features = pd.DataFrame(columns=['IP_country_code_AF', 'IP_country_code_AT', 'IP_country_code_BR',
       'IP_country_code_CA', 'IP_country_code_CL', 'IP_country_code_DE',
       'IP_country_code_IN', 'IP_country_code_IR', 'IP_country_code_JP',
       'IP_country_code_NO', 'IP_country_code_PK', 'IP_country_code_RU',
       'IP_country_code_TR', 'IP_country_code_UK', 'IP_country_code_US'])
    
    initial_record = pd.Series({col: 0 for col in ip_features.columns})
    ip_features = ip_features.append(initial_record, ignore_index=True) 
    column_to_change = f'IP_country_code_{IP_country_code}'
    ip_features.at[0, column_to_change] = 1

    redis_features = redis_fetch_features(sessionId)
    
    x_encoded = pd.DataFrame()
    x_encoded = pd.concat([x_encoded,ip_features], axis=1)
    x_encoded = pd.concat([x_encoded,redis_features], axis=1)
    x_encoded['paste_count'] = paste_count

    x_encoded[['avg_vel', 'tot_dist']] = x_encoded[['tot_dist', 'avg_vel']]
    x_encoded.rename(columns={'avg_vel': 'tot_dist', 'tot_dist': 'avg_vel'}, inplace=True)
    x_encoded.fillna(0,inplace=True)

    predictions = classifier.predict(x_encoded)
    return predictions