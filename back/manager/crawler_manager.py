

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import json
import os
import datetime
import mysql.connector
import re
import time
import requests
from functools import partial
from multiprocessing import Process, Queue
import sys
from scrapy.exporters import JsonItemExporter
from os.path import abspath, join, dirname
sys.path.insert(0, abspath(join(dirname(__file__), '../webcrawler')))
from mercadolivre.spiders.ml import MlSpider
ROOT_DIRECTORY = os.getcwd()
DATA_DIRECTORY = '{0}/back/manager/dataset/data.json'.format(ROOT_DIRECTORY)
CONNECTION = mysql.connector.connect(user='root',
                                     password='akemih32',
                                     host='localhost',
                                     database='mercadolivre',
                                     auth_plugin='mysql_native_password')

# fazer a parte de que se o data set existe entao vc pega ele insere no database e depois disso deleta o dataset


def run_crawler(start_urls, category_id, category_name, crawler, filename):
    if (os.path.exists(f"./dataset/{filename}")):
        return
    else:

        crawler.crawl(
            MlSpider,
            start_urls=start_urls,
            category=category_id,
            category_name=category_name
        )
        crawler.start()
        crawler.join()


def generate_data(category):
    print("""

    Iniciando o processo de coleta de dados
       
    CATEGORIA: {0}
    TEMPO ESTIMADO: 50 segundos      
    """.format(category["name"]))

    settings = get_project_settings()
    settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    settings.set("DOWNLOAD_DELAY", 1)
    settings.set("FEED_FORMAT", "json")
    filename = f"data_{category['name'].lower().replace(' ', '_')}.json"

    settings.set("FEED_URI", f"dataset/{filename}")

    crawler = CrawlerProcess(settings)
    start_urls = category["url_search"]
    category_id = category["id"]
    category_name = category["name"]
    process = Process(target=run_crawler, args=(
        start_urls, category_id, category_name, crawler, filename))
    process.start()
    process.join()

    return True


def change_datajson_name(category):
    global DATA_DIRECTORY
    new_name = category["name"].lower().replace(" ", "_")
    path, filename = os.path.split(DATA_DIRECTORY)
    name, extension = os.path.splitext(filename)
    name = name.split("_")
    name = name[0].split(".")
    new_name = f"{name[0]}_{category['name']}{extension}"
    new_path = os.path.join(path, new_name)
    DATA_DIRECTORY = new_path


def validate_data(category):
    filename = "./dataset/data_{0}.json".format(
        category["name"].lower().replace(" ", "_"))
    if not os.path.exists(filename):
        return False
    else:
        time_difference = datetime.datetime.now(
        ) - datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        zero_time_difference = datetime.timedelta(0)

        return time_difference > zero_time_difference


def get_data(is_data_trusted, categorie):

    if is_data_trusted:
        reading_data(categorie)
    else:
        delete_datasets(categorie)
        generate_data(categorie)
        reading_data(categorie)


def delete_datasets(category):
    filename = f"./dataset/data_{
        category['name'].lower().replace(' ', '_')}.json"
    try:
        os.remove(f"./dataset/{filename}")
    except:
        pass


def reading_data(category):
    with open("./dataset/data_{0}.json".format(category["name"].lower().replace(" ", "_")), "r") as file:
        data = json.load(file)
        print("Inserindo no DB...")
        load_data(data, category)


def load_data(data, category):

    for prod in data:

        cupom_data = prod["cupom"]
        promotion_data = prod["promotion"]
        product_data = {
            "title": prod["title"],
            "price": prod["price"],
            "link": prod["link"],
            "image": prod["imageUrl"],
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        }

        id_cupom = insert_cupom(cupom_data)
        id_promotion = insert_promotion(promotion_data)
        insert_product(id_cupom, id_promotion, product_data, category)
    print("Inserção finalizada")


def insert_cupom(cupom_data):
    if cupom_data["haveCupom"]:
        sql_select = "SELECT id FROM cupom WHERE name = '{0}'".format(
            cupom_data["cupom"])
        result = execute_query(sql_select)
        percent = int(extract_percent(cupom_data["cupom"])[0])

        if not result:
            sql_insert = "INSERT INTO cupom (name, discount) VALUES ('{0}', {1})".format(
                cupom_data["cupom"], percent)
            res = execute_query(sql_insert, retornar_insert_id=True)
            return res

        else:
            return result


def extract_percent(cupom):
    if not cupom:
        return [0]
    numeros = re.findall(r'\b\d+\.*\d*\b', cupom)
    valores_numericos = [float(numero) for numero in numeros]
    return valores_numericos


def insert_promotion(promotion_data):
    sql_insert = "INSERT INTO promotion (gross_value, percent) VALUES ({0}, {1})".format(
        promotion_data["valorBruto"], extract_percent(promotion_data["porcentagem"])[0])
    res = execute_query(
        sql_insert, retornar_insert_id=True)

    return res


def insert_product(id_cupom, id_promotion, product_data, category):
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql_insert = "INSERT INTO product (title, price, link, image, category, fk_cupom, fk_promotion, date) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"

    parametros = (
        product_data["title"],
        product_data["price"],
        product_data["link"],
        product_data["image"],
        category["name"],
        id_cupom == id_cupom if (id_cupom is not None and isinstance(
            id_cupom, (int, float))) else None,
        id_promotion if (id_promotion is not None and isinstance(
            id_promotion, (int, float))) else None,
        current_datetime
    )

    insert_id = execute_query(sql_insert, parametros=parametros, retornar_insert_id=True)
    return insert_id


def execute_query(query, parametros=None, retornar_insert_id=False):
    cursor = CONNECTION.cursor()
    try:

        if parametros:
            cursor.execute(query, parametros)
        else:
            cursor.execute(query)

        if query.strip().upper().startswith("INSERT") or query.strip().upper().startswith("UPDATE") or query.strip().upper().startswith("DELETE"):
            CONNECTION.commit()
        if retornar_insert_id:
            insert_id = cursor.lastrowid
            return insert_id
        else:
            results = cursor.fetchall()
            return results

    except mysql.connector.Error as err:
        print(f'Erro na consulta {query}: {err}')

    finally:
        cursor.close()


def get_categories():
    # data = requests.get(
    #     'https://www.mercadolivre.com.br/menu/departments?zipcode=').json()
    # categories = []
    # for i in data["departments"][0]["categories"]:
    #     category_data = {
    #         "id": i["id"],
    #         "name": i["name"],
    #         "permalink": i["permalink"],
    #         "url_search": f"https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1001&category={i["id"]}#filter_applied=category_id&origin=qcat&filter_position=4?page=1"
    #     }
    #     categories.append(category_data)
    # print(categories)
    # sys.exit()
    categories = [{'id': 'MLB1051', 'name': 'Celulares e Telefones', 'permalink': 'https://www.mercadolivre.com.br/c/celulares-e-telefones#menu=categories', 'url_search': 'https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1001&category=MLB1051#filter_applied=category_id&origin=qcat&filter_position=4?page=1'}, {'id': 'MLB1648', 'name': 'Informática', 'permalink': 'https://www.mercadolivre.com.br/c/informatica#menu=categories', 'url_search': 'https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1001&category=MLB1648#filter_applied=category_id&origin=qcat&filter_position=4?page=1'}, {'id': 'MLB1039', 'name': 'Câmeras e Acessórios', 'permalink': 'https://www.mercadolivre.com.br/c/cameras-e-acessorios#menu=categories', 'url_search': 'https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1001&category=MLB1039#filter_applied=category_id&origin=qcat&filter_position=4?page=1'},
                  {'id': 'MLB1000', 'name': 'Eletrônicos, Áudio e Vídeo', 'permalink': 'https://www.mercadolivre.com.br/c/eletronicos-audio-e-video#menu=categories', 'url_search': 'https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1001&category=MLB1000#filter_applied=category_id&origin=qcat&filter_position=4?page=1'}, {'id': 'MLB1144', 'name': 'Games', 'permalink': 'https://www.mercadolivre.com.br/c/games#menu=categories', 'url_search': 'https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1001&category=MLB1144#filter_applied=category_id&origin=qcat&filter_position=4?page=1'}, {'id': 'MLB1002', 'name': 'Televisores', 'permalink': 'https://www.mercadolivre.com.br/c/eletronicos-audio-e-video/tv', 'url_search': 'https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1001&category=MLB1002#filter_applied=category_id&origin=qcat&filter_position=4?page=1'}]

    return categories


def main():

    categories = get_categories()

    for category in categories:
        print("Estou na categoria {0}".format(category["name"]))
        print("Faltam {0} categorias para finalizar".format(
            len(categories) - categories.index(category)))

        print(get_data(validate_data(category), category))


if __name__ == "__main__":
    main()
