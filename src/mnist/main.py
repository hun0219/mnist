from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import os
import datetime
import pymysql.cursors
import pytz

app = FastAPI()

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # 파일 저장
    img = await file.read()
    file_name = file.filename
    label = file_name[0]

    # 파일 확장자 받을 수 있음.
    file_ext = file.content_type.split('/')[-1]
    #rt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 디렉토리 없으면 오류, 코드에서 확인 및 만들기 추가
    upload_dir = "/home/hun/code/mnist/img"
    # 폴더 만들기 있으면 패스
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # 파일이 uuid명으로 저장된다
    # 랜덤하게 나오는 수 4(), 확장자(file_ext)  
    import uuid
    file_full_path = os.path.join(upload_dir, f'{uuid.uuid4()}.{file_ext}')

    # 폴더 만들기 있으면 패쓰
    #os.makedirs(upload_dir,exist_ok=True)

    with open(file_full_path, "wb") as f:
        f.write(img)


    # 파일 저장 경로 DB Insert
    # tablename : image_processing
    # 컬럼 정보 : num (초기 인서트, 자동 증가)
    # 컬럼 정보 : 파일이름, 파일경로, 요청시간(초기 insert), 요청사용자(n08)
    # 컬럼 정보 : 예측모델, 예측결과, 예측시간(추후 업데이트)
    
    connection = pymysql.connect(host=os.getenv("DB_IP", "172.17.0.1"),
                             user='mnist',
                             password='1234',
                             port = int(os.getenv("MY_PORT", "53306")),
                             database='mnistdb',
                             cursorclass=pymysql.cursors.DictCursor)

    sql = "INSERT INTO image_processing(`request_user`, `label`, `file_name`, `file_path`, `request_time`) VALUES (%s, %s, %s, %s, %s)"

    #https://pypi.org/project/pytz/ 'Asia/Seoul'
    from nowtime.main import now

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, ('n08', label, file_name, file_full_path, now()))
        connection.commit()


    return {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_full_path": file_full_path
            }


@app.get("/all/")
def all():
    # DB 연결 SELECT ALL
    # 결과값 리턴
    from mnist.db import select 
    sql = "SELECT * FROM image_processing"
    result = select(query=sql, size = -1)
    
    return result

@app.get("/one/")
def one():
    # DB 연결 SELECT 값 중 하나만 리턴
    # 결과값 리턴
    from mnist.db import select
    sql = """SELECT * FROM image_processing 
    WHERE prediction_time IS NULL ORDER BY num LIMIT 1"""
    result = select(query=sql, size = 1)

    return result[0]


@app.get("/many/")
def many(size: int = -1):
    from mnist.db import get_connection
    sql = "SELECT * FROM image_processing WHERE prediction_time IS NULL ORDER BY num"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchmany(size)

    return result
