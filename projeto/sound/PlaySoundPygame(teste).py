import cv2, pygame as pg


def play_sound(sound_file):
    '''
    Toca algum arquivo de áudio (mp3, wav...) por completo
    '''
    
    pg.mixer.init() #inicializa o módulos de mixer do pygame
    pg.mixer.music.load(sound_file) #Carrega o arquivo de som
    pg.mixer.music.play() #Toca o arquivo

    # Loop principal para continuar executando, pois o "pg.mixer.music.play()" toca a música de forma paralela ao código, então tenho que delimitar um loop
    while pg.mixer.music.get_busy(): #Verifica se a música está tocando
        pass  # Apenas continua o loop


###bCORPO DO CÓDIGO (usei um exemplo de um código que só abre a câmera) ###

# Inicializa a captura de vídeo da webcam
webcam = cv2.VideoCapture(0)
#Variável booleana para encerrar o loop de música e webcam
alarm = True

if webcam.isOpened():#Verifica se a Webcam está aberta e pronta
    status, frame = webcam.read()
    while alarm and status:
        pg.init() #Incia os módulos do pygame e também é o marco temporal
        status, frame = webcam.read() #usado para capturar (ler) um novo frame do fluxo de vídeo proveniente de uma fonte de vídeo, retorna uma tupla com um valor booleano(status) e o frame capturado (frame)
        if not status:
            alarm = False
        else:
            # Exibe o frame na janela "Webcam Georis"
            cv2.imshow("Webcam Georis", frame)
            # Captura a tecla "esc" quando pressionada e encerra a webcam
            key = cv2.waitKey(5)
            if key == 27:
                alarm = False
            else:
                # Verifica se deve começar a tocar o som
                if pg.time.get_ticks() >= 10000: #função do pygame que analisa o tempo em milissegundos desde que foi dado o "pg.init()"
                    play_sound("alarm.mp3")
                    pg.quit() #Desliga o pygame e consequentemente reinica o loop


# Libera a captura e gravação de vídeo e fecha todas as janelas
cv2.destroyAllWindows()
