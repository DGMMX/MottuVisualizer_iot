## 🏍️ Sistema de Monitoramento Inteligente de Motocicletas

Este projeto propõe um sistema de visão computacional em tempo real voltado para o reconhecimento e acompanhamento de motocicletas em pátios de locadoras ou centros de manutenção, utilizando técnicas de IA e automação.

Integrantes do grupo:

Diego Bassalo Canals Silva – RM558710 | Turma 2TDSPG

Giovanni de Souza Lima – RM556536 | Turma 2TDSPH

Vitor Tadeu Soares de Sousa – RM559105 | Turma 2TDSPH

## 🚀 Visão Geral do Projeto

O sistema faz o monitoramento contínuo de um ambiente com motocicletas, detectando:

Presença, entrada e saída de cada veículo;

Modelo da moto, através de classificação via API;

Eventos em tempo real exibidos em um dashboard visual.

Com isso, é possível automatizar o controle de movimentação dos veículos e gerar registros integrados ao banco de dados e API de backend.

## 🔍 Principais Funcionalidades

Detecção e Rastreamento Contínuo:
O modelo YOLOv8 realiza a detecção de motocicletas e atribui um identificador único (ID) a cada uma, acompanhando seus movimentos no vídeo.

Identificação de Modelos via API:
Cada moto detectada é classificada automaticamente por meio da integração com o Roboflow, identificando o modelo exato (exemplo: Mottu Pop, Mottu-E, Mottu Sport).

Interface Visual em Tempo Real:
Um painel exibido em vídeo mostra:

Quantidade total de motos ativas;

Distribuição por modelo;

Logs de entrada e saída;

Destaques visuais com cores (verde, amarelo e vermelho) indicando status.

Integração com Backend e Banco de Dados Oracle:
Os dados coletados são enviados para uma API REST e gravados em um banco Oracle, permitindo análises posteriores.

##🧠 Objetivo

Criar uma solução automatizada de gestão e rastreamento inteligente de motocicletas, que reduza a intervenção humana e aumente a confiabilidade no controle do fluxo de veículos.
## ⚙️ Como Configurar o Ambiente

💡 Recomendação: utilize um ambiente virtual Python para isolar as dependências do projeto.

 Clonar o repositório
git clone https://github.com/DGMMX/MottuVisualizer_iot.git


 Criar o ambiente virtual
python -m venv .venv



 Instalar dependências
pip install -r requirements.txt

 Instalar o Tesseract OCR
Windows

Baixe o instalador em: UB Mannheim Tesseract OCR

Adicione tesseract.exe ao PATH do sistema.

macOS
brew install tesseract
brew install tesseract-lang

Linux
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-eng

 Dependências Extras
pip install pytesseract numpy==1.26.4

 Execução do Sistema
🧩 1. Monitoramento em Tempo Real
python src/realtime_processing.py


Esse módulo:

Inicia a detecção ao vivo (webcam);

Exibe o painel de monitoramento com logs e contadores;

Envia eventos à API;

Registra cada detecção no banco Oracle (se configurado).

🖼️ 2. Análise de Imagem Estática
python src/detect_and_map.py


Esse script:

Detecta as motos em imagens/patio.jpg;

Faz OCR dos números identificadores;

Gera uma imagem anotada (output.jpg);

Cria um arquivo patio_map.json com as posições mapeadas.

📊 Resultados Esperados

Dashboard: interface com contagem e logs em tempo real.

Logs: mensagens no console, como:

EVENTO [ENTRADA]: moto_1 detectada
EVENTO [SAÍDA]: moto_1 removida


Banco de Dados: tabela Detections atualizada com histórico.

Arquivos Gerados: imagem anotada e JSON de mapeamento.

🧩 Principais Dependências

Python 3.9+

ultralytics (YOLOv8)

opencv-python

pytesseract

numpy

requests

oracledb

🤝 Contribuições

Sugestões e melhorias são bem-vindas!
Abra uma issue ou envie um pull request com novas ideias para o projeto.
