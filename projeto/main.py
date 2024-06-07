import cv2
import mediapipe as mp
import time 
from package import olhos_fechados as of, tocar_som as play

# Inicializar MediaPipe Face Mesh;
# variável para facilitar as diversas chamadas a esse módulo;
# atribuindo o módulo 'fase_mesh' do mediapipe à esta variável;
mp_face_mesh = mp.solutions.face_mesh
# outra variável de mesmo intuito mas já chamando a função 'FaceMesh()' para detectar a malha facial;
# mudando os parâmetros da função 'FaceMesh()' de confiança mínima de detecção e a de confiança mínima de rastreamento para 60%;
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.6, min_tracking_confidence=0.6)

# Inicializar desenho de utilidades MediaPipe;
# Idem ao anterior
# contém as funções para desenhar os pontos da malha facial;
mp_drawing = mp.solutions.drawing_utils
# contém os estilos predefinidos para desenhar as conexões da malha facial;
mp_drawing_styles = mp.solutions.drawing_styles

# Capturar vídeo da câmera
# Essa variavel será um objeto da classe 'cv2.VideoCapture';
# O parâmetro '0' refere-se a camera padrão do dispositivo;
webcam = cv2.VideoCapture(0)

# Controle do nosso While;
flag = False

#Controle do tempo decoorido;
start_time = 0
alarm_duration = 2 #A função time.time() retorna o tempo em segundos;

# se a webcam estiver aberta e a flag for False entramos no loop;
while (webcam.isOpened()) and (not flag):
    # barreira de verificação:
    # captura um frame da webcam;
    # 'success' é um valor booleano que indica se a captura foi bem-sucedida;
    # 'image' contém o frame capturado;
    success, image = webcam.read()
    if not success:  # se a captura não foi bem-sucedida;
        print("Ignorando frame vazio da câmera.")
        continue  # pulamos para o próximo ciclo do loop, não iremos fazer a analise de um frame que não existe;

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

    # Deixando o frame editavel e convertendo de volta para BGR;
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # "multi_face_landmarks" gera uma lista de landmarks faciais detectados em um frame;
    if results.multi_face_landmarks:  # se essa lista tiver elementos;
        # laço onde 'face_landmarks' será um elemento (que é o conjunto de landmarks) dessa lista;
        for face_landmarks in results.multi_face_landmarks:
            # Desenhar a malha do rosto na imagem;
            mp_drawing.draw_landmarks(
                # qual frame vamos desenhar os pontos chaves (landmarks);
                image=image,
                # qual a lista de landmarks que serão pontuados/desenhados na imagem;
                landmark_list=face_landmarks,
                # as ligações/conexões entre os landmarks;
                # definimos que vamos usar todos as landmarks da malha facial;
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                # como desenhar os landmarks individuais;
                # setamos para None o que significa que todas as ligações desenhadas serão iguais (sem diferença de cor, largura, ...);
                landmark_drawing_spec=None,
                # como desenhar as conexões entre os landmarks;
                # usamos as conexões da malha facial padrão do MediaPipe;
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())

            # Verificar se os olhos estão fechados usando a nossa função;
            # É aqui dentro que fica o código para tocar o alarme;
            if of.if_eyes_closed(face_landmarks.landmark):
                # vai printar True se olhos estiverem fechados;
                print(of.if_eyes_closed(face_landmarks.landmark))
                
                #Se o tempo inicial for 0 ele entra e gera um novo marco temporal inical em segundos desde a era (que é 1º de janeiro de 1970, 00:00:00 (UTC) em todas as plataformas) como um número em ponto flutuante
                if  start_time == 0:
                    start_time = time.time()
                    
                else:  
                    current_time = time.time() #Retorna o tempo em segundos desde a era, mas que fica atualizando a cada loop
                    
                    #Cálculo para calcular o tempo decorrido desde que os olhos se fecharam
                    if current_time - start_time >= alarm_duration:
                        play.play_sound("sound/alarm.mp3")
                        start_time  = 0

                
            else:
                #Se o indivíduo abriu os olhos antes do tempo necessário para tocar o alarme, a contagem reinicia. Isso evita levar em consideração piscadas
                start_time = 0
                # vai printar False se olhos estiverem abertos;
                print(of.if_eyes_closed(face_landmarks.landmark))


    # Mostrar a imagem com as detecções;
    cv2.imshow('Detector de Sono ao Volante', image)

    # Espera 5 milissegundos por uma tecla pressionada -> sai do loop se pressionado 'Esc';
    if cv2.waitKey(5) & 0xFF == 27:
        flag = True

# Liberar a captura de vídeo da webcam;
webcam.release()
# Fecha todas as janelas abertar pelo OpenCv;
cv2.destroyAllWindows()
