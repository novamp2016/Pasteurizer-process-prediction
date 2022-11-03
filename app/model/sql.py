import psycopg2

# 클라우드 데이터베이스
host = 'arjuna.db.elephantsql.com'
user = 'ppmxrrek'
password = 'kQz95JZRT5Wx__AlwouNdOrsXtcYAf8s'
database = 'ppmxrrek'

connection = psycopg2.connect(
     host=host,
     user=user,
     password=password,
     database=database,
 )

cur = connection.cursor()

def load_m_list(f_id):
    cur.execute("select m_name from factory where f_id={} order by id".format(f_id))
    tmp_list = cur.fetchall()
    return tmp_list

def load_list(Name):
    cur.execute("select M_Id, process, link, r_link from factory where M_Name='{}' limit 1".format(Name))
    tmp_list = cur.fetchone()
    sql_list = [tmp_list[0], tmp_list[1], tmp_list[2], tmp_list[3]]
    cur.execute("select std_dt from {} order by id desc limit 1".format(Name))
    tmp_list = cur.fetchone()
    sql_list.extend([tmp_list[0]])
    cur.execute("select target, pi, score, score_goal from models where M_Name='{}' limit 1".format(Name))
    tmp_list = cur.fetchone()
    sql_list.extend([tmp_list[0], tmp_list[1], tmp_list[2], tmp_list[3]])
    return sql_list



