import cv2
import mediapipe as mp
from package import olhos_fechados as os

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Inicializar desenho de utilidades MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Capturar vídeo da câmera
webcam = cv2.VideoCapture(0)

# Verifique se a câmera foi aberta corretamente
if not webcam.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

while webcam.isOpened():
    success, image = webcam.read()
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
            if os.are_eyes_closed(face_landmarks.landmark):
                cv2.putText(image, 'Dormindo', (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(image, 'Acordado', (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Mostrar a imagem com as detecções
    cv2.imshow('Detector de Sono ao Volante', image)

    # Sair do loop ao pressionar 'Esc'
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Liberar a captura e fechar janelas
webcam.release()
cv2.destroyAllWindows()
