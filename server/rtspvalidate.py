import cv2
import threading

def check_rtsp_opencv(rtsp_url):
    capture = cv2.VideoCapture(rtsp_url)
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

# Example code
# if __name__ == "__main__":
#     rtsp_url = "rtsp://127.0.0.1:8554/stream"
#     if is_rtsp_valid(rtsp_url):
#         print("RTSP stream is valid")
#     else:
#         print("RTSP stream is not valid")