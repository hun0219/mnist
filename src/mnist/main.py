from typing import Annotated

from fastapi import FastAPI, File, UploadFile
import os
import datetime
import pymysql.cursors

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # 파일 저장
    img = await file.read()
    file_name = file.filename
    # 파일 확장자 받을 수 있음.
    file_ext = file.content_type.split('/')[-1]
    rt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
    
    connection = pymysql.connect(host=os.getenv("DB_IP", "localhost"),
                             user='mnist',
                             password='1234',
                             port = int(os.getenv("MY_PORT", "53306")),
                             database='mnistdb',
                             cursorclass=pymysql.cursors.DictCursor)

    sql = "INSERT INTO image_processing(`request_user`, `file_name`, `file_path`, `request_time`) VALUES (%s, %s, %s, %s)"

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, ('n08', file_name, file_full_path, rt))
        connection.commit()


    return {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_full_path": file_full_path
            }
