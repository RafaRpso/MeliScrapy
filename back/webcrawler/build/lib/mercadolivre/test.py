import requests

url = 'http://localhost:6800/schedule.json'
data = {
    'project': 'mercadolivre',
    'spider': 'ml',
    'categories': 'ofertas',
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print('Spider agendada com sucesso!')
else:
    print('Erro ao agendar a spider.')