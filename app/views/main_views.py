from flask import Blueprint, render_template
import app.model.sql as sql
from app.model.sql import cur, load_m_list
import app.model.model_predict
from app.model.model_predict import *
import app.model.pas_simul
from app.model.pas_simul import load_data
import time

# main bp
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return '공장 코드를 주소에 추가해주세요.'

@bp.route('/<f_id>') # 공장 코드를 넣어 공장마다 프로젝트 홈페이지 불러옴.
def factory(f_id):
    project_list = []
    for i in sql.load_m_list(f_id):
        tmp_list = sql.load_list(i[0])
        tmp_list.append(i[0])
        project_list.append(tmp_list)
    return render_template('index.html', factoy_code=f_id, project_num=len(project_list), project_list=project_list)

@bp.route('/predict/<Name>') # 공정 이름을 넣어 현재 공정의 예측값 도출.
def make_prediction(Name):
    return render_template('predict.html', Name=Name, Timestamp=pickle_open(Name)[0], columns_list=columns_list(Name)[2:-2], fetch_list=pickle_open(Name)[1], prediction=pickle_open(Name)[2])

@bp.route('/model/<Name>') # 공정 이름을 넣어 데이터셋의 예측값 기록.
def make_model(Name):
    predict_row(Name)
    return '데이터셋 예측이 완료되었습니다.'

@bp.route('/load/<Name>') # 공정 데이터 불러오기
def load_dataset(Name):
    commit_data(Name, id_load(Name))
    return '{}번 로드'.format(id_load(Name)+1)

@bp.route('/cal/<Name>') # 모델 성능 계산
def cal_model(Name):
    update_pi(calc_model(Name, what_pi(Name)),Name)
    return '업로드 완료'