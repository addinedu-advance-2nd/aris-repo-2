import os
import face_recognition

def get_faces(faceDB):
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(faceDB):
        # 얼굴 이미지 파일을 로드하고 얼굴 인코딩 생성
        img_path = os.path.join(faceDB, filename)
        image = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(image)[0]
        
        known_face_encodings.append(encoding)
        known_face_names.append(os.path.splitext(filename)[0])  # 파일명에서 확장자 제거 후 이름 사용

    return known_face_encodings, known_face_names