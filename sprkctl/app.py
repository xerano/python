import RPi.GPIO as GPIO
import time
from flask import Flask, render_template

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

@app.route("/")
def hello():
    return render_template('index.html', name=None)

@app.route("/relay/<int:state>")
def relay(state):
    
    if state == 0:
        GPIO.output(16, GPIO.LOW)
    if state == 1:
        GPIO.output(16, GPIO.HIGH)

    return "set gpio to %d"  % (state)
