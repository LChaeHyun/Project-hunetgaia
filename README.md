# CCTV 화재 감지 시스템 개발 및 연구

> CCTV 모니터링 서비스

### 로그인 화면
![로그인 화면](./result_image/login.png)


### 회원가입 화면
![회원가입 화면](./result_image/signup.png)


### Profile 화면
![profile 화면](./result_image/profile.png)


### All feeds 화면
![All feeds 화면](./result_image/all%20feeds.png)


### 화재 감지 시 이메일 알림
![email](./result_image/email.png)

## 사용법

0. git과 node 설치

1. 레파지토리 다운로드 및 라이브러리 설치

    ```shell
    git clone https://github.com/LChaeHyun/Project-hunetgaia.git
    cd Project-hunetgaia
    pip install -r requirements.txt
    cd frontend
    npm install
    ```

2. 환경변수 설정
    - .env 파일 생성
    - .env 파일 내용
    ```shell
    // .env

    # app.config
    SECRET_KEY="hunetgia_secret_key"
    SESSION_TYPE="filesystem"

    # MYSQL
    DB_HOST='127.0.0.1'
    DB_USER='root'
    DB_PASSWORD='root'
    ```

3. 데이터베이스 설정
    - 로컬에 hunet이라는 mysql db 추가 필요
    - db 구조
    ```shell
    create database hunet;
    use hunet;
    create table manager(
        id varchar(50) NOT NULL primary key,
        pwd varchar(50) not null
    );

    create table rtsp(
        id int primary key auto_increment,
        name varchar(50),
        ip_address varchar(200)
    );

    create table email(
        id int primary key auto_increment,
        address varchar(50) not null
    );
    ```

4. 실행
    - detect 서버 실행
    ```shell
    cd Project-hunetgaia/server
    python detector.py
    ```


    - 모니터링 페이지 실행 (monitor.py 실행 후 npm start 실행)
    ```shell
    cd Project-hunetgaia/server
    python monitor.py
    ```


    ```shell
    cd Project-hunetgaia/frontend
    npm start
    ```

5. 모니터링 확인

    - localhost:3000으로 접속 시 모니터링 페이지 확인 가능

