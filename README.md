## Installing JS libraries

npm i

## Create python venv and install python packages

python -m venv flink  
source flink/bin/activate

pip3 install --upgrade pip  
pip3 install apache-flink kafka-python  
pip3 install Flask-SocketIO Flask Flask-Cors  

## Starting the application on localhost / network

Terminal 1 -> python3 server.py  
Terminal 2 -> npm run start  
Terminal 3 -> python3 flink.py  
