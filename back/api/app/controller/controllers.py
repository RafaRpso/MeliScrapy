
from flask import jsonify, request
from app.services.service import ProductService


class ProductController:
    def __init__(self):
        self.service = ProductService()

    def get_all_products(self):
        products = self.service.get_all_products()
        return jsonify(products)

    def get_all_products_join_promotion_join_cupom(self):
        products = self.service.get_all_products_join_promotion_join_cupom()
        return jsonify(products)