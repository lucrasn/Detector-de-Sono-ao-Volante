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
    landmarks : pontos chaves da malha facial
    retunr : retorna um valor booleano (olhos fechados == True e olhos abertos == False)
    '''
    olho_esquerdo_top = landmarks[159]
    olho_esquerdo_bottom = landmarks[145]
    olho_direto_top = landmarks[386]
    olho_direto_bottom = landmarks[374]

    # Distâncias euclidianas entre os pontos dos olhos
    distancia_olho_esquerdo = distancia_euclidiana(olho_esquerdo_top, olho_esquerdo_bottom)
    distancia_olho_direito = distancia_euclidiana(olho_direto_top, olho_direto_bottom)

    # Limite para considerar o olho fechado
    limiar_de_olho_fechado = 0.025

    return (distancia_olho_esquerdo < limiar_de_olho_fechado) and (distancia_olho_direito < limiar_de_olho_fechado)
