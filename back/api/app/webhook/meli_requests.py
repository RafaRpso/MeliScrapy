import requests
import json
import re
from datetime import datetime


class MercadoLivreRequests:

    def __init__(self):
        self.headers = ""

    def generate_headers(self, link):
        current_time = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

        return {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
            'Cookie': '_d2id=ae32d2b7-a818-471c-97d4-b80e7b6312ad; c_ui-navigation=6.6.15; ',
            'Device-Memory': '8',
            'Dnt': '1',
            'Downlink': '10',
            'Dpr': '1.25',
            'Ect': '4g',
            'Priority': 'u=1, i',
            'Referer': link,
            'Rtt': '50',
            'Sec-Ch-Ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Gpc': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ ',
            'X-Firefox-Http3': 'h3',
            'Accept-CH': 'device-memory, dpr, viewport-width, rtt, downlink, ect, save-data',
            'Accept-CH-Lifetime': '60',
            'Access-Control-Allow-Credentials': 'true',
            'Alt-Svc': 'h3=":443"; ma=86400',
            'Content-Encoding': 'gzip',
            'Content-Type': 'application/json; charset=utf-8',
            'Date': current_time,
            'ETag': 'W/"122c-qQfl6iE8Sx+w9kavVgeBgTQ9258"',
            'Expect-CT': 'max-age=0',
            'Referrer-Policy': 'no-referrer-when-downgrade',
            'Server': 'Tengine',
            'Strict-Transport-Security': 'max-age=15552000; includeSubDomains',
            'Vary': 'Origin',
            'Via': '1.1 4692c4e301d3d1e9a5129f3438a26148.cloudfront.net (CloudFront)',
            'X-Amz-Cf-Id': 'uVxmnshH4W7NIszfqyEVJEku_mlpQdLANom3_tT-iuvyM-cI7Lgl-g==',
            'X-Amz-Cf-Pop': 'GRU3-C1',
            'X-Cache': 'Miss from cloudfront',
            'X-Content-Type-Options': 'nosniff',
            'X-D2id': 'b0778d03-c8ef-4d8d-be99-50dcb896838d',
            'X-Dns-Prefetch-Control': 'on',
            'X-Download-Options': 'noopen',
            'X-Envoy-Upstream-Service-Time': '103',
            'X-Permitted-Cross-Domain-Policies': 'none',
            'X-Request-Device-Id': 'b0778d03-c8ef-4d8d-be99-50dcb896838d',
            'X-Request-Id': '10cdce34-a04e-4488-8da5-8e9fa68a7140',
            'X-Xss-Protection': '1; mode=block',
        }

    def execute_request(self, url):
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return f"A solicitação falhou com o código de status: {response.status_code}"

    def extrair_id_mercadolivre(self, url):
        padrao = r'/p/MLB(\d+)'
        resultado = re.search(padrao, url)
        if resultado:
            return resultado.group(1)
        else:

            return None

    def get_data_product(self, id):
        url = 'https://www.mercadolivre.com.br/product-fe-recommendations/recommendations?site_id=MLB&product_id={0}&tracking=true&product_details=true&client=pdp_comparator'.format(
            id)
        self.headers = self.generate_headers(url)
        return self.execute_request(url)

    def get_questions_product(self, link):

        questions = []
        true_id = 0
        id = "MLB" + str(self.extrair_id_mercadolivre(link))

        palavras = ["quant\\\\as", "toca", "220", "bateria", "android", "4g", "chip", "tamanho", "qualidade", "wifi", "bluetooth", 'linux', 'xbox', 'hz', 'material', "metal", "potência", "serve", "suporte", "polegadas", "peso", "material", "metros", "tamanho", "adaptador", "teclado", "ram", "gpu",
                    "slotes", "velocidade",  "led", "Boa noite", "funciona", "energia", "compatível", "tecido", "gramatura", "tamanho", "kit", "shorts", "garantia", "dimensão", "lavar", "saber", "gostaria", "bivolt", "gost\\\\", "Bom d\\\\ia", "sab\\\\e"]

        data_product = self.get_data_product(
            id)

        if "recommended_products" in data_product:
            true_id = data_product["recommended_products"][0]["item_id"]

        for i in palavras:

            if (len(questions) >= 10):
                break

            url = "https://www.mercadolivre.com.br/p/api/products/qadb/{0}/{1}/{2}".format(
                id, true_id, i)
            self.headers = self.generate_headers(link)

            data = self.execute_request(url)

            if "state" in data["components"][2]:
                if data["components"][2]["state"] == "VISIBLE":
                    if "questions" in data["components"][2]["components"][0]:
                        questions.extend(
                            data["components"][2]["components"][0]["questions"])
                        

        return questions
