import cv2
import mediapipe as mp
from imgbeddings import imgbeddings
import chromadb
from PIL import Image
import numpy as np

class FaceService:
    def __init__(self, db_path='./faces', similarity_threshold=0.15):
        # Mediapipe Face Detection 초기화
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

        # ChromaDB 초기화
        self.client = chromadb.PersistentClient(db_path)
        self.db = self.client.get_or_create_collection(
            name='facedb',
            metadata={"hnsw:space": 'cosine'}
        )

        # imgbeddings 초기화
        self.ibed = imgbeddings()

        # 유사도 임계값 설정
        self.similarity_threshold = similarity_threshold

        # 이전 프레임의 바운딩 박스와 라벨
        self.previous_bboxes = []
        self.previous_labels = []

    def detect_faces(self, image):
        """얼굴 탐지를 수행하고 바운딩 박스를 반환합니다."""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(image_rgb)

        bboxes = []
        if results.detections:
            h, w, _ = image.shape
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x1 = int(bbox.xmin * w)
                y1 = int(bbox.ymin * h)
                x2 = int((bbox.xmin + bbox.width) * w)
                y2 = int((bbox.ymin + bbox.height) * h)
                bboxes.append((x1, y1, x2, y2))
        return bboxes

    def recognize_faces(self, image, bboxes):
        """탐지된 얼굴을 인식하여 라벨을 반환합니다."""
        labels = []
        for bbox in bboxes:
            x1, y1, x2, y2 = bbox
            cropped_face = image[y1:y2, x1:x2]
            if cropped_face.size > 0:
                cropped_face_rgb = Image.fromarray(cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB))
                embedding = self.ibed.to_embeddings(cropped_face_rgb)[0]

                # ChromaDB에서 유사한 얼굴 검색
                search_results = self.db.query(
                    query_embeddings=[embedding.tolist()],
                    n_results=1,
                    include=["distances", "metadatas"]
                )
                try:
                    if search_results["distances"][0][0] < self.similarity_threshold:
                        label = search_results["metadatas"][0][0]["filename"]
                    else:
                        label = "Unknown"
                except (IndexError, KeyError):
                    label = "Unknown"
                labels.append(label)
        return labels

    def process_frame(self, image, frame_count):
        """단일 프레임을 처리하여 얼굴 탐지 및 인식을 수행합니다."""
        bboxes = self.detect_faces(image)

        if len(bboxes) != len(self.previous_bboxes) or frame_count % 50 == 0:
            labels = self.recognize_faces(image, bboxes)
        else:
            labels = self.previous_labels

        self.previous_bboxes = bboxes
        self.previous_labels = labels

        # 바운딩 박스 및 라벨 그리기
        for bbox, label in zip(bboxes, labels):
            x1, y1, x2, y2 = bbox
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0) if label != "Unknown" else (0, 0, 255), 2)
        return image

    def close(self):
        """리소스 해제."""
        self.face_detection.close()
