import cv2
import pygame as pg
import time

def play_sound(sound_file):
    '''
    Toca um arquivo de áudio (mp3, wav...) por completo
    '''
    pg.mixer.init()  # Inicializa o módulo de mixer do Pygame
    pg.mixer.music.load(sound_file)  # Carrega o arquivo de som
    pg.mixer.music.play()  # Toca o arquivo

    # Loop para continuar executando enquanto a música está tocando
    while pg.mixer.music.get_busy():  # Verifica se a música está tocando
        time.sleep(0.1)  # Espera um pouco antes de verificar novamente

def initialize_webcam():
    '''
    Inicializa a webcam e retorna o objeto de captura de vídeo
    '''
    webcam = cv2.VideoCapture(0)
    if not webcam.isOpened():
        print("Erro ao abrir a webcam.")
        return None
    return webcam

def capture_frames(webcam):
    '''
    Captura frames da webcam e os exibe em uma janela
    '''
    alarm = True
    start_time = pg.time.get_ticks()  # Marca o tempo inicial

    while alarm:
        ret, frame = webcam.read()  # Captura um frame da webcam
        if not ret:
            alarm = False
            print("Erro ao capturar o frame.")
        else:
            cv2.imshow("Webcam Georis", frame)  # Exibe o frame na janela

            key = cv2.waitKey(5)  # Captura a tecla pressionada
            if key == 27:  # Tecla 'esc' para encerrar
                alarm = False
            else:
                current_time = pg.time.get_ticks()
                if current_time - start_time >= 10000:  # 10 segundos passados
                    play_sound("alarm.mp3")
                    start_time = pg.time.get_ticks()  # Reinicia o tempo

    # Libera a captura e fecha as janelas
    webcam.release()
    cv2.destroyAllWindows()

def main():
    pg.init()  # Inicializa o Pygame
    webcam = initialize_webcam()  # Inicializa a webcam

    if webcam:
        capture_frames(webcam)  # Captura e exibe frames da webcam

    pg.quit()  # Encerra o Pygame

if __name__ == "__main__":
    main()
