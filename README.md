# Detector de Sono ao Volante
Projeto feito em python para o reconhecimento de motoristas que estão dormindo no volante. Foi utilizado uma machine learning de reconhecimento facal o Mediapipe juntamente com o OpenCV e o Numpy para ter acesso a camera do dispositivo e para realizar os cálculos e metricas entra as distancias das palpebras dos olhos, quando identificado o fechamento dos olhos será acionado uma contagem - realzada com a biblioteca time nativa do python - que chegando à 2,5 segundos irá acionar um alarme para que o motorista volte a acordar.
## Autores
- [@lucrasn](https://github.com/lucrasn)
- [@yuurixrl](https://github.com/yuurixrl)
- [@andcsp](https://github.com/andcsp)
- [@robertozoy](https://github.com/robertozoy)
- [@georiSamuel](https://github.com/georiSamuel)

## Divisão
### Reconhecimento e Medição
- yuurixrl
- lucrasn
### Processamento de Dados
- georiSamuel
- robertozoy
- andcsp

## Bibliotecas Usadas

- [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/guide?hl=pt-br)
- [OpenCV](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [PyDub](https://github.com/jiaaro/pydub)
- [Time](https://docs.python.org/pt-br/3/library/time.html)
