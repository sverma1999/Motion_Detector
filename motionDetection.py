from cv2 import cv2
import time, pandas
from datetime import datetime


initial_frame=None
status_list=[None,None]
times_list=[]
obj_Det=pandas.DataFrame(columns=["Start Time", "End Time"])

video= cv2.VideoCapture(0)
video.read()
time.sleep(3)

while True:
    check, frame = video.read()
    status=0
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)
    if initial_frame is None:
        initial_frame = gray
        continue

    delta_frame=cv2.absdiff(initial_frame, gray)

    threshhold_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    #threshhold_frame=cv2.dilate(threshhold_frame, None, iterations=3)

    (cnts,_) = cv2.findContours(threshhold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status=1
        (x, y, w, h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)

    status_list.append(status)

    status_list=status_list[-2:]

    if status_list[-1] == 1 and status_list[-2] == 0:
        times_list.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times_list.append(datetime.now())


    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame",delta_frame)
    cv2.imshow("Threshhold Frame", threshhold_frame)
    cv2.imshow("Color Frame", frame)

    key=cv2.waitKey(1)
    if key==ord('q'):
        if status==1:
            times_list.append(datetime.now())
        break

print(times_list)



for t in range(0, len(times_list),2):
    obj_Det=obj_Det.append({"Start Time": times_list[t], "End Time": times_list[t+1]}, ignore_index=True)

obj_Det.to_csv("DetectionTimes.csv")

video.release()
cv2.destroyAllWindows
