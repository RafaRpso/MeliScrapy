import requests

# URL do endpoint Scrapyd para agendar a execução da spider
url = 'http://localhost:6800/schedule.json'

# Dados necessários para agendar a spider
data = {
    'project': 'mercadolivre',  # Nome do projeto Scrapy
    'spider': 'ml',  # Nome da spider a ser executada
}

# Envia a solicitação POST para o endpoint Scrapyd
response = requests.post(url, data=data)  # Usando 'data' em vez de 'json'

# Verifica se a solicitação foi bem-sucedida (código de status 200)
if response.status_code == 200:
    print(response.json())  # Exibe a resposta JSON do Scrapyd
else:
    print(f'Erro ao agendar a spider. Código de status: {response.status_code}')
    print(response.text)  # Exibe a resposta completa para diagnóstico
