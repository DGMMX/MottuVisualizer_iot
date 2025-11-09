import requests
import json
from datetime import datetime

class APIClient:
    def __init__(self, base_url="http://localhost:5000/api"):
        
        self.base_url = base_url

    def send_detection_event(self, moto_id, model_name, center_x, center_y, status="em_patio"):
        
        endpoint = f"{self.base_url}/detections"
        payload = {
            "motoId": moto_id,
            "modelo": model_name,
            "centerX": center_x,
            "centerY": center_y,
            "timestamp": datetime.now().isoformat(),
            "status": status
        }

        print(f"📡 Enviando dados para API: {payload}")

        try:
            response = requests.post(endpoint, json=payload, timeout=5)
            
            if response.status_code == 201:
                print("✅ Evento registrado com sucesso.")
            else:
                print(f"⚠️ API retornou um status inesperado: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao comunicar com a API ({endpoint}): {e}")

    def send_event(self, event_type, moto_id):
        
        print(f"ℹ️ O método 'send_event' foi substituído por 'send_detection_event'. Evento '{event_type}' para '{moto_id}' não foi enviado.")
