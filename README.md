## Installing JS libraries

`npm i`

## Create python venv and install python packages

```bash
python -m venv flink
source flink/bin/activate
```

<br>

```bash
pip3 install --upgrade pip
pip3 install apache-flink
pip install confluent-kafka redis
pip3 install Flask-SocketIO Flask Flask-Cors kafka-python
```

## Starting the application on localhost / network

Terminal 1 -> `python3 server.py`  
Terminal 2 -> `npm run start`  
Terminal 3 -> `python3 flink.py`  
Terminal 4 -> `python3 redis_sink.py`  
Terminal 5 -> `python3 flink_2.py`  
Terminal 6 -> `python3 redis_sink2.py`
