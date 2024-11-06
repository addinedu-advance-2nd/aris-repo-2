import cv2
import face_recognition
import os
from utils.get_faces import get_faces # faceDB에서 얼굴 데이터를 불러오는 함수

# 카메라 스트림 관리를 위한 변수
camera_streams = {}

faceDB = './faceDB'
os.makedirs(faceDB, exist_ok=True)
known_face_encodings, known_face_names = get_faces(faceDB)

def open_camera(camera_id):
    """특정 카메라 ID로 카메라를 열고 스트림을 시작합니다."""
    if camera_id in camera_streams:
        print(f"Camera {camera_id} is already open.")
        return camera_streams[camera_id]
    
    # 카메라 ID에 맞는 스트림 열기
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"Cannot open camera {camera_id}")
        return None

    camera_streams[camera_id] = cap
    print(f"Camera {camera_id} opened.")
    return cap

def close_camera(camera_id):
    """특정 카메라 ID로 카메라를 닫고 스트림을 중지합니다."""
    cap = camera_streams.get(camera_id)
    if cap and cap.isOpened():
        cap.release()
        print(f"Camera {camera_id} closed.")
        del camera_streams[camera_id]
    else:
        print(f"Camera {camera_id} is not open.")

def get_camera_frame(camera_id):
    """특정 카메라 ID의 현재 프레임을 캡처하여 반환합니다."""
    cap = camera_streams.get(camera_id)
    if not cap or not cap.isOpened():
        print(f"Camera {camera_id} is not open.")
        return None
    
    ret, frame = cap.read()
    if not ret:
        print(f"Failed to capture frame from camera {camera_id}.")
        return None

    #rgb로 변환하여 face_recognition 에서 사용할 수 있도록 설정
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    #얼굴 위치와 인코딩 추출
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    for face_encoding in face_encodings:
        #faceDB의 등록된 얼굴과 비교
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown" # 일치하지 않을 경우 "unknown으로 설정"

        if True in matches:
            match_index = matches.index(True)
            name = known_face_names[match_index]
        
    #얼굴 위치와 이름을 프레임에 표시 
    for(top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2) #얼굴 사각형
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED) #이름 표시 사각형
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

    # 프레임을 JPEG로 인코딩
    _, jpeg_frame = cv2.imencode('.jpg', frame)
    return jpeg_frame.tobytes()

