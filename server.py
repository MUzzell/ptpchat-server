#!/usr/bin/python
#
# Experimental ptpchat-server (HTTP)
# Very much wip
#
#
#

import pdb, os, datetime, sys
from flask import Flask, make_response, render_template, request, abort


app = Flask(__name__)
app.debug = True

@app.errorhandler(500)
def error_500(e):
    return "oh noes!"

@app.route("/msg", methods=['GET'])
def msg_get():
	pdp.set_trace()
	return "{\"msg_type\": \"hello\"}"

@app.route("/msg", methods=['POST'])
def msg():
    pdb.set_trace()
    content = request.json
    
    return "{\"msg_type\": \"hello\"}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001)
