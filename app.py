from flask import Flask
import time

app = Flask(__name__)

@app.route('/')
def display_time():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return f"hello, Mike, again,2 Current Time: {current_time}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
