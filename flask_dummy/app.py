#-*- coding:utf-8 -*-

from subprocess import check_output
from flask import Flask, redirect, request, render_template
from utils.decorator_auth import requires_auth

app = Flask(__name__)

# @app.before_request
@requires_auth
def basic_auth():
    pass

@app.route("/")
def index():
    return render_template("sample.html")
    # return agent.talk("hogehoge")

@app.route("/api/getref", methods=["POST"])
def get_reference():

    output = {}
    output["result"] = True
    return json.dumps(output, indent = 4)


if __name__ == "__main__":
    app.run(host="153.127.200.187", port=8080, debug = True)
