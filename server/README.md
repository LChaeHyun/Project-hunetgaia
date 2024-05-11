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

해결안 된 문제
1. GPU서버에서 돌렸을 때 이제는 영상이 뒤죽박죽 안 섞이는지 테스트
    - 어제는 Flask 돌리면 페이지 접속이 됐는데 오늘은 안 되고 있음
2. server2.py 실행결과 두 번째 영상의 ObjectDetection.displayfps() 박스 크기가 더 작음