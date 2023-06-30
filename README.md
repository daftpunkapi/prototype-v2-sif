# Installing JS libraries

npm i

# Create python venv and install python packages

python -m venv flink
source flink/bin/activate

pip3 install --upgrade pip
pip3 install apache-flink

# Starting the application on localhost / network

Terminal 1 -> npm run server
Terminal 2 -> npm run start
Terminal 3 -> python3 flink.py
