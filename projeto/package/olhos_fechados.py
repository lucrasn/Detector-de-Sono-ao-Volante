import numpy as np


# Função para calcular a distância euclidiana entre dois pontos -> √((x1 – x2)² + (y1 – y2)²)
    # Calcula a distância euclidiana entre o 'point1' e o 'point2'
        # o 'point1' será o ponto superior do olho e o 'point2' será o inferior
    # Criamos um vetor de duas dimensões com as coordenadas 'x' e 'y' com 'np.array([x, y])
def distancia_euclidiana(point1, point2):
    return np.linalg.norm(np.array([point1.x, point1.y]) - np.array([point2.x, point2.y]))


# Função para verificar se os olhos estão fechados
def are_eyes_closed(landmarks):
    left_eye_top = landmarks[159]
    left_eye_bottom = landmarks[145]
    right_eye_top = landmarks[386]
    right_eye_bottom = landmarks[374]

    # Distâncias euclidianas entre os pontos dos olhos
    left_eye_distance = distancia_euclidiana(left_eye_top, left_eye_bottom)
    right_eye_distance = distancia_euclidiana(right_eye_top, right_eye_bottom)

    # Limite para considerar o olho fechado (ajuste conforme necessário)
    eye_closed_threshold = 0.025

    return left_eye_distance < eye_closed_threshold and right_eye_distance < eye_closed_threshold

