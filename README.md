## Installing JS libraries

npm i

## Create python venv and install python packages

python -m venv flink  
source flink/bin/activate

pip3 install --upgrade pip  
pip3 install apache-flink kafka-python  
pip3 install Flask-SocketIO Flask Flask-Cors  
pip3 install confluent-kafka redis

## Starting the application on localhost / network

Terminal 1 -> python3 server.py  
Terminal 2 -> npm run start  
Terminal 3 -> python3 flink.py  
Terminal 4 -> python3 redis_sink.py  
Terminal 5 -> python3 flink_2.py  
Terminal 6 -> python3 redis_sink2.py
