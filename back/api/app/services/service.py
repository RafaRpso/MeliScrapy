from app.models.models import Product, Promotion, Cupom
from app.database.database import Database


class ProductService:

    def __init__(self):
        self.db = Database()

    def get_all_products(self):
        query = "SELECT * FROM product"
        products = self.db.execute_query(query)
        return products

    def get_all_products_join_promotion_join_cupom(self):
        query = "SELECT * FROM product LEFT JOIN promotion ON product.fk_promotion = promotion.id LEFT JOIN cupom ON product.fk_cupom = cupom.id"
        products = self.db.execute_query(query)
        return products
