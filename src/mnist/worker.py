import nowtime.main
from mnist.db import get_connection, select, dml
import random
import requests
import os

def get_job_img_task():
    """image_processing 테이블을 읽어서 가장 오래된 요청 하나씩을 처리"""
  
    # STEP 1
    # image_processing 테이블의 prediction_result IS NULL 인 ROW 1 개 조회 - num 갖여오기

    sql = """
    SELECT num, file_name, file_path 
    FROM image_processing 
    WHERE prediction_result IS NULL 
    ORDER BY num 
    LIMIT 1
    """

    r = select(sql, 1)

    if len(r) > 0:
        return r[0]
    else:
        return None
#    conn = get_connection()
#    with conn:
#        with conn.cursor() as cursor:
#            cursor.execute(sql)
#            result = cursor.fetchall()


    # STEP 2
    # RANDOM 으로 0 ~ 9 중 하나 값을 prediction_result 컬럼에 업데이트
    # 동시에 prediction_model, prediction_time 도 업데이트


def prediction(file_path, num):
    sql="""
    UPDATE image_processing
    SET prediction_result=%s, 
        prediction_model=%s,
        prediction_time=%s
    WHERE num=%s
    """
    from mnist.model import predict_digit
    presult = predict_digit(image_path)
    img_model_path = '/home/hun/code/mnist/note/train_img/'
    dml(sql, presult, img_model_path, nowtime.main.now(), num)

    return presult

def run():
    job = get_job_img_task()

    if job is None:
        print(f"{nowtime.main.now()} - job is None")
        return

    num = job['num']
    file_name = job['file_name']
    file_path = job['file_path']


    presult = prediction(file_path, num)


    # STEP 3
    # LINE 으로 처리 결과 전송

    print(nowtime.main.now())

    send_line_noti(file_name, presult)

def send_line_noti(file_name, presult):
    api_url = "https://notify-api.line.me/api/notify"
    token = os.getenv('LINE_NOTI_TOKEN', 'NULL')
    headers = {'Authorization':'Bearer '+token}
    print(token)
    message = {
            "message": f"{file_name} => {presult}"
    }

    resp = requests.post(api_url, headers=headers, data=message)
    
    print(resp.text)

    print("SEND LINE NOTI")
    
