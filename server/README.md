## Dependency
Flask 설치가 필요합니다.
```
pip install Flask
```

***

## Usage

1. File detector.py line 47: 모델 파일 경로('./v8sbest.pt')를 적어준다.
2. monitor.py를 실행
3. 127.0.0.1:5000/orange/all 에 접속하여 모니터링
4. 127.0.0.1:5000/orange/profile 에 접속하여 CCTV주소 추가 혹은 삭제

- 나머지 페이지 미구현

***

## detector.py 코드 설명

Class 두 개: Reader, ObjectDetection

Class Reader : 

메소드
- read() : OpenCV 이미지를 출력 버퍼에 추가합니다.
- capture() : 출력 버퍼에서 이미지 가져오기
- \_\_call\_\_() :  read()하는 스레드 시작
- terminate() : 스레드 종료

속성
- frame_buffer = deque로 만든 출력 버퍼
- stop : 스레드를 멈추기 위해 사용


***

Class ObjectDetection:
- detect() : Reader에서 읽어 온 이미지를 predict해서 바운딩 박스 치고 fps도 넣어서  출력 버퍼에 저장
- capture() : 출력 버퍼에서 이미지 가져오기
- \_\_call\_\_() :  detect()하는 스레드 시작
- terminate() : 스레드 종료
- predict() display_fps(), plot_bboxes() : detect() 내에서만 사용합니다. YOLO공식 문서에 있는 코드 약간 수정한 거라 저도 잘 모릅니다.

***

##DBmanagement.py 설명

로컬에 hunet이라는 mysql db 추가 필요

-db 구조
```
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
 

***

## 해결안 된 문제

1. GPU서버에서 돌렸을 때 이제는 영상이 뒤죽박죽 안 섞이는지 테스트
    - 어제는 Flask 돌리면 페이지 접속이 됐는데 오늘은 안 되고 있음
2. server2.py 실행결과 두 번째 영상의 ObjectDetection.displayfps() 박스 크기가 더 작음
3. fps조절용으로 중간중간 time.sleep(0.03) 넣어 놨는데 없어도 잘 돌아갑니다. 원래는 디버깅할 때 넣은 건데 디버깅 끝나고 지우다가 굳이 싶어서 남겨둔 건 데 FPS 성능 측정을 위해서는 제거해야 합니다.
4. 모니터링 화면 <-> 프로필 화면 간 링크 혹은 네비게이션 바 추가하기
5. requirements.txt 추가하기
6. e-mail 알림 발송, 모델 교체, detector 코드 교체 하기
