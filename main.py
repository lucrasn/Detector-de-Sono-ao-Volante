import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Inicializar desenho de utilidades MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


# Função para calcular a distância euclidiana entre dois pontos
def euclidean_distance(point1, point2):
    return np.linalg.norm(np.array([point1.x, point1.y]) - np.array([point2.x, point2.y]))


# Função para verificar se os olhos estão fechados
def are_eyes_closed(landmarks):
    left_eye_top = landmarks[159]
    left_eye_bottom = landmarks[145]
    right_eye_top = landmarks[386]
    right_eye_bottom = landmarks[374]

    # Distâncias euclidianas entre os pontos dos olhos
    left_eye_distance = euclidean_distance(left_eye_top, left_eye_bottom)
    right_eye_distance = euclidean_distance(right_eye_top, right_eye_bottom)

    # Limite para considerar o olho fechado (ajuste conforme necessário)
    # Esse limite de 0.025 está perfeito para uma distancia rezoavelmente perto, o suficiente para o nosso contexto
    eye_closed_threshold = 0.025

    return left_eye_distance < eye_closed_threshold and right_eye_distance < eye_closed_threshold


# Capturar vídeo da câmera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignorando frame vazio da câmera.")
        continue

    # Converter a imagem BGR para RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = face_mesh.process(image)

    # Converter de volta para BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Desenhar a malha do rosto na imagem
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())

            # Verificar se os olhos estão fechados
            if are_eyes_closed(face_landmarks.landmark):
                cv2.putText(image, 'Dormindo', (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(image, 'Acordado', (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Mostrar a imagem com as detecções
    cv2.imshow('MediaPipe Face Mesh', image)

    # Sair do loop ao pressionar 'Esc'
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Liberar a captura e fechar janelas
cap.release()
cv2.destroyAllWindows()
