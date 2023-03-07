import sqlite3

'''
클라우드 데이터베이스
host = ''
user = ''
password = ''
database = ''

connection = psycopg2.connect(
     host=host,
     user=user,
     password=password,
     database=database,
 )
'''
connection = sqlite3.connect('simul.db')
cur = connection.cursor()

def load_data(name, id): # 시뮬레이션을 위한 데이터 수집
    from app.model.model_predict import columns_list
    name_list = []
    for i in columns_list(name)[:-1]: name_list.append(i[0])
    cur.execute('select * from {} where id={}'.format(name, id+1))
    fetch_data = cur.fetchone()
    data_list = []
    for i in fetch_data[:-1]: data_list.append(str(i))
    return name_list, data_list