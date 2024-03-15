import scrapy


class MlSpider(scrapy.Spider):
    name = "ml"
    allowed_domains = ["www.mercadolivre.com", "www.mercadolivre.com.br"]
    start_urls = [
        "https://www.mercadolivre.com.br/ofertas?page=1"
    ]

    def parse(self, response):
        xpaths = {
            "promotion_item": '//li[@class="promotion-item max"]',

        }
        for i in response.xpath(xpaths["promotion_item"]):
            price = i.xpath(
                './/div[@class="andes-money-amount-combo__main-container"]/span/span[@class="andes-money-amount__fraction"]//text()').get()
            title = i.xpath(
                './/p[@class="promotion-item__title"]//text()').get()
            link = i.xpath(
                '//a[@class="promotion-item__link-container"]/@href').get()

            yield {
                "price": price,
                "title": title,
                "link": link
            }

        next_page = response.xpath(
            '//a[contains(@title,"Próxima")]/@href').get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
