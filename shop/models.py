from django.db import models
from django.utils.timezone import now  
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")
    created_at = models.DateTimeField(default=now, verbose_name="Дата добавления")  
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

    def is_in_stock(self):
        """Проверяет, есть ли товар на складе."""
        return self.stock > 0

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    customer_name = models.CharField(max_length=100, verbose_name="Имя покупателя")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Заказ #{self.id} от {self.customer_name}"

    def save(self, *args, **kwargs):
        """Автоматически рассчитывает общую стоимость при сохранении заказа."""
        self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
