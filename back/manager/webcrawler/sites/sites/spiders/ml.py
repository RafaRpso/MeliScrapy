import scrapy
import logging


class MlSpider(scrapy.Spider):
    name = "ml"
    allowed_domains = ["www.mercadolivre.com", "www.mercadolivre.com.br"]
    start_urls = [
        "https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1&category=MLB5672#filter_applied=category_id&origin=qcat&filter_position=4"
    ]
    first_page = True

    def __init__(self, start_urls=None,  category=None, category_name=None, *args, **kwargs):
        super(MlSpider, self).__init__(*args, **kwargs)

        self.start_urls = [start_urls] if start_urls else [
            "https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1&category=MLB5672#filter_applied=category_id&origin=qcat&filter_position=4" 
        ]

        self.category = [category] if category else ["MLB5672"]
        self.category_name = [category_name] if category else ["NOT MAPPED"]

    def parse(self, response):
        logging.info(f"Processing URL: {response.url}")

        if response.url != "https://www.mercadolivre.com.br/ofertas?page=1":
            self.first_page = False
        xpaths = {
            "promotion_item": '//li[@class="promotion-item"]',

        }
        for i in response.xpath(xpaths["promotion_item"]):
            price = i.xpath(
                './/div[@class="andes-money-amount-combo__main-container"]/span/span[@class="andes-money-amount__fraction"]//text()').get()
            title = i.xpath(
                './/p[@class="promotion-item__title"]//text()').get()
            link = i.xpath(
                './/a[@class="promotion-item__link-container"]/@href').get()

            imageUrl = i.xpath(
                '//div[@class="promotion-item__img-container"]/img/@src').get()

            enterprise = i.xpath(
                './/span[@class="promotion-item__seller"]//text()').get()

            promotion = {"valorBruto": 0, "porcentagem": 0}
            promotion["valorBruto"] = i.xpath(
                './/s[@class="andes-money-amount andes-money-amount-combo__previous-value andes-money-amount--previous andes-money-amount--cents-comma"]/span[@class="andes-money-amount__fraction"]//text()').get()
            promotion["porcentagem"] = i.xpath(
                './/span[@class="promotion-item__discount-text"]//text()').get()

            if enterprise is not None:
                enterprise = enterprise.replace("por", "")
                enterprise = enterprise.replace(" ", "")
            isFull = True if i.xpath(
                './/div[@class="promotion-item__newshipping-container"]/span[@class="fulfillment-text"]').get() else False

            cupom = {"haveCupom": False, "cupom": ""}

            cupom["haveCupom"] = True if i.xpath(
                './/div[@class="promotion-item__coupon-div"]').get() else False

            if cupom["haveCupom"]:
                cupom["cupom"] = i.xpath(
                    './/div[@class="promotion-item__coupon-div"]/span/text()').get()

            yield {
                "price": price,
                "title": title,
                "link": link,
                "imageUrl": imageUrl,
                "enterprise": enterprise,
                "isFull": isFull,
                "cupom": cupom,
                "type": title.split(" ")[0:3] if title is not None else None,
                "category": self.category_name[0],
                "promotion": promotion,
                "first_page": self.first_page,
                "category_url": response.url
            }

        next_page = response.xpath(
            '//a[contains(@title,"Próxima")]/@href').get()

        if next_page:
            next_page = str(next_page)+"&category="+self.category[0]
            yield scrapy.Request(url=next_page, callback=self.parse)
