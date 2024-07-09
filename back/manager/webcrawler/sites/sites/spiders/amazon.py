from typing import Any
import scrapy
import re 

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["www.amazon.com.br"]
    start_urls = ["https://www.amazon.com.br/s?i=videogames&fs=true&page=2"]

    def __init__(self, start_urls=None, *args: Any, **kwargs: Any) -> None:
        super(AmazonSpider, self).__init__(*args, **kwargs)

        self.start_urls = [start_urls] if start_urls else [
            "https://www.amazon.com.br/s?rh=n%3A16339926011&fs=true&ref=lp_16339926011_sar"]

    def get_enterprise_product(self, link: str) -> str:
        return

    def get_percent(self, ac_price: str, old_price: str) -> str:
        return "10%"

    def clean_price(self, price: str) -> float : 
        price_str = re.search(r'\((.*?)\)', price[0]).group(1)
        return float(price_str.replace("R$", "").replace("\xa0", "").replace(",", "").replace(" ", ""))
    def clean_promotion(self, price: str) -> float:
        n_price = price.replace("R$", "").replace(
            "\xa0", "").replace(",", "").replace(" ", "")
        cleaned_price = ''
        decimal_point_count = 0

        for c in n_price:
            if c.isdigit():
                cleaned_price += c
            elif c == '.':
                if decimal_point_count == 0:
                    cleaned_price += c
                    decimal_point_count += 1

        return float(cleaned_price) if cleaned_price else 0.0

    def parse(self, response):

        xpath_main = '//div[@class="sg-col-inner"]'
        for prd in response.xpath(xpath_main):
            title_xpath = './/h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-4"]'

            promotion = self.clean_promotion(prd.xpath(
                '//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]//span[@class="a-price a-text-price"]//text()').get("null"))

            price = self.clean_price(prd.xpath(
                './/span[@class="a-price"]/span[@class="a-offscreen"]').get()),

            data = {
                "title": prd.xpath(title_xpath + "//text()").get(" "),
                "price": price,
                "link": prd.xpath(title_xpath + '//a/@href').get(),
                "imageUrl": prd.xpath('.//*[contains(concat(" ", @class, " "), " s-image ")]/@src').get(),
                # "enterprise": self.get_enterprise_product(prd.xpath('').get()),
                # "type": prd.xpath(title_xpath + "//text()").get().split(" ")[0:3] ,
                # "category_url": response.url,
                "promotion": {"old_value":  promotion, "percentage": self.get_percent(price, promotion)


                              }}

            yield data
