import datetime
import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

CONFIDENCE_THRESHOLD = 0.4
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

fire_label = open('./Fire.txt', 'r')
data = fire_label.read()
class_list = data.split('\n')
fire_label.close()

model = YOLO('./yolo8s_best.pt')
tracker = DeepSort(max_age=60)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    start = datetime.datetime.now()

    ret, frame = cap.read()
    if not ret:
        print('Camera Error')
        break

    detection = model.predict(source=[frame], save=False)[0]
    results = []

    for data in detection.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
        confidence = float(data[4])
        if confidence < CONFIDENCE_THRESHOLD:
            continue

        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        label = int(data[5])
        results.append([[xmin, ymin, xmax-xmin, ymax-ymin], confidence, label])

    tracks = tracker.update_tracks(results, frame=frame)

    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        ltrb = track.to_ltrb()
        xmin, ymin, xmax, ymax = int(ltrb[0]), int(ltrb[1]), int(ltrb[2]), int(ltrb[3])
        for i in results:
            gap_xmin = i[0][0] - xmin
            gap_ymin = i[0][1] - ymin
            error_range = 20
            if (gap_xmin > -error_range and  gap_xmin < error_range and gap_ymin > -error_range and gap_ymin < error_range):
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)
                cv2.rectangle(frame, (xmin, ymin - 20), (xmin + 20, ymin), GREEN, -1)
                cv2.putText(frame, str(track_id) + ' ' + class_list[label]+' '+str(round(confidence, 2)), (xmin + 5, ymin - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
                print('id : %s label : %s (xmin, ymin) : (%d, %d) (xmax, ymax) : (%d, %d)' % (track_id,class_list[label],xmin,ymin,xmax,ymax))
                break
                
    end = datetime.datetime.now()
    total = (end - start).total_seconds()
    # print(f'Time to process 1 frame: {total * 1000:.0f} milliseconds')

    fps = f'FPS: {1 / total:.2f}'
    cv2.putText(frame, fps, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()