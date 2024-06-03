import cv2
import threading
# import datetime

def check_rtsp_opencv(rtsp_url):
    # now = datetime.datetime.now()
    # print(now)
    capture = cv2.VideoCapture(rtsp_url)
    # now = datetime.datetime.now()
    # print(now)
    return capture.isOpened()

def is_rtsp_valid(rtsp_url, timeout=10):
    def target(result):
        result['valid'] = check_rtsp_opencv(rtsp_url)
    
    result = {'valid': False}
    thread = threading.Thread(target=target, args=(result,))
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        return False
    return result['valid']

if __name__ == "__main__":
    # Example usage
    rtsp_url = "rtsp://127.0.0.1:8554/stream"
    if is_rtsp_valid(rtsp_url):
        print("RTSP stream is valid")
    else:
        print("RTSP stream is not valid")

# usage:
# import is_rtsp_valid from rtspvalidate
# if is_rtsp_valid(rtsp_url, timeout=5):
#     #your code here
#     pass

# 실행결과

# 2024-06-03 13:07:11.677579
# RTSP stream is not valid
# [ WARN:0@30.018] global cap_ffmpeg_impl.hpp:453 _opencv_ffmpeg_interrupt_callback Stream timeout triggered after 30015.494000 ms
# 2024-06-03 13:16:14.041437
# 스레드 종료까지는 9분 걸렸지만 결과는 timeout으로 지정해준 초 만에 나옴