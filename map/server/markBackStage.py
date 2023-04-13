#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

from Textdeal.scriptDeal import person_dict
from API.bert_ner import get_des_information
from Textdeal.exActor import screenplay, divid_launch, format_information, dialogue, clear, performance_distribution, words_count

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
# CORS(app,supports_credentials=True)


# sanity check route
@app.route('/open', methods=['GET'])
def open_door():
    # return jsonify(u'芝麻开门！')
    return jsonify('我亲爱的朋友啊啊啊啊啊')
    # return '我亲爱的朋友啊啊啊啊啊'


@app.route('/api/put/txt', methods=['POST'])
# @cross_origin()
def save_file():
    if request.method == 'POST':
        # 获取vue中传递的值
        get_msg = request.get_data(as_text=True)
        # GetMSG = request.data
        print(get_msg)
        print(type(get_msg))
        print(get_msg[5])

        a = random.randint(0, 30)
        print(a)
        # print(int(GetMSG) + 10)
        return jsonify(get_msg)
    else:
        return 'defeat'


#获得 信息 “超级” 大阵
@app.route('/api/post/screenplay', methods=['GET'])
def get_screenplay():
    act = screenplay('Joker.txt')

    return jsonify(act)

#获得每一幕 人物的对话
@app.route('/api/post/dialogue', methods=['GET'])
def geta():
    act = divid_launch('Joker.txt')

    return jsonify(act)
#获得格式化的 slug_line 数据
    """
{
    "door": "EXT",
    "id": 2,
    "place": "GOTHAM SQUARE, MIDTOWN - KENNY'S MUSIC SHOP ",
    "slug": "2   EXT. GOTHAM SQUARE, MIDTOWN - KENNY'S MUSIC SHOP - DAY         2\n",
    "time": "DAY"
  },
"""
@app.route('/api/post/sluginfo', methods=['GET'])
def get_slug_info():
    slug = format_information('Joker.txt')

    return jsonify(slug)

#获得每一幕的文字
@app.route('/api/post/textscreen', methods=['GET'])
def get_c():
    dia_slug = dialogue('Joker.txt')

    return dia_slug

@app.route('/api/post/actor', methods=['GET'])
def get_actor_frequency():
    actor_frequency = clear('Joker.txt')

    return jsonify(actor_frequency)

@app.route('/api/post/fenbu', methods=['GET'])
def distribution():
    actor_dis = performance_distribution('Joker.txt')
    return actor_dis
    # return jsonify(actor_dis)

@app.route('/api/post/emotion', methods=['GET'])
def emo():
    with open('data/emotion.json', 'r') as f:
        information = json.load(f)
    return jsonify(information)
    # return jsonify(actor_dis)

@app.route('/api/post/actoremo', methods=['GET'])
def actor_emo():
    with open('data/emo_final.json', 'r') as f:
        information = json.load(f)
    return jsonify(information)

@app.route('/api/post/relationactor', methods=['GET'])
def fre_emo():
    with open('data/freRealtion', 'r') as f:
        information = json.load(f)
    return information

@app.route('/api/post/locationInfo', methods=['GET'])
def get_location():
    with open('data/location.json', 'r') as f:
        information = json.load(f)
    return information

#aggregate scheduling 总进度
@app.route('/api/post/scheduling', methods=['GET'])
def get_aggregate_scheduling():
    information = words_count('Joker.txt')
    return information

#雷达图 使用的 演员 for 章节
@app.route('/api/post/actorEmotionSlug', methods=['GET'])
def get_emotion_slug():
    with open('data/actor_emotion_slug.json', 'r') as f:
        information = json.load(f)
    return information

@app.route('/api/put/txt', methods=['PUT', 'POST','GET'])
# @cross_origin()
def getText():
    print('asas')
    if request.method == 'PUT':
        # 获取vue中传递的值
        GetMSG = request.get_data(as_text=True)
        # GetMSG = request.data
        personList = person_dict(GetMSG,"PERSON")
        # personList = personSet(GetMSG,"PERSON")
        # res=[GetMSG,jsonify(personList)]
        print(personList)
        return [GetMSG,personList]
        # return jsonify(personList)
    else:
        # 获取vue中传递的值
        GetMSG = request.get_data(as_text=True)
        # GetMSG = request.data
        personList = person_dict(GetMSG, "PERSON")
        personList={'Bowie': 17, 'Cambridge': 3, 'Space Oddity': 3, 'Pitt': 2, 'Marc Bolan': 2}
        return jsonify(personList)
        # return 'defeat'

@app.route('/api/get/slug_content', methods=['POST'])
def post_content():
    content: str = request.get_data(as_text=True)
    person_list = get_des_information(content)
    print(person_list)
    return jsonify(person_list)


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=5000, debug = True)




#

