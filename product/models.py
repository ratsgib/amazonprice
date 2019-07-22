from django.db import models


class Product(models.Model):
    '''
    商品モデル。
    '''
    title = models.CharField(max_length=255)
    asin = models.CharField(max_length=10, unique=True) # ASIN or ISBN
    image = models.CharField(max_length=255, null=True) # product image url
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Price(models.Model):
    '''
    商品の価格モデル。
    scrape_priceバッチを起動する度に作成され、更新は考慮していない。
    '''
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="prices")
    price = models.IntegerField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.asin}: {self.price}"

    class Meta:
        ordering = ['created_date']
