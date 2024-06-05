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
        time.sleep(0.1)  # Espera um pouco antes de verificar novamente, para evitar sobrevargar