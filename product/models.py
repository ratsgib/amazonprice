from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    asin = models.CharField(max_length=10, unique=True)
    image = models.CharField(max_length=255, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f("{self.product.title}({created_date}): {price}")
