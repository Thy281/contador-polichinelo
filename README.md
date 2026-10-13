# Contador de Polichinelos

Projeto em Python que usa MediaPipe Pose para acompanhar os braços em um vídeo e contar polichinelos. O OpenCV desenha os pontos do corpo e exibe o contador em um retângulo sobre o vídeo.

## Requisitos

- Python compatível com as versões instaláveis de OpenCV e MediaPipe no seu sistema
- OpenCV
- MediaPipe Tasks
- Um vídeo chamado poli.mp4
- O modelo pose_landmarker_lite.task

## Instalação

Clone o repositório e instale as dependências:

git clone https://github.com/Thy281/contador-polichinelo.git
cd contador-polichinelo
pip install -r requirements.txt

Coloque poli.mp4 na pasta de onde o programa será executado. Coloque pose_landmarker_lite.task na mesma pasta do script.

## Execução

Execute python contadorPolichinelo.py na pasta do projeto.

Pressione q para fechar a janela do vídeo.

## Como a contagem funciona

O programa considera os pulsos levantados quando ficam acima dos ombros. Quando os braços voltam para baixo depois de terem sido levantados, o contador aumenta em um.
