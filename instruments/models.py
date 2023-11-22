from django.db import models


class Instruments(models.Model):
    name = models.CharField(max_length=255)
    desription = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Instruments, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    costumer_name = models.CharField(max_length=255)
    costumer_email = models.EmailField()
    date_of_order = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order for {self.product.name} by {self.costumer_name}'
