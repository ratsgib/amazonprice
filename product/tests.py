from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup
from product.models import Product, Price


def create_data(product_nums, price_nums):
    '''
    テストデータをnums件登録する
    '''
    for num in range(product_nums):
        p = Product.objects.create(
            title=f"テスト商品{num}",
            asin=f"{num:010}",
            image="<img>"
        )
        for num in range(price_nums):
            price = Price.objects.create(
                product=p, price=num*100,
            )


class ProductTests(TestCase):
    def test_index_noresult(self):
        '''
        indexにアクセスし、商品の登録がないこと。
        '''
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content.decode(), "html.parser")
        self.assertTrue(soup.find(id="result_empty"))

    def test_index_one(self):
        '''
        1件登録データがあるとき、リストが表示されていること。
        '''
        create_data(1, 1)
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content.decode(), "html.parser")
        self.assertNotEqual(soup.select("#result_container .card"), [])
        self.assertFalse(soup.find(id="result_empty"))
