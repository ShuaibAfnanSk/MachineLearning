import pickle
from flask import Flask, request, app, render_template, url_for
import requests
import numpy as np
import pandas as pd
import os
from flask import redirect
data = pickle.load(open('pickle/anime.pickle', 'rb'))
similarity = pickle.load(open('pickle/similarity.pickle', 'rb'))
dataset = pickle.load(open('pickle/trend.pickle', 'rb'))
action = pickle.load(open('pickle/action.pickle', 'rb'))
drama = pickle.load(open('pickle/drama.pickle', 'rb'))
sports = pickle.load(open('pickle/Sports.pickle', 'rb'))
mt = pickle.load(open('pickle/matcher.pickle', 'rb'))
mecha = pickle.load(open('pickle/mecha.pickle', 'rb'))
supernatural = pickle.load(open('pickle/supernatural.pickle', 'rb'))
romance = pickle.load(open('pickle/romance.pickle', 'rb'))
comedy = pickle.load(open('pickle/comedy.pickle', 'rb'))
scifi = pickle.load(open('pickle/scifi.pickle', 'rb'))
adventure = pickle.load(open('pickle/adventure.pickle', 'rb'))
fear = pickle.load(open('pickle/fear.pickle','rb'))
surprised = pickle.load(open('pickle/surprised.pickle','rb'))
pivotTab = pickle.load(open('pickle/pivotTab.pickle','rb'))
collabanimeDf = pickle.load(open('pickle/collabanimeDf.pickle','rb'))
simscore = pickle.load(open('pickle/simscore.pickle','rb'))
app = Flask(__name__)
def recommender(anime_name):
    index = np.where(pivotTab.index==anime_name)[0][0]
    similar_items = sorted(list(enumerate(simscore[index])),key=lambda x:x[1],reverse=True)[1:11]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = collabanimeDf[collabanimeDf['Name'] == pivotTab.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Name')['Name'].values))
        item.extend(list(temp_df.drop_duplicates('Name')['Genres'].values))
        item.extend(list(temp_df.drop_duplicates('Name')['Score'].values))
        item.extend(list(temp_df.drop_duplicates('Name')['Type'].values))
        
        data.append(item)
    
    return data

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/recommend-anime', methods=['post','get'])
def recommend():
    # anime_name = request.form.get('user_input')
    # points = np.where(mt.index == anime_name)[0][0]
    # distances = similarity[points]
    # similar_items = sorted(list(enumerate(distances)),
    #                        reverse=True, key=lambda x: x[1])[1:6]
    # names = []
    # for i in similar_items:
    #     item = []
    #     temp_df = data[data['Name'] == mt.index[i[0]]]
    #     item.extend(list(temp_df.drop_duplicates('Name')['Name'].values))
    #     item.extend(list(temp_df.drop_duplicates('Name')['Score'].values))
    #     item.extend(list(temp_df.drop_duplicates('Name')['Type'].values))
    #     names.append(item)
    # print(names)
    # input = request.form.get('user_input')
    # datas = recommender(input)
    # return render_template('recommend-name.html', names=names,datas=datas)
    try:
        anime_name = request.form.get('user_input')
        points = np.where(mt.index == anime_name)[0][0]
        distances = similarity[points]
        similar_items = sorted(list(enumerate(distances)),
                            reverse=True, key=lambda x: x[1])[1:6]
        names = []
        for i in similar_items:
            item = []
            temp_df = data[data['Name'] == mt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Name')['Name'].values))
            item.extend(list(temp_df.drop_duplicates('Name')['Score'].values))
            item.extend(list(temp_df.drop_duplicates('Name')['Type'].values))
            names.append(item)
        input = request.form.get('user_input')
        datas = recommender(input)
        return render_template('recommend-name.html', names=names, datas=datas)
    except IndexError:
        return redirect('/error')



@app.route('/trending')
def trending():
    return render_template('trending.html', Name=list(dataset['Name_x'].values), Score=list(dataset['Score_x'].values), Type=list(dataset['Type'].values))

@app.route('/action')
def recommend_action():
    return render_template('mood.html', Name=list(action['Name'].sample(5).values))

@app.route('/comedy')
def recommend_comedy():
    return render_template('mood.html', Name=list(comedy['Name'].sample(5).values))

@app.route('/supernatural')
def recommend_supernatural():
    return render_template('mood.html', Name=list(supernatural['Name'].sample(5).values))

@app.route('/surprised')
def recommend_surprised():
    return render_template('mood.html', Name=list(surprised['Name'].sample(5).values))

@app.route('/fear')
def recommend_fear():
    return render_template('mood.html', Name=list(fear['Name'].sample(5).values))

@app.route('/sports')
def recommend_sports():
    return render_template('mood.html', Name=list(sports['Name'].sample(5).values))

@app.route('/drama')
def recommend_drama():
    return render_template('mood.html', Name=list(drama['Name'].sample(5).values))

@app.route('/romance')
def recommend_romance():
    return render_template('mood.html', Name=list(romance['Name'].sample(5).values))

@app.route('/scifi')
def recommend_scifi():
    return render_template('mood.html', Name=list(scifi['Name'].sample(5).values))

@app.route('/mecha')
def recommend_mecha():
    return render_template('mood.html', Name=list(mecha['Name'].sample(5).values))

@app.route('/adventure')
def recommend_adventure():
    return render_template('mood.html', Name=list(adventure['Name'].sample(5).values))

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == "__main__":
    app.run(debug=True)