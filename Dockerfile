#  컨테이너 만들때 3.11버전으로 만듦
# 도커허브이미지 가따 쓰는거 #베이스 이미지
#FROM datamario24/python311scikitlearn-fastapi:1.0.0
#FROM python:3.11.9-slim-bullseye
#FROM python:3.11.9-slim
#FROM python:3.11-alpine3.20
#FROM leshgi2447/fishmlserv:1.1.0
FROM python:3.11

# docker 컨테이너 루트밑에 code 만듦
WORKDIR /code

# 지금 로컬의 모든 걸 컨테이너 code 디렉토리 밑에 복사
#COPY . /code/
COPY src/samdul08food/main.py /code/
# pip /code/requirment.txt 설치 하기 위해 /code/에 복사
#COPY requirements.txt /code/

# 
#COPY ./requirements.txt /code/requirements.txt

#@@@@ 모델 서빙만(의존성의 위 BASE 이미지에서 모두 설치 했다.)
# 컨테이너가 실행될때 requirements.txt안에꺼 설치 / .toml디펜던시 설정넣은거(.toml에 있음)
#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#RUN pip install --no-cache-dir --upgrade git+https://github.com/hun0219/fishregresstion.git@0.2.0/cli
#RUN pip install git+https://github.com/hun0219/fishmlserv.git@1.0.0/k
RUN pip install --no-cache-dir --upgrade git+https://github.com/hun0219/samdul08food.git@0.3.0

# 위까지는 이미지를 만들때 처리됨
#---------------------------------------------------
# 아래는 RUN될때 처리됨

#@@@@ 모델 서빙을 위해 API 구동을 위한 FastAPI RUN
# 서버실행시 커맨드 실행 ","가 띄워쓰기임
# 도커 안에서 reload할 수 있게 하는 명령 추가 --reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
#CMD ["uvicorn", "src.fishmlserv.main:app", "--host", "0.0.0.0", "--port", "8080"]
# 포트를 내부적으로 열어준다 8765
