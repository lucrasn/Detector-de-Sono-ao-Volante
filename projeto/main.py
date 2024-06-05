import cv2
import mediapipe as mp
from package import olhos_fechados as of, tocar_som as play

# Inicializar MediaPipe Face Mesh;
# variável para facilitar as diversas chamadas a esse módulo;
mp_face_mesh = mp.solutions.face_mesh # atribuindo o módulo 'fase_mesh' do mediapipe à esta variável;
# outra variável de mesmo intuito mas já chamando a função 'FaceMesh()' para detectar a malha facial;
    # mudando os parâmetros da função 'FaceMesh()' de confiança mínima de detecção e a de confiança mínima de rastreamento para 60%;
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.6, min_tracking_confidence=0.6)

# Inicializar desenho de utilidades MediaPipe;
# Idem ao anterior
mp_drawing = mp.solutions.drawing_utils # contém as funções para desenhar os pontos da malha facial;
mp_drawing_styles = mp.solutions.drawing_styles # contém os estilos predefinidos para desenhar as conexões da malha facial;

# Capturar vídeo da câmera
# Essa variavel será um objeto da classe 'cv2.VideoCapture';
webcam = cv2.VideoCapture(0) # O parâmetro '0' refere-se a camera padrão do dispositivo;

# Controle do nosso While;
flag = False

while (webcam.isOpened()) and (not flag): # se a webcam estiver aberta e a flag for False entramos no loop;
    # barreira de verificação:
        # captura um frame da webcam;
            # 'success' é um valor booleano que indica se a captura foi bem-sucedida;
            # 'image' contém o frame capturado;
    success, image = webcam.read()
    if not success: # se a captura não foi bem-sucedida;
        print("Ignorando frame vazio da câmera.")
        continue # pulamos para o próximo ciclo do loop, não iremos fazer a analise de um frame que não existe;

    # Converter a imagem BGR (Blue-Green-Red) para RGB (Red-Green_Blue);
        # O padrão do OpenCV é o BGR mas precisamos do RGB para o MediaPipe;
    # Conversão de espaço de cores na imagem;
        # 'image' -> variável que contém a imagem que será convertida;
        # 'cv2.COLOR_BGR2RGB' -> parâmetro que especifica o tipo de conversão;
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Definindo o frame como não editável para melhor desempenho durante o precessamento;
    image.flags.writeable = False
    # Processando o frame como o modelo de malha facial do MediaPipe e guardando na variável;
    results = face_mesh.process(image)

    # Deixando o frame editavel e convertendo de volta para BGR
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
            # É AQUI DENTRO QUE VAI FICAR O PROGRAMA DE TOCAR O ALARME!!
            if of.if_eyes_closed(face_landmarks.landmark):
                # print(of.if_eyes_closed(face_landmarks.landmark))
                cv2.putText(image, 'Dormindo', (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                # print(of.if_eyes_closed(face_landmarks.landmark))
                cv2.putText(image, 'Acordado', (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Mostrar a imagem com as detecções
    cv2.imshow('Detector de Sono ao Volante', image)

    # Sair do loop ao pressionar 'Esc'
    if cv2.waitKey(5) & 0xFF == 27:
        flag = True

# Liberar a captura e fechar janelas
webcam.release()
cv2.destroyAllWindows()
