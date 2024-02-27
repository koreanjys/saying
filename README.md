# 명언 백엔드 산출물


## 1. 환경설정

### 1.1 설치 프로그램
- python==3.8.9
- MySQL==8.0.36

### 1.2 설치 라이브러리
requirements.txt 파일에 해당 목록이 있음*
```
annotated-types==0.6.0
anyio==4.2.0
cffi==1.16.0
click==8.1.7
colorama==0.4.6
cryptography==42.0.2
fastapi==0.109.0
greenlet==3.0.3
h11==0.14.0
httptools==0.6.1
idna==3.6
pycparser==2.21
pydantic==2.6.0
pydantic-settings==2.1.0
pydantic_core==2.16.1
PyMySQL==1.1.0
python-dotenv==1.0.1
PyYAML==6.0.1
sniffio==1.3.0
SQLAlchemy==2.0.25
sqlmodel==0.0.14
starlette==0.35.1
typing_extensions==4.9.0
uvicorn==0.27.0.post1
watchfiles==0.21.0
websockets==12.0
```

### 1.3 .env 파일
main.py 파일이 있는 디렉터리에 .env 파일이 필수로 필요.

아래는 .env 파일 내용 예시
```
DATABASE_CONNECTION_STRING="mysql+pymysql://{user}:{password}@127.0.0.1:3306/{db_name}"
UVICORN_IP="0.0.0.0"
UVICORN_PORT=8000
```

## 2. DB 테이블

### 2.1 saying
