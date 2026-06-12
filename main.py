import cv2
import mediapipe as mp

# Инициализация инструментов MediaPipe для поиска лиц
mp_face_detection = mp.solutions.face_detection
cap = cv2.VideoCapture(0) # Включаем камеру

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success: break

        # Преобразуем цвет для обработки
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image_rgb)

        # Если лицо найдено — рисуем рамку
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                # Здесь в будущем будет вызываться функция проверки на дипфейк
                cv2.putText(image, "ANALYZING...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('TrueFace Detector', image)
        if cv2.waitKey(5) & 0xFF == 27: # Выход на ESC
            break
cap.release()