## Dependency
Flask 설치가 필요합니다.
```
pip install Flask
```

***

## Usage

1. File detector.py line 47: 모델 파일 경로('./v8sbest.pt')를 적어준다.
2. server1.py 또는 server2.py를 실행

server1.py는 video_feed가 하나, server2.py는 video_feed가 두 개입니다.

동영상 주소를 변경하고 싶으시면 6~8번째 line 쯤에 있는 코드를 변경하시면 됩니다.

그냥 영상 모니터링만 하고 싶으시면 아래 코드처럼 Reader()의 파라미터로 주소를 넣어주시면 됩니다.

```
reader = Reader('rtsp://210.99.70.120:1935/live/cctv001.stream')
reader()
```


영상에서 객체를 검출하고 bounding box를 plot한 영상을 모니터링하고 싶으면 아래 코드처럼 ObjectDetection()의 파라미터로 주소를 넣어주시면 됩니다.

```
detector = ObjectDetection('rtsp://210.99.70.120:1935/live/cctv001.stream')
detector()
```

***

## 해결안 된 문제

1. GPU서버에서 돌렸을 때 이제는 영상이 뒤죽박죽 안 섞이는지 테스트
    - 어제는 Flask 돌리면 페이지 접속이 됐는데 오늘은 안 되고 있음
2. server2.py 실행결과 두 번째 영상의 ObjectDetection.displayfps() 박스 크기가 더 작음

***

## detector.py 코드 설명

Class 두 개: Reader, ObjectDetection



Class Reader : 



메소드
- read() : OpenCV 이미지를 출력 버퍼에 추가합니다.
- capture() : 출력 버퍼에서 이미지 가져오기
- __call__() :  read()하는 스레드 시작
- terminate() : 스레드 종료



속성
- frame_buffer = deque로 만든 출력 버퍼
- stop : 스레드를 멈추기 위해 사용



***



Class ObjectDetection:
- detect() : Reader에서 읽어 온 이미지를 predict해서 바운딩 박스 치고 fps도 넣어서  출력 버퍼에 저장
- capture() : 출력 버퍼에서 이미지 가져오기
- __call__() :  detect()하는 스레드 시작
- terminate() : 스레드 종료
- predict() display_fps(), plot_bboxes() : detect() 내에서만 사용합니다. YOLO공식 문서에 있는 코드 약간 수정한 거라 저도 잘 모릅니다.



fps조절용으로 중간중간 time.sleep(0.03) 넣어 놨는데 없어도 잘 돌아갑니다. 원래는 디버깅할 때 넣은 건데 디버깅 끝나고 지우다가 굳이 싶어서 남겨둔 건 데 FPS 성능 측정을 위해서는 제거해야 합니다.