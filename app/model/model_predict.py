import pickle
import numpy as np
import warnings
from app.model.sql import cur, connection
from app.model.pas_simul import load_data

warnings.filterwarnings(action='ignore')

def pickle_open(Name): # 가장 최근의 로그 id, timestamp, target, predict 제외 후 Name.pickle에서 예측값을 불러옴.
    with open('{}.pickle'.format(Name), 'rb') as f: model = pickle.load(f)
    cur.execute('select * from {} order by id desc limit 1'.format(Name))
    fetch_data = cur.fetchone()
    prediction = model.predict(np.array([fetch_data[2:-2]]))
    return fetch_data[1] ,fetch_data[2:-2], prediction

def columns_list(Name): # 공정 이름을 넣으면 id, timestamp, target, predict 제외 후 다른 특성 이름을 가져온다.
    cur.execute("select column_name from information_schema.columns where table_name='{}'".format(Name))
    fetch_data = cur.fetchall()
    tmp_list = []
    for i in fetch_data: tmp_list.append(i)
    return tmp_list

def predict_row(Name): # 예측값이 기록되지 않은 모든 row들의 예측값을 기록한다.
    with open('{}.pickle'.format(Name), 'rb') as f: model = pickle.load(f)
    cur.execute('select * from {} where predict is null'.format(Name))
    fetch_data = cur.fetchall()
    for i in fetch_data:
        prediction = model.predict(np.array([i[2:-2]]))
        cur.execute('update {} set predict = {} where id={}'.format(Name, prediction[0], i[0]))
        connection.commit()

def id_load(Name):
    cur.execute('select id from {} order by id desc limit 1'.format(Name))
    fetch_data = cur.fetchone()
    return fetch_data[0]

def commit_data(name, id):
    cur.execute('INSERT INTO {} {} VALUES {}'.format(name, str(tuple(load_data(name, id)[0])[:-1]).replace("'",''), tuple(load_data(name, id)[1])))
    connection.commit()

def calc_model(Name, method='all'):
    with open('{}.pickle'.format(Name), 'rb') as f: model = pickle.load(f)
    cur.execute('select insp, predict from {} where predict is not null and insp is not null'.format(Name))
    fetch_data = cur.fetchall()
    cal_list = [0,0,0,0]
    for i in fetch_data: 
        sum = i[0]+i[1]
        if sum == 2: cal_list[0] += 1 
        elif sum == 0: cal_list[1] += 1
        elif i[0] == 0 & i[1] == 1 : cal_list[2] += 1
        else: cal_list[3] += 1
    accuracy = (cal_list[0]+cal_list[1])/(cal_list[0]+cal_list[1]+cal_list[2]+cal_list[3])
    recall = cal_list[0]/(cal_list[0]+cal_list[3])
    precision = cal_list[0]/(cal_list[0]+cal_list[2])
    F1 = 2*(precision * recall)/(precision + recall)
    if method == 'all': return accuracy, recall, precision, F1
    elif method == 'accuracy': return accuracy
    elif method == 'recall': return recall
    elif method == 'precision': return precision
    else: return F1

def what_pi(Name):
    cur.execute("select pi from models where m_name='{}'".format(Name))
    fetch_data = cur.fetchone()
    return fetch_data

def update_pi(result, Name):
    cur.execute("update models set score = {} where m_name='{}'".format(round(result,3),Name))
    cur.execute("select id from models where m_name='{}' order by id desc limit 1".format(Name))
    fetch_data = cur.fetchone()
    tmp_tuple = (fetch_data[0], calc_model(Name)[0], calc_model(Name)[1], calc_model(Name)[2], calc_model(Name)[3])
    cur.execute("insert into models_pi values {}".format(tmp_tuple))
    connection.commit()