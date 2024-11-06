import cv2
# q 클릭해서 끄기 

cap=cv2.VideoCapture(0)                  # 0번 카메라에 연결

if cap.isOpened():                  
    while True:
        ret, img=cap.read()              # 카메라를 읽습니다
        if ret:
            cv2.imshow('camera',img)     # 이미지를 표시합니다
            if cv2.waitKey(10) != -1:    # 10ms동안 키 입력을 대기
                break                    # 키가 입력되면 중지합니다

else:
    print("can't open camera")
cap.release()
cv2.destroyAllWindows()