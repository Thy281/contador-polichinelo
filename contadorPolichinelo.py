import cv2
import mediapipe as mp
from pathlib import Path

WEB = 0
VIDEO = 'poli.mp4'
MODELO = Path(__file__).with_name("pose_landmarker_lite.task")

video = cv2.VideoCapture(VIDEO)
fps = video.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 30

opcoes = mp.tasks.vision.PoseLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path=str(MODELO)),
    running_mode=mp.tasks.vision.RunningMode.VIDEO,
    min_pose_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

with mp.tasks.vision.PoseLandmarker.create_from_options(opcoes) as pose:
    numero_frame = 0
    contador = 0
    bracos_subiram = False
    while True:
        ret, frame = video.read()
        if not ret:
            break

        videoRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imagem = mp.Image(image_format=mp.ImageFormat.SRGB, data=videoRGB)
        tempo_ms = int(numero_frame * 1000 / fps)
        resultado = pose.detect_for_video(imagem, tempo_ms)

        if resultado.pose_landmarks:
            pontos = resultado.pose_landmarks[0]
            mp.tasks.vision.drawing_utils.draw_landmarks(
                frame,
                pontos,
                mp.tasks.vision.PoseLandmarksConnections.POSE_LANDMARKS,
                mp.tasks.vision.drawing_styles.get_default_pose_landmarks_style(),
            )

            ombro_esquerdo = pontos[11]
            ombro_direito = pontos[12]
            pulso_esquerdo = pontos[15]
            pulso_direito = pontos[16]

            pontos_visiveis = min(
                ombro_esquerdo.visibility,
                ombro_direito.visibility,
                pulso_esquerdo.visibility,
                pulso_direito.visibility,
            ) > 0.5

            if pontos_visiveis:
                bracos_levantados = (
                    pulso_esquerdo.y < ombro_esquerdo.y - 0.05
                    and pulso_direito.y < ombro_direito.y - 0.05
                )
                bracos_abaixados = (
                    pulso_esquerdo.y > ombro_esquerdo.y + 0.1
                    and pulso_direito.y > ombro_direito.y + 0.1
                )

                if bracos_levantados:
                    bracos_subiram = True
                elif bracos_abaixados and bracos_subiram:
                    contador += 1
                    bracos_subiram = False

        texto = f"Polichinelos: {contador}"
        tamanho_texto, _ = cv2.getTextSize(
            texto,
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            2,
        )
        x_texto = 20
        linha_base = 20 + tamanho_texto[1]
        cv2.rectangle(
            frame,
            (10, 10),
            (x_texto + tamanho_texto[0] + 10, linha_base + 10),
            (0, 255, 0),
            -1,
        )
        cv2.putText(
            frame,
            texto,
            (x_texto, linha_base),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        cv2.imshow("Video", frame)
        numero_frame += 1

        if cv2.waitKey(40) & 0xFF == ord("q"):
            break

video.release()
cv2.destroyAllWindows()
