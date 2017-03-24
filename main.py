#!/usr/bin/env python

from flask import Flask, request
from controller.engine_one import launch_engine_one
from controller.engine_two import launch_engine_two
app = Flask(__name__)

@app.route('/engine_one', methods=['GET', 'POST'])
def e1():
    return launch_engine_one(request.get_json())

@app.route('/engine_two', methods=['GET', 'POST'])
def e2():
    return launch_engine_two()

if __name__ == '__main__':
  app.run(debug=True)