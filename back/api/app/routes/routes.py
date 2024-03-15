
from flask import Blueprint
from app.controller.controllers import ProductController
import json
from flask import jsonify
from flask_cors import CORS


api_blueprint = Blueprint('api', __name__)
CORS(api_blueprint, resources={
     r"/products/promotion/cupom": {"origins": "*"}}, supports_credentials=True, methods=["GET"])


@api_blueprint.route('/products/promotion', methods=['GET'])
def get_products_join_promotion():
    return ProductController().get_all_products_join_promotion()


@api_blueprint.route('/products', methods=['GET'])
def get_products():
    return ProductController().get_all_products()


@api_blueprint.route('/products/promotion/cupom', methods=['GET'])
def get_products_join_promotion_join_cupom():
    data = json.loads(
        ProductController().get_all_products_join_promotion_join_cupom().data.decode('utf-8'))
    result = []
    for i in data:

        js = {
            "product": {
                "title": i["title"],
                "price": i["price"],
                "link": i["link"],
                "image": i["image"],
                "date": i["date"],
                "promotion": {
                    "gross_value_before_promotion": i["gross_value"],
                    "discount_percentage": i["percent"]
                }
            }

        }
        result.append(js)

    return result


@api_blueprint.route('/test', methods=['GET'])
def test_route():
    return jsonify({'message': 'Test route is working!'})
