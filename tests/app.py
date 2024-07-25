from flask import Flask
from threading import Thread
import time
import psutil
import os

app = Flask(__name__)

def background_task():
    while True:
        print("Background task running")
        time.sleep(5)

@app.route('/')
def home():
    return "Hello, World!"

def memory_monitor():
    process = psutil.Process(os.getpid())
    while True:
        mem_info = process.memory_info()
        print(f"Memory usage: {mem_info.rss / 1024 / 1024:.2f} MB")
        time.sleep(5)

def start_background_task():
    thread = Thread(target=background_task)
    thread.daemon = True
    thread.start()

def start_memory_monitor():
    thread = Thread(target=memory_monitor)
    thread.daemon = True
    thread.start()

start_background_task()
start_memory_monitor()

application = app
