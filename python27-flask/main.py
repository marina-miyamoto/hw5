#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import urlfetch
import json
from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True

networkJson = urlfetch.fetch("http://tokyo.fantasy-transit.appspot.com/net?format=json").content  # ウェブサイトから電車の線路情報をJSON形式でダウンロードする
network = json.loads(networkJson.decode('utf-8'))  # JSONとしてパースする（stringからdictのlistに変換する）

@app.route('/')
# / のリクエスト（例えば http://localhost:8080/ ）をこの関数で処理する。
# ここでメニューを表示をしているだけです。
def root():
  return render_template('hello.html')

@app.route('/pata')
# /pata のリクエスト（例えば http://localhost:8080/pata ）をこの関数で処理する。
# これをパタトクカシーーを処理するようにしています。
def pata():
  # とりあえずAとBをつなぐだけで返事を作っていますけど、パタタコカシーーになるように自分で直してください！
  
  tmp = []
  a = list(request.args.get('a', ''))
  b = list(request.args.get('b', ''))
  
  if len(a) != len(b):
    pata = "ERROR"
    return render_template('pata.html', pata=pata)
  
  else:
    for i in range(len(a)):
      tmp.append(a[i])
      tmp.append(b[i])
    pata = ''.join(tmp)
    # pata.htmlのテンプレートの内容を埋め込んで、返事を返す。
    return render_template('pata.html', pata=pata)

@app.route('/norikae', methods=['GET', 'POST'])
# /norikae のリクエスト（例えば http://localhost:8080/norikae ）をこの関数で処理する。
# ここで乗り換え案内をするように編集してください。


def where(station):
    station_is_at = []
    for train_line in range(len(network)):
        #print(network[i]["Stations"])
        if station in network[train_line]["Stations"]:
            index = network[train_line]["Stations"].index(station)
            station_is_at.append((train_line, index))
    return station_is_at

def norikae(self):
  start = request.form.get("from")
  goal = request.form.get("to")

  #出発駅
  Start = where(start)
  #降車駅
  Goal = where(goal)


  #BFS探索をスター
  Q = []
  Checked = set()
  #出発駅からその路線の終点までをQに入れる
  for i in range(len(network[Start[0][0]]["Stations"])):
    if Goal[0] in where(network[Start[0][0]]["Stations"][i]):
      #print("Train Line is: " + str(network[Start[0][0]]["Name"]))
      network = "No Need To Change Lines"
      exit(1)
    else:
      Q.append((network[Start[0][0]]["Stations"][i], 0))
      for j in range(len(where(network[Start[0][0]]["Stations"][i]))):
        if where(network[Start[0][0]]["Stations"][i])[j][0] == Start[0][0]:
          Checked.add(where(network[Start[0][0]]["Stations"][i])[j])
            
  #print("Train Line Starts At: " + str(network[Start[0][0]]["Name"]))

  tmp = []
  change_train = []
  while len(Q) > 0:
    if where(Q[0][0]) == Goal:
      break
    else:   
      #Qに入っている駅が他の路線にあればその（路線、駅が何番目か）を求める。なければ何もしない。
      for k in range(len(Q)):
        tmp = where(Q[k][0])           
        #tmpに入ってる路線の駅からスタートしてその路線を調べ、その中の駅が「降車駅じゃない」かつ「まだ行っていない駅」か調べる
        for l in range(len(tmp)):
          if tmp[l] not in Checked:
            for m in range(tmp[l][1], len(network[tmp[l][0]]['Stations'])):
              change_train.append(tmp[l])
              #もしその駅が降車駅ではなかったらQに追加する
              if where(network[tmp[l][0]]['Stations'][m]) != Goal:
                Q.append((network[tmp[l][0]]['Stations'][m], Q[0][1] + 1))
              else: 
                #print("Change Trains At: " + str(network[change_train[len(change_train) - 1][0]]['Stations'][change_train[len(change_train) - 1][1]]))
                network = network[change_train[len(change_train) - 1][0]]['Stations'][change_train[len(change_train) - 1][1]]
                exit(1)
          tmp = []
        Q.pop(0)

  return render_template('norikae.html', network=network)
