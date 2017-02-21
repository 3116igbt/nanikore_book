#-*- coding:utf-8 -*-

from subprocess import check_output
from flask import Flask, redirect, request, render_template
from utils.decorator_auth import requires_auth
import psycopg2

import json

import img2name

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

    '''
    やること
    1. 画像をはまうえ君のメソッドになげる
    2. 名前が返ってくる
    3. 名前でSQL 文を作る
    4. json の準備
    '''
    # 1.2. 
    name = img2name.recognize(request.form["img"])
    # 3.

    output = {}
    output["refisExist"] = False
    output["refId"] = -1
    output["name"] = ""
    output["explanation"] = ""
    output["quizisExist"] = False
    output["quizId"] = -1
    output["quizText"] = ""
    output["answer"] = ""
    output["description"] = ""


    conn = psycopg2.connect("dbname=docomohack host=localhost user=postgres password=post")
    cur = conn.cursor()
    # ここにSQL 文を書き続ける
    # 
    cur.execute("select * from item where name="+name)
    tpl_ref = cur.fetchone()
    if type(tpl_ref) == type(()):
        output["name"] = name
        output["refisExist"] = True
        ref_id = tpl_ref[0]
        user_id = request.form["userId"]
        # 問題文をとってくる
        tpl_ref = cur.execute("select * from item where name=(%s)",(name,))
        quiz = cur.fetchone()
        if type(quiz) == type(()):
            output["quizId"] = quiz[1]
            output["quizisExist"] = True
            output["quizText"] = quiz[2]
            output["description"] = quiz[4]

    # output["name"] = hogehoge(request.[])
    
    return json.dumps(output, indent = 4)


@app.route("/api/hello")
def hello():
    output = {}
    output["hello"] = "flask"
    return json.dumps(output, indent = 4)

@app.route("/test/getref")
def test_get_reference():

    '''
    テスト用．識別物体名を決め打ち
    '''
    # 1.2.
    name = "puyo"
    # 3.

    output = {}
    output["refisExist"] = False
    output["refId"] = -1
    output["name"] = ""
    output["explanation"] = ""
    output["quizisExist"] = False
    output["quizId"] = -1
    output["quizText"] = ""
    output["answer"] = ""
    output["description"] = ""


    conn = psycopg2.connect("dbname=docomohack host=localhost user=postgres password=post")
    cur = conn.cursor()
    # ここにSQL 文を書き続ける
    #
    tpl_ref = cur.execute("select * from item where name=(%s)",(name,))
    tpl_ref = cur.fetchone()
    if type(tpl_ref) == type(()):
        output["name"] = name
        output["refisExist"] = True
        ref_id = tpl_ref[0]
        user_id = "1"

        # print("DEBUG:name:"+name+"    ref_id:"+ref_id+"    ")        

        # 問題文をとってくる
        cur.execute("select * from quiz where itemid=(%s); ", (ref_id,))
        quiz = cur.fetchone()
        if type(quiz) == type(()):
            output["quizId"] = quiz[1]
            output["quizisExist"] = True
            output["quizText"] = quiz[2]
            output["description"] = quiz[4]

    # output["name"] = hogehoge(request.[])

    return json.dumps(output, indent = 4)






@app.route("/api/postquestion", methods=["POST"])
def post_question():

    '''
    やること
    1. ユーザーID,画像，図鑑ID,質問内容を受け取る
    2. それを insert するSQL 文を書く
    3. アプリにステータスを返す
    '''
    # 1,
    user_id = request.form["userId"]
    img = request.form["img"]
    ref_id = request.form["refId"]
    question = request.form["question"]

    # 2.
    conn = psycopg2.connect("dbname=docomohack host=localhost user=postgres password=post")
    cur = conn.cursor()
    # ここにSQL 文を書き続ける
    tpl_ref = cur.execute("insert into userquestion(userid,itemid,answerd,content) values((%s),(%s),false,(%s))", (user_id, ref_id, question))
    tpl_ref = cur.fetchone()
    # 3.
    output = {}
    output["status"] = True
    return json.dumps(output, indent = 4)

@app.route("/api/showref", methods=["POST"])
def show_reference():

    '''
    やること
    1. ユーザID, アイテムID を受け取る
    2. 説明文を SQL に問い合わせ(複数)
    3. json 返す
    '''
    # 1. 
    user_id = request.form["userId"]
    ref_id = request.form["refId"]
    # 2.
    output = {}
    descriptions = []
    conn = psycopg2.connect("dbname=docomohack host=localhost user=postgres password=post")
    cur = conn.cursor()
    # ここにSQL 文を書き続ける
    cur.execute("select quizid from quizanswer where userid=(%s) and itemID=(%s) and cleared=true", (user_id, ref_id))
    while True:
        temp = cur.fetchone()[0]
        if type(temp) == type(""):
            cur2 = conn.cursor()
            cur2.execute("select descript from quiz where quizid = (%s)", (temp, ))
            descriptions.append(cur2.fetchone()[0])
        else:
            break
    # 3. 
    output["descriptions"] = descriptions
    return json.dumps(output, indent = 4)



if __name__ == "__main__":
    app.run(host="153.127.200.187", port=8080, debug = True)
