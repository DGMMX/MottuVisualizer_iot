import logging
from ultralytics import YOLO
import cv2
import pytesseract
import json
import os
import numpy as np


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


IMG_PATH = 'data/input/patio.jpg'
OUTPUT_IMG = 'data/output/patio_result.jpg'
JSON_PATH = 'data/output/patio_motos.json'

logging.info(f"Imagem de entrada: {IMG_PATH}")
logging.info(f"Imagem de saída: {OUTPUT_IMG}")
logging.info(f"Arquivo JSON: {JSON_PATH}")


try:
    logging.info("Carregando modelo YOLOv8...")
    model = YOLO('yolov8n.pt')
    logging.info("Modelo YOLOv8 carregado com sucesso.")
except Exception as e:
    logging.error(f"Erro ao carregar o modelo YOLOv8: {e}")
    exit(1)


try:
    logging.info("Iniciando detecção de motocicletas...")
    results = model(IMG_PATH)[0]
    logging.info(f"Detecção concluída: {len(results.boxes)} objetos encontrados.")
except Exception as e:
    logging.error(f"Erro durante a detecção: {e}")
    exit(1)


try:
    image = cv2.imread(IMG_PATH)
    if image is None:
        logging.error(f"Não foi possível carregar a imagem: {IMG_PATH}")
        exit(1)
    logging.info("Imagem carregada com sucesso.")
except Exception as e:
    logging.error(f"Erro ao abrir a imagem: {e}")
    exit(1)


motos_detectadas = []

for i, box in enumerate(results.boxes):
    try:
        cls = int(box.cls)
        conf = float(box.conf)

        if cls != 3:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy.cpu().numpy()[0])
        cropped_moto = image[y1:y2, x1:x2].copy()

        h_start = int((y2 - y1) * 0.5)
        h_end = int((y2 - y1) * 0.8)
        cropped_area = cropped_moto[h_start:h_end, :]

        hsv = cv2.cvtColor(cropped_area, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        result = cv2.bitwise_and(cropped_area, cropped_area, mask=mask)
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        resized = cv2.resize(binary, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

        numero = pytesseract.image_to_string(
            resized,
            config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789'
        )
        numero = ''.join(filter(str.isdigit, numero))

        moto_id = numero if numero else f"moto_{i}"
        motos_detectadas.append({
            "id": moto_id,
            "x": (x1 + x2) // 2,
            "y": (y1 + y2) // 2
        })

        # Desenho na imagem
        label = numero if numero else f"#{i}"
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    except Exception as e:
        logging.error(f"Erro ao processar moto {i}: {e}")


os.makedirs(os.path.dirname(OUTPUT_IMG), exist_ok=True)

try:
    cv2.imwrite(OUTPUT_IMG, image)
    logging.info(f"Imagem anotada salva em: {OUTPUT_IMG}")
except Exception as e:
    logging.error(f"Erro ao salvar imagem anotada: {e}")

try:
    with open(JSON_PATH, 'w') as f:
        json.dump({'motos': motos_detectadas}, f, indent=2)
    logging.info(f"Arquivo JSON salvo em: {JSON_PATH}")
except Exception as e:
    logging.error(f"Erro ao salvar arquivo JSON: {e}")

print(f"✅ Total de motos detectadas: {len(motos_detectadas)}")
logging.info("Execução finalizada com sucesso.")
