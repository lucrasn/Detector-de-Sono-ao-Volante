import numpy as np


# Função para calcular a distância euclidiana entre dois pontos -> √((x1 – x2)² + (y1 – y2)²);
def distancia_euclidiana(point1, point2):
    '''
    point1 : coordenada do parte superior do olho
    point2 : coordenada da parte inferior do olho
    return : calculo da distancia entre os pontos 'point1' e 'point2'
    '''

    # Criamos um vetor de duas dimensões com as coordenadas 'x' e 'y' com 'np.array([x, y]);
        # Como estamos utilizando uma malha facial com o Face Mesh cada um dos 468 pontos tem uma coordenada (x, y);
        # A função np.array() cria um array a partir de sequência de dados, podendo ser uma lista, ou tupla, ...;
            # Quando usamos essa função juntamente dos parâmetros passamos os atributos 'x' e 'y';
                # Para pegar reespectivamente os valores x e y dos pontos point1 e do point2;
    # Com os vetores em mão fazemos a diferença entre eles para calculamos a norma euclidiana com a função "np.linalg.norm()"
    return np.linalg.norm(np.array([point1.x, point1.y]) - np.array([point2.x, point2.y]))


# Função para verificar se os olhos estão fechados
def are_eyes_closed(landmarks):
    '''
    landmarks : 
    retunr :
    '''
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
